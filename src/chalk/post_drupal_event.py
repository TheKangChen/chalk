import httpx

from chalk.classes.models import DRUPAL_EVENT_FILE_DEFAULT  # TODO: import all models

# TODO: Login to automatically get cookies and headers
cookies = {}
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryAHAw1gGIipKQtkkr",
    "origin": "https://www.nypl.org",
    "priority": "u=0, i",
    "referer": "https://www.nypl.org/node/add/event-program",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    # 'cookie': '',
}

files = DRUPAL_EVENT_FILE_DEFAULT

# TODO: Build Final ditionary

response = httpx.post(
    "https://www.nypl.org/node/add/event-program",
    cookies=cookies,
    headers=headers,
    files=files,
)
