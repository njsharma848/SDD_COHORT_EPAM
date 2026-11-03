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

from calorie_tracker.validation import ValidationError


def test_tc003_ac003_future_date_rejected_and_data_unchanged(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        try:
            service.create_meal(conn, "Too soon", "100", "5", date_raw="2026-11-04", today=today)
            assert False, "Expected ValidationError for a future date"
        except ValidationError:
            pass

        cal, prot = repository.daily_totals(conn, date(2026, 11, 4))
        assert (cal, prot) == (0, 0)
    finally:
        conn.close()


def test_tc006a_ac006a_meal_exactly_at_maximum_accepted(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        meal = service.create_meal(conn, "Max meal", "10000", "1000", today=today)
        assert meal.calories_tenths == 100000
        assert meal.protein_tenths == 10000
    finally:
        conn.close()


def test_tc006b_ac006b_meal_above_maximum_rejected_and_data_unchanged(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        try:
            service.create_meal(conn, "Too many calories", "10000.1", "5", today=today)
            assert False, "Expected ValidationError above the calorie maximum"
        except ValidationError:
            pass

        cal, prot = repository.daily_totals(conn, today)
        assert (cal, prot) == (0, 0)
    finally:
        conn.close()


def test_tc007_ac007_missing_name_rejected_and_data_unchanged(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        try:
            service.create_meal(conn, "", "100", "5", today=today)
            assert False, "Expected ValidationError for a missing name"
        except ValidationError:
            pass
        cal, prot = repository.daily_totals(conn, today)
        assert (cal, prot) == (0, 0)
    finally:
        conn.close()


def test_tc007_ac007_non_numeric_calories_rejected_and_data_unchanged(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        try:
            service.create_meal(conn, "Snack", "abc", "5", today=today)
            assert False, "Expected ValidationError for non-numeric calories"
        except ValidationError:
            pass
        cal, prot = repository.daily_totals(conn, today)
        assert (cal, prot) == (0, 0)
    finally:
        conn.close()


def test_tc007_ac007_negative_protein_rejected_and_data_unchanged(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        try:
            service.create_meal(conn, "Snack", "100", "-5", today=today)
            assert False, "Expected ValidationError for negative protein"
        except ValidationError:
            pass
        cal, prot = repository.daily_totals(conn, today)
        assert (cal, prot) == (0, 0)
    finally:
        conn.close()


def test_tc007_ac007_too_many_decimal_places_rejected_and_data_unchanged(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        try:
            service.create_meal(conn, "Snack", "12.34", "5", today=today)
            assert False, "Expected ValidationError for more than one decimal place"
        except ValidationError:
            pass
        cal, prot = repository.daily_totals(conn, today)
        assert (cal, prot) == (0, 0)
    finally:
        conn.close()


def test_tc008_ac008_meal_recorded_successfully_with_no_target_set(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        assert repository.latest_target_for_date(conn, today) is None

        meal = service.create_meal(conn, "No target yet", "300", "20", today=today)
        assert meal.id is not None
    finally:
        conn.close()

from calorie_tracker.service import UnknownMealError


def test_tc009_ac009_delete_known_meal_removes_it_from_totals(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        meal = service.create_meal(conn, "Oatmeal", "150", "5", today=today)

        cal, prot = repository.daily_totals(conn, today)
        assert (cal, prot) == (1500, 50)

        service.delete_meal(conn, meal.id)

        cal, prot = repository.daily_totals(conn, today)
        assert (cal, prot) == (0, 0)
    finally:
        conn.close()


def test_tc009_ac009_delete_unknown_id_reports_error_and_leaves_data_unchanged(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        meal = service.create_meal(conn, "Oatmeal", "150", "5", today=today)

        try:
            service.delete_meal(conn, meal.id + 999)
            assert False, "Expected UnknownMealError for an unknown ID"
        except UnknownMealError:
            pass

        # The existing meal must still be present and unchanged.
        cal, prot = repository.daily_totals(conn, today)
        assert (cal, prot) == (1500, 50)
    finally:
        conn.close()