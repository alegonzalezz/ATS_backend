"""
Example usage of the Clients CRUD client

This file demonstrates how to use the clients module
for CRUD operations on the client table.
"""

# =============
# OPTION 1: Direct Python Usage
# =============

from clients import (
    Client,
    get_all_clients,
    get_client_by_id,
    search_clients,
    create_client,
    update_client,
    delete_client,
    deactivate_client,
    reactivate_client,
)

# Create a new client
new_client = Client(
    description="TechCorp - Software development company based in Buenos Aires"
)

created = create_client(new_client)
print(f"Created client with ID: {created.id}")

# Get all active clients
clients = get_all_clients()
for client in clients:
    print(f"Client: {client.id} - {client.description}")

# Get all clients including inactive
all_clients = get_all_clients(include_inactive=True)

# Get a specific client by ID
client = get_client_by_id("uuid-here")
if client:
    print(f"Found: {client.description}")

# Search clients by description
results = search_clients(description="TechCorp")

# Update a client
updated = update_client("uuid-here", {
    "description": "TechCorp - Updated description"
})

# Deactivate (soft delete)
deactivate_client("uuid-here")

# Reactivate
reactivate_client("uuid-here")

# Permanently delete
delete_client("uuid-here")


# =============
# OPTION 2: Using HTTP API Endpoints
# =============

# The following endpoints are available:

# 1. List all clients (active by default)
# GET /api/clients
# GET /api/clients?include_inactive=true

# 2. Search clients by description
# GET /api/clients/search?description=TechCorp

# 3. Get single client
# GET /api/clients/<uuid>

# 4. Create client
# POST /api/clients
# Body: {
#   "description": "Company description here"
# }

# 5. Update client
# PUT /api/clients/<uuid>
# Body: {
#   "description": "Updated description"
# }

# 6. Delete client (permanent)
# DELETE /api/clients/<uuid>

# 7. Deactivate (soft delete)
# POST /api/clients/<uuid>/deactivate

# 8. Reactivate
# POST /api/clients/<uuid>/reactivate


# =============
# Example cURL commands
# =============

"""
# Create client
curl -X POST http://localhost:5000/api/clients \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Globant - Global IT and software development company"
  }'

# List all clients
curl http://localhost:5000/api/clients

# Search by description
curl "http://localhost:5000/api/clients/search?description=Globant"

# Update client
curl -X PUT http://localhost:5000/api/clients/<uuid> \
  -H "Content-Type: application/json" \
  -d '{"description": "Globant - Updated company info"}'

# Deactivate
curl -X POST http://localhost:5000/api/clients/<uuid>/deactivate

# Reactivate
curl -X POST http://localhost:5000/api/clients/<uuid>/reactivate

# Delete permanently
curl -X DELETE http://localhost:5000/api/clients/<uuid>
"""
