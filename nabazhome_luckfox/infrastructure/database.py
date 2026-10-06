from __future__ import annotations

import sqlite3
from pathlib import Path


class DatabaseManager:
    """SQLite-backed application database manager."""

    def __init__(self, database_path: str | Path = "nabazhome.db") -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.database_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.initialize()

    def initialize(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS alarms (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                trigger_at TEXT NOT NULL,
                enabled INTEGER NOT NULL DEFAULT 1,
                recurring INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()
