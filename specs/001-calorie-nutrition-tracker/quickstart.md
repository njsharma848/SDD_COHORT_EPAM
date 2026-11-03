# Quickstart: Calorie and Nutrition Tracker

This guide is for validating the completed feature. It assumes Python 3.12 and pytest are available and the project implementation has been added under `src/`.

## Run Automated Tests

From the project root:

```powershell
python -m pytest
```

Expected result: all unit, storage, service, and CLI tests pass. Tests that write to SQLite use isolated temporary databases and do not alter the user's normal tracker data.

## Run the CLI

From the project root, make the source package available for this PowerShell session and run:

```powershell
$env:PYTHONPATH = "src"
python -m calorie_tracker --help
python -m calorie_tracker add-meal --name "Breakfast" --calories 350.5 --protein 18.2
python -m calorie_tracker set-targets --calories 2000 --protein 120
python -m calorie_tracker progress
```

Expected outcomes:

- Help lists the add-meal, delete-meal, set-targets, and progress commands.
- Adding a valid meal succeeds and reports its generated ID.
- Setting both valid targets succeeds.
- Progress shows the current day's totals, targets, remaining amounts, and statuses; all displayed nutrition values have one decimal place.

The CLI stores local data under the current user's home directory. Use a disposable user profile when manually exercising commands if you do not want to change existing tracker data.

## Validate Key Outcomes

- Add a meal for a past date, then view progress for that date; only that date's meals contribute to its totals.
- View a date with no meals and no target; totals are `0.0` and the output says `no target set`.
- Try a meal above 10,000 kcal or 1,000 g protein, a negative value, or a future meal date; each must fail and leave stored data unchanged.
- Set a target pair, then change it on a later day; progress for a past day retains its earlier target.
- Compare consumed values within and outside the 5 kcal / 1 g tolerances; verify status labels and signed remaining values.

For exact command arguments and expected CLI behavior, see [contracts/cli.md](contracts/cli.md). For persisted fields and validation ranges, see [data-model.md](data-model.md).
