import os

import google.auth.exceptions
from googleapiclient.discovery import build, MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]
CREDS = None
DRIVE_SERVICE = None
token_filename = "token.json"


def initialize_auth_flow():
    global CREDS
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    CREDS = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_filename, "w") as token:
        token.write(CREDS.to_json())


def gdrive_login():
    global CREDS
    global DRIVE_SERVICE
    if os.path.exists(token_filename):
        CREDS = Credentials.from_authorized_user_file(token_filename, SCOPES)
    if not CREDS or not CREDS.valid:
        if CREDS and CREDS.expired and CREDS.refresh_token:
            try:
                CREDS.refresh(Request())
            except google.auth.exceptions.RefreshError:
                initialize_auth_flow()
        else:
            initialize_auth_flow()
    DRIVE_SERVICE = build("drive", "v3", credentials=CREDS)


def gdrive_upload_file(desired_file_name):
    file_metadata = {"name": desired_file_name}
    file = MediaFileUpload(
        desired_file_name, mimetype="application/zip", resumable=True
    )
    print("Uploading... Please wait")
    try:
        result = (
            DRIVE_SERVICE.files()
            .create(body=file_metadata, media_body=file, fields="id")
            .execute()
        )
    except google.auth.exceptions.RefreshError:
        initialize_auth_flow()
        gdrive_login()
        result = (
            DRIVE_SERVICE.files()
            .create(body=file_metadata, media_body=file, fields="id")
            .execute()
        )
    print(f"File ID: {result.get('id')}")
