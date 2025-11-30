import os
import base64
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def _gmail_service():
    creds = Credentials(
        token=None,
        refresh_token=os.environ["GMAIL_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GMAIL_CLIENT_ID"],
        client_secret=os.environ["GMAIL_CLIENT_SECRET"],
        scopes=SCOPES,
    )
    return build("gmail", "v1", credentials=creds)


def send_gmail(to_email: str, subject: str, body_text: str):
    message = MIMEText(body_text)
    message["to"] = to_email
    message["subject"] = subject
    message["from"] = os.environ["GMAIL_FROM_EMAIL"]

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service = _gmail_service()
    return service.users().messages().send(
        userId="me",
        body={"raw": raw},
    ).execute()

