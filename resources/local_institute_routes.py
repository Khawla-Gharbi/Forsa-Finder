from flask import Blueprint, request, jsonify
from models.local_institute import LocalInstituteDetails   
from schemas.local_institute import LocalInstituteSchema
from app import db

local_institute_routes = Blueprint('local_institute_routes', __name__)

local_institute_schema = LocalInstituteSchema() 
local_institutes_schema = LocalInstituteSchema(many=True)

@local_institute_routes.route('/institute', methods=['POST'])
def add_local_institute():
    data = request.get_json()
    
    
    errors = local_institute_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
        
    new_institute = LocalInstituteDetails(
        name=data['name'],
        type=data['type'],
        service_offered=data['service_offered'],
        location=data['location'],
        contact_email=data.get('contact_email'),
        phone_number=data.get('phone_number'),
        website=data.get('website'),
        target_audience=data['target_audience'],
        cost=data.get('cost')
    )
    
    db.session.add(new_institute)
    db.session.commit()
    
    return jsonify(local_institute_schema.dump(new_institute)), 201

@local_institute_routes.route('/institutes', methods=['GET'])
def get_all_institutes():
    try:
        institutes = LocalInstituteDetails.query.all()
        if not institutes:
            return jsonify({"message": "No institutes found."}), 404
        return jsonify(local_institutes_schema.dump(institutes)), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching all institutes.", "details": str(e)}), 500


@local_institute_routes.route('/institute/<int:id>', methods=['PUT'])
def update_institute(id):
    institute = LocalInstituteDetails.query.get_or_404(id)
    data = request.get_json()
    
    
    errors = local_institute_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
        
    institute.name = data['name']
    institute.type = data['type']
    institute.service_offered = data['service_offered']
    institute.location = data['location']
    institute.contact_email = data.get('contact_email')
    institute.phone_number = data.get('phone_number')
    institute.website = data.get('website')
    institute.target_audience = data['target_audience']
    institute.cost = data.get('cost')
    
    db.session.commit()
    return jsonify(local_institute_schema.dump(institute))

@local_institute_routes.route('/institute/<int:id>', methods=['DELETE'])
def delete_institute(id):
    institute = LocalInstituteDetails.query.get_or_404(id)
    db.session.delete(institute)
    db.session.commit()
    return jsonify({"message": "Institute deleted successfully"}), 200

@local_institute_routes.route('/institutes/service/<string:service_offered>', methods=['GET'])
def get_institutes_by_service(service_offered):
    try:
        institutes = LocalInstituteDetails.query.filter_by(service_offered=service_offered).all()
        if not institutes:
            return jsonify({"message": f"No institutes found offering the service: {service_offered}"}), 404
        return jsonify(local_institutes_schema.dump(institutes)), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching institutes by service.", "details": str(e)}), 500

@local_institute_routes.route('/institutes/location/<string:location>', methods=['GET'])
def get_institutes_by_location(location):
    try:
        institutes = LocalInstituteDetails.query.filter_by(location=location).all()
        if not institutes:
            return jsonify({"message": f"No institutes found in the location: {location}"}), 404
        return jsonify(local_institutes_schema.dump(institutes)), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching institutes by location.", "details": str(e)}), 500
