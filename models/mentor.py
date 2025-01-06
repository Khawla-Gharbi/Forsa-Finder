from app import db

class MentorDetails(db.Model):
    __tablename__ = "mentor_details"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contact_link = db.Column(db.String(255), nullable=True)
    field_of_expertise = db.Column(db.String(100), nullable=False)
    previous_attended_program = db.Column(db.String(100), nullable=True)
    type_of_mentorship = db.Column(db.String(50), nullable=False)
    organization = db.Column(db.String(100), nullable=True)
    availability = db.Column(db.String(50), nullable=False)
