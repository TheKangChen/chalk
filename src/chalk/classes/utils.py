import csv
from os import PathLike
from pathlib import Path


def sync_database(db: PathLike, csv_dir: Path) -> None:
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
    print(active_classes)
    print(schedule_files)

    # read all csv files
    schedule_data = []
    for f in schedule_files:
        with open(f, "r") as fp:
            reader = csv.reader(fp)
            header_row = next(reader)
            for row in reader:
                schedule_data.append(row)
    schedule_data.insert(0, header_row)
    print(schedule_data)

    # check if duplicate -> update

    # write to database




def update_database() -> None:
    """Update exisiting rows"""
    raise
