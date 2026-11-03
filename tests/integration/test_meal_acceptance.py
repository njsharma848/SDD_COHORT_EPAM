"""Acceptance tests for meal creation (T011 — Covers: AC-001, AC-002,
AC-004, AC-005). Each test name encodes its test case ID and the
acceptance criterion it verifies, per constitution P-2.
"""

from datetime import date

from calorie_tracker import repository, service


def _conn(tmp_path):
    return repository.connect(tmp_path / "t.db")


def test_tc001_ac001_meal_without_date_defaults_to_today(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        meal = service.create_meal(conn, "Oatmeal", "150", "5", today=today)
        assert meal.meal_date == today
        assert meal.calories_tenths == 1500
        assert meal.protein_tenths == 50
    finally:
        conn.close()


def test_tc002_ac002_meal_recorded_for_past_date(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        meal = service.create_meal(
            conn, "Yesterday's lunch", "500", "30", date_raw="2026-11-02", today=today
        )
        assert meal.meal_date == date(2026, 11, 2)
    finally:
        conn.close()


def test_tc002_ac002_meal_recorded_for_present_date(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        meal = service.create_meal(
            conn, "Today's lunch", "500", "30", date_raw="2026-11-03", today=today
        )
        assert meal.meal_date == today
    finally:
        conn.close()


def test_tc004_ac004_meal_values_stored_rounded_to_one_decimal(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        meal = service.create_meal(conn, "Snack", "12.3", "4.5", today=today)
        assert meal.calories_tenths == 123
        assert meal.protein_tenths == 45

        cal, prot = repository.daily_totals(conn, today)
        assert cal == 123
        assert prot == 45
    finally:
        conn.close()


def test_tc005_ac005_zero_calories_and_protein_accepted(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        meal = service.create_meal(conn, "Water", "0", "0", today=today)
        assert meal.calories_tenths == 0
        assert meal.protein_tenths == 0
    finally:
        conn.close()