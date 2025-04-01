import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def authenticate_google():
    """
    Authenticates the user with Google Calendar API using OAuth2.

    This function checks for existing credentials saved in 'token.pkl'.
    If valid credentials are found, they are used to build the Google Calendar API service.
    If not, the user is prompted to authenticate via the browser, and the new credentials
    are saved for future use.

    Returns:
        googleapiclient.discovery.Resource: A service object for interacting with the
        Google Calendar API.
    """
    creds = None

    if os.path.exists('../Morning_Sync/token.pkl'):
        with open('../Morning_Sync/token.pkl', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('../credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        with open('../Morning_Sync/token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service
