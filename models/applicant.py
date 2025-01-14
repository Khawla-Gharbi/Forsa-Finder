from app import db

class ApplicantDetails(db.Model):
    __tablename__ = "applicant_details"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    university = db.Column(db.String(100), nullable=False)
    level_of_study = db.Column(db.String(50), nullable=False)
    field_of_study = db.Column(db.String(100), nullable=False)
    goals = db.Column(db.Text, nullable=True)
    languages_spoken = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
