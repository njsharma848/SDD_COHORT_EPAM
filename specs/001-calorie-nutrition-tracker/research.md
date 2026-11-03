# Research: Calorie and Nutrition Tracker

**Baseline**: Spec v1.0, reconciled as recorded in `docs/review-record.md`

## Technology Decisions

### CLI: `argparse`

- **Decision**: Use Python's standard-library `argparse`.
- **Rationale**: The specified surface has four straightforward commands. `argparse` supports subcommands, required flags, help, and parse errors without adding runtime dependencies.
- **Alternatives considered**: Typer provides a more concise declaration style but adds a third-party dependency and no necessary behavior for this small CLI.

### Storage: SQLite via `sqlite3`

- **Decision**: Use the standard-library `sqlite3` module and two compact tables for meals and effective-dated target history.
- **Rationale**: A local embedded database supports persistent records and atomic transactions without a server or ORM. It is suitable for the specified single user.
- **Alternatives considered**: In-memory state would not retain records across runs; flat-file persistence would require custom update and transaction behavior for deletions and target history.

### Exact Decimal Handling

- **Decision**: Parse CLI number text as `decimal.Decimal`, validate precision and bounds, and store integer tenths.
- **Rationale**: Meal and target values have at most one decimal place. Integer tenths keep sums, tolerance comparisons, and remaining amounts exact while using SQLite integer values.
- **Alternatives considered**: SQLite `REAL`/Python `float` can introduce binary representation drift; storing decimal strings complicates arithmetic and ordering.

### Date Representation

- **Decision**: Use `datetime.date` and ISO date strings for meals and target effective dates.
- **Rationale**: The domain is defined by local calendar days, not instants. Date-only values avoid timezone conversion and represent the midnight-to-midnight boundary directly.
- **Alternatives considered**: UTC timestamps add conversion rules not needed by the specification.

### Test Strategy

- **Decision**: Use pytest, with tests for pure validation/calculation, SQLite repository behavior, service workflows, and user-visible CLI results.
- **Rationale**: This covers business rules and failure effects at the relevant boundaries, meeting constitution P-2 and P-3.
- **Alternatives considered**: Standard-library `unittest` would work but pytest is explicitly requested.

## Storage Location

- **Decision**: Place the SQLite file in a fixed application-specific directory under the current user's home directory; do not expose a database-path configuration option.
- **Rationale**: User records are persistent local data and should not be written into or accidentally committed with the source repository. A fixed local path avoids adding configuration surface.
- **Trade-off**: Users do not choose a storage location through the CLI; backup and relocation are outside the current feature scope.

## Open Implementation Questions

No business-rule clarifications remain for the v1.0 baseline. Implementation-specific choice: initialize the minimal schema when opening the database, without adding a general migration system; the project starts with a fresh schema and does not specify deployed-version upgrades.
