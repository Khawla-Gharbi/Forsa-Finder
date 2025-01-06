from flask import Blueprint, request, jsonify
from models.mentor import MentorDetails
from schemas.mentor import MentorSchema
from app import db
from marshmallow.exceptions import ValidationError

mentor_routes = Blueprint('mentor_routes', __name__)

mentor_schema = MentorSchema()
mentors_schema = MentorSchema(many=True)

@mentor_routes.route('/mentor', methods=['POST'])
def register_mentor():
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 415

        data = request.get_json()

        try:
            validated_data = mentor_schema.load(data)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        new_mentor = MentorDetails(**validated_data)
        db.session.add(new_mentor)
        db.session.commit()

        return jsonify(mentor_schema.dump(new_mentor)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mentor_routes.route('/mentors', methods=['GET'])
def get_all_mentors():
    try:
        mentors = MentorDetails.query.all()
        if not mentors:
            return jsonify({"message": "No mentors found."}), 404
        return jsonify(mentors_schema.dump(mentors)), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching all mentors.", "details": str(e)}), 500

@mentor_routes.route('/mentor/<int:id>', methods=['GET'])
def get_mentor(id):
    try:
        mentor = MentorDetails.query.get(id)
        if not mentor:
            return jsonify({"error": f"No mentor found with ID {id}."}), 404
        return jsonify(mentor_schema.dump(mentor)), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching the mentor.", "details": str(e)}), 500


@mentor_routes.route('/mentor/<int:id>', methods=['PUT'])
def update_mentor(id):
    try:
        mentor = MentorDetails.query.get(id)
        if not mentor:
            return jsonify({"error": f"No mentor found with ID {id}."}), 404
        
        data = request.get_json()
        try:
            validated_data = mentor_schema.load(data, partial=True)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        for key, value in validated_data.items():
            setattr(mentor, key, value)

        db.session.commit()
        return jsonify(mentor_schema.dump(mentor)), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while updating the mentor.", "details": str(e)}), 500

@mentor_routes.route('/mentor/<int:id>', methods=['DELETE'])
def delete_mentor(id):
    try:
        mentor = MentorDetails.query.get(id)
        if not mentor:
            return jsonify({"error": f"No mentor found with ID {id}."}), 404

        db.session.delete(mentor)
        db.session.commit()
        return jsonify({"message": "Mentor deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while deleting the mentor.", "details": str(e)}), 500

@mentor_routes.route('/mentors/field/<string:field_of_expertise>', methods=['GET'])
def get_mentors_by_field(field_of_expertise):
    try:
        mentors = MentorDetails.query.filter_by(field_of_expertise=field_of_expertise).all()
        if not mentors:
            return jsonify({"message": f"No mentors found with field of expertise '{field_of_expertise}'."}), 404
        return jsonify(mentors_schema.dump(mentors)), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching mentors by field of expertise.", "details": str(e)}), 500

@mentor_routes.route('/mentors/type/<string:type_of_mentorship>', methods=['GET'])
def get_mentors_by_type(type_of_mentorship):
    try:
        mentors = MentorDetails.query.filter_by(type_of_mentorship=type_of_mentorship).all()
        if not mentors:
            return jsonify({"message": f"No mentors found with type of mentorship '{type_of_mentorship}'."}), 404
        return jsonify(mentors_schema.dump(mentors)), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching mentors by type of mentorship.", "details": str(e)}), 500
