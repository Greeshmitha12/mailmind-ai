import os

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive"
]


def get_google_services(user_id: int):

    token_file = f"token_{user_id}.json"

    creds = None

    if os.path.exists(token_file):

        try:
            creds = Credentials.from_authorized_user_file(
                token_file,
                SCOPES
            )

        except Exception:
            os.remove(token_file)
            creds = None

    if not creds:
        raise Exception(
            f"Google account not connected for user {user_id}"
        )

    if creds.expired and creds.refresh_token:

        creds.refresh(Request())

        with open(token_file, "w") as token:
            token.write(creds.to_json())

    gmail_service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    calendar_service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    drive_service = build(
        "drive",
        "v3",
        credentials=creds
    )

    return (
        gmail_service,
        calendar_service,
        drive_service
    )