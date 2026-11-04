"""CLI tests for the `progress` command (T019).

Covers: AC-013, AC-016, AC-017, AC-019, AC-021
"""

from __future__ import annotations

import pytest

from calorie_tracker.cli import run


@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "test.db"


def test_progress_with_target_shows_calories_and_protein_lines(db_path, capsys):
    run(["add-meal", "--name", "Oatmeal", "--calories", "500", "--protein", "30",
         "--date", "2026-11-03"], db_path=db_path)
    run(["set-targets", "--calories", "2000", "--protein", "150"], db_path=db_path)

    exit_code = run(["progress", "--date", "2026-11-03"], db_path=db_path)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Progress for 2026-11-03" in captured.out
    assert "Calories:" in captured.out
    assert "Protein:" in captured.out


def test_progress_without_target_reports_no_target_set(db_path, capsys):
    run(["add-meal", "--name", "Oatmeal", "--calories", "500", "--protein", "30",
         "--date", "2026-11-03"], db_path=db_path)

    exit_code = run(["progress", "--date", "2026-11-03"], db_path=db_path)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "no target set" in captured.out
    assert "Consumed:" in captured.out


def test_progress_date_option_selects_the_requested_day(db_path, capsys):
    run(["add-meal", "--name", "Soup", "--calories", "300", "--protein", "10",
         "--date", "2026-11-01"], db_path=db_path)
    run(["add-meal", "--name", "Salad", "--calories", "400", "--protein", "20",
         "--date", "2026-11-02"], db_path=db_path)

    exit_code = run(["progress", "--date", "2026-11-01"], db_path=db_path)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Progress for 2026-11-01" in captured.out
    assert "300.0" in captured.out  # consumed calories for Nov 1  # consumed calories for Nov 1 (300 -> 30.0 kcal tenths display)


def test_progress_rejects_malformed_date(db_path, capsys):
    exit_code = run(["progress", "--date", "not-a-date"], db_path=db_path)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error:" in captured.err


def test_progress_usable_without_account_or_login(db_path, capsys):
    exit_code = run(["progress"], db_path=db_path)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Error" not in captured.err

def test_progress_with_target_shows_calories_and_protein_lines(db_path, capsys):
    run(["add-meal", "--name", "Oatmeal", "--calories", "500", "--protein", "30"],
        db_path=db_path)
    run(["set-targets", "--calories", "2000", "--protein", "150"], db_path=db_path)

    exit_code = run(["progress"], db_path=db_path)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Calories:" in captured.out
    assert "Protein:" in captured.out
    assert "500.0" in captured.out
    assert "2000.0" in captured.out