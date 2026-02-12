"""
Main Flask application for Vercel serverless deployment
"""
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from .database import query_table, insert_record, update_record, delete_record
from .applicants import (
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
from .clients import (
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
from .recruiters import (
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
from .job_descriptions import (
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
from .applicant_job_apply import (
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

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

# Error handler for 500
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running"""
    return jsonify({
        "status": "healthy",
        "message": "API is running successfully"
    }), 200

# Generic GET endpoint - retrieve all records from a table
@app.route('/api/<table_name>', methods=['GET'])
def get_records(table_name):
    """
    Get all records from a specified table
    
    Query parameters:
        - Any column name can be used as a filter (e.g., ?status=active)
    """
    try:
        # Get query parameters for filtering
        filters = request.args.to_dict()
        
        # Query the table
        data = query_table(table_name, filters if filters else None)
        
        return jsonify({
            "success": True,
            "data": data,
            "count": len(data)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Generic GET endpoint - retrieve a single record by ID
@app.route('/api/<table_name>/<int:record_id>', methods=['GET'])
def get_record(table_name, record_id):
    """Get a single record by ID from a specified table"""
    try:
        data = query_table(table_name, {"id": record_id})
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Record not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": data[0]
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Generic POST endpoint - create a new record
@app.route('/api/<table_name>', methods=['POST'])
def create_record(table_name):
    """
    Create a new record in a specified table
    
    Request body should be JSON with the record data
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Insert the record
        result = insert_record(table_name, data)
        
        return jsonify({
            "success": True,
            "data": result,
            "message": "Record created successfully"
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Generic PUT endpoint - update a record
@app.route('/api/<table_name>/<int:record_id>', methods=['PUT'])
def update_record_endpoint(table_name, record_id):
    """
    Update a record in a specified table
    
    Request body should be JSON with the fields to update
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Update the record
        result = update_record(table_name, record_id, data)
        
        if not result:
            return jsonify({
                "success": False,
                "error": "Record not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": result,
            "message": "Record updated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Generic DELETE endpoint - delete a record
@app.route('/api/<table_name>/<int:record_id>', methods=['DELETE'])
def delete_record_endpoint(table_name, record_id):
    """Delete a record from a specified table"""
    try:
        # Delete the record
        result = delete_record(table_name, record_id)
        
        if not result:
            return jsonify({
                "success": False,
                "error": "Record not found"
            }), 404
        
        return jsonify({
            "success": True,
            "message": "Record deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================
# APPLICANTS API ENDPOINTS
# ============================

@app.route('/api/applicants', methods=['GET'])
def list_applicants():
    """Get all applicants (active by default)"""
    try:
        include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
        applicants = get_all_applicants(include_inactive=include_inactive)
        
        return jsonify({
            "success": True,
            "data": [{
                "id": str(a.id),
                "name": a.name,
                "last_name": a.last_name,
                "linkedin": a.linkedin,
                "email": a.email,
                "phone": a.phone,
                "city": a.city,
                "english": a.english,
                "created_at": a.created_at.isoformat() if a.created_at else None,
                "deactive_at": a.deactive_at.isoformat() if a.deactive_at else None,
            } for a in applicants],
            "count": len(applicants)
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicants/search', methods=['GET'])
def search_applicants_endpoint():
    """Search applicants by name, city, english level, or email"""
    try:
        name = request.args.get('name')
        city = request.args.get('city')
        english = request.args.get('english')
        email = request.args.get('email')
        
        applicants = search_applicants(
            name=name,
            city=city,
            english_level=english,
            email=email
        )
        
        return jsonify({
            "success": True,
            "data": [{
                "id": str(a.id),
                "name": a.name,
                "last_name": a.last_name,
                "linkedin": a.linkedin,
                "email": a.email,
                "phone": a.phone,
                "city": a.city,
                "english": a.english,
            } for a in applicants],
            "count": len(applicants)
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicants/<applicant_id>', methods=['GET'])
def get_applicant(applicant_id):
    """Get a single applicant by ID"""
    try:
        applicant = get_applicant_by_id(applicant_id)
        
        if not applicant:
            return jsonify({"success": False, "error": "Applicant not found"}), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": str(applicant.id),
                "name": applicant.name,
                "last_name": applicant.last_name,
                "linkedin": applicant.linkedin,
                "email": applicant.email,
                "phone": applicant.phone,
                "city": applicant.city,
                "english": applicant.english,
                "created_at": applicant.created_at.isoformat() if applicant.created_at else None,
                "deactive_at": applicant.deactive_at.isoformat() if applicant.deactive_at else None,
            }
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicants', methods=['POST'])
def create_applicant_endpoint():
    """Create a new applicant"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Required fields
        required = ['name', 'last_name', 'email', 'phone', 'city', 'english']
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({"success": False, "error": f"Missing fields: {', '.join(missing)}"}), 400
        
        applicant = Applicant(
            name=data['name'],
            last_name=data['last_name'],
            linkedin=data.get('linkedin', ''),
            email=data['email'],
            phone=data['phone'],
            city=data['city'],
            english=data['english'],
        )
        
        created = create_applicant(applicant)
        
        return jsonify({
            "success": True,
            "data": {
                "id": str(created.id),
                "name": created.name,
                "last_name": created.last_name,
                "email": created.email,
            },
            "message": "Applicant created successfully"
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicants/<applicant_id>', methods=['PUT'])
def update_applicant_endpoint(applicant_id):
    """Update an applicant"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        updated = update_applicant(applicant_id, data)
        
        if not updated:
            return jsonify({"success": False, "error": "Applicant not found"}), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": str(updated.id),
                "name": updated.name,
                "last_name": updated.last_name,
                "email": updated.email,
            },
            "message": "Applicant updated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicants/<applicant_id>', methods=['DELETE'])
def delete_applicant_endpoint(applicant_id):
    """Permanently delete an applicant"""
    try:
        success = delete_applicant(applicant_id)
        
        if not success:
            return jsonify({"success": False, "error": "Applicant not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Applicant deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicants/<applicant_id>/deactivate', methods=['POST'])
def deactivate_applicant_endpoint(applicant_id):
    """Soft delete - deactivate an applicant"""
    try:
        updated = deactivate_applicant(applicant_id)
        
        if not updated:
            return jsonify({"success": False, "error": "Applicant not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Applicant deactivated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicants/<applicant_id>/reactivate', methods=['POST'])
def reactivate_applicant_endpoint(applicant_id):
    """Reactivate a deactivated applicant"""
    try:
        updated = reactivate_applicant(applicant_id)
        
        if not updated:
            return jsonify({"success": False, "error": "Applicant not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Applicant reactivated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================
# CLIENTS API ENDPOINTS
# ============================

@app.route('/api/clients', methods=['GET'])
def list_clients():
    """Get all clients (active by default)"""
    try:
        include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
        clients = get_all_clients(include_inactive=include_inactive)
        
        return jsonify({
            "success": True,
            "data": [{
                "id": str(c.id),
                "description": c.description,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "deactive": c.deactive.isoformat() if c.deactive else None,
            } for c in clients],
            "count": len(clients)
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/clients/search', methods=['GET'])
def search_clients_endpoint():
    """Search clients by description"""
    try:
        description = request.args.get('description')
        
        clients = search_clients(description=description)
        
        return jsonify({
            "success": True,
            "data": [{
                "id": str(c.id),
                "description": c.description,
                "created_at": c.created_at.isoformat() if c.created_at else None,
            } for c in clients],
            "count": len(clients)
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/clients/<client_id>', methods=['GET'])
def get_client(client_id):
    """Get a single client by ID"""
    try:
        client = get_client_by_id(client_id)
        
        if not client:
            return jsonify({"success": False, "error": "Client not found"}), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": str(client.id),
                "description": client.description,
                "created_at": client.created_at.isoformat() if client.created_at else None,
                "deactive": client.deactive.isoformat() if client.deactive else None,
            }
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/clients', methods=['POST'])
def create_client_endpoint():
    """Create a new client"""
    try:
        data = request.get_json()
        
        client = Client(
            description=data.get('description') if data else None
        )
        
        created = create_client(client)
        
        return jsonify({
            "success": True,
            "data": {
                "id": str(created.id),
                "description": created.description,
            },
            "message": "Client created successfully"
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/clients/<client_id>', methods=['PUT'])
def update_client_endpoint(client_id):
    """Update a client"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        updated = update_client(client_id, data)
        
        if not updated:
            return jsonify({"success": False, "error": "Client not found"}), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": str(updated.id),
                "description": updated.description,
            },
            "message": "Client updated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/clients/<client_id>', methods=['DELETE'])
def delete_client_endpoint(client_id):
    """Permanently delete a client"""
    try:
        success = delete_client(client_id)
        
        if not success:
            return jsonify({"success": False, "error": "Client not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Client deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/clients/<client_id>/deactivate', methods=['POST'])
def deactivate_client_endpoint(client_id):
    """Soft delete - deactivate a client"""
    try:
        updated = deactivate_client(client_id)
        
        if not updated:
            return jsonify({"success": False, "error": "Client not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Client deactivated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/clients/<client_id>/reactivate', methods=['POST'])
def reactivate_client_endpoint(client_id):
    """Reactivate a deactivated client"""
    try:
        updated = reactivate_client(client_id)
        
        if not updated:
            return jsonify({"success": False, "error": "Client not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Client reactivated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================
# RECRUITERS API ENDPOINTS
# ============================

@app.route('/api/recruiters', methods=['GET'])
def list_recruiters():
    """Get all recruiters (active by default)"""
    try:
        include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
        recruiters = get_all_recruiters(include_inactive=include_inactive)
        
        return jsonify({
            "success": True,
            "data": [{
                "id": str(r.id),
                "name": r.name,
                "description": r.description,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "deactive_at": r.deactive_at.isoformat() if r.deactive_at else None,
            } for r in recruiters],
            "count": len(recruiters)
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/recruiters/search', methods=['GET'])
def search_recruiters_endpoint():
    """Search recruiters by name or description"""
    try:
        name = request.args.get('name')
        description = request.args.get('description')
        
        recruiters = search_recruiters(name=name, description=description)
        
        return jsonify({
            "success": True,
            "data": [{
                "id": str(r.id),
                "name": r.name,
                "description": r.description,
            } for r in recruiters],
            "count": len(recruiters)
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/recruiters/<recruiter_id>', methods=['GET'])
def get_recruiter(recruiter_id):
    """Get a single recruiter by ID"""
    try:
        recruiter = get_recruiter_by_id(recruiter_id)
        
        if not recruiter:
            return jsonify({"success": False, "error": "Recruiter not found"}), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": str(recruiter.id),
                "name": recruiter.name,
                "description": recruiter.description,
                "created_at": recruiter.created_at.isoformat() if recruiter.created_at else None,
                "deactive_at": recruiter.deactive_at.isoformat() if recruiter.deactive_at else None,
            }
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/recruiters', methods=['POST'])
def create_recruiter_endpoint():
    """Create a new recruiter"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({"success": False, "error": "Name is required"}), 400
        
        recruiter = Recruiter(
            name=data['name'],
            description=data.get('description')
        )
        
        created = create_recruiter(recruiter)
        
        return jsonify({
            "success": True,
            "data": {
                "id": str(created.id),
                "name": created.name,
                "description": created.description,
            },
            "message": "Recruiter created successfully"
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/recruiters/<recruiter_id>', methods=['PUT'])
def update_recruiter_endpoint(recruiter_id):
    """Update a recruiter"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        updated = update_recruiter(recruiter_id, data)
        
        if not updated:
            return jsonify({"success": False, "error": "Recruiter not found"}), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": str(updated.id),
                "name": updated.name,
                "description": updated.description,
            },
            "message": "Recruiter updated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/recruiters/<recruiter_id>', methods=['DELETE'])
def delete_recruiter_endpoint(recruiter_id):
    """Permanently delete a recruiter"""
    try:
        success = delete_recruiter(recruiter_id)
        
        if not success:
            return jsonify({"success": False, "error": "Recruiter not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Recruiter deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/recruiters/<recruiter_id>/deactivate', methods=['POST'])
def deactivate_recruiter_endpoint(recruiter_id):
    """Soft delete - deactivate a recruiter"""
    try:
        updated = deactivate_recruiter(recruiter_id)
        
        if not updated:
            return jsonify({"success": False, "error": "Recruiter not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Recruiter deactivated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/recruiters/<recruiter_id>/reactivate', methods=['POST'])
def reactivate_recruiter_endpoint(recruiter_id):
    """Reactivate a deactivated recruiter"""
    try:
        updated = reactivate_recruiter(recruiter_id)
        
        if not updated:
            return jsonify({"success": False, "error": "Recruiter not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Recruiter reactivated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================
# JOB DESCRIPTIONS API ENDPOINTS
# ============================

@app.route('/api/job-descriptions', methods=['GET'])
def list_job_descriptions():
    """Get all job descriptions (active by default)"""
    try:
        include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
        jobs = get_all_job_descriptions(include_inactive=include_inactive)
        
        return jsonify({
            "success": True,
            "data": [{
                "id": str(j.id),
                "description": j.description,
                "min_salary": j.min_salary,
                "max_salary": j.max_salary,
                "status": j.status,
                "recruiter_id": j.recruiter_id,
                "client_id": str(j.client_id) if j.client_id else None,
                "created_at": j.created_at.isoformat() if j.created_at else None,
                "deactive_at": j.deactive_at.isoformat() if j.deactive_at else None,
            } for j in jobs],
            "count": len(jobs)
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/job-descriptions/search', methods=['GET'])
def search_job_descriptions_endpoint():
    """Search job descriptions by filters"""
    try:
        status = request.args.get('status')
        client_id = request.args.get('client_id')
        recruiter_id = request.args.get('recruiter_id', type=int)
        min_salary_min = request.args.get('min_salary_min', type=float)
        min_salary_max = request.args.get('min_salary_max', type=float)
        
        jobs = search_job_descriptions(
            status=status,
            client_id=client_id,
            recruiter_id=recruiter_id,
            min_salary_min=min_salary_min,
            min_salary_max=min_salary_max
        )
        
        return jsonify({
            "success": True,
            "data": [{
                "id": str(j.id),
                "description": j.description,
                "min_salary": j.min_salary,
                "max_salary": j.max_salary,
                "status": j.status,
                "recruiter_id": j.recruiter_id,
                "client_id": str(j.client_id) if j.client_id else None,
            } for j in jobs],
            "count": len(jobs)
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/job-descriptions/<job_id>', methods=['GET'])
def get_job_description(job_id):
    """Get a single job description by ID"""
    try:
        job = get_job_description_by_id(job_id)
        
        if not job:
            return jsonify({"success": False, "error": "Job description not found"}), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": str(job.id),
                "description": job.description,
                "min_salary": job.min_salary,
                "max_salary": job.max_salary,
                "status": job.status,
                "recruiter_id": job.recruiter_id,
                "client_id": str(job.client_id) if job.client_id else None,
                "created_at": job.created_at.isoformat() if job.created_at else None,
                "deactive_at": job.deactive_at.isoformat() if job.deactive_at else None,
            }
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/job-descriptions', methods=['POST'])
def create_job_description_endpoint():
    """Create a new job description"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Required field
        if 'min_salary' not in data:
            return jsonify({"success": False, "error": "min_salary is required"}), 400
        
        # Parse client_id if provided
        client_id = None
        if data.get('client_id'):
            client_id = uuid.UUID(data['client_id'])
        
        job = JobDescription(
            description=data.get('description'),
            min_salary=float(data['min_salary']),
            max_salary=float(data['max_salary']) if data.get('max_salary') else None,
            status=data.get('status', 'OPEN'),
            recruiter_id=data.get('recruiter_id'),
            client_id=client_id,
        )
        
        created = create_job_description(job)
        
        return jsonify({
            "success": True,
            "data": {
                "id": str(created.id),
                "description": created.description,
                "min_salary": created.min_salary,
                "max_salary": created.max_salary,
                "status": created.status,
            },
            "message": "Job description created successfully"
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/job-descriptions/<job_id>', methods=['PUT'])
def update_job_description_endpoint(job_id):
    """Update a job description"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        updated = update_job_description(job_id, data)
        
        if not updated:
            return jsonify({"success": False, "error": "Job description not found"}), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": str(updated.id),
                "description": updated.description,
                "min_salary": updated.min_salary,
                "max_salary": updated.max_salary,
                "status": updated.status,
            },
            "message": "Job description updated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/job-descriptions/<job_id>', methods=['DELETE'])
def delete_job_description_endpoint(job_id):
    """Permanently delete a job description"""
    try:
        success = delete_job_description(job_id)
        
        if not success:
            return jsonify({"success": False, "error": "Job description not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Job description deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/job-descriptions/<job_id>/close', methods=['POST'])
def close_job_description_endpoint(job_id):
    """Close a job description"""
    try:
        updated = close_job_description(job_id)
        
        if not updated:
            return jsonify({"success": False, "error": "Job description not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Job description closed successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/job-descriptions/<job_id>/reopen', methods=['POST'])
def reopen_job_description_endpoint(job_id):
    """Reopen a closed job description"""
    try:
        updated = reopen_job_description(job_id)
        
        if not updated:
            return jsonify({"success": False, "error": "Job description not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Job description reopened successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/job-descriptions/<job_id>/status', methods=['PUT'])
def change_job_status_endpoint(job_id):
    """Change job description status"""
    try:
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({"success": False, "error": "Status is required"}), 400
        
        updated = change_job_status(job_id, data['status'])
        
        if not updated:
            return jsonify({"success": False, "error": "Job description not found"}), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": str(updated.id),
                "status": updated.status,
            },
            "message": "Status updated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================
# APPLICANT JOB APPLICATIONS API ENDPOINTS
# ============================

@app.route('/api/applicant-job-applications', methods=['GET'])
def list_applications():
    """Get all job applications (active by default)"""
    try:
        include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
        applications = get_all_applications(include_inactive=include_inactive)
        
        return jsonify({
            "success": True,
            "data": [{
                "id": a.id,
                "applicant_id": str(a.applicant_id),
                "job_description_id": str(a.job_description_id),
                "recruiter_id": str(a.recruiter_id) if a.recruiter_id else None,
                "created_at": a.created_at.isoformat() if a.created_at else None,
                "deactive_at": a.deactive_at.isoformat() if a.deactive_at else None,
            } for a in applications],
            "count": len(applications)
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicant-job-applications/search', methods=['GET'])
def search_applications_endpoint():
    """Search job applications by filters"""
    try:
        applicant_id = request.args.get('applicant_id')
        job_description_id = request.args.get('job_description_id')
        recruiter_id = request.args.get('recruiter_id')
        
        applications = search_applications(
            applicant_id=applicant_id,
            job_description_id=job_description_id,
            recruiter_id=recruiter_id
        )
        
        return jsonify({
            "success": True,
            "data": [{
                "id": a.id,
                "applicant_id": str(a.applicant_id),
                "job_description_id": str(a.job_description_id),
                "recruiter_id": str(a.recruiter_id) if a.recruiter_id else None,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            } for a in applications],
            "count": len(applications)
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicant-job-applications/<int:application_id>', methods=['GET'])
def get_application(application_id):
    """Get a single job application by ID"""
    try:
        application = get_application_by_id(application_id)
        
        if not application:
            return jsonify({"success": False, "error": "Job application not found"}), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": application.id,
                "applicant_id": str(application.applicant_id),
                "job_description_id": str(application.job_description_id),
                "recruiter_id": str(application.recruiter_id) if application.recruiter_id else None,
                "created_at": application.created_at.isoformat() if application.created_at else None,
                "deactive_at": application.deactive_at.isoformat() if application.deactive_at else None,
            }
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicant-job-applications', methods=['POST'])
def create_application_endpoint():
    """Create a new job application"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Required fields
        if 'applicant_id' not in data:
            return jsonify({"success": False, "error": "applicant_id is required"}), 400
        if 'job_description_id' not in data:
            return jsonify({"success": False, "error": "job_description_id is required"}), 400
        
        # Parse UUIDs
        applicant_id = uuid.UUID(data['applicant_id'])
        job_description_id = uuid.UUID(data['job_description_id'])
        recruiter_id = uuid.UUID(data['recruiter_id']) if data.get('recruiter_id') else None
        
        application = ApplicantJobApply(
            applicant_id=applicant_id,
            job_description_id=job_description_id,
            recruiter_id=recruiter_id,
        )
        
        created = create_application(application)
        
        return jsonify({
            "success": True,
            "data": {
                "id": created.id,
                "applicant_id": str(created.applicant_id),
                "job_description_id": str(created.job_description_id),
                "recruiter_id": str(created.recruiter_id) if created.recruiter_id else None,
                "created_at": created.created_at.isoformat() if created.created_at else None,
            },
            "message": "Job application created successfully"
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicant-job-applications/<int:application_id>', methods=['PUT'])
def update_application_endpoint(application_id):
    """Update a job application"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Convert UUID strings to UUID objects if present
        updates = data.copy()
        if 'applicant_id' in updates:
            updates['applicant_id'] = str(uuid.UUID(updates['applicant_id']))
        if 'job_description_id' in updates:
            updates['job_description_id'] = str(uuid.UUID(updates['job_description_id']))
        if 'recruiter_id' in updates and updates['recruiter_id']:
            updates['recruiter_id'] = str(uuid.UUID(updates['recruiter_id']))
        
        updated = update_application(application_id, updates)
        
        if not updated:
            return jsonify({"success": False, "error": "Job application not found"}), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": updated.id,
                "applicant_id": str(updated.applicant_id),
                "job_description_id": str(updated.job_description_id),
                "recruiter_id": str(updated.recruiter_id) if updated.recruiter_id else None,
            },
            "message": "Job application updated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicant-job-applications/<int:application_id>', methods=['DELETE'])
def delete_application_endpoint(application_id):
    """Permanently delete a job application"""
    try:
        success = delete_application(application_id)
        
        if not success:
            return jsonify({"success": False, "error": "Job application not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Job application deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicant-job-applications/<int:application_id>/deactivate', methods=['POST'])
def deactivate_application_endpoint(application_id):
    """Soft delete - deactivate/withdraw a job application"""
    try:
        updated = deactivate_application(application_id)
        
        if not updated:
            return jsonify({"success": False, "error": "Job application not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Job application deactivated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicant-job-applications/<int:application_id>/reactivate', methods=['POST'])
def reactivate_application_endpoint(application_id):
    """Reactivate a deactivated job application"""
    try:
        updated = reactivate_application(application_id)
        
        if not updated:
            return jsonify({"success": False, "error": "Job application not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Job application reactivated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicant-job-applications/<int:application_id>/assign-recruiter', methods=['POST'])
def assign_recruiter_endpoint(application_id):
    """Assign a recruiter to a job application"""
    try:
        data = request.get_json()
        
        if not data or 'recruiter_id' not in data:
            return jsonify({"success": False, "error": "recruiter_id is required"}), 400
        
        updated = assign_recruiter(application_id, data['recruiter_id'])
        
        if not updated:
            return jsonify({"success": False, "error": "Job application not found"}), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": updated.id,
                "recruiter_id": str(updated.recruiter_id) if updated.recruiter_id else None,
            },
            "message": "Recruiter assigned successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/applicant-job-applications/<int:application_id>/unassign-recruiter', methods=['POST'])
def unassign_recruiter_endpoint(application_id):
    """Remove recruiter assignment from a job application"""
    try:
        updated = unassign_recruiter(application_id)
        
        if not updated:
            return jsonify({"success": False, "error": "Job application not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Recruiter unassigned successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# For local development
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
