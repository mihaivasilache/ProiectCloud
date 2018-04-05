import json
from oauth2client.client import OAuth2WebServerFlow
import webbrowser


def get_auth_uri(redirect_url):
    config = json.load(open('client_json.json'))
    flow = OAuth2WebServerFlow(client_id=config['installed']['client_id'],
                               client_secret=config['installed']['client_secret'],
                               scope='https://www.googleapis.com/auth/cloud-platform',
                               redirect_uri=redirect_url)
    auth_uri = flow.step1_get_authorize_url()
    webbrowser.open(auth_uri)
    return auth_uri


def main():
    print(get_auth_uri('http://www.google.com'))


if __name__ == '__main__':
    main()
