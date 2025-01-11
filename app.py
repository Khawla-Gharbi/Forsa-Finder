from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS
import os
from flask import redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import render_template ,request 


# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:Postgres25@localhost:5432/prepadvisor')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_NAME'] = None


# Configure CORS properly
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Import and register blueprints
from resources.program_routes import program_routes
from resources.applicant_routes import applicant_routes
from resources.mentor_routes import mentor_routes
from resources.local_institute_routes import local_institute_routes

app.register_blueprint(program_routes, url_prefix='/api')
app.register_blueprint(applicant_routes, url_prefix='/api')
app.register_blueprint(mentor_routes, url_prefix='/api')
app.register_blueprint(local_institute_routes, url_prefix='/api')

# Initialize database
with app.app_context():
    db.create_all()

# Routes for rendering the HTML pages
@app.route('/')
def index():
    return render_template('index1.html') 
@app.route('/mentors')
def mentors_page():
    return render_template('mentor_database.html')
@app.route('/institutes')
def institutes_page():
    return render_template('institutes.html')

if __name__ == "__main__":
    app.run(debug=True)