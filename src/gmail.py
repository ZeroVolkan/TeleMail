import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
PATH_CREDENTIALS = "secret/credentials.json"  # Реквезиты
REDIRECT_URI = 'http://localhost:8080/'


async def auth(chat_id: int, token: str | None = None, refresh=False):
    creds = Credentials.from_authorized_user_info(PATH_CREDENTIALS, SCOPES) if token else None

    if not creds or not creds.valid or refresh:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(PATH_CREDENTIALS):
                raise FileNotFoundError("You don't have credentials in the folder 'secret'")
            flow = InstalledAppFlow.from_client_secrets_file(PATH_CREDENTIALS, SCOPES)
            creds = flow.run_local_server(timeout_seconds=120)

    return json.loads(creds.to_json())


def get_last_email_sender(token: str) -> str:
    # Получаю информацию
    creds = Credentials.from_authorized_user_info(token)

    # Инициализация Gmail API
    service = build("gmail", "v1", credentials=creds)

    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
        message = service.users().messages().get(
            userId='me',
            id=results.get('messages', ['id'])[0]['id']
        ).execute()

        header = list(filter(lambda i: i['name'] == 'Subject' ,message['payload']['headers']))[0]['value']
        frm = list(filter(lambda i: i['name'] == 'From' ,message['payload']['headers']))[0]['value']



        return f"{header}\n{frm}"
    except Exception as e:
        return f"Произошла ошибка при чтении сообщения: {e}"
