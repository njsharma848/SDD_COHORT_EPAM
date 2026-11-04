"""Acceptance tests for setting daily targets (T017 — Covers: AC-010,
AC-011, AC-012; Supports: P-3).
"""

from datetime import date

from calorie_tracker import repository, service
from calorie_tracker.validation import ValidationError


def _conn(tmp_path):
    return repository.connect(tmp_path / "t.db")


def test_tc010_ac010_set_paired_targets_together(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        target = service.set_targets(conn, "2000", "150", today=today)
        assert target.calories_tenths == 20000
        assert target.protein_tenths == 1500

        stored = repository.latest_target_for_date(conn, today)
        assert (stored.calories_tenths, stored.protein_tenths) == (20000, 1500)
    finally:
        conn.close()


def test_tc010_ac010_set_paired_targets_at_maximum(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        target = service.set_targets(conn, "10000", "1000", today=today)
        assert target.calories_tenths == 100000
        assert target.protein_tenths == 10000
    finally:
        conn.close()


def test_tc011_ac011_missing_target_value_rejected_and_history_unchanged(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        try:
            service.set_targets(conn, "", "150", today=today)
            assert False, "Expected ValidationError for a missing calorie target"
        except ValidationError:
            pass
        assert repository.latest_target_for_date(conn, today) is None
    finally:
        conn.close()


def test_tc011_ac011_negative_target_rejected_and_history_unchanged(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        try:
            service.set_targets(conn, "-100", "150", today=today)
            assert False, "Expected ValidationError for a negative calorie target"
        except ValidationError:
            pass
        assert repository.latest_target_for_date(conn, today) is None
    finally:
        conn.close()


def test_tc011_ac011_above_maximum_target_rejected_and_history_unchanged(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        try:
            service.set_targets(conn, "10000.1", "150", today=today)
            assert False, "Expected ValidationError above the target maximum"
        except ValidationError:
            pass
        assert repository.latest_target_for_date(conn, today) is None
    finally:
        conn.close()


def test_tc011_ac011_too_many_decimal_places_rejected_and_history_unchanged(tmp_path):
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        try:
            service.set_targets(conn, "2000.55", "150", today=today)
            assert False, "Expected ValidationError for more than one decimal place"
        except ValidationError:
            pass
        assert repository.latest_target_for_date(conn, today) is None
    finally:
        conn.close()


def test_tc011_ac011_rejecting_one_field_leaves_prior_valid_target_unchanged(tmp_path):
    # A rejected target change (bad protein) must not clobber an
    # already-set valid target for the same day.
    conn = _conn(tmp_path)
    try:
        today = date(2026, 11, 3)
        service.set_targets(conn, "2000", "150", today=today)

        try:
            service.set_targets(conn, "2200", "-10", today=today)
            assert False, "Expected ValidationError for negative protein"
        except ValidationError:
            pass

        stored = repository.latest_target_for_date(conn, today)
        assert (stored.calories_tenths, stored.protein_tenths) == (20000, 1500)
    finally:
        conn.close()


def test_tc012_ac012_target_change_preserves_past_effective_dates(tmp_path):
    conn = _conn(tmp_path)
    try:
        day1 = date(2026, 11, 1)
        day5 = date(2026, 11, 5)

        service.set_targets(conn, "2000", "150", today=day1)
        service.set_targets(conn, "1800", "120", today=day5)

        past = repository.latest_target_for_date(conn, date(2026, 11, 3))
        assert (past.calories_tenths, past.protein_tenths) == (20000, 1500)

        current = repository.latest_target_for_date(conn, day5)
        assert (current.calories_tenths, current.protein_tenths) == (18000, 1200)
    finally:
        conn.close()