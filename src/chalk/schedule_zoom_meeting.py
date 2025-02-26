import os
import sys

import pytz

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from datetime import datetime

from chalk.zoom.scheduler import (
    ZoomLoginCreds,
    ZoomMeetingConfig,
    schedule_zoom_meetings,
)
from config.config import nypl_email, zoom_password

if __name__ == "__main__":
    headless_mode = True
    login_creds = ZoomLoginCreds(email=nypl_email, password=zoom_password)
    meeting_configs = [
        ZoomMeetingConfig(
            topic="Excel Genius Class 4: Tables and Data Validation",
            date=datetime(2025, 2, 26, 11, 0),
            duration_hours=1,
            duration_minutes=30,
        ),
        ZoomMeetingConfig(
            topic="JavaScript Basics Part 1",
            date=datetime(2025, 2, 26, 15, 30),
            duration_hours=1,
            duration_minutes=30,
        ),
        ZoomMeetingConfig(
            topic="Consuming Web APIs with Python",
            date=datetime(2025, 2, 27, 11, 0),
            duration_hours=1,
            duration_minutes=30,
        ),
    ]

    try:
        meeting_infos = schedule_zoom_meetings(
            meeting_configs, login_creds, headless_mode
        )
        for m in meeting_infos:
            print(f"Meeting Link: {m.meeting_link}")
            print(f"Meeting ID: {m.meeting_id}")
            print(f"Passcode: {m.passcode}")

    except Exception as e:
        print(f"Failed to schedule meeting: {e}")
