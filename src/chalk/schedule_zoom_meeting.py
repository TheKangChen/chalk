import os
import sys

import pytz

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from datetime import datetime

from chalk.chalk_utils.env_vars import get_env_vars
from chalk.zoom.scheduler import (
    ZoomLoginCreds,
    ZoomMeetingConfig,
    schedule_zoom_meetings,
)
# from config.default import nypl_email, zoom_password

if __name__ == "__main__":
    creds = get_env_vars()
    headless_mode = True
    login_creds = ZoomLoginCreds(email=creds["NYPL_EMAIL"], password=creds["ZOOM_PASSWORD"])
    meeting_configs = [
        # BUG: When schedule on same day, it sometimes schedule the day of the next month
        ZoomMeetingConfig(
            topic="Excel Genius Class 5: Pivot Tables",
            date=datetime(2025, 3, 5, 11, 0),
            duration_hours=1,
            duration_minutes=30,
        ),
        ZoomMeetingConfig(
            topic="Advanced Powerpoint",
            date=datetime(2025, 3, 5, 15, 30),
            duration_hours=1,
            duration_minutes=30,
        ),
        ZoomMeetingConfig(
            topic="Web Scraping with Python Part 1",
            date=datetime(2025, 3, 6, 11, 0),
            duration_hours=1,
            duration_minutes=30,
        ),
    ]

    try:
        meeting_infos = schedule_zoom_meetings(
            meeting_configs, login_creds, headless_mode
        )
        for c, m in zip(meeting_configs, meeting_infos):
            print(c.topic)
            print(f"Meeting Link: {m.meeting_link}")
            print()
            print(f"Meeting ID: {m.meeting_id}")
            print(f"Passcode: {m.passcode}")

    except Exception as e:
        print(f"Failed to schedule meeting: {e}")
