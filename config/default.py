# google api scopes
GOOGLE_API_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://mail.google.com/",
    "https://www.googleapis.com/auth/calendar.events.owned",
]

# google api tokens
CRED_DIR = "./credentials"
CRED_PATH = f"{CRED_DIR}/credentials.json"
TOKEN_PATH = f"{CRED_DIR}/token.json"

# logs directory
LOG_DIR = "./run_logs"

# database
DB_PATH = "./db/chalk_schedule.sqlite"

# config default directory
CONFIG_DIR = "./config"
DEFAULT_CONF = f"{CONFIG_DIR}/default.py"

# schedule & active classes csv directory
SCHEDULE_DIR = f"{CONFIG_DIR}/schedule"
ACTIVE_CLASSES = f"{CONFIG_DIR}/schedule/active_classes.csv"
