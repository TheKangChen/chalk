import csv
import os
import sqlite3
from typing import Dict, List, Literal, Tuple, Union

from chalk.chalk_utils.logging import get_rich_logger

logger = get_rich_logger()


class SQLiteConnection:
    def __init__(self, database: Union[str, os.PathLike, Literal[":memory:"]]) -> None:
        self._conn = sqlite3.connect(database)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        try:
            self.close()
        except Exception as e:
            logger.error(f"Error closing connection: {e}")
        if exc_type:
            raise exc_type(exc_value, exc_tb)

    @property
    def connection(self) -> sqlite3.Connection:
        return self._conn

    @property
    def cursor(self) -> sqlite3.Cursor:
        return self._cursor

    def check_table_exists(self, table_name: str) -> bool:
        sql = f"SELECT '{table_name}' FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone() is not None  # type: ignore
        except Exception as e:
            logger.error(f"Error checking table existence: {e}")
            raise

    def commit(self) -> None:
        self.connection.commit()

    def close(self, commit=True) -> None:
        if commit:
            self.commit()
        self.connection.close()

    def create_table(
        self, table_name: str, schema: Dict[str, str], unsafe: bool = False
    ) -> None:
        if self.check_table_exists(table_name) and not unsafe:
            logger.info(f"Table: '{table_name}' already exists, skipping creation")
            return
        column_defs = []
        for name, definition in schema.items():
            column_defs.append(f"{name} {definition}")
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({','.join(column_defs)});"
        try:
            self.execute(sql)
            self.commit()
            logger.info(f"Table: '{table_name}' created")
        except Exception as e:
            self.rollback()
            logger.error(f"Error creating table: {e}")
            raise

    def execute(self, sql: str, params: Dict = {}) -> None:
        self.cursor.execute(sql, params or ())

    def executemany(self, sql: str, vars_list: List[Tuple]) -> None:
        self.cursor.executemany(sql, vars_list)

    def fetchall(self) -> List[Tuple]:
        return self.cursor.fetchall()

    def insert_csv(self, table_name: str, csv_file: str) -> None:
        """Inserts data from a CSV file into the specified table."""
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)  # Get the header row
            placeholders = ("?," * len(header))[:-1]
            sql = f"INSERT INTO {table_name} ({','.join(header)}) VALUES ({placeholders});"
            data = list(reader)  # Read all rows into a list
            try:
                self.executemany(sql, data)
                self.commit()
            except Exception as e:
                self.rollback()
                logger.error(f"Error inserting CSV data: {e}")
                raise

    def rollback(self) -> None:
        self.connection.rollback()
