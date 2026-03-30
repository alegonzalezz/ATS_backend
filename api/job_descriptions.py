from .job_description_skills import get_skills_for_job, set_skills_for_job, validate_no_skill_duplicates

# ... Existing code remains unchanged ...

def get_job_description_with_skills(job_id: str) -> dict:
    """
    Get a job description and include required/preferred skills
    """
    job = get_job_description_by_id(job_id)
    if not job:
        return None
    skill_map = get_skills_for_job(job_id)
    return {
        **job.to_dict(),
        "id": str(job.id),
        "skills_required": skill_map["required"],
        "skills_preferred": skill_map["preferred"],
    }


def create_job_description_with_skills(job: JobDescription, required_skill_ids: list, preferred_skill_ids: list) -> JobDescription:
    """
    Create job and its associated skills at once (transactional logic).
    """
    # 1. Validar duplicados
    validate_no_skill_duplicates(required_skill_ids, preferred_skill_ids)
    # 2. Crear job
    created = create_job_description(job)
    # 3. Asignar skills
    set_skills_for_job(str(created.id), required_skill_ids, preferred_skill_ids)
    return created


def update_job_description_with_skills(job_id: str, updates: dict, required_skill_ids: list, preferred_skill_ids: list) -> JobDescription:
    """
    Update job and its skills at once
    """
    validate_no_skill_duplicates(required_skill_ids, preferred_skill_ids)
    updated = update_job_description(job_id, updates)
    set_skills_for_job(job_id, required_skill_ids, preferred_skill_ids)
    return updated
