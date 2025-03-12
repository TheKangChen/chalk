import os
import sys
from pathlib import Path

from classes.utils import sync_database

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config.default import SCHEDULE_DIR


def main():
    sync_database(Path(), SCHEDULE_DIR)


if __name__ == "__main__":
    main()
