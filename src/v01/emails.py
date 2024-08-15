import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage
import google.auth
import jinja2
from src.config import settings


# If modifying these scopes, delete the file token.json.
SCOPES = [
  "https://www.googleapis.com/auth/gmail.readonly",
  "https://www.googleapis.com/auth/gmail.compose",
  "https://www.googleapis.com/auth/gmail.insert",
  "https://www.googleapis.com/auth/gmail.modify",
  "https://www.googleapis.com/auth/gmail.send"
]

GOOGLE_TOKEN_PATH= settings.GOOGLE_TOKEN_PATH
GOOGLE_CREDENTIALS_PATH= settings.GOOGLE_CREDENTIALS_PATH


def authorize():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          GOOGLE_CREDENTIALS_PATH, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")



def gmail_create_draft():
    """Create and insert a draft email.
    Print the returned draft's message and id.
    Returns: Draft object, including draft id and message meta data.
    """
    authorize()  # Ensure this is called to create/refresh the token
    
    try:
        # Load credentials from the token.json file
        creds = Credentials.from_authorized_user_file(GOOGLE_TOKEN_PATH, SCOPES)
        
        # create gmail api client
        service = build("gmail", "v1", credentials=creds)

        message = EmailMessage()

        message.set_content("This is automated draft mail")

        message["To"] = "gduser1@workspacesamples.dev"
        message["From"] = "gduser2@workspacesamples.dev"
        message["Subject"] = "Automated draft"

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"message": {"raw": encoded_message}}
        # pylint: disable=E1101
        draft = (
            service.users()
            .drafts()
            .create(userId="me", body=create_message)
            .execute()
        )

        print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        draft = None

    return draft

def gmail_send_mail_to(recipient: str, subject: str, body_html: str):
    """
    Send an HTML email to a specified recipient using Gmail API.
    
    Args:
    recipient (str): Email address of the recipient
    subject (str): Subject of the email
    body_html (str): HTML content of the email body
    
    Returns:
    dict: The sent message if successful, None otherwise
    """
    authorize()  # Ensure this is called to create/refresh the token
    
    try:
        # Load credentials from the token.json file
        creds = Credentials.from_authorized_user_file(GOOGLE_TOKEN_PATH, SCOPES)
        
        # Create Gmail API client
        service = build("gmail", "v1", credentials=creds)

        message = EmailMessage()

        # Set the HTML content
        message.add_alternative(body_html, subtype='html')

        message["To"] = recipient
        message["From"] = "me"  # 'me' is a special value that represents the authenticated user
        message["Subject"] = subject

        # Encode the message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}

        # Send the message
        sent_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )

        print(f'Message Id: {sent_message["id"]}')
        return sent_message

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

if __name__ == "__main__":
    recipient="mario@yopmail.com"
    subject="Test email"

    ## render custom email template
    with open("email_template.html") as file:
        body_html = file.read()
    body = jinja2.Template(body_html).render(title="Porca madonna!", text="This is a test email")

    gmail_send_mail_to(recipient=recipient, subject=subject, body_html=body)
