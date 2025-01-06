from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS
import os
from flask import redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import render_template


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
# Configure OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={
        'scope': 'openid email profile',  # Request email and profile info
    },
)

@app.route('/')
def home():
    return render_template('index.html')
def index():
    return 'Welcome to the Google OAuth Flask App! <a href="/login">Login with Google</a>'

@app.route('/login')
def login():
    # Redirect the user to the Google login page
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/callback')
def authorize():
    # Handle the callback from Google
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()  # Fetch user info from Google
    session['user'] = user_info  # Save user info to session
    return jsonify(user_info)  # Display user info

@app.route('/logout')
def logout():
    session.pop('user', None)  # Clear user session
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)