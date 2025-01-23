import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
CRED_PATH = "./secrets/credentials.json"
TOKEN_PATH = "./secrets/token.json"

SPREADSHEET_ID = "1stmP7HQ_lfKxP0FmFHv1CNLYmnf5lGwuan2HPJvoXUc"
TMR = datetime.date.today() + datetime.timedelta(days=1)
DATE_STR = TMR.strftime("%m/%d")[1:]
SHEET_NAME = f"{TMR.year} {TMR.strftime("%B")}"
RANGE_NAME = SHEET_NAME + "!A1:P50"



def authorize():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CRED_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return creds


def get_links(sheet):
    result = (
        sheet.values()
        .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

    if not values:
        print("No data found.")
        return
    # Get all drupal post links for tmr
    links = []
    for row in values:
        # Get column L: drupal_link
        if row[0] == DATE_STR:
            links.append(row[11])
    return links


def get_csv(drupal_link: str):
    raise


def get_resevations(csv) -> list:
    raise


def schedule_email():
    raise


def send_email():
    raise


def main():

    creds = authorize()

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        links = get_links(sheet)
    except HttpError as err:
        print(err)

    print(links)

if __name__ == "__main__":
    main()

