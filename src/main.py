import base64
import datetime
import os
import os.path
import re
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Optional

import google.auth
import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Google API authorization
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://mail.google.com/",
    # "https://www.googleapis.com/auth/gmail.modify",
    # "https://www.googleapis.com/auth/gmail.compose",
    # "https://www.googleapis.com/auth/gmail.readonly",
    # "https://www.googleapis.com/auth/gmail.metadata",
    # "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/calendar.events.owned",
]
CRED_PATH = "./secrets/credentials.json"
TOKEN_PATH = "./secrets/token.json"


# G Sheets
SPREADSHEET_ID = "1stmP7HQ_lfKxP0FmFHv1CNLYmnf5lGwuan2HPJvoXUc"
TMR = datetime.date.today() + datetime.timedelta(days=1)
# DATE_STR = TMR.strftime("%m/%d")[1:]
DATE_STR = "1/23"
SHEET_NAME = f"{TMR.year} {TMR.strftime('%B')}"
RANGE_NAME = SHEET_NAME + "!A1:P50"


# Drupal
LOGIN_URL = "https://www.nypl.org/user"


# Named idices
date_idx = 0
start_time_idx = 2
end_time_idx = 3
location_idx = 4
class_idx = 7
drupal_link_idx = 11


@dataclass
class VirtualClassInfo:
    class_name: str
    date: str
    start_time: str
    end_time: str
    drupal_link: Optional[str] = None
    csv_link: Optional[str] = None
    csv_data: Optional[str] = None
    registration_emails: Optional[list[str]] = None
    email_created: Optional[bool] = None
    email_sent: Optional[bool] = None
    calander_event_created: Optional[bool] = None


def authorize_google():
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
            flow = InstalledAppFlow.from_client_secrets_file(CRED_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return creds


def get_links(sheet):
    result = (
        sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    )
    values = result.get("values", [])

    if not values:
        print("No data found.")
        return
    # Get all drupal post links for tmr
    links = []
    for row in values:
        # Get column L: drupal_link
        if row[date_idx] == DATE_STR and row[location_idx].lower() == "online":
            links.append(
                VirtualClassInfo(
                    class_name=row[class_idx],
                    date=row[date_idx],
                    start_time=row[start_time_idx],
                    end_time=row[end_time_idx],
                    drupal_link=row[drupal_link_idx],
                )
            )
    return links


def get_login_client(username: str, password: str, login_url: str) -> httpx.Client:
    client = httpx.Client()
    resp = client.get(login_url).raise_for_status()
    form_build_id = (
        BeautifulSoup(resp.content, features="html.parser")
        .find("input", attrs={"name": "form_build_id"})
        .get("value")
    )
    payload = {
        "name": username,
        "pass": password,
        "form_build_id": form_build_id,
        "form_id": "user_login",
        "op": "Log in",
    }
    _ = client.post(login_url, data=payload, follow_redirects=True).raise_for_status()
    return client


def get_csv(virtual_class: VirtualClassInfo, client: httpx.Client) -> None:
    resp = client.get(virtual_class.drupal_link).raise_for_status()
    match = re.search(r"/node/(\d+)/registrations", resp.text)

    virtual_class.csv_link = f"https://www.nypl.org{match[0]}/export/registrations.csv "
    print(virtual_class.csv_link)

    resp = client.get(virtual_class.csv_link).raise_for_status()
    virtual_class.csv_data = resp.text


def get_registration_emails(virtual_class: VirtualClassInfo) -> None:
    csv = virtual_class.csv_data
    rows = csv.replace('"', "").split("\r\n")
    email_list = []
    for r in rows[1:]:
        r = r.split(",")
        if len(r) > 2:
            email_list.append(r[1])
    virtual_class.registration_emails = email_list


# test
def gmail_create_draft():
    creds, _ = google.auth.default()

    try:
        # create gmail api client
        service = build("gmail", "v1", credentials=creds)

        # message = EmailMessage()
        # message.set_content("This is automated draft mail")
        #
        # message["To"] = "gduser1@workspacesamples.dev"
        # message["From"] = "gduser2@workspacesamples.dev"
        # message["Subject"] = "Automated draft"
        #
        # # encoded message
        # encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        #
        # create_message = {"message": {"raw": encoded_message}}
        # pylint: disable=E1101
        # draft = (
        #     service.users()
        #     .drafts()
        #     .create(userId="me", body=create_message)
        #     .execute()
        # )

        # print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

        res = service.users().drafts().list(userId="me").execute()
        print(res)

    except HttpError as error:
        print(f"An error occurred: {error}")
        draft = None

    return draft


def schedule_email():
    raise


def send_email():
    raise


def main():
    load_dotenv()
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    creds = authorize_google()
    try:
        # service = build("sheets", "v4", credentials=creds)
        # sheet = service.spreadsheets()
        # classes = get_links(sheet)
        # client = get_login_client(
        #     username=username, password=password, login_url=LOGIN_URL
        # )
        # for _class in classes:
        #     get_csv(_class, client)
        #     get_registration_emails(_class)
        #     print(_class.registration_emails)

        service = build("gmail", "v1", credentials=creds)

        message = EmailMessage()

        message.set_content("This is automated draft mail")

        message["To"] = "gduser1@workspacesamples.dev"
        message["Bcc"] = ["gduser1@workspacesamples.dev", "test1@example.com", "test2@example.com"]
        message["From"] = "instructor19@nypl.org"
        message["Subject"] = "Automated draft"

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

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
