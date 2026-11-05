"""End-to-end safe-failure test (AC-020): no invalid input, of any
kind covered by BR-12, ever leaves a partial write behind.

Covers: AC-020
"""

from __future__ import annotations

from datetime import date

import pytest

from calorie_tracker import repository, service
from calorie_tracker.validation import ValidationError


@pytest.fixture
def conn(tmp_path):
    connection = repository.connect(tmp_path / "test.db")
    yield connection
    connection.close()


def _snapshot(conn, today):
    """Capture everything observable: both days' totals and the
    active target, so we can prove nothing moved at all.
    """
    return {
        "today_progress": service.get_progress(conn, today=today),
        "yesterday_progress": service.get_progress(
            conn, date_raw="2026-11-02", today=today
        ),
    }


def test_tc020_ac020_invalid_meal_and_target_inputs_leave_all_data_unchanged(conn):
    today = date(2026, 11, 3)

    # Establish a known-good baseline: one meal on a past day, one on
    # today, and a target — so there is real state to protect.
    service.create_meal(conn, "Yesterday's lunch", "400", "25",
                         date_raw="2026-11-02", today=today)
    service.create_meal(conn, "Breakfast", "500", "30", today=today)
    service.set_targets(conn, "2000", "150", today=today)

    baseline = _snapshot(conn, today)

    invalid_operations = [
        # Meal: missing name
        lambda: service.create_meal(conn, "", "100", "10", today=today),
        # Meal: non-numeric calories
        lambda: service.create_meal(conn, "Snack", "abc", "10", today=today),
        # Meal: negative protein
        lambda: service.create_meal(conn, "Snack", "100", "-5", today=today),
        # Meal: more than one decimal place
        lambda: service.create_meal(conn, "Snack", "100.55", "10", today=today),
        # Meal: above the per-meal maximum
        lambda: service.create_meal(conn, "Feast", "10000.1", "10", today=today),
        # Meal: future date
        lambda: service.create_meal(conn, "Future meal", "100", "10",
                                     date_raw="2099-01-01", today=today),
        # Delete: unknown meal ID
        lambda: service.delete_meal(conn, 999_999),
        # Target: missing/non-numeric calories
        lambda: service.set_targets(conn, "abc", "150", today=today),
        # Target: negative protein
        lambda: service.set_targets(conn, "2000", "-10", today=today),
        # Target: above maximum
        lambda: service.set_targets(conn, "10000.1", "150", today=today),
    ]

    for operation in invalid_operations:
        with pytest.raises((ValidationError, service.DomainError)):
            operation()

    after = _snapshot(conn, today)

    # Every invalid attempt was rejected, and the whole state —
    # today's totals/target/status, and yesterday's totals — is
    # identical to the baseline captured before any of them ran.
    assert after["today_progress"] == baseline["today_progress"]
    assert after["yesterday_progress"] == baseline["yesterday_progress"]


def test_tc020_ac020_rejecting_a_target_field_leaves_the_prior_target_fully_intact(conn):
    today = date(2026, 11, 3)
    service.create_meal(conn, "Breakfast", "500", "30", today=today)
    service.set_targets(conn, "2000", "150", today=today)

    baseline = service.get_progress(conn, today=today)

    with pytest.raises(ValidationError):
        service.set_targets(conn, "2000", "-1", today=today)

    after = service.get_progress(conn, today=today)
    assert after == baseline
    assert after.target.calories_tenths == 20000
    assert after.target.protein_tenths == 1500


    