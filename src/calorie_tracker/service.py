"""Service layer: domain error types, plus (in later tasks) the
business logic that validates input, calls the repository, and
returns results to the CLI.

Keeping error types in one place lets the CLI catch a single
exception hierarchy (DomainError, plus ValidationError from
validation.py) and print a clear, field-specific message without
leaking a raw traceback or SQLite internals (constitution P-3).
"""

from __future__ import annotations

import sqlite3

from .validation import ValidationError  # re-exported for convenience
from datetime import date as _date

from . import repository
from .models import DailyProgress, Meal, Target
from .validation import parse_date, validate_calories, validate_meal_date, validate_name, validate_protein

class DomainError(Exception):
    """Base class for all expected, user-facing errors raised by the
    service layer.
    """


class UnknownMealError(DomainError):
    """Raised when a meal ID does not identify a recorded meal
    (AC-009's unknown-ID case).
    """

    def __init__(self, meal_id: int):
        self.meal_id = meal_id
        super().__init__(f"No meal exists with id {meal_id}")


class PersistenceError(DomainError):
    """Raised when a storage operation fails unexpectedly. Wraps the
    underlying sqlite3 error without exposing it directly to callers.
    """

    def __init__(self, operation: str, cause: Exception):
        self.operation = operation
        self.__cause__ = cause
        super().__init__(f"{operation} failed and no data was changed")


def run_safely(operation: str, fn, *args, **kwargs):
    """Call fn(*args, **kwargs), translating any sqlite3.Error into a
    PersistenceError so callers only ever see DomainError/ValidationError,
    never a raw sqlite3 exception or traceback.
    """
    try:
        return fn(*args, **kwargs)
    except sqlite3.Error as exc:
        raise PersistenceError(operation, exc) from exc

def create_meal(conn, name, calories_raw, protein_raw, date_raw=None, today=None) -> Meal:
    """Validate and record a new meal. Returns the persisted Meal
    (with its assigned id).

    Raises ValidationError for any invalid field (AC-003, AC-006b,
    AC-007) or PersistenceError on storage failure. Validation runs
    entirely before the repository call, so no partial write ever
    occurs (AC-020).

    `today` is injectable for testing; defaults to the real local date.
    """
    if today is None:
        today = _date.today()

    validated_name = validate_name(name)
    calories_tenths = validate_calories(calories_raw)
    protein_tenths = validate_protein(protein_raw)
    meal_date = validate_meal_date(date_raw, today)

    meal_id = run_safely(
        "record meal",
        repository.insert_meal,
        conn, validated_name, calories_tenths, protein_tenths, meal_date,
    )

    return Meal(
        id=meal_id,
        name=validated_name,
        calories_tenths=calories_tenths,
        protein_tenths=protein_tenths,
        meal_date=meal_date,
    )

def delete_meal(conn, meal_id: int) -> None:
    """Delete a meal by ID.

    Raises UnknownMealError if no meal with that ID exists (AC-009).
    On failure, no data is changed — repository.delete_meal only
    deletes a row if one actually matches.
    """
    deleted = run_safely("delete meal", repository.delete_meal, conn, meal_id)
    if not deleted:
        raise UnknownMealError(meal_id)

def set_targets(conn, calories_raw, protein_raw, today=None) -> Target:
    """Validate and set/change today's daily calorie and protein
    targets together.

    Both values are fully validated before any write (AC-011) — a
    rejection leaves the previous target history completely
    unchanged. Earlier effective dates are never modified; this only
    affects today forward (AC-012, BR-06).

    `today` is injectable for testing; defaults to the real local date.
    """
    if today is None:
        today = _date.today()

    calories_tenths = validate_calories(calories_raw)
    protein_tenths = validate_protein(protein_raw)

    run_safely(
        "set targets",
        repository.upsert_target,
        conn, today, calories_tenths, protein_tenths,
    )

    return Target(
        effective_date=today,
        calories_tenths=calories_tenths,
        protein_tenths=protein_tenths,
    )
CALORIE_TOLERANCE_TENTHS = 50  # 5.0 kcal
PROTEIN_TOLERANCE_TENTHS = 10  # 1.0 g


def _status_for(difference_tenths: int, tolerance_tenths: int) -> str:
    """BR-11: 'met' includes the boundary on both sides."""
    if abs(difference_tenths) <= tolerance_tenths:
        return "met"
    if difference_tenths < -tolerance_tenths:
        return "under"
    return "over"


def get_progress(conn, date_raw=None, today=None) -> DailyProgress:
    """Compute the progress view for one selected day.

    Aggregates only meals dated exactly on the selected day (AC-013),
    defaults to local today when omitted, looks up the latest
    effective target on or before that day, and — when a target
    exists — calculates signed remaining amounts and an
    under/met/over status per nutrient using BR-11's tolerances.
    When no target applies, remaining/status are None (BR-09/AC-019).
    """
    if today is None:
        today = _date.today()

    selected_date = parse_date(date_raw, today)

    consumed_cal, consumed_prot = run_safely(
        "view progress", repository.daily_totals, conn, selected_date
    )
    target = run_safely(
        "view progress", repository.latest_target_for_date, conn, selected_date
    )

    if target is None:
        return DailyProgress(
            selected_date=selected_date,
            consumed_calories_tenths=consumed_cal,
            consumed_protein_tenths=consumed_prot,
            target=None,
            remaining_calories_tenths=None,
            remaining_protein_tenths=None,
            calories_status=None,
            protein_status=None,
        )

    remaining_cal = target.calories_tenths - consumed_cal
    remaining_prot = target.protein_tenths - consumed_prot
    cal_diff = consumed_cal - target.calories_tenths
    prot_diff = consumed_prot - target.protein_tenths

    return DailyProgress(
        selected_date=selected_date,
        consumed_calories_tenths=consumed_cal,
        consumed_protein_tenths=consumed_prot,
        target=target,
        remaining_calories_tenths=remaining_cal,
        remaining_protein_tenths=remaining_prot,
        calories_status=_status_for(cal_diff, CALORIE_TOLERANCE_TENTHS),
        protein_status=_status_for(prot_diff, PROTEIN_TOLERANCE_TENTHS),
    )