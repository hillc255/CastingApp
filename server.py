from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

# Initialize Authlib

app = Flask(__name__)

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='f7ZLU2DmWeRcLuikyEKjqk0893KA2Mbj',
    client_secret='b6t4L2VnWaPAvVfXJ0QVTIzqbNxgALsY8_ikVO-0OMza0_RG-vXKg_89AQxoiyLj',
    api_base_url='https://autumn-voice-0666.us.auth0.com',
    access_token_url='https://autumn-voice-0666.us.auth0.com/oauth/token',
    authorize_url='https://autumn-voice-0666.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

# Callback Handler

# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')

# Trigger Authentication

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='https://cast-app.herokuapp.com/callback')

# Check if user is authenticated

def requires_auth(f):
      @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated