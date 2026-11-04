"""Acceptance tests for viewing daily progress (AC-013 through AC-019).

Covers: AC-013, AC-014, AC-015, AC-016, AC-017, AC-018, AC-019
"""

from __future__ import annotations

from datetime import date

import pytest

from calorie_tracker import repository, service


@pytest.fixture
def conn(tmp_path):
    connection = repository.connect(tmp_path / "test.db")
    yield connection
    connection.close()


def test_tc013_ac013_progress_aggregates_only_meals_on_the_selected_date(conn):
    today = date(2026, 11, 3)
    service.create_meal(conn, "Breakfast", "300", "20", today=today)
    service.create_meal(conn, "Lunch", "500", "30", today=today)
    service.create_meal(conn, "Yesterday's dinner", "900", "40",
                         date_raw="2026-11-02", today=today)

    progress = service.get_progress(conn, today=today)

    assert progress.consumed_calories_tenths == 8000  # 300 + 500 kcal, tenths
    assert progress.consumed_protein_tenths == 500    # 20 + 30 g, tenths


def test_tc014_ac014_zero_totals_on_a_day_with_no_meals(conn):
    today = date(2026, 11, 3)

    progress = service.get_progress(conn, today=today)

    assert progress.consumed_calories_tenths == 0
    assert progress.consumed_protein_tenths == 0


def test_tc015_ac015_consumption_exactly_equals_target_is_met_with_zero_remaining(conn):
    today = date(2026, 11, 3)
    service.create_meal(conn, "Meal", "2000", "150", today=today)
    service.set_targets(conn, "2000", "150", today=today)

    progress = service.get_progress(conn, today=today)

    assert progress.remaining_calories_tenths == 0
    assert progress.remaining_protein_tenths == 0
    assert progress.calories_status == "met"
    assert progress.protein_status == "met"


def test_tc016_ac016_more_than_tolerance_below_target_is_under(conn):
    today = date(2026, 11, 3)
    # Tolerance is 5.0 kcal / 1.0 g. Use tolerance + 0.1 to land just past it.
    service.create_meal(conn, "Meal", "1994.9", "148.9", today=today)
    service.set_targets(conn, "2000", "150", today=today)

    progress = service.get_progress(conn, today=today)

    assert progress.remaining_calories_tenths > 0
    assert progress.remaining_protein_tenths > 0
    assert progress.calories_status == "under"
    assert progress.protein_status == "under"


def test_tc017_ac017_met_tolerance_boundary_on_the_under_side(conn):
    today = date(2026, 11, 3)
    # Exactly 5.0 kcal / 1.0 g below target — boundary, inclusive.
    service.create_meal(conn, "Meal", "1995", "149", today=today)
    service.set_targets(conn, "2000", "150", today=today)

    progress = service.get_progress(conn, today=today)

    assert progress.calories_status == "met"
    assert progress.protein_status == "met"


def test_tc017_ac017_met_tolerance_boundary_on_the_over_side(conn):
    today = date(2026, 11, 3)
    # Exactly 5.0 kcal / 1.0 g above target — boundary, inclusive.
    service.create_meal(conn, "Meal", "2005", "151", today=today)
    service.set_targets(conn, "2000", "150", today=today)

    progress = service.get_progress(conn, today=today)

    assert progress.calories_status == "met"
    assert progress.protein_status == "met"


def test_tc018_ac018_more_than_tolerance_above_target_is_over(conn):
    today = date(2026, 11, 3)
    # Tolerance + 0.1 above target.
    service.create_meal(conn, "Meal", "2005.1", "151.1", today=today)
    service.set_targets(conn, "2000", "150", today=today)

    progress = service.get_progress(conn, today=today)

    assert progress.remaining_calories_tenths < 0
    assert progress.remaining_protein_tenths < 0
    assert progress.calories_status == "over"
    assert progress.protein_status == "over"


def test_tc019_ac019_no_target_shows_consumed_totals_and_no_target_set(conn):
    today = date(2026, 11, 3)
    service.create_meal(conn, "Breakfast", "500", "30", today=today)

    progress = service.get_progress(conn, today=today)

    assert progress.target is None
    assert progress.has_target is False
    assert progress.remaining_calories_tenths is None
    assert progress.remaining_protein_tenths is None
    assert progress.calories_status is None
    assert progress.protein_status is None
    assert progress.consumed_calories_tenths == 5000
    assert progress.consumed_protein_tenths == 300