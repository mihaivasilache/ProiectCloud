import time

from google.cloud import storage
from oauth2client.client import OAuth2WebServerFlow
import webbrowser
import json
import socketserver
import http.server

CODE = None


class MyHttpRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        global CODE
        if self.path.startswith('/?code'):
            CODE = self.path[self.path.rfind('code=') + len('code='):]
            self.send_response(200)
            self.end_headers()


def create_server():
    port = 8000
    server_handler = MyHttpRequestHandler
    httpd = socketserver.TCPServer(("", port), server_handler)
    print("serving at port" + str(port))
    httpd.serve_forever()


def create_credentials():
    global CODE
    print("create credentials")
    config = json.load(open('client_json.json'))
    flow = OAuth2WebServerFlow(client_id=config['installed']['client_id'],
                               client_secret=config['installed']['client_secret'],
                               scope='https://www.googleapis.com/auth/cloud-platform',
                               redirect_uri='http://localhost:8000')
    auth_uri = flow.step1_get_authorize_url()
    webbrowser.open(auth_uri)
    while CODE is None:
        time.sleep(1)
    print(CODE)
    credentials = flow.step2_exchange(CODE)
    print(credentials)


def create_bucket(bucket_name, credentials=None):
    """Creates a new bucket."""
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.create_bucket(bucket_name)
    print('Bucket {} created'.format(bucket.name))


def main():
    # thread = threading.Thread(target=create_server)
    # thread.start()
    create_credentials()


if __name__ == '__main__':
    main()
