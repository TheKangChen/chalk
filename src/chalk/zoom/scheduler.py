import logging  # HACK: Use rich logger
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from playwright.sync_api import Playwright, sync_playwright

from src.chalk_utils.sys_utils import kill_zoom_processes


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
    def __init__(self, config: ZoomMeetingConfig) -> None:
        self.config = config
        self.logger = logging.getLogger(__name__)  # HACK: switch to rich logger

    def schedule_meeting(self, playwright: Playwright) -> ZoomMeetingInfo:
        """Schedule a Zoom meeting and return meeting information."""
        kill_zoom_processes()

        try:
            browser = playwright.chromium.launch(
                headless=True,
                args=[
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-gpu",
                    "--disable-software-rasterizer",
                ],
            )
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            )
            page = context.new_page()

            page.on("console", lambda msg: self.logger.debug(f"Browser console: {msg.text}"))

            # Enable request interception for faster loading
            page.route("**/*.{png,jpg,jpeg,gif,svg}", lambda route: route.abort())

            self._login(page)
            self._fill_meeting_details(page)
            invitation = self._get_meeting_invitation(page)

            return self._parse_zoom_invite(invitation)
        except Exception as e:
            self.logger.error(
                f"Failed to schedule meeting: {e!s}"
            )  # HACK: switch to rich logger
            if page:
                # Take screenshot to diagnose the issue
                page.screenshot(path=f"{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}_error_screenshot.png")
                self.logger.error(f"Current URL: {page.url}")
            raise
        finally:
            if context:
                context.close()
            if browser:
                browser.close()

    def _login(self, page) -> None:
        """Handle Zoom login."""

        page.goto("https://app.zoom.us/meeting/schedule")

        # Wait for login form and fill credentials
        page.wait_for_selector('input[name="email"]')
        page.fill('input[name="email"]', self.config.email)
        page.fill('input[name="password"]', self.config.password)

        # NOTE: codegen: page.get_by_role("button", name="Sign In", exact=True).click()

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
        # NOTE: codegen: page.get_by_role("combobox", name="choose date").click()
        page.get_by_role("button", name=date_str).first.click()

        # Set time
        hour = self.config.date.strftime("%-I:%M")
        page.get_by_role("combobox", name="select start time").click()
        page.get_by_role("option", name=hour).click()

        # Set meridiem
        meridiem = self.config.date.strftime("%p")
        page.click('[role="button"][id="start_time2"]')
        page.get_by_role("option", name=meridiem).locator("div").click()

        # Set duration
        page.get_by_role("button", name="select duration hours,1").click()
        page.get_by_role(
            "option", name=f"{self.config.duration_hours}", exact=True
        ).locator("div").click()
        page.get_by_role("combobox", name="select duration minutes").click()
        page.get_by_role("option", name=f"{self.config.duration_minutes}").locator(
            "div"
        ).click()

        # Save meeting
        page.mouse.wheel(0, 1000)
        page.get_by_role("button", name="Save").click()

    def _get_meeting_invitation(self, page) -> str:
        """Get meeting invitation text."""

        page.get_by_role("button", name="Copy Invitation").click()

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


def schedule_zoom_meeting(config: ZoomMeetingConfig) -> ZoomMeetingInfo:
    """Main function to schedule a Zoom meeting."""
    scheduler = ZoomScheduler(config)
    with sync_playwright() as playwright:
        return scheduler.schedule_meeting(playwright)
