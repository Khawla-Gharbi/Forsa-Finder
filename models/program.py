from app import db

class ProgramDetails(db.Model):
    __tablename__ = "programs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    eligibility_criteria = db.Column(db.Text, nullable=False)
    application_deadline = db.Column(db.Date, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    funding_details = db.Column(db.Text, nullable=True)
    application_link = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    tunisian_eligibility = db.Column(db.String(50), nullable=False)
