from enum import Enum
import os
import sys

from chalk.chalk_utils.env_vars import get_env_vars

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import base64
import datetime
import uuid
from email.message import EmailMessage

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from chalk.classes.auth import get_login_client
from chalk.classes.fetch import get_registration_csv, get_registration_emails
from chalk.classes.models import VirtualClassInfo
from chalk.google_api.apps import GoogleService, get_service
from chalk.google_api.auth import authorize_google
from config.default import (
    CRED_PATH,
    GOOGLE_API_SCOPES,
    TOKEN_PATH,
)

# G Sheets
SCHEDULED_DATE = datetime.date.today() + datetime.timedelta(days=1)
# FMT_DATE = SCHEDULED_DATE.strftime("%Y/%m/%d")
FMT_DATE = "2025/03/06"
SHEET_NAME = f"{SCHEDULED_DATE.year} {SCHEDULED_DATE.strftime('%B')}"
RANGE_NAME = SHEET_NAME + "!A1:P50"


# G sheets column enums
class Column_Idx(Enum):
    DATE = 0
    DAY = 1
    START_TIME = 2
    END_TIME = 3
    LOCATION = 4
    CLASS = 7
    DRUPAL_LINK = 11


def get_links(sheet, creds: dict) -> list[VirtualClassInfo] | None:
    result = (
        sheet.values()
        .get(spreadsheetId=creds["SPREADSHEET_ID"], range=RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

    if not values:
        print("No data found.")
        return None
    # Get all drupal post links for tmr
    links = []
    for row in values:
        # Get column L: drupal_link
        if (
            row[Column_Idx.DATE.value] == FMT_DATE
            and row[Column_Idx.LOCATION.value].lower() == "online"
        ):
            links.append(
                VirtualClassInfo(
                    class_name=row[Column_Idx.CLASS.value],
                    date=row[Column_Idx.DATE.value],
                    weekday=row[Column_Idx.DAY.value],
                    start_time=row[Column_Idx.START_TIME.value],
                    end_time=row[Column_Idx.END_TIME.value],
                    drupal_link=row[Column_Idx.DRUPAL_LINK.value],
                )
            )
    return links


def create_pre_class_email(
    virtual_class: VirtualClassInfo, zoom_info, creds: dict
) -> EmailMessage:
    message = EmailMessage()

    message["From"] = creds["INSTRUCTOR_EMAIL"]
    message["To"] = creds["TECHCONNECT_EMAIL"]
    message["Bcc"] = virtual_class.registration_emails
    message["Subject"] = f"TechConnect: Join Link for {virtual_class.class_name}"

    message.set_content("This is fallback content,\n\nHello world!\n\nBest,\nKang")
    message.add_alternative(
        f"""\
        <!DOCTYPE html>
        <html>
            <body>
                <div style="font-family: Arial, sans-serif; font-size: 10pt; line-height: 1.2; max-width: 600px; margin: 0 auto; vertical-align:baseline;">
                    <p style="margin-top: 0pt; margin-bottom: 0pt;">
                        Thank you for registering for TechConnect's 
                        <span style="font-weight: 700">{virtual_class.class_name}</span> 
                        virtual class taking place today, 
                        <span style="font-weight: 700">{virtual_class.date} {virtual_class.weekday}</span> 
                        at 
                        <span style="font-weight: 700">{virtual_class.start_time}</span>!
                    </p>
                    <br>
                    <p style="margin-top: 0pt; margin-bottom: 0pt;">
                        The Library uses Zoom to conduct virtual classes. The Library does not own Zoom. We want you to understand how you and the Library use this service. Read the 
                        <a href="https://www.nypl.org/help/about-nypl/legal-notices/privacy-policy" style="color: #2b66cc; text-decoration: underline;">Library's Privacy Policy</a>, 
                        especially the section "Third-Party Library Services Providers."
                    </p>
                    <br>
                    <p style="margin-top: 0pt; margin-bottom: 0pt; font-weight: 700;">To join the class, click on the following link or copy & paste it into your browser:</p>
                    <div style="font-size:13.3333px;">
                        {zoom_info}
                    </div>
                    <br>
                    <div style="font-size:13.3333px;">
                        <div>Meeting ID: {zoom_info}</div>
                        <div>Passcode: {zoom_info}</div>
                    </div>
                    <br>
                    <p style="font-weight: 700; margin-top:0pt; margin-bottom:0pt;">
                        Arrival to class on time is mandatory. Entrance into a class will not be permitted 15 minutes after class begins.
                    </p>
                    <br>
                    <br>
                    <div style="margin-top:0pt; margin-bottom:0pt;">
                        <p style="font-weight: 700; margin-top:0pt; margin-bottom:0pt;">USING THE CHAT BOX</p>
                        <p>To communicate with the instructor and the rest of the class:</p>
                        <ul style="margin-top:0pt; margin-bottom:0pt; padding-left: 20px;">
                            <li style="margin-top:0pt; margin-bottom:0pt;">Click the Chat icon in the meeting control bar at the bottom of the window.</li>
                            <li style="margin-top:0pt; margin-bottom:0pt;">Once the chat window is open on the right side of the window, click on a gray box at the bottom of the sidebar where it says "Type message here."</li>
                            <li style="margin-top:0pt; margin-bottom:0pt;">Type your question or comment.</li>
                            <li style="margin-top:0pt; margin-bottom:0pt;">Hit the "Enter" or "Return" key on your keyboard to submit your question or comment.</li>
                        </ul>
                    </div>
                    <br>
                    <br>
                    <p style="color: #cc0000; margin: 15px 0;">
                        Please note that the entire group will be able to see your question or comment so be careful not to include any personal information in your messages.
                    </p>
                    <br>
                    <p style="margin-top: 20px;">
                        See you soon!<br>
                        Your friends at 
                        <span style="color: #6aa84f;">Tech</span><span style="color: #3d85c6;">Connect</span>
                    </p>
                </div>
            </body>
        </html>
        """,
        subtype="html",
    )

    return message


def create_post_class_email(
    virtual_class: VirtualClassInfo, creds: dict
) -> EmailMessage:
    message = EmailMessage()

    message["From"] = creds["INSTRUCTOR_EMAIL"]
    message["To"] = creds["TECHCONNECT_EMAIL"]
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


def send_email(message: EmailMessage, service, user_id: str = "me"):
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"message": {"raw": encoded_message}}
    raise


def main() -> None:
    creds = get_env_vars()
    g_creds = authorize_google(TOKEN_PATH, GOOGLE_API_SCOPES, CRED_PATH)
    try:
        # Google Sheets
        service = get_service(GoogleService.SHEETS, g_creds)
        sheet = service.spreadsheets()
        classes = get_links(sheet, creds)

        # Login to drupal
        client = get_login_client(
            username=creds["NYPL_EMAIL"],
            password=creds["DRUPAL_PASSWORD"],
            login_url=creds["DRUPAL_LOGIN_URL"],
        )
        # get registration emails from drupal
        if classes:
            for _class in classes:
                get_registration_csv(_class, client)
                get_registration_emails(_class)
                print(_class.registration_emails)

            # Gmail
            service = get_service(GoogleService.GMAIL, g_creds)

            # Test email
            for c in classes:
                message = create_pre_class_email(c, None, creds)
                create_draft_email(message, service)

        # Calendar
        # service = build(GoogleService.CALENDAR, creds)
        # event = {
        #     "summary": "Fundamentals of Programming with Python Part 1",
        #     "location": "",
        #     "description": "",
        #     "start": {
        #         "dateTime": "2025-02-08T11:00:00",
        #         "timeZone": "America/New_York",
        #     },
        #     "end": {
        #         "dateTime": "2025-02-08T12:30:00",
        #         "timeZone": "America/New_York",
        #     },
        #     "recurrence": [],
        #     "attendees": [],
        #     "reminders": {},
        #     "conferenceData": {
        #         "createRequest": {
        #             "conferenceSolutionKey": {"type": "addOn"},
        #             "requestId": str(uuid.uuid4()),
        #         }
        #     },
        # }
        # event = (
        #     service.events()
        #     .insert(calendarId="primary", body=event, conferenceDataVersion=0)
        #     .execute()
        # )
        # print(f"Event created: {event.get('htmlLink')}")
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
