from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# google api scopes
GOOGLE_API_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://mail.google.com/",
    "https://www.googleapis.com/auth/calendar.events.owned",
]

# google api tokens
CRED_DIR = BASE_DIR / "credentials"
CRED_PATH = CRED_DIR / "credentials.json"
TOKEN_PATH = CRED_DIR / "token.json"

# logs directory
LOG_DIR = BASE_DIR / "run_logs"

# database
DB_DIR = BASE_DIR / "db"
DB_PATH = DB_DIR / "chalk_schedule.sqlite"

# config default directory
CONFIG_DIR = BASE_DIR / "config"
DEFAULT_CONF = CONFIG_DIR / "default.py"

# schedule & active classes csv directory
SCHEDULE_DIR = CONFIG_DIR / "schedule"
ACTIVE_CLASSES = SCHEDULE_DIR / "active_classes.csv"
