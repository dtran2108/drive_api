from pickle import load as picLoad, dump as picDump
from os.path import exists
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Auth:
    def __init__(self, SCOPES, CLIENT_SECRET_FILE):
        self.SCOPES = SCOPES
        self.CLIENT_SECRET = CLIENT_SECRET_FILE

    def get_credentials(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.CLIENT_SECRET, self.SCOPES)
        creds = flow.run_local_server()
        return creds.token
