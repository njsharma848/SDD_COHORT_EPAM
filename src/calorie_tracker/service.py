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
from .models import Meal,Target
from .validation import validate_calories, validate_meal_date, validate_name, validate_protein

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