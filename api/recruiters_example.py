"""
Example usage of the Recruiters CRUD client

This file demonstrates how to use the recruiters module
for CRUD operations on the recruiter table.
"""

# =============
# OPTION 1: Direct Python Usage
# =============

from recruiters import (
    Recruiter,
    get_all_recruiters,
    get_recruiter_by_id,
    search_recruiters,
    create_recruiter,
    update_recruiter,
    delete_recruiter,
    deactivate_recruiter,
    reactivate_recruiter,
)

# Create a new recruiter
new_recruiter = Recruiter(
    name="Ana Martinez",
    description="Senior IT Recruiter specialized in Python developers"
)

created = create_recruiter(new_recruiter)
print(f"Created recruiter with ID: {created.id}")

# Get all active recruiters
recruiters = get_all_recruiters()
for rec in recruiters:
    print(f"Recruiter: {rec.id} - {rec.name}")

# Get all recruiters including inactive
all_recruiters = get_all_recruiters(include_inactive=True)

# Get a specific recruiter by ID (id is UUID)
recruiter = get_recruiter_by_id("uuid-here")
if recruiter:
    print(f"Found: {recruiter.name}")

# Search recruiters
results = search_recruiters(name="Ana")
results = search_recruiters(description="Python")

# Update a recruiter
updated = update_recruiter("uuid-here", {
    "description": "Updated description"
})

# Deactivate (soft delete)
deactivate_recruiter("uuid-here")

# Reactivate
reactivate_recruiter("uuid-here")

# Permanently delete
delete_recruiter("uuid-here")


# =============
# OPTION 2: Using HTTP API Endpoints
# =============

# The following endpoints are available:

# 1. List all recruiters (active by default)
# GET /api/recruiters
# GET /api/recruiters?include_inactive=true

# 2. Search recruiters
# GET /api/recruiters/search?name=Ana&description=Python

# 3. Get single recruiter
# GET /api/recruiters/<id>

# 4. Create recruiter
# POST /api/recruiters
# Body: {
#   "name": "Ana Martinez",
#   "description": "Senior IT Recruiter"
# }

# 5. Update recruiter
# PUT /api/recruiters/<id>
# Body: {
#   "description": "Updated description"
# }

# 6. Delete recruiter (permanent)
# DELETE /api/recruiters/<id>

# 7. Deactivate (soft delete)
# POST /api/recruiters/<id>/deactivate

# 8. Reactivate
# POST /api/recruiters/<id>/reactivate


# =============
# Example cURL commands
# =============

"""
# Create recruiter
curl -X POST http://localhost:5000/api/recruiters \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Carlos Rodriguez",
    "description": "Technical Recruiter specialized in backend developers"
  }'

# List all recruiters
curl http://localhost:5000/api/recruiters

# Search by name
curl "http://localhost:5000/api/recruiters/search?name=Carlos"

# Get recruiter by ID (UUID)
curl http://localhost:5000/api/recruiters/<uuid>

# Update recruiter
curl -X PUT http://localhost:5000/api/recruiters/<uuid> \
  -H "Content-Type: application/json" \
  -d '{"description": "Senior Technical Recruiter"}'

# Deactivate
curl -X POST http://localhost:5000/api/recruiters/<uuid>/deactivate

# Reactivate
curl -X POST http://localhost:5000/api/recruiters/<uuid>/reactivate

# Delete permanently
curl -X DELETE http://localhost:5000/api/recruiters/<uuid>
"""
