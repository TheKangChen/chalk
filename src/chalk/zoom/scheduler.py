import logging  # HACK: Use rich logger
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional

import pytz
from playwright.sync_api import Page, Playwright, sync_playwright

from chalk.chalk_utils.sys_utils import Platform, get_current_platform, kill_processes


@dataclass
class ZoomLoginCreds:
    email: str
    password: str


@dataclass
class ZoomMeetingConfig:
    topic: str
    date: datetime
    duration_hours: int
    duration_minutes: int


@dataclass
class ZoomMeetingInfo:
    meeting_link: Optional[str] = None
    meeting_id: Optional[str] = None
    passcode: Optional[str] = None


def kill_zoom_processes() -> None:
    current_platform = get_current_platform()

    if current_platform != Platform.UNKNOWN:
        process_name = {
            Platform.WINDOWS: "Zoom.exe",
            Platform.MACOS: "zoom.us",
            Platform.LINUX: "zoom",
        }.get(current_platform)

        if process_name:
            kill_processes(process_name)
        else:
            logging.error(f"Attempted to kill unauthorized process: {process_name}")


class ZoomScheduler:
    def __init__(
        self,
        configs: Iterable[ZoomMeetingConfig],
        creds: ZoomLoginCreds,
        headless_mode: bool = True,
    ) -> None:
        self.configs = configs
        self.creds = creds
        self.is_headless = headless_mode
        self.logger = logging.getLogger(__name__)  # HACK: switch to rich logger

    def schedule_meetings(self, playwright: Playwright) -> list[ZoomMeetingInfo]:
        """Schedule a Zoom meeting and return meeting information."""
        kill_zoom_processes()
        meeting_infos = []
        try:
            browser = playwright.chromium.launch(
                headless=self.is_headless,
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
            page.on(
                "console", lambda msg: self.logger.debug(f"Browser console: {msg.text}")
            )

            # Enable request interception for faster loading
            page.route("**/*.{png,jpg,jpeg,gif,svg}", lambda route: route.abort())

            self._login(page, username=self.creds.email, password=self.creds.password)

            # self._fill_meeting_details(page)
            # invitation = self._get_meeting_invitation(page)

            for config in self.configs:
                self.logger.info(f"Scheduling meeting: {config.topic}")
                self._fill_meeting_details(page, config)
                invitation = self._get_meeting_invitation(page)
                meeting_info = self._parse_zoom_invite(invitation)
                meeting_infos.append(meeting_info)

                page.goto("https://app.zoom.us/meeting/schedule")

            # return self._parse_zoom_invite(invitation)
            return meeting_infos
        except Exception as e:
            self.logger.error(
                f"Failed to schedule meeting: {e!s}"
            )  # HACK: switch to rich logger
            if page:
                # Take screenshot to diagnose the issue
                page.screenshot(
                    path=f"./run_logs/{datetime.now(tz=pytz.timezone('America/New_York')).strftime('%Y-%m-%d_%H-%M-%S')}_error_screenshot.png"
                )
                self.logger.error(f"Current URL: {page.url}")
            raise
        finally:
            if context:
                context.close()
            if browser:
                browser.close()

    def _login(self, page: Page, username: str, password: str) -> None:
        """Handle Zoom login."""

        page.goto("https://app.zoom.us/meeting/schedule")

        # Wait for login form and fill credentials
        page.wait_for_selector('input[name="email"]')
        page.fill('input[name="email"]', username)
        page.fill('input[name="password"]', password)

        # NOTE: codegen: page.get_by_role("button", name="Sign In", exact=True).click()

        page.click('button[id="js_btn_login"]')

        # Handle potential CAPTCHA
        if "recaptcha" in page.url:
            raise Exception(
                "CAPTCHA detected. Please try again later or use manual scheduling."
            )

    def _fill_meeting_details(self, page: Page, config: ZoomMeetingConfig) -> None:
        """Fill in meeting details."""

        # Fill topic
        page.fill('input[id="topic"]', config.topic)

        # Set date
        date_str = config.date.strftime("%B %-d %Y %A")
        day_str = config.date.strftime("-d")
        page.click('[id="mt_time"]')
        # NOTE: codegen: page.get_by_role("combobox", name="choose date").click()
        page.get_by_role("button", name=date_str, exact=True).last.click()

        # Set time
        hour = config.date.strftime("%-I:%M")
        page.get_by_role("combobox", name="select start time").click()
        page.get_by_role("option", name=hour).click()

        # Set meridiem
        meridiem = config.date.strftime("%p")
        page.click('[role="button"][id="start_time2"]')
        page.get_by_role("option", name=meridiem).locator("div").click()

        # Set duration
        page.get_by_role("button", name="select duration hours,1").click()
        page.get_by_role("option", name=f"{config.duration_hours}", exact=True).locator(
            "div"
        ).click()
        page.get_by_role("combobox", name="select duration minutes").click()
        page.get_by_role("option", name=f"{config.duration_minutes}").locator(
            "div"
        ).click()

        # Save meeting
        page.mouse.wheel(0, 1000)
        page.get_by_role("button", name="Save").click()

    def _get_meeting_invitation(self, page: Page) -> str:
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


def schedule_zoom_meetings(
    configs: Iterable[ZoomMeetingConfig],
    login_creds: ZoomLoginCreds,
    headless_mode: bool = True,
) -> list[ZoomMeetingInfo]:
    """Main function to schedule a Zoom meeting."""
    scheduler = ZoomScheduler(configs, login_creds, headless_mode)
    with sync_playwright() as playwright:
        return scheduler.schedule_meetings(playwright)
