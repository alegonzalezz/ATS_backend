"""
Example usage of the ApplicantJobApply CRUD client

This file demonstrates how to use the applicant_job_apply module
for CRUD operations on the applicant_job_apply table.
"""

# =============
# OPTION 1: Direct Python Usage
# =============

import uuid
from applicant_job_apply import (
    ApplicantJobApply,
    get_all_applications,
    get_application_by_id,
    get_applications_by_applicant,
    get_applications_by_job,
    search_applications,
    create_application,
    update_application,
    delete_application,
    deactivate_application,
    reactivate_application,
    assign_recruiter,
    unassign_recruiter,
)

# Create a new job application
new_application = ApplicantJobApply(
    applicant_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440000"),
    job_description_id=uuid.UUID("660e8400-e29b-41d4-a716-446655440001"),
    recruiter_id=uuid.UUID("770e8400-e29b-41d4-a716-446655440002"),  # optional
)

created = create_application(new_application)
print(f"Created application with ID: {created.id}")

# Get all active applications
applications = get_all_applications()
for app in applications:
    print(f"Application {app.id}: Applicant {app.applicant_id} -> Job {app.job_description_id}")

# Get all applications including inactive
all_applications = get_all_applications(include_inactive=True)

# Get a specific application by ID
application = get_application_by_id(123)
if application:
    print(f"Found application: {application.id}")

# Get all applications for a specific applicant
applicant_apps = get_applications_by_applicant("550e8400-e29b-41d4-a716-446655440000")
print(f"Applicant has {len(applicant_apps)} applications")

# Get all applications for a specific job
job_apps = get_applications_by_job("660e8400-e29b-41d4-a716-446655440001")
print(f"Job has {len(job_apps)} applications")

# Search applications
results = search_applications(
    applicant_id="550e8400-e29b-41d4-a716-446655440000",
    job_description_id="660e8400-e29b-41d4-a716-446655440001",
    recruiter_id="770e8400-e29b-41d4-a716-446655440002"
)

# Update an application
updated = update_application(123, {
    "recruiter_id": "880e8400-e29b-41d4-a716-446655440003"
})

# Assign a recruiter to an application
assigned = assign_recruiter(123, "880e8400-e29b-41d4-a716-446655440003")
print(f"Assigned recruiter to application: {assigned.recruiter_id}")

# Unassign recruiter from an application
unassigned = unassign_recruiter(123)
print("Recruiter unassigned")

# Deactivate (soft delete/withdraw)
deactivate_application(123)

# Reactivate
reactivate_application(123)

# Permanently delete
delete_application(123)


# =============
# OPTION 2: Using HTTP API Endpoints
# =============

# The following endpoints are available:

# 1. List all applications (active by default)
# GET /api/applicant-job-applications
# GET /api/applicant-job-applications?include_inactive=true

# 2. Search applications
# GET /api/applicant-job-applications/search?applicant_id=uuid&job_description_id=uuid&recruiter_id=uuid

# 3. Get single application
# GET /api/applicant-job-applications/<id>

# 4. Create application
# POST /api/applicant-job-applications
# Body: {
#   "applicant_id": "550e8400-e29b-41d4-a716-446655440000",
#   "job_description_id": "660e8400-e29b-41d4-a716-446655440001",
#   "recruiter_id": "770e8400-e29b-41d4-a716-446655440002"  # optional
# }

# 5. Update application
# PUT /api/applicant-job-applications/<id>
# Body: {
#   "recruiter_id": "880e8400-e29b-41d4-a716-446655440003"
# }

# 6. Delete application (permanent)
# DELETE /api/applicant-job-applications/<id>

# 7. Deactivate (soft delete/withdraw)
# POST /api/applicant-job-applications/<id>/deactivate

# 8. Reactivate
# POST /api/applicant-job-applications/<id>/reactivate

# 9. Assign recruiter
# POST /api/applicant-job-applications/<id>/assign-recruiter
# Body: {
#   "recruiter_id": "880e8400-e29b-41d4-a716-446655440003"
# }

# 10. Unassign recruiter
# POST /api/applicant-job-applications/<id>/unassign-recruiter


# =============
# Example cURL commands
# =============

"""
# Create application
curl -X POST http://localhost:5000/api/applicant-job-applications \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "550e8400-e29b-41d4-a716-446655440000",
    "job_description_id": "660e8400-e29b-41d4-a716-446655440001",
    "recruiter_id": "770e8400-e29b-41d4-a716-446655440002"
  }'

# List all applications
curl http://localhost:5000/api/applicant-job-applications

# Search by applicant
curl "http://localhost:5000/api/applicant-job-applications/search?applicant_id=550e8400-e29b-41d4-a716-446655440000"

# Search by job
curl "http://localhost:5000/api/applicant-job-applications/search?job_description_id=660e8400-e29b-41d4-a716-446655440001"

# Search by recruiter
curl "http://localhost:5000/api/applicant-job-applications/search?recruiter_id=770e8400-e29b-41d4-a716-446655440002"

# Update application
curl -X PUT http://localhost:5000/api/applicant-job-applications/123 \
  -H "Content-Type: application/json" \
  -d '{"recruiter_id": "880e8400-e29b-41d4-a716-446655440003"}'

# Assign recruiter
curl -X POST http://localhost:5000/api/applicant-job-applications/123/assign-recruiter \
  -H "Content-Type: application/json" \
  -d '{"recruiter_id": "880e8400-e29b-41d4-a716-446655440003"}'

# Unassign recruiter
curl -X POST http://localhost:5000/api/applicant-job-applications/123/unassign-recruiter

# Deactivate
curl -X POST http://localhost:5000/api/applicant-job-applications/123/deactivate

# Reactivate
curl -X POST http://localhost:5000/api/applicant-job-applications/123/reactivate

# Delete permanently
curl -X DELETE http://localhost:5000/api/applicant-job-applications/123
"""
