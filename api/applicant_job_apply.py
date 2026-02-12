"""
ApplicantJobApply module - CRUD operations for the applicant_job_apply table
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
class ApplicantJobApply:
    """ApplicantJobApply data model - represents a job application"""
    applicant_id: uuid.UUID
    job_description_id: uuid.UUID
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    deactive_at: Optional[datetime] = None
    recruiter_id: Optional[uuid.UUID] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert job application to dictionary"""
        data = {
            "applicant_id": str(self.applicant_id),
            "job_description_id": str(self.job_description_id),
        }
        if self.recruiter_id:
            data["recruiter_id"] = str(self.recruiter_id)
        if self.id:
            data["id"] = self.id
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApplicantJobApply":
        """Create ApplicantJobApply from dictionary"""
        return cls(
            id=data.get("id"),
            applicant_id=uuid.UUID(data["applicant_id"]) if data.get("applicant_id") else None,
            job_description_id=uuid.UUID(data["job_description_id"]) if data.get("job_description_id") else None,
            recruiter_id=uuid.UUID(data["recruiter_id"]) if data.get("recruiter_id") else None,
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            deactive_at=datetime.fromisoformat(data["deactive_at"]) if data.get("deactive_at") else None,
        )


# Table name constant
TABLE_NAME = "applicant_job_apply"


def get_all_applications(include_inactive: bool = False) -> List[ApplicantJobApply]:
    """
    Get all job applications
    
    Args:
        include_inactive: If True, includes deactivated applications
        
    Returns:
        List of ApplicantJobApply objects
    """
    if include_inactive:
        data = query_table(TABLE_NAME)
    else:
        # Only active applications (deactive_at is NULL)
        data = query_table(TABLE_NAME, {"deactive_at": None})
    
    return [ApplicantJobApply.from_dict(record) for record in data]


def get_application_by_id(application_id: int) -> Optional[ApplicantJobApply]:
    """
    Get a single job application by ID
    
    Args:
        application_id: Numeric ID of the application
        
    Returns:
        ApplicantJobApply object or None if not found
    """
    data = query_table(TABLE_NAME, {"id": application_id})
    if data:
        return ApplicantJobApply.from_dict(data[0])
    return None


def get_applications_by_applicant(applicant_id: str) -> List[ApplicantJobApply]:
    """
    Get all applications for a specific applicant
    
    Args:
        applicant_id: UUID of the applicant
        
    Returns:
        List of ApplicantJobApply objects
    """
    data = query_table(TABLE_NAME, {"applicant_id": applicant_id})
    return [ApplicantJobApply.from_dict(record) for record in data]


def get_applications_by_job(job_description_id: str) -> List[ApplicantJobApply]:
    """
    Get all applications for a specific job description
    
    Args:
        job_description_id: UUID of the job description
        
    Returns:
        List of ApplicantJobApply objects
    """
    data = query_table(TABLE_NAME, {"job_description_id": job_description_id})
    return [ApplicantJobApply.from_dict(record) for record in data]


def search_applications(
    applicant_id: Optional[str] = None,
    job_description_id: Optional[str] = None,
    recruiter_id: Optional[str] = None,
) -> List[ApplicantJobApply]:
    """
    Search job applications by filters
    
    Args:
        applicant_id: Filter by applicant UUID
        job_description_id: Filter by job description UUID
        recruiter_id: Filter by recruiter UUID
        
    Returns:
        List of matching ApplicantJobApply objects
    """
    filters = {}
    if applicant_id:
        filters["applicant_id"] = applicant_id
    if job_description_id:
        filters["job_description_id"] = job_description_id
    if recruiter_id:
        filters["recruiter_id"] = recruiter_id
    
    # Default to active applications only
    if "deactive_at" not in filters:
        filters["deactive_at"] = None
    
    data = query_table(TABLE_NAME, filters if filters else None)
    return [ApplicantJobApply.from_dict(record) for record in data]


def create_application(application: ApplicantJobApply) -> ApplicantJobApply:
    """
    Create a new job application
    
    Args:
        application: ApplicantJobApply object to create
        
    Returns:
        Created ApplicantJobApply with ID and timestamps
    """
    data = application.to_dict()
    result = insert_record(TABLE_NAME, data)
    
    if result and len(result) > 0:
        return ApplicantJobApply.from_dict(result[0])
    raise Exception("Failed to create job application")


def update_application(application_id: int, updates: Dict[str, Any]) -> Optional[ApplicantJobApply]:
    """
    Update a job application
    
    Args:
        application_id: Numeric ID of the application to update
        updates: Dictionary of fields to update
        
    Returns:
        Updated ApplicantJobApply or None if not found
    """
    result = update_record(TABLE_NAME, application_id, updates)
    
    if result and len(result) > 0:
        return ApplicantJobApply.from_dict(result[0])
    return None


def delete_application(application_id: int) -> bool:
    """
    Permanently delete a job application
    
    Args:
        application_id: Numeric ID of the application to delete
        
    Returns:
        True if deleted, False if not found
    """
    result = delete_record(TABLE_NAME, application_id)
    return bool(result and len(result) > 0)


def deactivate_application(application_id: int) -> Optional[ApplicantJobApply]:
    """
    Soft delete - mark application as inactive (withdrawn)
    
    Args:
        application_id: Numeric ID of the application to deactivate
        
    Returns:
        Updated ApplicantJobApply or None if not found
    """
    updates = {"deactive_at": datetime.utcnow().isoformat()}
    return update_application(application_id, updates)


def reactivate_application(application_id: int) -> Optional[ApplicantJobApply]:
    """
    Reactivate a deactivated application
    
    Args:
        application_id: Numeric ID of the application to reactivate
        
    Returns:
        Updated ApplicantJobApply or None if not found
    """
    updates = {"deactive_at": None}
    return update_application(application_id, updates)


def assign_recruiter(application_id: int, recruiter_id: str) -> Optional[ApplicantJobApply]:
    """
    Assign a recruiter to a job application
    
    Args:
        application_id: Numeric ID of the application
        recruiter_id: UUID of the recruiter to assign
        
    Returns:
        Updated ApplicantJobApply or None if not found
    """
    updates = {"recruiter_id": recruiter_id}
    return update_application(application_id, updates)


def unassign_recruiter(application_id: int) -> Optional[ApplicantJobApply]:
    """
    Remove recruiter assignment from a job application
    
    Args:
        application_id: Numeric ID of the application
        
    Returns:
        Updated ApplicantJobApply or None if not found
    """
    updates = {"recruiter_id": None}
    return update_application(application_id, updates)
