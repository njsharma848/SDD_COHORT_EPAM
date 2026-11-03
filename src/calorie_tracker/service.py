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