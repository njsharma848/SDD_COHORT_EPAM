"""Unit tests for the core value models (AC-001, AC-004, AC-010,
AC-013, AC-015 — construction and value integrity only; behavior
and validation are tested elsewhere per tasks.md).
"""

from datetime import date

from calorie_tracker.models import DailyProgress, Meal, Target


def test_tc_model_meal_construction_holds_supplied_values():
    meal = Meal(
        id=None,
        name="Oatmeal",
        calories_tenths=1500,  # 150.0 kcal
        protein_tenths=50,     # 5.0 g
        meal_date=date(2026, 11, 3),
    )
    assert meal.id is None
    assert meal.name == "Oatmeal"
    assert meal.calories_tenths == 1500
    assert meal.protein_tenths == 50
    assert meal.meal_date == date(2026, 11, 3)


def test_tc_model_meal_is_immutable():
    meal = Meal(1, "Oatmeal", 1500, 50, date(2026, 11, 3))
    try:
        meal.name = "Toast"  # type: ignore[misc]
        assert False, "Meal should be frozen/immutable"
    except AttributeError:
        pass


def test_tc_model_target_construction_holds_supplied_values():
    target = Target(
        effective_date=date(2026, 11, 3),
        calories_tenths=20000,  # 2,000.0 kcal
        protein_tenths=1500,    # 150.0 g
    )
    assert target.effective_date == date(2026, 11, 3)
    assert target.calories_tenths == 20000
    assert target.protein_tenths == 1500


def test_tc_model_daily_progress_without_target_reports_no_target():
    progress = DailyProgress(
        selected_date=date(2026, 11, 3),
        consumed_calories_tenths=0,
        consumed_protein_tenths=0,
        target=None,
        remaining_calories_tenths=None,
        remaining_protein_tenths=None,
        calories_status=None,
        protein_status=None,
    )
    assert progress.has_target is False


def test_tc_model_daily_progress_with_target_reports_has_target():
    target = Target(date(2026, 11, 3), 20000, 1500)
    progress = DailyProgress(
        selected_date=date(2026, 11, 3),
        consumed_calories_tenths=1500,
        consumed_protein_tenths=50,
        target=target,
        remaining_calories_tenths=18500,
        remaining_protein_tenths=1450,
        calories_status="under",
        protein_status="under",
    )
    assert progress.has_target is True
    assert progress.target.calories_tenths == 20000