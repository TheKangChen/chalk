from enum import Enum, auto
from typing import Any

from googleapiclient.discovery import build
from googleapiclient.errors import UnknownApiNameOrVersion


class GoogleService(Enum):
    SHEETS = auto()
    GMAIL = auto()
    CALENDAR = auto()


def get_service(app: GoogleService, creds) -> Any:
    match app:
        case GoogleService.CALENDAR:
            service = "calendar"
            version = "v3"
        case GoogleService.GMAIL:
            service = "gmail"
            version = "v1"
        case GoogleService.SHEETS:
            service = "sheets"
            version = "v4"
    try:
        return build(service, version, credentials=creds)
    except UnknownApiNameOrVersion as e:
        # HACK: use rich logger
        print(e)
