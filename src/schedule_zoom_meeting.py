# FIX: Fix this janky import
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
from zoom.scheduler import schedule_zoom_meeting, ZoomMeetingConfig
from config.config import nypl_email, zoom_password


if __name__ == "__main__":
    meeting_config = ZoomMeetingConfig(
        topic="Excel Genius Class 3: Charts and Sparklines",
        date=datetime(2025, 2, 19, 11, 0),
        duration_hours=1,
        duration_minutes=30,
        email=nypl_email,
        password=zoom_password,
    )
    meeting_config_2 = ZoomMeetingConfig(
        topic="Responsive Web Design - CSS Layout Modules: CSS Grid Basics",
        date=datetime(2025, 2, 19, 15, 30),
        duration_hours=1,
        duration_minutes=30,
        email=nypl_email,
        password=zoom_password,
    )
    meetings = [meeting_config, meeting_config_2]

    try:
        meeting_info = [schedule_zoom_meeting(conf) for conf in meetings]
        for m in meeting_info:
            print(f"Meeting Link: {m.meeting_link}")
            print(f"Meeting ID: {m.meeting_id}")
            print(f"Passcode: {m.passcode}")

    except Exception as e:
        print(f"Failed to schedule meeting: {e}")
