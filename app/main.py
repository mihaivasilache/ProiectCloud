import os
import json
from flask import Flask, request, session, redirect, url_for
import storage
import datastore
import google.cloud.logging
import google.oauth2.credentials
from flask_oauth import OAuth
import json


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'app.json'
CONFIG = json.load(open('client_json.json'))
CLOUD_STORAGE_BUCKET = 'tema-cloud3.appspot.com'
GOOGLE_CLIENT_ID = CONFIG['installed']['client_id']
GOOGLE_CLIENT_SECRET = CONFIG['installed']['client_secret']
REDIRECT_URI = '/auth'
SECRET_KEY = 'AIzaSyAcgsLVd26JLnZW3SyvszXgZ3WJJbI8OxA'
DEBUG = True

storage_client = None
datastore_client = None
logger = None
project_id = 'tema-cloud3'

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

google_auth = oauth.remote_app('tema-cloud3',
                               base_url='https://www.google.com/accounts/',
                               authorize_url='https://accounts.google.com/o/oauth2/auth',
                               request_token_url=None,
                               request_token_params={'scope': 'https://www.googleapis.com/auth/cloud-platform',
                                                     'response_type': 'code'},
                               access_token_url='https://accounts.google.com/o/oauth2/token',
                               access_token_method='POST',
                               access_token_params={'grant_type': 'authorization_code'},
                               consumer_key=GOOGLE_CLIENT_ID,
                               consumer_secret=GOOGLE_CLIENT_SECRET)


@app.route('/upload', methods=['POST'])
def upload():
    logger.log_text('Request for /upload')
    uploaded_file = request.files.get('file')
    datastore.insert(datastore_client, uploaded_file)
    if not uploaded_file:
        return 'No file uploaded.', 400
    return storage.upload_file(storage_client, uploaded_file)


@app.route('/list', methods=['GET'])
def list_files():
    logger.log_text('Request for /list')
    access_token = session.get('access_token')
    logger.log_text('Request for /home')
    if access_token is None:
        return redirect(url_for('login'))

    files = []
    creds = google.oauth2.credentials.Credentials(session.get('access_token')[0])
    datastore_client = datastore.get_client(creds)
    print creds
    for file in datastore.list_files(datastore_client):
        file_ = {}
        items = file.items()
        for item in items:
            if item[0] == 'added':
                file_[item[0]] = str(item[1])
            else:
                file_[item[0]] = str(item[1])
        files.append(file_)
    # storage_files = storage.list_blobs(storage_client)
    # print 'in storage: ', storage_files
    print 'in datastore: ', files
    return json.dumps(files)


@app.route('/delete', methods=['DELETE'])
def delete_files():
    return datastore.delete_files(datastore_client)


@app.route('/login')
def login():
    callback = url_for('authorized', _external=True)
    return google_auth.authorize(callback=callback)


@app.route(REDIRECT_URI)
@google_auth.authorized_handler
def authorized(resp):
    print 'resp', resp
    access_token = resp['access_token']
    print 'access_token', access_token
    session['access_token'] = access_token, ''
    return redirect(url_for('hello'))


@google_auth.tokengetter
def get_access_token():
    return session.get('access_token')


@app.route('/')
def redirect_home():
    return redirect(url_for('hello'))


@app.route('/home')
def hello():
    access_token = session.get('access_token')
    logger.log_text('Request for /home')
    if access_token is None:
        return redirect(url_for('login'))

    # access_token = access_token[0]
    # from urllib2 import Request, urlopen, URLError
    #
    # headers = {'Authorization': 'OAuth ' + access_token}
    # req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
    #               None, headers)
    # try:
    #     res = urlopen(req)
    # except URLError as e:
    #     if e.code == 401:
    #         # Unauthorized - bad token
    #         session.pop('access_token', None)
    #         return redirect(url_for('login'))
    #     return 'Error'

    return 'Hello World!', 200


@app.errorhandler(500)
def server_error(e):
    logger.log_text('An error occurred during a request.')
    return "An internal error occurred: <pre>{}</pre>See logs for full stacktrace.".format(e), 500


@app.before_first_request
def execute_this():
    global logger, storage_client, datastore_client
    logging_client = google.cloud.logging.Client(project_id)
    log_name = 'my-log'
    logger = logging_client.logger(log_name)
    storage_client = storage.get_client()
    # datastore_client = datastore.get_client()
    if 'access_token' in session:
        del session['access_token']


'''
def main(environ, start_response):
	app.run(host='127.0.0.1', port=8000, debug=True)
'''
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
