"""SQLite persistence foundation: schema creation and connection
management. Business logic lives in service.py; this module only
owns the database file and its schema (structural constraints from
BR-01..BR-12), per plan.md's Components table.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import date as _date
from .models import Target

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

def insert_meal(conn: sqlite3.Connection, name: str, calories_tenths: int,
                 protein_tenths: int, meal_date: _date) -> int:
    """Insert a meal and return its new ID.

    Runs inside a transaction: `with conn:` commits on success and
    rolls back automatically if any exception is raised inside it.
    """
    with conn:
        cur = conn.execute(
            "INSERT INTO meals (name, calories_tenths, protein_tenths, meal_date) "
            "VALUES (?, ?, ?, ?)",
            (name, calories_tenths, protein_tenths, meal_date.isoformat()),
        )
    return cur.lastrowid


def delete_meal(conn: sqlite3.Connection, meal_id: int) -> bool:
    """Delete a meal by ID.

    Returns True if a row was deleted, False if no meal with that ID
    exists (AC-009's unknown-ID case — the service layer turns False
    into a clear error).
    """
    with conn:
        cur = conn.execute("DELETE FROM meals WHERE id = ?", (meal_id,))
    return cur.rowcount > 0


def daily_totals(conn: sqlite3.Connection, selected_date: _date) -> tuple[int, int]:
    """Sum calories/protein tenths for meals on exactly selected_date.

    Returns (0, 0) when there are no meals that day (AC-014).
    """
    row = conn.execute(
        "SELECT COALESCE(SUM(calories_tenths), 0) AS cal, "
        "COALESCE(SUM(protein_tenths), 0) AS prot "
        "FROM meals WHERE meal_date = ?",
        (selected_date.isoformat(),),
    ).fetchone()
    return row["cal"], row["prot"]


def upsert_target(conn: sqlite3.Connection, effective_date: _date,
                   calories_tenths: int, protein_tenths: int) -> None:
    """Insert a target for effective_date, or replace it if one
    already exists for that exact date (a same-day target change).
    Earlier effective dates are never modified (BR-06).
    """
    with conn:
        conn.execute(
            "INSERT INTO target_history (effective_date, calories_tenths, protein_tenths) "
            "VALUES (?, ?, ?) "
            "ON CONFLICT(effective_date) DO UPDATE SET "
            "calories_tenths = excluded.calories_tenths, "
            "protein_tenths = excluded.protein_tenths",
            (effective_date.isoformat(), calories_tenths, protein_tenths),
        )


def latest_target_for_date(conn: sqlite3.Connection, selected_date: _date) -> Target | None:
    """Return the target whose effective_date is the greatest date
    <= selected_date, or None if no target has ever applied on or
    before that date (BR-06 history lookup / BR-09 no-target case).
    """
    row = conn.execute(
        "SELECT effective_date, calories_tenths, protein_tenths "
        "FROM target_history WHERE effective_date <= ? "
        "ORDER BY effective_date DESC LIMIT 1",
        (selected_date.isoformat(),),
    ).fetchone()
    if row is None:
        return None
    return Target(
        effective_date=_date.fromisoformat(row["effective_date"]),
        calories_tenths=row["calories_tenths"],
        protein_tenths=row["protein_tenths"],
    )

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