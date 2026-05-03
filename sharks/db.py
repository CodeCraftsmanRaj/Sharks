from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from sharks.config import settings


def database_path() -> str:
    if settings.database_url.startswith("sqlite:///"):
        return settings.database_url.replace("sqlite:///", "", 1)
    return "./sharks.db"


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(database_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    db_path = Path(database_path())
    if db_path.parent.as_posix() not in {".", ""}:
        db_path.parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS student_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                whatsapp_id TEXT NOT NULL,
                name TEXT,
                email TEXT,
                marks REAL,
                budget REAL,
                target_country TEXT,
                target_course TEXT,
                work_experience REAL,
                family_income REAL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS conversation_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                whatsapp_id TEXT NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS document_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                whatsapp_id TEXT NOT NULL,
                document_type TEXT NOT NULL,
                raw_text TEXT,
                extracted_json TEXT,
                created_at TEXT NOT NULL
            )
            """
        )


init_db()
