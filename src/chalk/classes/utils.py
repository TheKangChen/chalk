import csv
from os import PathLike
from pathlib import Path

from chalk.chalk_utils.db_utils import SQLiteConnection
from chalk.chalk_utils.logging import get_rich_logger

logger = get_rich_logger()


def sync_database(db_str: PathLike, csv_dir: Path) -> None:
    """Automatically find csv files of schedules and active classes and add to database or update class information"""
    # find all csv files
    schedule_files = []
    active_classes = ""
    for f in csv_dir.rglob("**/*.csv"):
        if "example" not in f.stem:
            if "class" in f.stem:
                active_classes = f
            else:
                schedule_files.append(f)
    logger.info("Active classes csv file found")
    logger.info(f"Number of schedule csv files found: {len(schedule_files)}")

    # read all csv files
    schedule_data = []
    for f in schedule_files:
        with open(f, "r") as fp:
            reader = csv.reader(fp)
            header_row = next(reader)
            for row in reader:
                schedule_data.append(row)
    # schedule_data.insert(0, header_row)
    logger.debug(schedule_data)

    # check if duplicate -> update
    with SQLiteConnection(db_str) as conn:
        query = "SELECT * FROM library_names;"
        # query = "SELECT date('now');"
        conn.execute(sql=query)
        res = conn.fetchall()
        print(res)

        # write to database




def update_database() -> None:
    """Update exisiting rows"""
    raise
