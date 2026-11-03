"""SQLite persistence foundation: schema creation and connection
management. Business logic lives in service.py; this module only
owns the database file and its schema (structural constraints from
BR-01..BR-12), per plan.md's Components table.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

DEFAULT_DB_DIR = Path.home() / ".calorie_tracker"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "tracker.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    calories_tenths INTEGER NOT NULL CHECK (calories_tenths BETWEEN 0 AND 100000),
    protein_tenths INTEGER NOT NULL CHECK (protein_tenths BETWEEN 0 AND 10000),
    meal_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS target_history (
    effective_date TEXT PRIMARY KEY,
    calories_tenths INTEGER NOT NULL CHECK (calories_tenths BETWEEN 0 AND 100000),
    protein_tenths INTEGER NOT NULL CHECK (protein_tenths BETWEEN 0 AND 10000)
);
"""


def get_db_path(db_path: Path | None = None) -> Path:
    """Resolve the database file path.

    Defaults to a file under the user's home directory, outside the
    repository. Tests pass an explicit db_path (e.g. a pytest
    tmp_path) to avoid touching the real user's data.
    """
    return db_path if db_path is not None else DEFAULT_DB_PATH


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    """Open a connection to the tracker database, creating its
    parent directory and schema on first use.
    """
    path = get_db_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    init_schema(conn)
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    """Create the meals and target_history tables if they don't exist."""
    conn.executescript(_SCHEMA)
    conn.commit()