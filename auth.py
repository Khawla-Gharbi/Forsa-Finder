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