"""CLI tests for set-targets (T016 — Covers: AC-010, AC-011, AC-021)."""

from calorie_tracker.cli import run


def test_set_targets_success_reports_values(tmp_path, capsys):
    db_path = tmp_path / "t.db"
    exit_code = run(["set-targets", "--calories", "2000", "--protein", "150"], db_path=db_path)
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "2000.0 kcal" in out
    assert "150.0 g protein" in out


def test_set_targets_invalid_value_reports_error_and_nonzero_exit(tmp_path, capsys):
    db_path = tmp_path / "t.db"
    exit_code = run(["set-targets", "--calories", "-1", "--protein", "150"], db_path=db_path)
    captured = capsys.readouterr()
    assert exit_code != 0
    assert "Error" in captured.err


def test_set_targets_above_maximum_reports_error_and_nonzero_exit(tmp_path, capsys):
    db_path = tmp_path / "t.db"
    exit_code = run(["set-targets", "--calories", "10000.1", "--protein", "150"], db_path=db_path)
    captured = capsys.readouterr()
    assert exit_code != 0
    assert "Error" in captured.err


def test_set_targets_usable_without_login(tmp_path, capsys):
    # AC-021: works immediately, no prior account/auth setup.
    db_path = tmp_path / "t.db"
    exit_code = run(["set-targets", "--calories", "1800", "--protein", "120"], db_path=db_path)
    assert exit_code == 0