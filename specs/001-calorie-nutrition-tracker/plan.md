# Implementation Plan: Calorie and Nutrition Tracker

**Branch**: `001-calorie-nutrition-tracker` | **Date**: 2026-11-03 | **Spec**: [spec.md](spec.md)

**Baseline**: Spec v1.0, as recorded in [review-record.md](../../../docs/review-record.md). This plan uses the reviewed daily target limits of 10,000 kcal and 1,000 g protein and the separately testable AC-006a / AC-006b. The working specification was reconciled to that baseline before planning.

## Summary

Build a single-user command-line nutrition tracker using Python 3.12, `argparse`, and SQLite. Keep business behavior in a small service layer, validate all inputs before persistence, store one-decimal nutrition quantities exactly as integer tenths, and retain target history by effective date. The CLI provides meal creation/deletion, paired daily target setting, and progress for one date.

## Technology Choice and Rationale

| Choice | Rationale |
|---|---|
| Python 3.12 | Matches the project's learning scope and supports readable, typed code without a compiled toolchain. |
| Standard library for runtime | `argparse`, `sqlite3`, `decimal`, and `datetime` cover the required CLI, persistence, numeric precision, and local dates without framework or service overhead. |
| `argparse` | Built into Python, conventional for a small command-line program, and sufficient for four commands and their required arguments. Typer would add a dependency without needed capability. |
| SQLite through `sqlite3` | Embedded, local, transactional storage suited to one user's meals and target history; no server or ORM is needed. |
| `pytest` for tests | Matches the requested test runner and supports unit, persistence, service, and CLI behavior tests. It is a development/test dependency only. |

No web framework, ORM, external service, runtime dependency, cache, or configurable infrastructure is planned.

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: Python standard library at runtime; pytest for tests  
**Storage**: SQLite via `sqlite3`  
**Testing**: pytest; tests organized by unit, service/integration, and CLI behavior  
**Target Platform**: Local machine with Python 3.12; standard-library portability  
**Project Type**: Single-user CLI  
**Performance Goals**: Correct daily meal totals and target lookup for personal use; no specific throughput target is required.  
**Constraints**: Local midnight-to-midnight days; no future-dated meals; precise one-decimal values; invalid input must not mutate persisted data.  
**Scale/Scope**: One user; meals and target changes across calendar days; progress is requested for one day at a time.

## Constitution Check

| Principle | Plan compliance |
|---|---|
| P-1 Specification-First | Components and contracts trace to FR-001–FR-014 and BR-01–BR-12. The baseline discrepancy was recorded before aligning the working spec; see `docs/review-record.md`. |
| P-2 Test Coverage | Each acceptance criterion is to receive at least one automated test; test cases will assert observable output and unchanged data on rejected writes. |
| P-3 Safe Failure | Validate all user input before write operations; use a transaction for each mutation; rollback on persistence errors. |
| P-4 Simplicity | One CLI, one SQLite database, small responsibility-focused modules, and standard-library runtime only. |
| P-5 No Secrets | No credentials are required. The local database is stored outside the repository; no secret values or credential configuration are introduced. |
| P-6 Code Standards | Python modules use type hints, PEP 8 style, and single responsibilities. |
| P-7 Transparent AI | This plan and its user clarification are recorded in `docs/prompt-log.md`. |

**Gate**: Pass. The design has no components or runtime dependencies beyond the user-requested scope. The local database location is the user's home directory, keeping personal records outside the repository.

## Components and Responsibilities

| Component | Responsibility |
|---|---|
| `models.py` | Typed value objects for a meal, a target snapshot, and a daily progress result; no persistence or CLI concerns. |
| `validation.py` | Parse and validate meal/target numeric values and dates; produce field-specific validation errors. |
| `repository.py` | Own SQLite connection/schema setup and parameterized reads/writes; expose meal, target-history, and daily-total operations. |
| `service.py` | Coordinate use cases, perform domain calculations, and ensure invalid input is rejected before repository mutation. |
| `cli.py` | Define the `argparse` command/argument surface, invoke services, render concise success/progress output, and convert expected domain errors to clear user messages and non-zero exits. |
| `__main__.py` | Entry point that starts the CLI. |
| `tests/` | Automated tests for validation, repository behavior, business rules, and CLI outcomes. |

The implementation should be a single Python project, organized under `src/calorie_tracker/`. Keep these modules small; do not introduce separate packages or abstractions without a requirement.

## Data Model

The database has two entities. Numeric amounts are persisted as integer tenths to represent exactly one decimal place without binary floating-point drift. See [data-model.md](data-model.md) for field definitions and constraints.

### Meal

- `id`: integer primary identifier, generated by storage.
- `name`: required text.
- `calories_tenths`: integer amount in tenths of kcal; 0 through 100,000 (0.0–10,000.0 kcal).
- `protein_tenths`: integer amount in tenths of grams; 0 through 10,000 (0.0–1,000.0 g).
- `meal_date`: ISO calendar date (`YYYY-MM-DD`), local day with no time component; not later than today's local date.

### Daily target history

- `effective_date`: ISO calendar date (`YYYY-MM-DD`), primary key; target applies from this local day forward until another target becomes effective.
- `calories_tenths`: integer amount in tenths of kcal; 0 through 100,000 (0.0–10,000.0 kcal).
- `protein_tenths`: integer amount in tenths of grams; 0 through 10,000 (0.0–1,000.0 g).

Both target values are stored together, matching the paired target-setting behavior. A subsequent change on the same effective date replaces that date's target; changes on later dates add history and do not rewrite past target periods. Database constraints complement application validation; they are not a substitute for clear user-facing errors.

## CLI Command Surface

Use one executable entry point with these commands:

| Command | Arguments | Behavior |
|---|---|---|
| `add-meal` | `--name`, `--calories`, `--protein`; optional `--date YYYY-MM-DD` | Record a meal; omitted date defaults to today's local date. |
| `delete-meal` | `--id` | Delete the meal with the given ID; unknown ID returns a clear error. |
| `set-targets` | `--calories`, `--protein` | Set/change both targets together, effective from today's local date. |
| `progress` | optional `--date YYYY-MM-DD` | Display consumed totals and, when available, the target, signed remaining amounts, and statuses for the selected date; defaults to today. |

The command names and argument labels are user-facing contract choices for this plan; no command is provided for editing meals or multi-day reports.

## Processing Sequences

### A. Recording a Meal

1. `argparse` reads the required name/calories/protein and optional date; omitted date resolves to `date.today()` in local system time.
2. The validation layer rejects missing or malformed values, non-numeric amounts, values below zero, more than one decimal place, amounts above 10,000 kcal / 1,000 g, malformed dates, and future dates.
3. Convert accepted `Decimal` amounts to integer tenths; do not use binary floating-point for validation or arithmetic.
4. The service passes the fully validated meal to the repository.
5. The repository inserts the meal in a transaction and commits only on success; any persistence failure rolls back.
6. The CLI reports success and the assigned meal ID, or presents a clear error with non-zero exit status. Rejected input leaves stored data unchanged. See AC-001–AC-008.

### B. Setting or Changing Targets

1. `argparse` requires both calorie and protein target values.
2. Validate both values completely before any write: numeric, non-negative, no more than one decimal place, and no greater than 10,000 kcal / 1,000 g.
3. Resolve the effective date as today's local date and convert both values to integer tenths.
4. In one transaction, insert the target-history row for today or replace the row for today if one already exists.
5. Commit both values together; on validation or storage failure, preserve the previous target history and report an error.
6. Report successful target values in one-decimal format. Earlier effective dates remain unchanged. See AC-010–AC-012.

### C. Viewing Progress for a Day

1. Parse the optional date as an ISO calendar date; default to today's local date.
2. Query the sum of meal calories/protein for exactly that date, returning zero totals when no meal rows match.
3. Query the latest target with `effective_date` less than or equal to the selected date.
4. If no target is found, render the totals and “no target set”; omit remaining values and statuses.
5. Otherwise calculate signed remaining values as target minus consumed amount, and derive each status using its nutrient-specific tolerance.
6. Render totals, target, remaining amounts, and status labels to one decimal place. This flow is read-only. See AC-013–AC-019.

### Meal Deletion

1. Parse the meal ID and ask the repository to delete that row in a transaction.
2. If exactly one row is deleted, commit and report success.
3. If no row matches, roll back/no-op, report a clear unknown-ID error, and leave all stored data unchanged. See AC-009.

## Test Coverage Outline

Tests should be traceable by acceptance criterion ID and verify output plus persistence effects as applicable:

| Test area | Acceptance criteria |
|---|---|
| CLI input, date defaulting, valid past/today and rejected future date, zero values, and no-account use | AC-001, AC-002, AC-003, AC-005, AC-021 |
| Meal precision, boundaries, and rejected input | AC-004, AC-006a, AC-006b, AC-007, AC-020 |
| Meal deletion and logging without targets | AC-008, AC-009 |
| Paired targets, target validation, and historical effective dates | AC-010, AC-011, AC-012 |
| Selected-day totals, empty-day output, target/no-target rendering | AC-013, AC-014, AC-019 |
| Remaining amount and status calculations, including tolerance edges | AC-015, AC-016, AC-017, AC-018 |

Each test for a rejected mutation must assert that the affected prior database state is unchanged.

## Data Handling and Calculations

### Dates and Local Day Boundary

- Use `datetime.date.today()` to determine today's date in local system time.
- Parse and persist dates as calendar dates in ISO form (`YYYY-MM-DD`); do not attach UTC offsets or timestamps to meals or target-effective dates.
- Date-only meal entries naturally belong to the local midnight-to-midnight day defined by BR-07.
- Reject a meal date greater than today's local date. The progress command selects one date and sums only meals with an equal date.
- A target set today is effective for today and later days. Lookup uses the greatest effective date not later than the selected day, preserving historical target behavior.

### Decimal Precision and Display

- Parse numeric CLI values using `decimal.Decimal` from their text representation.
- Reject values with more than one fractional decimal digit rather than silently truncating or rounding invalid input.
- Convert valid values to integer tenths (for example, 12.3 becomes 123 tenths); format output by dividing by ten and displaying exactly one decimal digit.
- Sum integer tenths in SQLite/Python. This prevents floating-point accumulation errors and preserves exact one-decimal totals.

### “Met” Tolerance

For each nutrient, calculate `difference = consumed_tenths - target_tenths`. Calories use a tolerance of 50 tenths (5.0 kcal); protein uses 10 tenths (1.0 g).

- `met` when `abs(difference) <= tolerance`
- `under` when `difference < -tolerance`
- `over` when `difference > tolerance`

Remaining amount is independently `target_tenths - consumed_tenths`; therefore it remains a signed amount even when a small over-target difference is classified as “met.” This matches BR-10 and BR-11.

## Error Handling

Expected input/domain errors are caught at the CLI boundary, shown in clear field-specific language on stderr, and return a non-zero exit code. Validation completes before writes. Repository mutations use transactions; failures roll back. “Unchanged” means no persisted meals or target history are added, removed, or altered.

| Condition | Detection point | User-facing response | Effect on stored data | Related AC |
|---|---|---|---|---|
| Missing required meal name/value or either target | CLI argument validation / service validation | Identify the missing field and state that the operation was not completed. | unchanged | AC-007, AC-011, AC-020 |
| Non-numeric meal or target amount | Validation layer | Identify the field and require a numeric value. | unchanged | AC-007, AC-011, AC-020 |
| Negative meal amount or target | Validation layer | State that the value must be zero or greater. | unchanged | AC-007, AC-011, AC-020 |
| More than one decimal place | Validation layer | State that at most one decimal place is accepted. | unchanged | AC-007, AC-011, AC-020 |
| Meal amount above 10,000 kcal or 1,000 g | Validation layer; database constraint as defense in depth | State the applicable per-meal maximum. | unchanged | AC-006b, AC-020 |
| Target above 10,000 kcal or 1,000 g | Validation layer; database constraint as defense in depth | State the applicable target maximum. | unchanged | AC-011, AC-020 |
| Malformed meal/progress date | Date validation | State that the date must be a valid `YYYY-MM-DD` calendar date. | unchanged | AC-002, AC-013 |
| Future meal date | Date validation | State that meal dates may not be in the future. | unchanged | AC-003, AC-020 |
| Unknown meal ID | Repository result checked by service | State that no meal exists for that ID. | unchanged | AC-009 |
| SQLite or other storage failure during mutation | Repository transaction boundary | Report that the operation failed and data was not changed; include no raw traceback in normal CLI output. | unchanged (transaction rolled back) | — (operational failure; no dedicated AC) |

## Functional Requirement to Component Mapping

| Requirement | Responsible component(s) |
|---|---|
| FR-001 | CLI, validation, service, repository, Meal model |
| FR-002 | CLI, validation, service |
| FR-003 | Validation, service, repository, display formatter |
| FR-004 | Validation, repository constraints |
| FR-005 | CLI, service, repository |
| FR-006 | CLI, validation, service, repository, target model |
| FR-007 | Service, repository target-history lookup |
| FR-008 | CLI, service, repository, progress model |
| FR-009 | Repository daily aggregation, service, CLI |
| FR-010 | Service, CLI |
| FR-011 | Service progress calculation, CLI formatter |
| FR-012 | Service progress calculation, CLI formatter |
| FR-013 | Validation, service, repository transaction handling, CLI error rendering |
| FR-014 | CLI entry point and command parser |

## Risks and Trade-offs

| Risk / trade-off | Mitigation or accepted consequence |
|---|---|
| Integer tenths are less immediately readable than decimal values in storage. | Keep conversion centralized in validation/formatting and name columns with `_tenths`; exact arithmetic is preferable to float drift. |
| Local system date/time changes can affect what “today” means. | Use the local date consistently as specified by BR-07; timezone selection and travel synchronization are out of scope. |
| SQLite is a single-user local store and does not provide multi-user synchronization. | This is an intentional match for the single-user requirement; shared access and accounts are excluded. |
| A local database can be deleted or copied accidentally. | Store it under the user's home directory rather than the repository; backup/restore behavior is not specified and remains out of scope. |
| `argparse` has less concise declaration syntax than a third-party CLI library. | Its built-in availability and sufficient command surface reduce dependencies and setup. |
| Target edits on the same date replace that date's target row. | The spec requires the target active for that day and future, not intra-day target revisions; one effective target per calendar date is sufficient. |
| Future dates may be requested for read-only progress, while future meal dates are expressly rejected. | Keep validation rule-specific: reject future meal dates; do not add a future-progress restriction absent from the specification. |

## Project Structure

```text
src/
└── calorie_tracker/
    ├── __init__.py
    ├── __main__.py
    ├── cli.py
    ├── models.py
    ├── repository.py
    ├── service.py
    └── validation.py

tests/
├── unit/
├── integration/
└── cli/
```

**Structure Decision**: One small Python CLI project under `src/calorie_tracker/`, with focused tests grouped by validation/business logic, SQLite-backed service behavior, and observable CLI behavior.

## Design Artifacts

- [Research decisions](research.md)
- [Data model](data-model.md)
- [CLI contract](contracts/cli.md)
- [Quickstart validation guide](quickstart.md)

## Constitution Check (Post-Design)

The design continues to pass P-1 through P-7: every module has a direct requirement, validation precedes mutations, writes are transactional, the runtime uses only the standard library, the scope remains single-user CLI, and test/AI traceability is planned. No constitution violation requires a complexity exception.
