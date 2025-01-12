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


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:Postgres25@localhost:5432/prepadvisor')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
app.config['SESSION_PERMANENT']=False


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


# OAuth configuration
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',  # Add this line

)

# Route for initiating the Google OAuth login
@app.route('/login')
def login():
    try:
        redirect_uri = url_for('authorize', _external=True)
        print(f"Redirect URI: {redirect_uri}")  # Debugging
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        print(f"Error in /login: {e}")  # Debugging
        return "An error occurred during login. Please try again."

# Route for handling the callback after Google OAuth login
@app.route('/callback')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['user'] = user_info
    return redirect('/')  # Redirect to the homepage after successful login

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# Route for the homepage
@app.route('/')
def index():
    user = session.get('user')
    return render_template('index1.html', user=user)
# Routes for rendering the HTML pages

@app.route('/mentors')
def mentors_page():
    return render_template('mentor_database.html')
@app.route('/institutes')
def institutes_page():
    return render_template('institutes.html')


if __name__ == "__main__":
    app.run(debug=True)