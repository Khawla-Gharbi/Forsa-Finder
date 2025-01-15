from flask import Blueprint, request, jsonify
from models.applicant import ApplicantDetails
from schemas.applicant import ApplicantSchema
from app import db

applicant_routes = Blueprint('applicant_routes', __name__)
applicant_schema = ApplicantSchema()
applicants_schema = ApplicantSchema(many=True)

@applicant_routes.route('/applicant', methods=['POST'])
def create_applicant():
    try:
        data = request.get_json()

        errors = applicant_schema.validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        new_applicant = ApplicantDetails(
            full_name=data['full_name'],
            email=data['email'],
            university=data['university'],
            level_of_study=data['level_of_study'],
            field_of_study=data['field_of_study'],
            goals=data.get('goals'),
            languages_spoken=data.get('languages_spoken'),
            location=data.get('location')
        )

        db.session.add(new_applicant)
        db.session.commit()

        return jsonify(applicant_schema.dump(new_applicant)), 201
    except Exception as e:
        return jsonify({"error": "An error occurred while creating the applicant.", "details": str(e)}), 500

@applicant_routes.route('/applicants', methods=['GET'])
def get_all_applicants():
    try:
        applicants = ApplicantDetails.query.all()
        if not applicants:
            return jsonify({"message": "No applicants found."}), 404
        return jsonify(applicants_schema.dump(applicants)), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching all applicants.", "details": str(e)}), 500

@applicant_routes.route('/applicant/<int:id>', methods=['GET'])
def get_applicant(id):
    try:
        applicant = ApplicantDetails.query.get_or_404(id)
        return jsonify(applicant_schema.dump(applicant)), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while fetching the applicant with ID {id}.", "details": str(e)}), 500

@applicant_routes.route('/applicant/<int:id>', methods=['PUT'])
def update_applicant(id):
    try:
        applicant = ApplicantDetails.query.get_or_404(id)
        data = request.get_json()

        errors = applicant_schema.validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        applicant.full_name = data['full_name']
        applicant.email = data['email']
        applicant.university = data['university']
        applicant.level_of_study = data['level_of_study']
        applicant.field_of_study = data['field_of_study']
        applicant.goals = data.get('goals')
        applicant.languages_spoken = data.get('languages_spoken')
        applicant.location = data.get('location')

        db.session.commit()
        return jsonify(applicant_schema.dump(applicant)), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while updating the applicant with ID {id}.", "details": str(e)}), 500

@applicant_routes.route('/applicant/<int:id>', methods=['DELETE'])
def delete_applicant(id):
    try:
        applicant = ApplicantDetails.query.get_or_404(id)
        db.session.delete(applicant)
        db.session.commit()
        return jsonify({"message": "Applicant deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while deleting the applicant with ID {id}.", "details": str(e)}), 500
