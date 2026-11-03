"""Schema and initialization tests for the SQLite repository layer
(T004 — Covers: AC-001, AC-006a, AC-010, AC-012; Supports: P-5).
"""

import sqlite3
from pathlib import Path

from calorie_tracker import repository


def test_connect_creates_schema_with_meals_and_target_history_tables(tmp_path):
    db_path = tmp_path / "test_tracker.db"
    conn = repository.connect(db_path)
    try:
        tables = {
            row["name"]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        assert "meals" in tables
        assert "target_history" in tables
    finally:
        conn.close()


def test_meals_table_accepts_value_at_maximum(tmp_path):
    # AC-006a: a meal exactly at the maximum is accepted.
    db_path = tmp_path / "test_tracker.db"
    conn = repository.connect(db_path)
    try:
        conn.execute(
            "INSERT INTO meals (name, calories_tenths, protein_tenths, meal_date) "
            "VALUES (?, ?, ?, ?)",
            ("Max meal", 100000, 10000, "2026-11-03"),
        )
        conn.commit()
    finally:
        conn.close()


def test_meals_table_rejects_value_above_maximum(tmp_path):
    db_path = tmp_path / "test_tracker.db"
    conn = repository.connect(db_path)
    try:
        try:
            conn.execute(
                "INSERT INTO meals (name, calories_tenths, protein_tenths, meal_date) "
                "VALUES (?, ?, ?, ?)",
                ("Too many calories", 100001, 0, "2026-11-03"),
            )
            conn.commit()
            assert False, "Expected a CHECK constraint violation"
        except sqlite3.IntegrityError:
            pass
    finally:
        conn.close()


def test_target_history_effective_date_is_primary_key(tmp_path):
    # AC-010/AC-012: one target row per effective_date; the service
    # layer later handles "replace today's target" via upsert, not
    # a raw duplicate insert.
    db_path = tmp_path / "test_tracker.db"
    conn = repository.connect(db_path)
    try:
        conn.execute(
            "INSERT INTO target_history (effective_date, calories_tenths, protein_tenths) "
            "VALUES (?, ?, ?)",
            ("2026-11-01", 20000, 1500),
        )
        conn.commit()

        try:
            conn.execute(
                "INSERT INTO target_history (effective_date, calories_tenths, protein_tenths) "
                "VALUES (?, ?, ?)",
                ("2026-11-01", 18000, 1200),
            )
            conn.commit()
            assert False, "Expected a PRIMARY KEY violation"
        except sqlite3.IntegrityError:
            pass
    finally:
        conn.close()


def test_default_database_path_resolves_outside_the_repository():
    # P-5: the database must live outside the repository (under the
    # user's home directory), not inside the project tree.
    resolved = repository.get_db_path()
    assert str(resolved).startswith(str(Path.home()))