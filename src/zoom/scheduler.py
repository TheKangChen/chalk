from playwright.sync_api import Playwright, sync_playwright, expect
from dataclasses import dataclass
from typing import Optional
import re
from datetime import datetime
import logging  # HACK: Use rich logger


@dataclass
class ZoomMeetingConfig:
    topic: str
    date: datetime
    duration_hours: int
    duration_minutes: int
    email: str
    password: str


@dataclass
class ZoomMeetingInfo:
    meeting_link: Optional[str] = None
    meeting_id: Optional[str] = None
    passcode: Optional[str] = None


class ZoomScheduler:
    def __init__(self, config: ZoomMeetingConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)  # HACK: switch to rich logger

    def schedule_meeting(self, playwright: Playwright) -> ZoomMeetingInfo:
        """Schedule a Zoom meeting and return meeting information."""
        try:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()

            # Enable request interception for faster loading
            page.route("**/*.{png,jpg,jpeg,gif,svg}", lambda route: route.abort())

            self._login(page)
            self._fill_meeting_details(page)
            invitation = self._get_meeting_invitation(page)

            return self._parse_zoom_invite(invitation)
        except Exception as e:
            self.logger.error(f"Failed to schedule meeting: {str(e)}")
            raise
        finally:
            context.close()
            browser.close()

    def _login(self, page) -> None:
        """Handle Zoom login."""
        page.goto("https://app.zoom.us/meeting/schedule")

        # Wait for login form and fill credentials
        page.wait_for_selector('input[name="email"]')
        page.fill('input[name="email"]', self.config.email)
        page.fill('input[name="password"]', self.config.password)

        # page.get_by_role("button", name="Sign In", exact=True).click()

        with page.expect_navigation():
            page.click('button[id="js_btn_login"]')

        # Handle potential CAPTCHA
        if "recaptcha" in page.url:
            raise Exception(
                "CAPTCHA detected. Please try again later or use manual scheduling."
            )

    def _fill_meeting_details(self, page) -> None:
        """Fill in meeting details."""

        # Fill topic
        page.fill('input[id="topic"]', self.config.topic)

        # Set date
        date_str = self.config.date.strftime("%B %-d %Y %A")
        page.click('[id="mt_time"]')
        # page.get_by_role("combobox", name="choose date").click()
        page.get_by_role("button", name=date_str).first.click()

        # Set time
        hour = self.config.date.strftime("%-I:%M")
        page.get_by_role("combobox", name="select start time").click()
        page.get_by_role("option", name=hour).click()

        # Set meridiem
        meridiem = self.config.date.strftime("%p")
        page.click('[role="button"][id="start_time2"]')
        page.get_by_role("option", name=meridiem).locator("div").click()

        # FIX: Set duration
        # page.click(f'button[name="select duration hours,{self.config.duration_hours}"]')
        # page.click(f'[role="option"][name="{self.config.duration_minutes}"]')

        # page.click('[role="button"][id="duration_time"]')
        # page.get_by_role("button", name="select duration hours,1").click()
        # page.get_by_role("option", name=self.config.duration_hours, exact=True).locator("div").click()
        # page.get_by_role("combobox", name="select duration minutes").click()
        # page.get_by_role("option", name=self.config.duration_minutes).locator("div").click()

        page.get_by_role("button", name="select duration hours,1").click()
        page.get_by_role("option", name="1", exact=True).locator("div").click()
        page.get_by_role("combobox", name="select duration minutes").click()
        page.get_by_role("option", name="30").locator("div").click()


        # Save meeting
        page.wait_for_selector('button[name="Save"]')
        page.click('button[name="Save"]')

    def _get_meeting_invitation(self, page) -> str:
        """Get meeting invitation text."""
        page.wait_for_selector('button[name=" Copy Invitation"]')
        page.click('button[name=" Copy Invitation"]')

        textarea = page.query_selector("textarea")
        return textarea.evaluate("node => node.value")

    @staticmethod
    def _parse_zoom_invite(invite_text: str) -> ZoomMeetingInfo:
        """Parse Zoom invitation text to extract meeting details."""
        patterns = {
            "meeting_link": r"https://[^\s]+\.zoom\.us/j/\d+\?pwd=[^\s]+",
            "meeting_id": r"Meeting ID: (\d+(?:\s+\d+)*)",
            "passcode": r"Passcode: ([^\s]+)",
        }

        results = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, invite_text)
            results[key] = (
                match.group(1)
                if match and key != "meeting_link"
                else (match.group(0) if match else None)
            )

        return ZoomMeetingInfo(**results)


def schedule_zoom_meeting(config: ZoomMeetingConfig):
    """Main function to schedule a Zoom meeting."""
    scheduler = ZoomScheduler(config)
    with sync_playwright() as playwright:
        return scheduler.schedule_meeting(playwright)


if __name__ == "__main__":
    # Example Usage
    meeting_config = ZoomMeetingConfig(
        topic="Fundamentals of Programming with Python Part 2",
        date=datetime(2025, 2, 6, 11, 0),  # 11:00 AM on Feb 6, 2025
        duration_hours=1,
        duration_minutes=30,
        email="your_email@example.com",
        password="your_password",
    )

    try:
        meeting_info = schedule_zoom_meeting(meeting_config)
        print(f"Meeting Link: {meeting_info.meeting_link}")
        print(f"Meeting ID: {meeting_info.meeting_id}")
        print(f"Passcode: {meeting_info.passcode}")
    except Exception as e:
        print(f"Failed to schedule meeting: {e}")
