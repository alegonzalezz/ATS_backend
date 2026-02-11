"""
Example usage of the Applicants CRUD client

This file demonstrates how to use the applicants module
for CRUD operations on the applicants table.
"""

# =============
# OPTION 1: Direct Python Usage
# =============

from applicants import (
    Applicant,
    get_all_applicants,
    get_applicant_by_id,
    search_applicants,
    create_applicant,
    update_applicant,
    delete_applicant,
    deactivate_applicant,
    reactivate_applicant,
)

# Create a new applicant
new_applicant = Applicant(
    name="John",
    last_name="Doe",
    linkedin="https://linkedin.com/in/johndoe",
    email="john.doe@example.com",
    phone="+1234567890",
    city="New York",
    english="advanced",
)

created = create_applicant(new_applicant)
print(f"Created applicant with ID: {created.id}")

# Get all active applicants
applicants = get_all_applicants()
for app in applicants:
    print(f"{app.name} {app.last_name} - {app.email}")

# Get all applicants including inactive
all_applicants = get_all_applicants(include_inactive=True)

# Get a specific applicant by ID
applicant = get_applicant_by_id("uuid-here")
if applicant:
    print(f"Found: {applicant.name}")

# Search applicants
results = search_applicants(
    name="John",
    city="New York",
    english_level="advanced"
)

# Update an applicant
updated = update_applicant("uuid-here", {
    "city": "San Francisco",
    "english": "fluent"
})

# Deactivate (soft delete)
deactivate_applicant("uuid-here")

# Reactivate
reactivate_applicant("uuid-here")

# Permanently delete
delete_applicant("uuid-here")


# =============
# OPTION 2: Using HTTP API Endpoints
# =============

# The following endpoints are available:

# 1. List all applicants (active by default)
# GET /api/applicants
# GET /api/applicants?include_inactive=true

# 2. Search applicants
# GET /api/applicants/search?name=John&city=New York&english=advanced

# 3. Get single applicant
# GET /api/applicants/<uuid>

# 4. Create applicant
# POST /api/applicants
# Body: {
#   "name": "John",
#   "last_name": "Doe",
#   "linkedin": "https://linkedin.com/in/johndoe",
#   "email": "john.doe@example.com",
#   "phone": "+1234567890",
#   "city": "New York",
#   "english": "advanced"
# }

# 5. Update applicant
# PUT /api/applicants/<uuid>
# Body: {
#   "city": "San Francisco",
#   "english": "fluent"
# }

# 6. Delete applicant (permanent)
# DELETE /api/applicants/<uuid>

# 7. Deactivate (soft delete)
# POST /api/applicants/<uuid>/deactivate

# 8. Reactivate
# POST /api/applicants/<uuid>/reactivate


# =============
# Example cURL commands
# =============

"""
# Create applicant
curl -X POST http://localhost:5000/api/applicants \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria",
    "last_name": "Garcia",
    "linkedin": "https://linkedin.com/in/mariagarcia",
    "email": "maria.garcia@example.com",
    "phone": "+5491122334455",
    "city": "Buenos Aires",
    "english": "fluent"
  }'

# List all applicants
curl http://localhost:5000/api/applicants

# Search by name
curl "http://localhost:5000/api/applicants/search?name=Maria"

# Update applicant
curl -X PUT http://localhost:5000/api/applicants/<uuid> \
  -H "Content-Type: application/json" \
  -d '{"city": "Cordoba"}'

# Deactivate
curl -X POST http://localhost:5000/api/applicants/<uuid>/deactivate

# Reactivate
curl -X POST http://localhost:5000/api/applicants/<uuid>/reactivate

# Delete permanently
curl -X DELETE http://localhost:5000/api/applicants/<uuid>
"""
