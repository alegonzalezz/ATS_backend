"""
JobDescriptionSkills module - CRUD operations for the job_description_skills table
Handles the relation between job descriptions and their required/preferred skills
"""
import uuid
from typing import List, Dict, Any
from datetime import datetime
from .database import get_supabase_client

# Table name constant
TABLE_NAME = "job_description_skills"


def get_skills_for_job(job_description_id: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get all skills for a given job, split into required and preferred
    Returns a dict: {"required": [..], "preferred": [..]}
    """
    client = get_supabase_client()
    # Join with skills to get name
    query = (
        client.table(TABLE_NAME)
        .select("id, skill_id, required, skill:skills(*)")
        .eq("job_description_id", job_description_id)
    )
    response = query.execute()
    required = []
    preferred = []
    for record in response.data:
        skill = record.get("skill")
        if not skill:
            continue
        entry = {
            "id": skill["id"],
            "name": skill["name"]
        }
        if record.get("required"):
            required.append(entry)
        else:
            preferred.append(entry)
    return {"required": required, "preferred": preferred}


def set_skills_for_job(job_description_id: str,
                       required_skill_ids: List[str],
                       preferred_skill_ids: List[str]) -> None:
    """
    Overwrite all skill associations for a job description.
    Ensures no duplicates and correct required/preferred assignment.
    """
    client = get_supabase_client()
    # Ensure no duplicates between lists
    overlap = set(required_skill_ids) & set(preferred_skill_ids)
    if overlap:
        raise Exception(f"Skills cannot be both required and preferred: {list(overlap)}")
    # Delete existing associations for this job
    client.table(TABLE_NAME).delete().eq("job_description_id", job_description_id).execute()
    # Prepare data
    rows = [
        {"job_description_id": job_description_id, "skill_id": sid, "required": True} for sid in required_skill_ids
    ] + [
        {"job_description_id": job_description_id, "skill_id": sid, "required": False} for sid in preferred_skill_ids
    ]
    if rows:
        client.table(TABLE_NAME).insert(rows).execute()


def validate_no_skill_duplicates(required_skill_ids: List[str], preferred_skill_ids: List[str]):
    """
    Validate there are no skills in both required and preferred.
    """
    overlap = set(required_skill_ids) & set(preferred_skill_ids)
    if overlap:
        raise Exception(f"Skills cannot be both required and preferred: {list(overlap)}")
