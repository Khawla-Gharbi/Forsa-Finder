from flask import Blueprint, request, jsonify
from models.program import ProgramDetails
from schemas.program import ProgramSchema
from app import db

program_routes = Blueprint('program_routes', __name__)
program_schema = ProgramSchema()
programs_schema= ProgramSchema(many=True)


@program_routes.route('/program', methods=['POST'])
def add_program():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Check if a program with the same name and location already exists
        existing_program = ProgramDetails.query.filter_by(name=data['name'], location=data['location']).first()
        if existing_program:
            return jsonify({"error": f"A program with the name '{data['name']}' already exists in location '{data['location']}'."}), 400

        new_program = ProgramDetails(
            name=data['name'],
            description=data['description'],
            eligibility_criteria=data['eligibility_criteria'],
            application_deadline=data['application_deadline'],
            duration=data['duration'],
            location=data['location'],
            funding_details=data.get('funding_details'),
            application_link=data['application_link'],
            category=data['category'],
            tunisian_eligibility=data['tunisian_eligibility']
        )

        db.session.add(new_program)
        db.session.commit()

        return jsonify(program_schema.dump(new_program)), 201
    except KeyError as e:
        return jsonify({"error": "Missing required fields in the request data.", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while adding the program.", "details": str(e)}), 500

@program_routes.route('/programs', methods=['GET'])
def get_all_programs():
    try:
        programs = ProgramDetails.query.all()
        return jsonify(programs_schema.dump(programs)), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching programs.", "details": str(e)}), 500
    
@program_routes.route('/program/<int:id>', methods=['PUT'])
def update_program(id):
    try:
        program = ProgramDetails.query.get(id)
        if not program:
            return jsonify({"error": f"Program with ID {id} does not exist."}), 404

        data = request.get_json()

        errors = program_schema.validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        program.name = data['name']
        program.description = data['description']
        program.eligibility_criteria = data['eligibility_criteria']
        program.application_deadline = data['application_deadline']
        program.duration = data['duration']
        program.location = data['location']
        program.funding_details = data.get('funding_details')
        program.application_link = data['application_link']
        program.category = data['category']
        program.tunisian_eligibility = data['tunisian_eligibility']

        db.session.commit()
        return jsonify(program_schema.dump(program)), 200

    except KeyError as e:
        return jsonify({"error": "Missing required fields in the request data.", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred while updating the program with ID {id}.", "details": str(e)}), 500

@program_routes.route('/program/<int:id>', methods=['DELETE'])
def delete_program(id):
    try:
        program = ProgramDetails.query.get_or_404(id)
        db.session.delete(program)
        db.session.commit()
        return jsonify({"message": "Program deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while deleting the program with ID {id}.", "details": str(e)}), 500

@program_routes.route('/programs/location/<string:location>', methods=['GET'])
def get_programs_by_location(location):
    try:
        programs = ProgramDetails.query.filter_by(location=location).all()
        if not programs:
            return jsonify({"message": f"No programs found in location: {location}"}), 404
        return jsonify(programs_schema.dump(programs)), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while fetching programs by location {location}.", "details": str(e)}), 500


@program_routes.route('/programs/category/<string:category>', methods=['GET'])
def get_programs_by_category(category):
    try:
        programs = ProgramDetails.query.filter_by(category=category).all()
        if not programs:
            return jsonify({"message": f"No programs found in category: {category}"}), 404
        return jsonify(programs_schema.dump(programs)), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while fetching programs by category {category}.", "details": str(e)}), 500
    
@program_routes.route('/programs/eligibility/<string:tunisian_eligibility>', methods=['GET'])
def get_programs_by_eligibility(tunisian_eligibility):
    try:
        tunisian_eligibility = tunisian_eligibility.capitalize()
        if tunisian_eligibility not in ['Eligible', 'Not Eligible']:
            return jsonify({"message": "Invalid input for Tunisian eligibility. Use 'Eligible' or 'Not Eligible'."}), 400

        programs = ProgramDetails.query.filter_by(tunisian_eligibility=tunisian_eligibility).all()
        if not programs:
            return jsonify({"message": f"No programs found with Tunisian eligibility: {tunisian_eligibility}"}), 404

        return jsonify(programs_schema.dump(programs)), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while fetching programs by eligibility {tunisian_eligibility}.", "details": str(e)}), 500
