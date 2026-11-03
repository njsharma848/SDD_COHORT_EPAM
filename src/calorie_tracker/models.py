"""Typed value objects for the Calorie and Nutrition Tracker.

No persistence or CLI concerns live here — see repository.py and cli.py.
Nutrition amounts are stored as integer tenths (e.g. 12.3 kcal -> 123)
to avoid binary floating-point drift, per plan.md's Data Handling section.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Meal:
    """A single recorded meal.

    id is None until the repository assigns one on insert.
    """

    id: int | None
    name: str
    calories_tenths: int  # 0..100_000  (0.0 .. 10,000.0 kcal)
    protein_tenths: int   # 0..10_000   (0.0 .. 1,000.0 g)
    meal_date: date


@dataclass(frozen=True)
class Target:
    """A daily target pair, effective from effective_date forward
    until superseded by a later effective_date (BR-06).
    """

    effective_date: date
    calories_tenths: int  # 0..100_000  (0.0 .. 10,000.0 kcal)
    protein_tenths: int   # 0..10_000   (0.0 .. 1,000.0 g)


@dataclass(frozen=True)
class DailyProgress:
    """The computed progress view for one selected day (BR-08..BR-11)."""

    selected_date: date
    consumed_calories_tenths: int
    consumed_protein_tenths: int
    target: Target | None  # None means "no target set" (BR-09)

    @property
    def has_target(self) -> bool:
        return self.target is not None