from dataclasses import dataclass
from typing import Optional


@dataclass
class VirtualClassInfo:
    class_name: str
    date: str
    weekday: str
    start_time: str
    end_time: str
    drupal_link: Optional[str] = None
    csv_link: Optional[str] = None
    csv_data: Optional[str] = None
    registration_emails: Optional[list[str]] = None
    email_created: Optional[bool] = None
    email_sent: Optional[bool] = None
    calander_event_created: Optional[bool] = None


