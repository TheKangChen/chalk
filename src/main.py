import base64
import datetime
import os
import os.path
import re
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Optional

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
SCHEDULED_DATE = datetime.date.today() + datetime.timedelta(days=1)
FMT_DATE = SCHEDULED_DATE.strftime("%Y/%m/%d")
# FMT_DATE = "1/23"
SHEET_NAME = f"{SCHEDULED_DATE.year} {SCHEDULED_DATE.strftime('%B')}"
RANGE_NAME = SHEET_NAME + "!A1:P50"


# Drupal
LOGIN_URL = "https://www.nypl.org/user"


# Named idices
date_idx = 0
day_idx = 1
start_time_idx = 2
end_time_idx = 3
location_idx = 4
class_idx = 7
drupal_link_idx = 11


@dataclass
class VirtualClassInfo:
    class_name: str
    date: str
    weekday: str
    start_time: str
    end_time: str
    drupal_link: Optional[str] = None
    csv_link: Optional[str] = None
    csv_data: Optional[str] = None
    registration_emails: Optional[list[str]] = None
    email_created: Optional[bool] = None
    email_sent: Optional[bool] = None
    calander_event_created: Optional[bool] = None


def create_email(html_template, *args):
    ...
    # meta-class to create email class with the correct template and arg inseart


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


def schedule_zoom_meeting():
    raise


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
        if row[date_idx] == FMT_DATE and row[location_idx].lower() == "online":
            links.append(
                VirtualClassInfo(
                    class_name=row[class_idx],
                    date=row[date_idx],
                    weekday=row[day_idx],
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


def create_pre_class_email(virtual_class: VirtualClassInfo, zoom_info) -> EmailMessage:
    message = EmailMessage()

    message["From"] = "instructor19@nypl.org"
    message["To"] = "techconnect@nypl.org"
    message["Bcc"] = virtual_class.registration_emails
    message["Subject"] = f"TechConnect: Join Link for {virtual_class.class_name}"

    message.set_content("This is fallback content,\n\nHello world!\n\nBest,\nKang")
    message.add_alternative(
        f"""\
        <html>
          <body style="margin: 0; padding: 0; line-height: 1.2; font-size: 13.5px;">
            <p style="margin: 0; padding: 0;">Thank you for registering for TechConnect's <b>{virtual_class.class_name}</b> virtual class taking place today, <b>{virtual_class.date}</b> <b>{virtual_class.weekday}</b> at <b>{virtual_class.start_time}</b>!</p>
            <p>The Library uses Zoom to conduct virtual classes. The Library does not own Zoom. We want you to understand how you and the Library use this service. Read the <a href="https://www.nypl.org/help/about-nypl/legal-notices/privacy-policy">Library’s Privacy Policy</a>, especially the section "Third-Party Library Services Providers."</p>
            <p style="margin: 0; padding: 0;"><b>To join the class, click on the following link or copy & paste it into your browser:</b></p>
            <p style="margin: 0; padding: 0;">zoom_link</p>
            <br>
            <p style="margin: 0; padding: 0;">Meeting ID: m_id</p>
            <p style="margin: 0; padding: 0;">Passcode: p_code</p>
            <br>
            <p><b>Arrival to class on time is mandatory. Entrance into a class will not be permitted 15 minutes after class begins.</b></p>
            <br>
            <p style="margin: 0; padding: 0;"><b>USING THE CHAT BOX</b></p>
            <p style="margin: 0; padding: 0;">To communicate with the instructor and the rest of the class:</p>
            <ul>
                <li>Click the Chat icon in the meeting control bar at the bottom of the window.</li>
                <li>Once the chat window is open on the right side of the window, click on a gray box at the bottom of the sidebar where it says "Type message here."</li>
                <li>Type your question or comment.</li>
                <li>Hit the "Enter" or "Return" key on your keyboard to submit your question or comment.</li>
            </ul>
            <br>
            <p style="color: #D0343A;">Please note that the entire group will be able to see your question or comment so be careful not to include any personal information in your messages.</p>
            <p style="margin: 0; padding: 0;">See you soon!</p>
            <p style="margin: 0; padding: 0;">Your friends at <span style="color: #799A05;">Tech</span><span style="color: #0071CE;">Connect</span></p>
          </body>
        </html>
        """,
        subtype="html",
    )

    return message


def create_post_class_email(virtual_class: VirtualClassInfo, zoom_info) -> EmailMessage:
    message = EmailMessage()

    message["From"] = "instructor19@nypl.org"
    message["To"] = "techconnect@nypl.org"
    message["Bcc"] = virtual_class.registration_emails
    message["Subject"] = (
        f"TechConnect: {virtual_class.class_name} Class Handout, Practice Files & Survey"
    )

    message.set_content("This is fallback content,\n\nHello world!\n\nBest,\nKang")
    message.add_alternative(
        f"""\
        <html>
          <body style="margin: 0; padding: 0; line-height: 1.2; font-size: 13.5px;">
            <p style="margin: 0; padding: 0;">Hello friend,</p>
            <p>Thank you so much for attending {virtual_class.class_name}. Attached is the PDF handout and the files we worked on in class.</p>
            <p style="margin: 0; padding: 0;">Handout: </p>
            <p style="margin: 0; padding: 0;">Class File: </p>
            <br>
            <p>Directly below is a link to a survey that lets us know how we're doing and any additional feedback you might have. <b>Please take some time to fill out the survey in full so that we can learn how to better serve you.</b></p>
            <br>
            <p style="margin: 0; padding: 0;"><a href="https://docs.google.com/forms/d/e/1FAIpQLSeRoFsj9kC436jyBuImwv2QToGSYYZDo1SygTEnsQ-k3ozHng/viewform">Click here to complete our online class survey.</a></p>
            <br>
            <p style="margin: 0; padding: 0;">Kind regards,</p>
            <p style="margin: 0; padding: 0;">Your friends at <span style="color: #799A05;">Tech</span><span style="color: #0071CE;">Connect</span></p>
          </body>
        </html>
        """,
        subtype="html",
    )

    return message


def create_draft_email(message: EmailMessage, service: build, user_id: str = "me"):
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"message": {"raw": encoded_message}}
    # pylint: disable=E1101
    draft = (
        service.users().drafts().create(userId=user_id, body=create_message).execute()
    )
    print(f"Draft id: {draft['id']}\nDraft message: {draft['message']}")


def send_email(message: EmailMessage, service: build, user_id: str = "me"):
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"message": {"raw": encoded_message}}
    raise


def main():
    load_dotenv()
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    creds = authorize_google()
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        classes = get_links(sheet)
        client = get_login_client(
            username=username, password=password, login_url=LOGIN_URL
        )
        for _class in classes:
            get_csv(_class, client)
            get_registration_emails(_class)
            print(_class.registration_emails)

        service = build("gmail", "v1", credentials=creds)

        # Test email
        for c in classes:
            message = create_pre_class_email(c, None)
            create_draft_email(message, service)
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
