"""
Applicants module - CRUD operations for the applicants table
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
class Applicant:
    """Applicant data model"""
    name: str
    last_name: str
    linkedin: str
    email: str
    phone: str
    city: str
    english: str
    id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    deactive_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert applicant to dictionary"""
        data = {
            "name": self.name,
            "last_name": self.last_name,
            "linkedin": self.linkedin,
            "email": self.email,
            "phone": self.phone,
            "city": self.city,
            "english": self.english,
        }
        if self.id:
            data["id"] = str(self.id)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Applicant":
        """Create Applicant from dictionary"""
        return cls(
            id=uuid.UUID(data["id"]) if data.get("id") else None,
            name=data["name"],
            last_name=data["last_name"],
            linkedin=data["linkedin"],
            email=data["email"],
            phone=data["phone"],
            city=data["city"],
            english=data["english"],
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            deactive_at=datetime.fromisoformat(data["deactive_at"]) if data.get("deactive_at") else None,
        )


# Table name constant
TABLE_NAME = "applicants"


def get_all_applicants(include_inactive: bool = False) -> List[Applicant]:
    """
    Get all applicants
    
    Args:
        include_inactive: If True, includes deactivated applicants
        
    Returns:
        List of Applicant objects
    """
    if include_inactive:
        data = query_table(TABLE_NAME)
    else:
        # Only active applicants (deactive_at is NULL)
        data = query_table(TABLE_NAME, {"deactive_at": None})
    
    return [Applicant.from_dict(record) for record in data]


def get_applicant_by_id(applicant_id: str) -> Optional[Applicant]:
    """
    Get a single applicant by ID
    
    Args:
        applicant_id: UUID of the applicant
        
    Returns:
        Applicant object or None if not found
    """
    data = query_table(TABLE_NAME, {"id": applicant_id})
    if data:
        return Applicant.from_dict(data[0])
    return None


def search_applicants(
    name: Optional[str] = None,
    city: Optional[str] = None,
    english_level: Optional[str] = None,
    email: Optional[str] = None,
) -> List[Applicant]:
    """
    Search applicants by filters
    
    Args:
        name: Filter by name (partial match)
        city: Filter by city (partial match)
        english_level: Filter by English proficiency
        email: Filter by exact email
        
    Returns:
        List of matching Applicant objects
    """
    filters = {}
    if email:
        filters["email"] = email
    if english_level:
        filters["english"] = english_level
    
    # Note: Partial matches for name and city would require ilike queries
    # For now, using exact matches. Enhance with full-text search if needed.
    
    data = query_table(TABLE_NAME, filters if filters else {"deactive_at": None})
    applicants = [Applicant.from_dict(record) for record in data]
    
    # Apply partial match filtering in Python for now
    if name:
        name_lower = name.lower()
        applicants = [
            a for a in applicants 
            if name_lower in a.name.lower() or name_lower in a.last_name.lower()
        ]
    
    if city:
        city_lower = city.lower()
        applicants = [a for a in applicants if city_lower in a.city.lower()]
    
    return applicants


def create_applicant(applicant: Applicant) -> Applicant:
    """
    Create a new applicant
    
    Args:
        applicant: Applicant object to create
        
    Returns:
        Created Applicant with ID and timestamps
    """
    data = applicant.to_dict()
    result = insert_record(TABLE_NAME, data)
    
    if result and len(result) > 0:
        return Applicant.from_dict(result[0])
    raise Exception("Failed to create applicant")


def update_applicant(applicant_id: str, updates: Dict[str, Any]) -> Optional[Applicant]:
    """
    Update an applicant
    
    Args:
        applicant_id: UUID of the applicant to update
        updates: Dictionary of fields to update
        
    Returns:
        Updated Applicant or None if not found
    """
    result = update_record(TABLE_NAME, applicant_id, updates)
    
    if result and len(result) > 0:
        return Applicant.from_dict(result[0])
    return None


def delete_applicant(applicant_id: str) -> bool:
    """
    Permanently delete an applicant
    
    Args:
        applicant_id: UUID of the applicant to delete
        
    Returns:
        True if deleted, False if not found
    """
    result = delete_record(TABLE_NAME, applicant_id)
    return bool(result and len(result) > 0)


def deactivate_applicant(applicant_id: str) -> Optional[Applicant]:
    """
    Soft delete - mark applicant as inactive
    
    Args:
        applicant_id: UUID of the applicant to deactivate
        
    Returns:
        Updated Applicant or None if not found
    """
    updates = {"deactive_at": datetime.utcnow().isoformat()}
    return update_applicant(applicant_id, updates)


def reactivate_applicant(applicant_id: str) -> Optional[Applicant]:
    """
    Reactivate a deactivated applicant
    
    Args:
        applicant_id: UUID of the applicant to reactivate
        
    Returns:
        Updated Applicant or None if not found
    """
    updates = {"deactive_at": None}
    return update_applicant(applicant_id, updates)
