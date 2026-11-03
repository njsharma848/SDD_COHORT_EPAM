"""Repository operation tests (T005 — Covers: AC-009, AC-012, AC-013,
AC-014, AC-020).
"""

import sqlite3
from datetime import date

from calorie_tracker import repository


def test_insert_meal_returns_a_new_id(tmp_path):
    conn = repository.connect(tmp_path / "t.db")
    try:
        meal_id = repository.insert_meal(conn, "Eggs", 1500, 120, date(2026, 11, 3))
        assert isinstance(meal_id, int)
        assert meal_id > 0
    finally:
        conn.close()


def test_delete_meal_returns_true_for_known_id(tmp_path):
    conn = repository.connect(tmp_path / "t.db")
    try:
        meal_id = repository.insert_meal(conn, "Eggs", 1500, 120, date(2026, 11, 3))
        assert repository.delete_meal(conn, meal_id) is True
    finally:
        conn.close()


def test_delete_meal_returns_false_for_unknown_id(tmp_path):
    # AC-009: unknown ID -> no change, caller reports a clear error.
    conn = repository.connect(tmp_path / "t.db")
    try:
        assert repository.delete_meal(conn, 999) is False
    finally:
        conn.close()


def test_daily_totals_sums_only_the_selected_date(tmp_path):
    # AC-013: totals include only meals dated on the selected day.
    conn = repository.connect(tmp_path / "t.db")
    try:
        repository.insert_meal(conn, "Breakfast", 1000, 50, date(2026, 11, 3))
        repository.insert_meal(conn, "Lunch", 2000, 100, date(2026, 11, 3))
        repository.insert_meal(conn, "Other day", 9999, 999, date(2026, 11, 2))

        cal, prot = repository.daily_totals(conn, date(2026, 11, 3))
        assert cal == 3000
        assert prot == 150
    finally:
        conn.close()


def test_daily_totals_is_zero_with_no_meals(tmp_path):
    # AC-014: a day with no meals shows zero totals.
    conn = repository.connect(tmp_path / "t.db")
    try:
        cal, prot = repository.daily_totals(conn, date(2026, 11, 3))
        assert (cal, prot) == (0, 0)
    finally:
        conn.close()


def test_upsert_target_replaces_same_day_target(tmp_path):
    conn = repository.connect(tmp_path / "t.db")
    try:
        repository.upsert_target(conn, date(2026, 11, 3), 20000, 1500)
        repository.upsert_target(conn, date(2026, 11, 3), 18000, 1300)

        row = conn.execute(
            "SELECT COUNT(*) AS n FROM target_history WHERE effective_date = ?",
            ("2026-11-03",),
        ).fetchone()
        assert row["n"] == 1

        target = repository.latest_target_for_date(conn, date(2026, 11, 3))
        assert (target.calories_tenths, target.protein_tenths) == (18000, 1300)
    finally:
        conn.close()


def test_latest_target_preserves_past_effective_dates(tmp_path):
    # AC-012: changing today's target must not alter a past day's
    # applicable target.
    conn = repository.connect(tmp_path / "t.db")
    try:
        repository.upsert_target(conn, date(2026, 11, 1), 20000, 1500)
        repository.upsert_target(conn, date(2026, 11, 5), 18000, 1300)

        past = repository.latest_target_for_date(conn, date(2026, 11, 3))
        assert (past.calories_tenths, past.protein_tenths) == (20000, 1500)

        current = repository.latest_target_for_date(conn, date(2026, 11, 5))
        assert (current.calories_tenths, current.protein_tenths) == (18000, 1300)
    finally:
        conn.close()


def test_latest_target_is_none_before_any_target_was_set(tmp_path):
    conn = repository.connect(tmp_path / "t.db")
    try:
        assert repository.latest_target_for_date(conn, date(2026, 11, 3)) is None
    finally:
        conn.close()


def test_insert_meal_rejects_out_of_range_value_and_rolls_back(tmp_path):
    # AC-020: a rejected mutation leaves stored data unchanged.
    conn = repository.connect(tmp_path / "t.db")
    try:
        try:
            repository.insert_meal(conn, "Too much", 100001, 0, date(2026, 11, 3))
            assert False, "Expected a CHECK constraint violation"
        except sqlite3.IntegrityError:
            pass

        cal, prot = repository.daily_totals(conn, date(2026, 11, 3))
        assert (cal, prot) == (0, 0)
    finally:
        conn.close()