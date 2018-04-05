import google
import webbrowser
import httplib2
from flask import Flask, request, redirect, url_for, g
import google.oauth2.credentials
import google_auth_oauthlib.flow
from rauth.service import OAuth2Service
import simplejson as json


#
#
# def login_required():
#     def decorated_function(*args, **kwargs):
#         if g.user is None:
#             return redirect(url_for('login', next=request.url))
#         return f(*args, **kwargs)
#
#     return decorated_function
#
#
# @app.route('/')
# @login_required
# def index():
#     # logger.log_text('Request for /')
#     return 'Hello World!', 200
#
#
# @app.route('/login')
def login():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_json.json',
        scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'])
    flow.redirect_uri = 'http://localhost:8000/'
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    print authorization_url, state
    return redirect(authorization_url)

#
