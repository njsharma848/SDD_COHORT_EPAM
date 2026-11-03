"""CLI tests for add-meal and delete-meal (T010 — Covers: AC-001,
AC-002, AC-003, AC-004, AC-005, AC-006a, AC-006b, AC-007, AC-008,
AC-009, AC-021).
"""

from calorie_tracker.cli import run


def test_help_lists_add_and_delete_meal_commands(capsys):
    try:
        run(["--help"])
    except SystemExit:
        pass
    out = capsys.readouterr().out
    assert "add-meal" in out
    assert "delete-meal" in out


def test_add_meal_success_reports_id(tmp_path, capsys):
    db_path = tmp_path / "t.db"
    exit_code = run(
        ["add-meal", "--name", "Oatmeal", "--calories", "150", "--protein", "5"],
        db_path=db_path,
    )
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "Recorded meal 1" in out
    assert "Oatmeal" in out


def test_add_meal_invalid_input_reports_error_and_nonzero_exit(tmp_path, capsys):
    db_path = tmp_path / "t.db"
    exit_code = run(
        ["add-meal", "--name", "Bad", "--calories", "-5", "--protein", "5"],
        db_path=db_path,
    )
    captured = capsys.readouterr()
    assert exit_code != 0
    assert "Error" in captured.err


def test_delete_meal_success(tmp_path, capsys):
    db_path = tmp_path / "t.db"
    run(["add-meal", "--name", "Oatmeal", "--calories", "150", "--protein", "5"], db_path=db_path)
    exit_code = run(["delete-meal", "--id", "1"], db_path=db_path)
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "Deleted meal 1" in out


def test_delete_meal_unknown_id_reports_error_and_nonzero_exit(tmp_path, capsys):
    db_path = tmp_path / "t.db"
    exit_code = run(["delete-meal", "--id", "999"], db_path=db_path)
    captured = capsys.readouterr()
    assert exit_code != 0
    assert "Error" in captured.err