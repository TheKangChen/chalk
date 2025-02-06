import re
from playwright.sync_api import Playwright, sync_playwright, expect

from config import nypl_email, zoom_password


def run(playwright: Playwright) -> str:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Visit zoom schedule page
    page.goto("https://app.zoom.us/meeting/schedule")

    # Login
    page.get_by_text("Email Address").click()
    page.get_by_role("textbox", name="Email Address").fill(nypl_email)
    page.get_by_text("Password", exact=True).click()
    page.get_by_role("textbox", name="Password").fill(zoom_password)
    page.get_by_role(
        "button", name="Sign In", exact=True
    ).click()  # FIX: might get recaptcha blocked

    # Input meeting information
    # Meeting topic
    page.get_by_role("textbox", name="Topic").click()
    page.get_by_role("textbox", name="Topic").fill("Fundamentals of Programming with Python Part 2")

    # Date
    page.get_by_role("combobox", name="choose date").click()
    page.get_by_role("button", name="February 6 2025 Thursday").first.click()

    # Start time
    page.get_by_role("combobox", name="select start time").click()
    page.get_by_role("option", name="11:00").click()

    # AM/PM
    page.get_by_role(
        "button", name="select start time unit,PM"
    ).click()  # FIX: might not be PM, depending on when the script is ran
    page.get_by_role("option", name="AM").locator("div").click()

    # Duration
    page.get_by_role("button", name="select duration hours,1").click()
    page.get_by_role("option", name="1", exact=True).locator("div").click()
    page.get_by_role("combobox", name="select duration minutes").click()
    page.get_by_role("option", name="30").locator("div").click()

    # Scroll down to prevent from getting stuck
    page.mouse.wheel(0, 1000)

    page.get_by_role("button", name="Save").click()

    # Get meeting invite
    page.get_by_role("button", name=" Copy Invitation").click()
    textarea_handle = page.query_selector("textarea")
    invitation = textarea_handle.evaluate("node => node.value")

    context.close()
    browser.close()

    return invitation


def parse_zoom_invite(invite_text: str) -> dict:
    zoom_info = {"meeting_link": None, "meeting_id": None, "passcode": None}

    # Regular expressions for matching each component
    link_pattern = r"https://[^\s]+\.zoom\.us/j/\d+\?pwd=[^\s]+"
    meeting_id_pattern = r"Meeting ID: (\d+(?:\s+\d+)*)"
    passcode_pattern = r"Passcode: ([^\s]+)"

    # Extract meeting link
    link_match = re.search(link_pattern, invite_text)
    if link_match:
        zoom_info["meeting_link"] = link_match.group(0)

    # Extract meeting ID
    id_match = re.search(meeting_id_pattern, invite_text)
    if id_match:
        zoom_info["meeting_id"] = id_match.group(1)

    # Extract passcode
    passcode_match = re.search(passcode_pattern, invite_text)
    if passcode_match:
        zoom_info["passcode"] = passcode_match.group(1)

    return zoom_info


if __name__ == "__main__":
    with sync_playwright() as playwright:
        invitation = run(playwright)
        meeting_info = parse_zoom_invite(invitation)
        print(meeting_info["meeting_link"])
        print("Meeting ID:", meeting_info["meeting_id"])
        print("Passcode:", meeting_info["passcode"])

