"""
Example usage of the Job Descriptions CRUD client

This file demonstrates how to use the job_descriptions module
for CRUD operations on the job_description table.
"""

# =============
# OPTION 1: Direct Python Usage
# =============

import uuid
from job_descriptions import (
    JobDescription,
    get_all_job_descriptions,
    get_job_description_by_id,
    search_job_descriptions,
    create_job_description,
    update_job_description,
    delete_job_description,
    close_job_description,
    reopen_job_description,
    change_job_status,
)

# Create a new job description
new_job = JobDescription(
    description="Senior Python Developer - Remote position with competitive salary",
    min_salary=50000.0,
    max_salary=80000.0,
    status="OPEN",
    recruiter_id=1,  # ID del recruiter (int8 según el schema)
    client_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440000")  # UUID del cliente
)

created = create_job_description(new_job)
print(f"Created job description with ID: {created.id}")

# Get all active job descriptions
jobs = get_all_job_descriptions()
for job in jobs:
    print(f"Job: {job.id} - {job.description[:50]}... - ${job.min_salary}")

# Get all including inactive
all_jobs = get_all_job_descriptions(include_inactive=True)

# Get a specific job by ID
job = get_job_description_by_id("uuid-here")
if job:
    print(f"Found: {job.description}")

# Search jobs by filters
results = search_job_descriptions(
    status="OPEN",
    client_id="client-uuid-here",
    recruiter_id=1,
    min_salary_min=40000.0,
    min_salary_max=60000.0
)

# Update a job description
updated = update_job_description("uuid-here", {
    "description": "Updated description",
    "max_salary": 90000.0
})

# Change status
change_job_status("uuid-here", "PAUSED")

# Close job (soft delete)
close_job_description("uuid-here")

# Reopen job
reopen_job_description("uuid-here")

# Permanently delete
delete_job_description("uuid-here")


# =============
# OPTION 2: Using HTTP API Endpoints
# =============

# The following endpoints are available:

# 1. List all job descriptions (active by default)
# GET /api/job-descriptions
# GET /api/job-descriptions?include_inactive=true

# 2. Search job descriptions
# GET /api/job-descriptions/search?status=OPEN&client_id=uuid&recruiter_id=1
# GET /api/job-descriptions/search?min_salary_min=40000&min_salary_max=60000

# 3. Get single job description
# GET /api/job-descriptions/<uuid>

# 4. Create job description
# POST /api/job-descriptions
# Body: {
#   "description": "Senior Python Developer...",
#   "min_salary": 50000.0,
#   "max_salary": 80000.0,
#   "status": "OPEN",
#   "recruiter_id": 1,
#   "client_id": "550e8400-e29b-41d4-a716-446655440000"
# }

# 5. Update job description
# PUT /api/job-descriptions/<uuid>
# Body: {
#   "description": "Updated...",
#   "max_salary": 90000.0
# }

# 6. Change status
# PUT /api/job-descriptions/<uuid>/status
# Body: {"status": "PAUSED"}

# 7. Close job (soft delete)
# POST /api/job-descriptions/<uuid>/close

# 8. Reopen job
# POST /api/job-descriptions/<uuid>/reopen

# 9. Delete permanently
# DELETE /api/job-descriptions/<uuid>


# =============
# Example cURL commands
# =============

"""
# Create job description
curl -X POST http://localhost:5000/api/job-descriptions \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Senior Python Developer - Remote work",
    "min_salary": 50000.0,
    "max_salary": 80000.0,
    "status": "OPEN",
    "recruiter_id": 1,
    "client_id": "550e8400-e29b-41d4-a716-446655440000"
  }'

# List all job descriptions
curl http://localhost:5000/api/job-descriptions

# Search by status
curl "http://localhost:5000/api/job-descriptions/search?status=OPEN"

# Search by salary range
curl "http://localhost:5000/api/job-descriptions/search?min_salary_min=40000&min_salary_max=60000"

# Get job by ID
curl http://localhost:5000/api/job-descriptions/<uuid>

# Update job
curl -X PUT http://localhost:5000/api/job-descriptions/<uuid> \
  -H "Content-Type: application/json" \
  -d '{"max_salary": 90000.0}'

# Change status
curl -X PUT http://localhost:5000/api/job-descriptions/<uuid>/status \
  -H "Content-Type: application/json" \
  -d '{"status": "PAUSED"}'

# Close job
curl -X POST http://localhost:5000/api/job-descriptions/<uuid>/close

# Reopen job
curl -X POST http://localhost:5000/api/job-descriptions/<uuid>/reopen

# Delete permanently
curl -X DELETE http://localhost:5000/api/job-descriptions/<uuid>
"""
