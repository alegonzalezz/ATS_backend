"""
Clients module - CRUD operations for the client table
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from database import (
    query_table,
    insert_record,
    update_record,
    delete_record,
)


@dataclass
class Client:
    """Client data model"""
    description: Optional[str] = None
    id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    deactive: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert client to dictionary"""
        data = {}
        if self.description is not None:
            data["description"] = self.description
        if self.id:
            data["id"] = str(self.id)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Client":
        """Create Client from dictionary"""
        return cls(
            id=uuid.UUID(data["id"]) if data.get("id") else None,
            description=data.get("description"),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            deactive=datetime.fromisoformat(data["deactive"]) if data.get("deactive") else None,
        )


# Table name constant
TABLE_NAME = "client"


def get_all_clients(include_inactive: bool = False) -> List[Client]:
    """
    Get all clients
    
    Args:
        include_inactive: If True, includes deactivated clients
        
    Returns:
        List of Client objects
    """
    if include_inactive:
        data = query_table(TABLE_NAME)
    else:
        # Only active clients (deactive is NULL)
        data = query_table(TABLE_NAME, {"deactive": None})
    
    return [Client.from_dict(record) for record in data]


def get_client_by_id(client_id: str) -> Optional[Client]:
    """
    Get a single client by ID
    
    Args:
        client_id: UUID of the client
        
    Returns:
        Client object or None if not found
    """
    data = query_table(TABLE_NAME, {"id": client_id})
    if data:
        return Client.from_dict(data[0])
    return None


def search_clients(description: Optional[str] = None) -> List[Client]:
    """
    Search clients by description
    
    Args:
        description: Filter by description (partial match)
        
    Returns:
        List of matching Client objects
    """
    # Get all active clients first
    data = query_table(TABLE_NAME, {"deactive": None})
    clients = [Client.from_dict(record) for record in data]
    
    # Apply partial match filtering in Python
    if description:
        desc_lower = description.lower()
        clients = [
            c for c in clients 
            if c.description and desc_lower in c.description.lower()
        ]
    
    return clients


def create_client(client: Client) -> Client:
    """
    Create a new client
    
    Args:
        client: Client object to create
        
    Returns:
        Created Client with ID and timestamps
    """
    data = client.to_dict()
    # Remove id if present to let Supabase generate it
    if "id" in data:
        del data["id"]
    
    result = insert_record(TABLE_NAME, data)
    
    if result and len(result) > 0:
        return Client.from_dict(result[0])
    raise Exception("Failed to create client")


def update_client(client_id: str, updates: Dict[str, Any]) -> Optional[Client]:
    """
    Update a client
    
    Args:
        client_id: UUID of the client to update
        updates: Dictionary of fields to update
        
    Returns:
        Updated Client or None if not found
    """
    result = update_record(TABLE_NAME, client_id, updates)
    
    if result and len(result) > 0:
        return Client.from_dict(result[0])
    return None


def delete_client(client_id: str) -> bool:
    """
    Permanently delete a client
    
    Args:
        client_id: UUID of the client to delete
        
    Returns:
        True if deleted, False if not found
    """
    result = delete_record(TABLE_NAME, client_id)
    return bool(result and len(result) > 0)


def deactivate_client(client_id: str) -> Optional[Client]:
    """
    Soft delete - mark client as inactive
    
    Args:
        client_id: UUID of the client to deactivate
        
    Returns:
        Updated Client or None if not found
    """
    updates = {"deactive": datetime.utcnow().isoformat()}
    return update_client(client_id, updates)


def reactivate_client(client_id: str) -> Optional[Client]:
    """
    Reactivate a deactivated client
    
    Args:
        client_id: UUID of the client to reactivate
        
    Returns:
        Updated Client or None if not found
    """
    updates = {"deactive": None}
    return update_client(client_id, updates)
