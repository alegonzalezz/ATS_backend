"""
Recruiters module - CRUD operations for the recruiter table
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from .database import (
    query_table,
    insert_record,
    update_record,
    delete_record,
)


@dataclass
class Recruiter:
    """Recruiter data model"""
    name: str
    description: Optional[str] = None
    id: Optional[Any] = None
    created_at: Optional[datetime] = None
    deactive_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert recruiter to dictionary"""
        data = {
            "name": self.name,
        }
        if self.description is not None:
            data["description"] = self.description
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Recruiter":
        """Create Recruiter from dictionary"""
        # Handle both integer IDs and UUIDs
        id_val = data.get("id")
        if id_val is not None:
            if isinstance(id_val, str):
                try:
                    id_val = uuid.UUID(id_val)
                except ValueError:
                    pass  # Keep as string if not valid UUID
            # If it's already an int, keep it as is
        
        return cls(
            id=id_val,
            name=data["name"],
            description=data.get("description"),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            deactive_at=datetime.fromisoformat(data["deactive_at"]) if data.get("deactive_at") else None,
        )


# Table name constant
TABLE_NAME = "recruiter"


def get_all_recruiters(include_inactive: bool = False) -> List[Recruiter]:
    """
    Get all recruiters
    
    Args:
        include_inactive: If True, includes deactivated recruiters
        
    Returns:
        List of Recruiter objects
    """
    if include_inactive:
        data = query_table(TABLE_NAME)
    else:
        # Only active recruiters (deactive_at is NULL)
        data = query_table(TABLE_NAME, {"deactive_at": None})
    
    return [Recruiter.from_dict(record) for record in data]


def get_recruiter_by_id(recruiter_id: str) -> Optional[Recruiter]:
    """
    Get a single recruiter by ID
    
    Args:
        recruiter_id: UUID of the recruiter
        
    Returns:
        Recruiter object or None if not found
    """
    data = query_table(TABLE_NAME, {"id": recruiter_id})
    if data:
        return Recruiter.from_dict(data[0])
    return None


def search_recruiters(
    name: Optional[str] = None,
    description: Optional[str] = None
) -> List[Recruiter]:
    """
    Search recruiters by name or description
    
    Args:
        name: Filter by name (partial match)
        description: Filter by description (partial match)
        
    Returns:
        List of matching Recruiter objects
    """
    # Get all active recruiters first
    data = query_table(TABLE_NAME, {"deactive_at": None})
    recruiters = [Recruiter.from_dict(record) for record in data]
    
    # Apply partial match filtering in Python
    if name:
        name_lower = name.lower()
        recruiters = [
            r for r in recruiters 
            if name_lower in r.name.lower()
        ]
    
    if description:
        desc_lower = description.lower()
        recruiters = [
            r for r in recruiters 
            if r.description and desc_lower in r.description.lower()
        ]
    
    return recruiters


def create_recruiter(recruiter: Recruiter) -> Recruiter:
    """
    Create a new recruiter
    
    Args:
        recruiter: Recruiter object to create
        
    Returns:
        Created Recruiter with ID and timestamps
    """
    data = recruiter.to_dict()
    result = insert_record(TABLE_NAME, data)
    
    if result and len(result) > 0:
        return Recruiter.from_dict(result[0])
    raise Exception("Failed to create recruiter")


def update_recruiter(recruiter_id: str, updates: Dict[str, Any]) -> Optional[Recruiter]:
    """
    Update a recruiter
    
    Args:
        recruiter_id: UUID of the recruiter to update
        updates: Dictionary of fields to update
        
    Returns:
        Updated Recruiter or None if not found
    """
    result = update_record(TABLE_NAME, recruiter_id, updates)
    
    if result and len(result) > 0:
        return Recruiter.from_dict(result[0])
    return None


def delete_recruiter(recruiter_id: str) -> bool:
    """
    Permanently delete a recruiter
    
    Args:
        recruiter_id: UUID of the recruiter to delete
        
    Returns:
        True if deleted, False if not found
    """
    result = delete_record(TABLE_NAME, recruiter_id)
    return bool(result and len(result) > 0)


def deactivate_recruiter(recruiter_id: str) -> Optional[Recruiter]:
    """
    Soft delete - mark recruiter as inactive
    
    Args:
        recruiter_id: UUID of the recruiter to deactivate
        
    Returns:
        Updated Recruiter or None if not found
    """
    updates = {"deactive_at": datetime.utcnow().isoformat()}
    return update_recruiter(recruiter_id, updates)


def reactivate_recruiter(recruiter_id: str) -> Optional[Recruiter]:
    """
    Reactivate a deactivated recruiter
    
    Args:
        recruiter_id: UUID of the recruiter to reactivate
        
    Returns:
        Updated Recruiter or None if not found
    """
    updates = {"deactive_at": None}
    return update_recruiter(recruiter_id, updates)
