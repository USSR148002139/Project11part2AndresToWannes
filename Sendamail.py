import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


def authenticate_gmail():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def send_gmail(subject, to_address, body, creds):
    service = build("gmail", "v1", credentials=creds)

    message = EmailMessage()
    message.set_content(body)
    message["To"] = to_address
    message["From"] = "your_email@gmail.com"  # Replace with your actual Gmail address
    message["Subject"] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {"message": {"raw": encoded_message}}

    draft = service.users().drafts().create(userId="me", body=create_message).execute()
    print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

    service.users().drafts().send(userId="me", body=draft).execute()


def main():
    citylocation = input("What is the name of the city you are currently in?: ")
    CC = input("City code: ")
    address = input("Email address: ")

    # ... (your existing code)

    # Assuming Sendamail has a function like send_email(subject, to_address, body)
    send_gmail("Weather Report", address, mail_content, authenticate_gmail())

    print("Mail sent")


if __name__ == "__main__":
    main()