# Quickstart: Calorie and Nutrition Tracker

This guide is for validating the completed feature. It assumes Python 3.12 and pytest are available and the project implementation has been added under `src/`.

## Run Automated Tests

> **Environment note (added during T026 validation):** bare `python`
> is not on PATH in this project's dev environment (the Windows
> Store python alias was disabled during setup, per Phase 0). Use
> `uv run python` in place of `python` for every command below —
> verified working on 2026-11-05 (R-10).

From the project root:

```powershell
uv run python -m pytest
```

Expected result: all unit, storage, service, and CLI tests pass (87/87 as of the last run). Tests that write to SQLite use isolated temporary databases and do not alter the user's normal tracker data.

## Run the CLI

From the project root:

```powershell
uv run python -m calorie_tracker --help
uv run python -m calorie_tracker add-meal --name "Breakfast" --calories 350.5 --protein 18.2
uv run python -m calorie_tracker set-targets --calories 2000 --protein 120
uv run python -m calorie_tracker progress
```

> Note: setting `$env:PYTHONPATH = "src"` is **not** required under
> `uv run` — `uv`'s project environment already resolves the
> `calorie_tracker` package via `pyproject.toml`. Verified by
> clearing PYTHONPATH entirely and re-running successfully (R-11).

Expected outcomes:

- Help lists the add-meal, delete-meal, set-targets, and progress commands.
- Adding a valid meal succeeds and reports its generated ID.
- Setting both valid targets succeeds.
- Progress shows the current day's totals, targets, remaining amounts, and statuses; all displayed nutrition values have one decimal place.

## Validate Key Outcomes

- Add a meal for a past date, then view progress for that date; only that date's meals contribute to its totals.
- View a date with no meals and no target; totals are `0.0` and the output says `no target set`.
- Try a meal above 10,000 kcal or 1,000 g protein, a negative value, or a future meal date; each must fail and leave stored data unchanged.
- Set a target pair, then change it on a later day; progress for a past day retains its earlier target.
- Compare consumed values within and outside the 5 kcal / 1 g tolerances; verify status labels and signed remaining values.

For exact command arguments and expected CLI behavior, see [contracts/cli.md](contracts/cli.md). For persisted fields and validation ranges, see [data-model.md](data-model.md).
