from app import db

class LocalInstituteDetails(db.Model):
    __tablename__ = "local_institutes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    service_offered = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    target_audience = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.String(50), nullable=True)
