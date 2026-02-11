"""
Job Descriptions module - CRUD operations for the job_description table
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
class JobDescription:
    """Job Description data model"""
    min_salary: float
    status: str = "OPEN"
    description: Optional[str] = None
    max_salary: Optional[float] = None
    recruiter_id: Optional[int] = None
    client_id: Optional[uuid.UUID] = None
    id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    deactive_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert job description to dictionary"""
        data = {
            "min_salary": self.min_salary,
            "status": self.status,
        }
        if self.description is not None:
            data["description"] = self.description
        if self.max_salary is not None:
            data["max_salary"] = self.max_salary
        if self.recruiter_id is not None:
            data["recruiter_id"] = self.recruiter_id
        if self.client_id is not None:
            data["client_id"] = str(self.client_id)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JobDescription":
        """Create JobDescription from dictionary"""
        return cls(
            id=uuid.UUID(data["id"]) if data.get("id") else None,
            min_salary=data.get("min_salary", 0.0),
            max_salary=data.get("max_salary"),
            description=data.get("description"),
            status=data.get("status", "OPEN"),
            recruiter_id=data.get("recruiter_id"),
            client_id=uuid.UUID(data["client_id"]) if data.get("client_id") else None,
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            deactive_at=datetime.fromisoformat(data["deactive_at"]) if data.get("deactive_at") else None,
        )


# Table name constant
TABLE_NAME = "job_description"


def get_all_job_descriptions(include_inactive: bool = False) -> List[JobDescription]:
    """
    Get all job descriptions
    
    Args:
        include_inactive: If True, includes deactivated/closed positions
        
    Returns:
        List of JobDescription objects
    """
    if include_inactive:
        data = query_table(TABLE_NAME)
    else:
        # Only active positions (deactive_at is NULL)
        data = query_table(TABLE_NAME, {"deactive_at": None})
    
    return [JobDescription.from_dict(record) for record in data]


def get_job_description_by_id(job_id: str) -> Optional[JobDescription]:
    """
    Get a single job description by ID
    
    Args:
        job_id: UUID of the job description
        
    Returns:
        JobDescription object or None if not found
    """
    data = query_table(TABLE_NAME, {"id": job_id})
    if data:
        return JobDescription.from_dict(data[0])
    return None


def search_job_descriptions(
    status: Optional[str] = None,
    client_id: Optional[str] = None,
    recruiter_id: Optional[int] = None,
    min_salary_min: Optional[float] = None,
    min_salary_max: Optional[float] = None,
) -> List[JobDescription]:
    """
    Search job descriptions by filters
    
    Args:
        status: Filter by status (OPEN, CLOSED, PAUSED)
        client_id: Filter by client UUID
        recruiter_id: Filter by recruiter ID
        min_salary_min: Minimum salary filter (>=)
        min_salary_max: Maximum salary filter (<=)
        
    Returns:
        List of matching JobDescription objects
    """
    filters = {}
    if status:
        filters["status"] = status
    if client_id:
        filters["client_id"] = client_id
    if recruiter_id is not None:
        filters["recruiter_id"] = recruiter_id
    
    # Get filtered results or all active if no filters
    if filters:
        filters["deactive_at"] = None
        data = query_table(TABLE_NAME, filters)
    else:
        data = query_table(TABLE_NAME, {"deactive_at": None})
    
    jobs = [JobDescription.from_dict(record) for record in data]
    
    # Apply salary range filtering in Python
    if min_salary_min is not None:
        jobs = [j for j in jobs if j.min_salary >= min_salary_min]
    if min_salary_max is not None:
        jobs = [j for j in jobs if j.min_salary <= min_salary_max]
    
    return jobs


def create_job_description(job: JobDescription) -> JobDescription:
    """
    Create a new job description
    
    Args:
        job: JobDescription object to create
        
    Returns:
        Created JobDescription with ID and timestamps
    """
    data = job.to_dict()
    result = insert_record(TABLE_NAME, data)
    
    if result and len(result) > 0:
        return JobDescription.from_dict(result[0])
    raise Exception("Failed to create job description")


def update_job_description(job_id: str, updates: Dict[str, Any]) -> Optional[JobDescription]:
    """
    Update a job description
    
    Args:
        job_id: UUID of the job description to update
        updates: Dictionary of fields to update
        
    Returns:
        Updated JobDescription or None if not found
    """
    result = update_record(TABLE_NAME, job_id, updates)
    
    if result and len(result) > 0:
        return JobDescription.from_dict(result[0])
    return None


def delete_job_description(job_id: str) -> bool:
    """
    Permanently delete a job description
    
    Args:
        job_id: UUID of the job description to delete
        
    Returns:
        True if deleted, False if not found
    """
    result = delete_record(TABLE_NAME, job_id)
    return bool(result and len(result) > 0)


def close_job_description(job_id: str) -> Optional[JobDescription]:
    """
    Close a job description (soft delete)
    
    Args:
        job_id: UUID of the job description to close
        
    Returns:
        Updated JobDescription or None if not found
    """
    updates = {
        "deactive_at": datetime.utcnow().isoformat(),
        "status": "CLOSED"
    }
    return update_job_description(job_id, updates)


def reopen_job_description(job_id: str) -> Optional[JobDescription]:
    """
    Reopen a closed job description
    
    Args:
        job_id: UUID of the job description to reopen
        
    Returns:
        Updated JobDescription or None if not found
    """
    updates = {
        "deactive_at": None,
        "status": "OPEN"
    }
    return update_job_description(job_id, updates)


def change_job_status(job_id: str, status: str) -> Optional[JobDescription]:
    """
    Change job status (OPEN, CLOSED, PAUSED)
    
    Args:
        job_id: UUID of the job description
        status: New status value
        
    Returns:
        Updated JobDescription or None if not found
    """
    return update_job_description(job_id, {"status": status})
