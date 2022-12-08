import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_google_service(api_name: str, api_version: str, scopes: [str], key_file_location: str):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_file_location,
        scopes=scopes
    )

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service


def get_google_service_personal(api_name: str, api_version: str, scopes: [str], credentials_file_path: str, token_file_path: str):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        credentials_file_path: The path to a valid Google Console Project credentials.json
        token_file_path: The path to save/load the token.pickle from

    Returns:
        A service that is connected to the specified API.
    """

    creds = None

    if os.path.exists(token_file_path):
        with open(token_file_path, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file_path,
                scopes
            )

            creds = flow.run_console()

        # Save the credentials for the next run
        with open(token_file_path, 'wb') as token:
            pickle.dump(creds, token)

    # Build the service object.
    service = build(api_name, api_version, credentials=creds)

    return service
