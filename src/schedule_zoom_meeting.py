# FIX: Fix this janky import
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime

from config.config import nypl_email, zoom_password
from zoom.scheduler import ZoomMeetingConfig, schedule_zoom_meeting

if __name__ == "__main__":
    meeting_config = ZoomMeetingConfig(
        topic="Test event",
        date=datetime(2025, 2, 20, 15, 0),
        duration_hours=1,
        duration_minutes=30,
        email=nypl_email,
        password=zoom_password,
    )
    # meeting_config_2 = ZoomMeetingConfig(
    #     topic="Responsive Web Design - CSS Layout Modules: CSS Grid Basics",
    #     date=datetime(2025, 2, 19, 15, 30),
    #     duration_hours=1,
    #     duration_minutes=30,
    #     email=nypl_email,
    #     password=zoom_password,
    # )
    meetings = [meeting_config]

    try:
        meeting_info = [schedule_zoom_meeting(conf) for conf in meetings]
        for m in meeting_info:
            print(f"Meeting Link: {m.meeting_link}")
            print(f"Meeting ID: {m.meeting_id}")
            print(f"Passcode: {m.passcode}")

    except Exception as e:
        print(f"Failed to schedule meeting: {e}")
