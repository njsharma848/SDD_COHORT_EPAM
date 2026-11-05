# Calorie and Nutrition Tracker

A single-user, command-line calorie and nutrition tracker, built
using Spec-Driven Development (SDD) for EPAM's SDD cohort
Assignment 1.

## What it does

- Record a meal (name, calories, protein, date - defaults to today)
- Delete a meal by ID
- Set or change daily calorie and protein targets
- View progress for any day: consumed totals, remaining amounts,
  and an under/met/over status per nutrient

No accounts, no authentication, no micronutrients, no multi-day
history - see `specs/001-calorie-nutrition-tracker/spec.md` for the
full scope.

## Setup

Requires Python 3.12+ and `uv` (https://docs.astral.sh/uv/).

```powershell
uv python pin 3.12
uv sync
```

## Running

```powershell
uv run python -m calorie_tracker add-meal --name "Oatmeal" --calories 350 --protein 12
uv run python -m calorie_tracker set-targets --calories 2000 --protein 150
uv run python -m calorie_tracker progress
uv run python -m calorie_tracker delete-meal --id 1
```

Add `--date YYYY-MM-DD` to `add-meal` or `progress` to target a
specific day (defaults to today). Data is stored in a local SQLite
database at `~/.calorie_tracker/` by default.

## Testing

```powershell
uv run pytest -v
```

87 tests across unit, integration, and CLI layers - see
`docs/traceability-matrix.md` for how every acceptance criterion
maps to its implementing task and test(s).

## Artifact map

| Artifact | Path |
|---|---|
| Constitution | `.specify/memory/constitution.md` |
| Clarification log | `docs/clarification-log.md` |
| Specification | `specs/001-calorie-nutrition-tracker/spec.md` |
| Review record | `docs/review-record.md` |
| Plan | `specs/001-calorie-nutrition-tracker/plan.md` |
| Tasks | `specs/001-calorie-nutrition-tracker/tasks.md` |
| Traceability matrix | `docs/traceability-matrix.md` |
| Prompt log | `docs/prompt-log.md` |
| Source | `src/calorie_tracker/` |
| Tests | `tests/` |

## Tech choices

Python 3.12, `argparse` for the CLI, `sqlite3` for storage, `pytest`
for testing - chosen as the simplest stack that satisfies every
acceptance criterion without unnecessary dependencies (constitution
P-4, Simplicity).

Calories and protein are stored as integers in tenths (e.g. 12.3 kcal
is stored as `123`) rather than floats, to avoid floating-point
rounding drift across repeated arithmetic. Daily targets are stored
with an `effective_date` so that changing a target never rewrites
history - past days keep whatever target was active on them (BR-06).

## Reflection

**One decision:** Progress views for a *future* date are allowed (an
empty day with no meals), while *recording a meal* on a future date
is explicitly rejected (BR-02). This distinction is deliberate and
documented in `plan.md`'s Risks and Trade-offs table - viewing a
future day isn't the same claim as having eaten on it.

**One trade-off:** Target maximums (10,000 kcal / 1,000 g) deliberately
reuse the per-meal maximums rather than defining separate, larger
daily limits. This was confirmed via Spec Kit's own `/speckit.specify`
clarification step (decision `targetLimits=same_as_meals`, logged in
`docs/clarification-log.md` as A-15) rather than invented - but it
also means a user with several very large meals in one day could
plausibly want a target above what any single meal could register,
which this design doesn't accommodate. That's accepted as out of
scope for this assignment's fundamentals-level tracker.

## AI-use statement

This project was built with AI assistance (Claude) throughout the
SDD lifecycle - constitution drafting, specification and
clarification, planning, task breakdown, and implementation. Every
AI-generated artifact was reviewed line by line; genuine defects the
AI introduced (a missing CLI command handler that produced
false-positive tests, a stale "Done when" check copy-pasted from an
unrelated task, spec drift between two documented target-limit
values, and a test that encoded a wrong assumption about target
effective-dates) were caught, diagnosed, and fixed - see
`docs/review-record.md` (R-01 through R-09a) for the full record of
findings and `docs/prompt-log.md` for the prompt-by-prompt history of
what was accepted, modified, or rejected.
