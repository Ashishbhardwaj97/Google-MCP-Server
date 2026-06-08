import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/gmail.compose",
]

def get_credentials():
    """Gets valid user credentials from storage or initiates OAuth2 flow."""
    creds = None
    # Check for token in environment variables first (for Railway)
    token_json_env = os.environ.get("GOOGLE_TOKEN_JSON")
    if token_json_env:
        try:
            token_data = json.loads(token_json_env)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        except Exception as e:
            print(f"Error loading credentials from GOOGLE_TOKEN_JSON env var: {e}")

    # Fallback to local token.json
    if not creds and os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                raise FileNotFoundError(
                    "credentials.json not found. Please download it from "
                    "Google Cloud Console and place it in the same directory."
                )
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        try:
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        except Exception as e:
            print(f"Could not save token.json: {e}")
            
    return creds
