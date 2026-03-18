"""
Skills module - CRUD operations for the skills table
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from .database import (
    query_table,
    insert_record,
    update_record,
)


@dataclass
class Skill:
    """Skill data model"""
    name: str
    id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    deactive_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert skill to dictionary"""
        data = {
            "name": self.name,
        }
        if self.id:
            data["id"] = str(self.id)
        if self.created_at:
            data["created_at"] = self.created_at.isoformat()
        if self.deactive_at:
            data["deactive_at"] = self.deactive_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Skill":
        """Create Skill from dictionary"""
        # Ensure name is uppercase and present
        if "name" not in data:
            raise ValueError("Skill data must contain 'name' field")
        
        name = data["name"].upper()
        return cls(
            id=uuid.UUID(data["id"]) if data.get("id") else None,
            name=name,
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            deactive_at=datetime.fromisoformat(data["deactive_at"]) if data.get("deactive_at") else None,
        )


# Table name constant
TABLE_NAME = "skills"


def get_all_skills(include_inactive: bool = False, search: Optional[str] = None) -> List[Skill]:
    """
    Get all skills
    
    Args:
        include_inactive: If True, includes deactivated skills
        search: Optional search term for fuzzy matching by name
        
    Returns:
        List of Skill objects
    """
    client = query_table.__code__.co_consts  # Dummy line to avoid import issues, we need client here
    # We need to access the client directly to use ilike, so we'll use the database module's client getter
    from .database import get_supabase_client
    client = get_supabase_client()
    
    query = client.table(TABLE_NAME).select("*")
    
    # Filter by active status if not including inactive
    if not include_inactive:
        query = query.is_("deactive_at", None)
    
    # Apply search filter if provided
    if search:
        # Convert search to uppercase for case-insensitive matching against uppercase names
        search_upper = search.upper()
        query = query.ilike("name", f"%{search_upper}%")
    
    response = query.execute()
    return [Skill.from_dict(record) for record in response.data]


def get_skill_by_id(skill_id: str) -> Optional[Skill]:
    """
    Get a single skill by ID
    
    Args:
        skill_id: UUID of the skill
        
    Returns:
        Skill object or None if not found
    """
    data = query_table(TABLE_NAME, {"id": skill_id})
    if data:
        return Skill.from_dict(data[0])
    return None


def create_skill(name: str) -> Skill:
    """
    Create a new skill
    
    Args:
        name: Name of the skill (will be converted to uppercase)
        
    Returns:
        Created Skill object
        
    Raises:
        Exception: If skill with the same name already exists
    """
    # Ensure name is uppercase
    name_upper = name.upper()
    
    # Check if skill already exists (active or inactive)
    from .database import get_supabase_client
    client = get_supabase_client()
    response = client.table(TABLE_NAME).select("*").eq("name", name_upper).execute()
    
    if response.data:
        # Skill exists, raise error
        existing_skill = Skill.from_dict(response.data[0])
        raise Exception(f"Skill '{name_upper}' already exists with ID {existing_skill.id}")
    
    # Create new skill
    data = {"name": name_upper}
    result = insert_record(TABLE_NAME, data)
    
    if result:
        return Skill.from_dict(result[0])
    raise Exception("Failed to create skill")


def update_skill_status(skill_id: str, deactive_at: Optional[datetime] = None) -> Skill:
    """
    Update skill status (activate/deactivate)
    
    Args:
        skill_id: UUID of the skill
        deactive_at: Timestamp to deactivate (None to activate)
        
    Returns:
        Updated Skill object
    """
    data = {"deactive_at": deactive_at.isoformat() if deactive_at else None}
    result = update_record(TABLE_NAME, skill_id, data)
    
    if result:
        return Skill.from_dict(result[0])
    raise Exception("Failed to update skill status")


def get_applicant_skills(applicant_id: str, include_inactive: bool = False) -> List[Skill]:
    """
    Get skills associated with an applicant
    
    Args:
        applicant_id: UUID of the applicant
        include_inactive: If True, includes deactivated skill associations
        
    Returns:
        List of Skill objects
    """
    from .database import get_supabase_client
    client = get_supabase_client()
    
    query = (
        client.table("applicant_skills")
        .select("skill:skills(*)")
        .eq("applicant_id", applicant_id)
    )
    
    if not include_inactive:
        query = query.is_("deactive_at", None)
    
    response = query.execute()
    
    skills = []
    for record in response.data:
        if record.get("skill"):
            skills.append(Skill.from_dict(record["skill"]))
    
    return skills


def add_skill_to_applicant(applicant_id: str, skill_id: str) -> Dict[str, Any]:
    """
    Add a skill to an applicant (or reactivate if exists but inactive)
    
    Args:
        applicant_id: UUID of the applicant
        skill_id: UUID of the skill
        
    Returns:
        Dict with success status
    """
    from .database import get_supabase_client
    client = get_supabase_client()
    
    # Check if association already exists
    response = (
        client.table("applicant_skills")
        .select("*")
        .eq("applicant_id", applicant_id)
        .eq("skill_id", skill_id)
        .execute()
    )
    
    if response.data:
        # Association exists, reactivate if inactive
        record = response.data[0]
        if record.get("deactive_at"):
            # Reactivate
            update_data = {"deactive_at": None}
            client.table("applicant_skills").update(update_data).eq("id", record["id"]).execute()
            return {"success": True, "message": "Skill reactivated for applicant"}
        else:
            return {"success": False, "error": "Skill already associated with applicant"}
    else:
        # Create new association
        insert_data = {
            "applicant_id": applicant_id,
            "skill_id": skill_id,
            "deactive_at": None
        }
        client.table("applicant_skills").insert(insert_data).execute()
        return {"success": True, "message": "Skill added to applicant"}


def update_applicant_skill_status(applicant_id: str, skill_id: str, deactive_at: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Update the status of an applicant-skill association
    
    Args:
        applicant_id: UUID of the applicant
        skill_id: UUID of the skill
        deactive_at: Timestamp to deactivate (None to activate)
        
    Returns:
        Dict with success status
    """
    from .database import get_supabase_client
    client = get_supabase_client()
    
    # Find the association
    response = (
        client.table("applicant_skills")
        .select("*")
        .eq("applicant_id", applicant_id)
        .eq("skill_id", skill_id)
        .execute()
    )
    
    if not response.data:
        return {"success": False, "error": "Association not found"}
    
    record = response.data[0]
    update_data = {"deactive_at": deactive_at.isoformat() if deactive_at else None}
    
    client.table("applicant_skills").update(update_data).eq("id", record["id"]).execute()
    
    return {"success": True, "message": "Skill association status updated"}
