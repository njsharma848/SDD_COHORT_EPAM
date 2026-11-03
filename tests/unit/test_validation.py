"""Validation layer tests (T006 — Covers: AC-003, AC-006b, AC-007,
AC-011, AC-020).
"""

from datetime import date

import pytest

from calorie_tracker.validation import (
    ValidationError,
    validate_calories,
    validate_meal_date,
    validate_name,
    validate_protein,
)


# -- calories / protein (shared logic, exercised via calories) --

def test_validate_calories_accepts_integer_string():
    assert validate_calories("150") == 1500


def test_validate_calories_accepts_one_decimal_place():
    assert validate_calories("12.3") == 123


def test_validate_calories_accepts_zero():
    assert validate_calories("0") == 0


def test_validate_calories_accepts_value_at_maximum():
    assert validate_calories("10000") == 100000


def test_validate_calories_rejects_value_above_maximum():
    with pytest.raises(ValidationError):
        validate_calories("10000.1")


def test_validate_calories_rejects_more_than_one_decimal_place():
    with pytest.raises(ValidationError):
        validate_calories("12.34")


def test_validate_calories_rejects_negative():
    with pytest.raises(ValidationError):
        validate_calories("-5")


def test_validate_calories_rejects_non_numeric():
    with pytest.raises(ValidationError):
        validate_calories("abc")


def test_validate_calories_rejects_missing():
    with pytest.raises(ValidationError):
        validate_calories(None)
    with pytest.raises(ValidationError):
        validate_calories("")


def test_validate_protein_accepts_value_at_maximum():
    assert validate_protein("1000") == 10000


def test_validate_protein_rejects_value_above_maximum():
    with pytest.raises(ValidationError):
        validate_protein("1000.1")


# -- name --

def test_validate_name_rejects_empty():
    with pytest.raises(ValidationError):
        validate_name("")
    with pytest.raises(ValidationError):
        validate_name("   ")


def test_validate_name_strips_whitespace():
    assert validate_name("  Oatmeal  ") == "Oatmeal"


# -- date --

def test_validate_meal_date_defaults_to_today_when_omitted():
    today = date(2026, 11, 3)
    assert validate_meal_date(None, today) == today
    assert validate_meal_date("", today) == today


def test_validate_meal_date_accepts_past_date():
    today = date(2026, 11, 3)
    assert validate_meal_date("2026-10-01", today) == date(2026, 10, 1)


def test_validate_meal_date_accepts_today():
    today = date(2026, 11, 3)
    assert validate_meal_date("2026-11-03", today) == today


def test_validate_meal_date_rejects_future_date():
    today = date(2026, 11, 3)
    with pytest.raises(ValidationError):
        validate_meal_date("2026-11-04", today)


def test_validate_meal_date_rejects_malformed_date():
    today = date(2026, 11, 3)
    with pytest.raises(ValidationError):
        validate_meal_date("2026-13-45", today)
    with pytest.raises(ValidationError):
        validate_meal_date("not-a-date", today)