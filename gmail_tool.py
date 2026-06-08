import base64
from email.message import EmailMessage

from googleapiclient.discovery import build
from auth import get_credentials

def create_email_draft(to: str, subject: str, body: str) -> dict:
    """
    Creates a draft email in Gmail.
    
    Args:
        to: The recipient's email address.
        subject: The subject of the email.
        body: The plain text body of the email.
        
    Returns:
        The response from the Gmail API.
    """
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    message = EmailMessage()
    message.set_content(body)
    message["To"] = to
    message["From"] = "me"  # 'me' refers to the authenticated user
    message["Subject"] = subject

    # Encode the message as base64url
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"message": {"raw": encoded_message}}

    # Call the Gmail API to create the draft
    draft = (
        service.users()
        .drafts()
        .create(userId="me", body=create_message)
        .execute()
    )

    return draft
