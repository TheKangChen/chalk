import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
from zoom.scheduler import schedule_zoom_meeting, ZoomMeetingConfig
from config.config import nypl_email, zoom_password


if __name__ == "__main__":
    meeting_config = ZoomMeetingConfig(
        topic="Fundamentals of Programming with Python Part 2",
        date=datetime(2025, 2, 13, 11, 0),  # 11:00 AM on Feb 6, 2025
        duration_hours=1,
        duration_minutes=30,
        email=nypl_email,
        password=zoom_password,
    )

    try:
        meeting_info = schedule_zoom_meeting(meeting_config)
        print(f"Meeting Link: {meeting_info.meeting_link}")
        print(f"Meeting ID: {meeting_info.meeting_id}")
        print(f"Passcode: {meeting_info.passcode}")
    except Exception as e:
        print(f"Failed to schedule meeting: {e}")
