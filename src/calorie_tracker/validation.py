"""Input validation for meal and target fields (BR-01..BR-12).

All validation happens before any persistence call. Values are
parsed as Decimal to avoid float precision issues, then converted to
integer tenths. See plan.md's Decimal Precision and Display section.

Calorie/protein limits are shared by meals and targets (A-15: the
target maximum was deliberately set equal to the per-meal maximum).
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation

MAX_CALORIES_TENTHS = 100_000  # 10,000.0 kcal
MAX_PROTEIN_TENTHS = 10_000    # 1,000.0 g


class ValidationError(Exception):
    """A single field-level validation failure."""

    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


def _parse_amount_tenths(raw: str | None, field: str, max_tenths: int) -> int:
    """Parse a calorie/protein amount string into integer tenths.

    Rejects missing, non-numeric, negative, more-than-one-decimal-place,
    and above-maximum values (BR-03/BR-05/BR-12).
    """
    if raw is None or str(raw).strip() == "":
        raise ValidationError(field, "is required")

    try:
        value = Decimal(str(raw).strip())
    except InvalidOperation:
        raise ValidationError(field, "must be a number") from None

    if value < 0:
        raise ValidationError(field, "must be zero or greater")

    exponent = value.as_tuple().exponent
    if isinstance(exponent, int) and exponent < -1:
        raise ValidationError(field, "must have at most one decimal place")

    tenths = int(value * 10)

    if tenths > max_tenths:
        max_value = Decimal(max_tenths) / 10
        raise ValidationError(field, f"must not exceed {max_value}")

    return tenths


def validate_calories(raw: str | None) -> int:
    return _parse_amount_tenths(raw, "calories", MAX_CALORIES_TENTHS)


def validate_protein(raw: str | None) -> int:
    return _parse_amount_tenths(raw, "protein", MAX_PROTEIN_TENTHS)


def validate_name(raw: str | None) -> str:
    if raw is None or str(raw).strip() == "":
        raise ValidationError("name", "is required")
    return str(raw).strip()


def validate_meal_date(raw: str | None, today: date) -> date:
    """Parse and validate a meal date string (YYYY-MM-DD).

    Omitted/blank defaults to today. Rejects malformed dates and any
    date after today (BR-02/AC-003).
    """
    if raw is None or str(raw).strip() == "":
        return today

    try:
        parsed = date.fromisoformat(str(raw).strip())
    except ValueError:
        raise ValidationError("date", "must be a valid YYYY-MM-DD date") from None

    if parsed > today:
        raise ValidationError("date", "must not be in the future")

    return parsed

def parse_date(raw: str | None, today: date) -> date:
    """Parse an optional date string for read-only use (e.g. the
    progress command), defaulting to today.

    Unlike validate_meal_date, this does NOT reject future dates —
    viewing progress for a future (empty) day is allowed; only
    *logging a meal* on a future date is forbidden (plan.md Risks
    table: a deliberate, documented distinction).
    """
    if raw is None or str(raw).strip() == "":
        return today
    try:
        return date.fromisoformat(str(raw).strip())
    except ValueError:
        raise ValidationError("date", "must be a valid YYYY-MM-DD date") from None


    