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


load_dotenv()
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:Postgres25@localhost:5432/prepadvisor')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
app.config['SESSION_PERMANENT']=False


CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)
ma = Marshmallow(app)

from resources.program_routes import program_routes
from resources.applicant_routes import applicant_routes
from resources.mentor_routes import mentor_routes
from resources.local_institute_routes import local_institute_routes


app.register_blueprint(program_routes, url_prefix='/api')
app.register_blueprint(applicant_routes, url_prefix='/api')
app.register_blueprint(mentor_routes, url_prefix='/api')
app.register_blueprint(local_institute_routes, url_prefix='/api')


# FAQ Question Model
class FAQQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    user_email = db.Column(db.String(100), nullable=False)  # Store the user's email
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# FAQ Answer Model
class FAQAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    user_email = db.Column(db.String(100), nullable=False)  # Store the user's email
    question_id = db.Column(db.Integer, db.ForeignKey('faq_question.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

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
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',  

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
    return redirect('/')  

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

# Route to display the FAQ section
@app.route('/faq')
def faq():
    questions = FAQQuestion.query.order_by(FAQQuestion.timestamp.desc()).all()
    questions_with_answers = []
    for question in questions:
        answers = FAQAnswer.query.filter_by(question_id=question.id).order_by(FAQAnswer.timestamp.asc()).all()
        questions_with_answers.append({
            'question': question,
            'answers': answers
        })
    return render_template('faq.html', questions_with_answers=questions_with_answers, user=session.get('user'))

# Route to post a new question
@app.route('/post_question', methods=['POST'])
def post_question():
    if 'user' not in session:
        return jsonify({'error': 'You must be logged in to post a question.'}), 401

    data = request.json
    content = data.get('content')
    user_email = session['user']['email']  # Get the user's email from the session

    if not content:
        return jsonify({'error': 'Question content cannot be empty.'}), 400

    new_question = FAQQuestion(content=content, user_email=user_email)
    db.session.add(new_question)
    db.session.commit()

    return jsonify({'message': 'Question posted successfully!'}), 200

# Route to post a reply to a question
@app.route('/post_answer/<int:question_id>', methods=['POST'])
def post_answer(question_id):
    if 'user' not in session:
        return jsonify({'error': 'You must be logged in to post an answer.'}), 401

    data = request.json
    content = data.get('content')
    user_email = session['user']['email']  # Get the user's email from the session

    if not content:
        return jsonify({'error': 'Answer content cannot be empty.'}), 400

    new_answer = FAQAnswer(content=content, user_email=user_email, question_id=question_id)
    db.session.add(new_answer)
    db.session.commit()

    return jsonify({'message': 'Answer posted successfully!'}), 200
if __name__ == "__main__":
    app.run(debug=True)