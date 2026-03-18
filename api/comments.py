"""
Comments module - CRUD operations for the comments table
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from .database import insert_record, update_record, delete_record, get_comments_by_applicant


MAX_COMMENTS = 5


@dataclass
class Comment:
    """Comment data model"""
    recruiter_id: Optional[uuid.UUID]
    comment: Optional[str]
    applicant_id: Optional[uuid.UUID]
    id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert comment to dictionary"""
        data: Dict[str, Any] = {}
        if self.id:
            data["id"] = str(self.id)
        if self.recruiter_id:
            data["recruiter_id"] = str(self.recruiter_id)
        if self.comment is not None:
            data["comment"] = self.comment
        if self.applicant_id:
            data["applicant_id"] = str(self.applicant_id)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Comment":
        """Create Comment from dictionary"""
        return cls(
            id=uuid.UUID(data["id"]) if data.get("id") else None,
            recruiter_id=uuid.UUID(data["recruiter_id"]) if data.get("recruiter_id") else None,
            comment=data.get("comment"),
            applicant_id=uuid.UUID(data["applicant_id"]) if data.get("applicant_id") else None,
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
        )


TABLE_NAME = "comments"


def get_comments_by_applicant_id(applicant_id: str) -> List[Dict[str, Any]]:
    """
    Get comments for a specific applicant, ordered by most recent first,
    limited to MAX_COMMENTS, with recruiter info joined.

    Args:
        applicant_id: UUID of the applicant

    Returns:
        List of comment dictionaries with recruiter info
    """
    return get_comments_by_applicant(applicant_id, MAX_COMMENTS)


def create_comment(comment: Comment) -> Comment:
    """
    Create a new comment

    Args:
        comment: Comment object to create

    Returns:
        Created Comment with ID and timestamps
    """
    data = comment.to_dict()
    result = insert_record(TABLE_NAME, data)

    if result and len(result) > 0:
        return Comment.from_dict(result[0])
    raise Exception("Failed to create comment")


def update_comment(comment_id: str, updates: Dict[str, Any]) -> Optional[Comment]:
    """
    Update a comment

    Args:
        comment_id: UUID of the comment to update
        updates: Dictionary of fields to update

    Returns:
        Updated Comment or None if not found
    """
    result = update_record(TABLE_NAME, comment_id, updates)

    if result and len(result) > 0:
        return Comment.from_dict(result[0])
    return None


def delete_comment(comment_id: str) -> bool:
    """
    Permanently delete a comment

    Args:
        comment_id: UUID of the comment to delete

    Returns:
        True if deleted, False if not found
    """
    result = delete_record(TABLE_NAME, comment_id)
    return bool(result and len(result) > 0)
