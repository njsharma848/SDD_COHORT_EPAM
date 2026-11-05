# Tasks: Calorie and Nutrition Tracker

**Input**: Design documents in `specs/001-calorie-nutrition-tracker/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/cli.md`, `quickstart.md`

**Traceability convention**: Each task explicitly names covered acceptance criteria or supporting constitution principles. “Done when” is a concrete completion check. AC tests use names beginning with `test_tc###_ac###_...` to follow constitution P-2.

## Phase 1: Setup

**Purpose**: Establish only the Python package and test environment required by the plan.

- [x] T001 [P] Create `src/calorie_tracker/`, `tests/unit/`, `tests/integration/`, `tests/cli/`, and `screenshots/` with package initializers where needed; keep the implementation a single standard-library CLI package.  
  **Supports**: P-4, P-6  
  **Done when**: All listed directories exist and `src/calorie_tracker/__init__.py` imports under Python 3.12.

- [x] T002 Add the minimal Python project and pytest configuration in `pyproject.toml`, declaring Python 3.12 and pytest as a test-only dependency with no runtime dependencies.  
  **Supports**: P-4, P-6  
  **Done when**: `uv run pytest --version` succeeds and the project metadata declares no runtime dependencies.

## Phase 2: Foundational Models and Persistence

**Purpose**: Establish the shared domain and SQLite foundations before implementing user flows.

- [x] T003 Define typed Meal, Target, and DailyProgress value models in `src/calorie_tracker/models.py`, using integer tenths and local ISO dates as specified in `data-model.md`; add focused model tests in `tests/unit/test_models.py`.  
  **Covers**: AC-001, AC-004, AC-010, AC-013, AC-015  
  **Done when**: `uv run pytest tests/unit/test_models.py` passes model construction and type/value checks.

- [x] T004 Implement SQLite initialization and the meals/target-history tables in `src/calorie_tracker/repository.py`, including primary keys and range checks for 0–100,000 calorie tenths and 0–10,000 protein tenths; add schema tests in `tests/integration/test_repository_schema.py`. Store the database under the user's home directory, not in the repository.  
  **Covers**: AC-001, AC-006a, AC-010, AC-012  
  **Supports**: P-5  
  **Done when**: `uv run pytest tests/integration/test_repository_schema.py` verifies schema creation, constraints, and the resolved database path is outside the repository.

- [x] T005 Implement parameterized SQLite meal insert/delete, daily aggregate, and effective-target lookup operations in `src/calorie_tracker/repository.py`; add repository tests in `tests/integration/test_repository.py`. Each mutation must use a transaction and roll back on failure.  
  **Covers**: AC-009, AC-012, AC-013, AC-014, AC-020  
  **Done when**: `uv run pytest tests/integration/test_repository.py` passes insert, delete, date-filter, target-history, and rollback checks.

- [x] T006 Implement typed validation errors and reusable numeric/date validation in `src/calorie_tracker/validation.py`; add field-level unit tests in `tests/unit/test_validation.py`. Use `Decimal`; reject missing/non-numeric, negative, more-than-one-decimal-place, above-maximum values (meal/target limits: 10,000 kcal and 1,000 g protein), invalid dates, and future meal dates before any write.  
  **Covers**: AC-003, AC-006b, AC-007, AC-011, AC-020  
  **Supports**: P-3  
  **Done when**: `uv run pytest tests/unit/test_validation.py` passes the field-level valid, boundary, and invalid input cases.

- [x] T007 Implement shared service/domain error types in `src/calorie_tracker/service.py` so validation failures, unknown meal IDs, and persistence failures can be reported clearly without leaking tracebacks.  
  **Supports**: P-3, P-4, P-5  
  **Done when**: `uv run python -m compileall src/calorie_tracker/service.py` succeeds; error-type behavior (clear messages, no traceback leakage, unchanged data on rejection) is verified by T012, T017, and T021's rejection test cases.

## Phase 3: User Story 1 — Record and Remove Meals (Priority: P1)

**Goal**: Record a valid meal (defaulting to today when date is omitted), and delete a meal by its ID.

**Independent Test**: Use the CLI to add a meal, verify its ID and date/values in progress, then delete it and verify it no longer contributes to the day's totals.

### Implementation

- [x] T008 [US1] Implement meal creation in `src/calorie_tracker/service.py`: validate all fields before persistence, default the date to local today, convert valid one-decimal amounts to integer tenths, and return the new ID.  
  **Covers**: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006a, AC-006b, AC-007, AC-008  
  **Supports**: P-3  
  **Done when**: `uv run python -m compileall src/calorie_tracker/service.py` succeeds; acceptance behavior is verified in T011–T012.

- [x] T009 [US1] Implement meal deletion in `src/calorie_tracker/service.py`, raising a clear domain error when the repository finds no matching ID.  
  **Covers**: AC-009  
  **Supports**: P-3  
  **Done when**: `uv run python -m compileall src/calorie_tracker/service.py` succeeds; deletion behavior is verified in T013–T014.

- [x] T010 [US1] Add the `add-meal` and `delete-meal` argparse commands, required flags, optional `--date`, success messages including the assigned meal ID, and clear non-zero error responses in `src/calorie_tracker/cli.py` and `src/calorie_tracker/__main__.py`.  
  **Covers**: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006a, AC-006b, AC-007, AC-008, AC-009, AC-021  
  **Done when**: `uv run python -m calorie_tracker --help` lists both commands and `uv run pytest tests/cli/test_meal_commands.py` passes.

### Automated Acceptance Tests

- [x] T011 [US1] Add acceptance tests named `test_tc001_ac001_...`, `test_tc002_ac002_...`, `test_tc004_ac004_...`, and `test_tc005_ac005_...` in `tests/integration/test_meal_acceptance.py` for today's default, valid past/today dates, precision, and zero inputs.  
  **Covers**: AC-001, AC-002, AC-004, AC-005  
  **Done when**: `uv run pytest tests/integration/test_meal_acceptance.py -k 'tc001 or tc002 or tc004 or tc005'` passes.

- [x] T012 [US1] Add tests named `test_tc003_ac003_...`, `test_tc006a_ac006a_...`, `test_tc006b_ac006b_...`, `test_tc007_ac007_...`, and `test_tc008_ac008_...` in `tests/integration/test_meal_acceptance.py`; cover future dates, meal boundaries, invalid input, and logging without a target, asserting data is unchanged after rejection.  
  **Covers**: AC-003, AC-006a, AC-006b, AC-007, AC-008  
  **Supports**: P-3  
  **Done when**: `uv run pytest tests/integration/test_meal_acceptance.py -k 'tc003 or tc006a or tc006b or tc007 or tc008'` passes.

- [x] T013 [US1] Add deletion tests named `test_tc009_ac009_...` in `tests/integration/test_meal_acceptance.py` for deleting a known ID and rejecting an unknown ID without modifying records.  
  **Covers**: AC-009  
  **Supports**: P-3  
  **Done when**: `uv run pytest tests/integration/test_meal_acceptance.py -k tc009` passes.

- [x] T014 [US1] Add CLI tests named `test_tc001_ac001_cli_...`, `test_tc009_ac009_cli_...`, and `test_tc021_ac021_...` in `tests/cli/test_meal_commands.py` for add, delete, and use without login/account setup.  
  **Covers**: AC-001, AC-009, AC-021  
  **Done when**: `uv run pytest tests/cli/test_meal_commands.py` passes with no account or authentication setup.

## Phase 4: User Story 2 — Set Daily Targets (Priority: P1)

**Goal**: Set or change calorie and protein targets together and preserve past target history.

**Independent Test**: Set a valid target pair, view progress for its effective day, change it on a later day, and verify progress on the earlier date retains its prior target.

### Implementation

- [x] T015 [US2] Implement paired target validation and effective-date upsert in `src/calorie_tracker/service.py` and `src/calorie_tracker/repository.py`; validate both values before mutation, use local today, and retain prior effective dates.  
  **Covers**: AC-010, AC-011, AC-012  
  **Supports**: P-3  
  **Done when**: `uv run python -m compileall src/calorie_tracker/service.py src/calorie_tracker/repository.py` succeeds; acceptance behavior is verified in T017.

- [x] T016 [US2] Add the `set-targets` command with required `--calories` and `--protein` flags, clear output, non-zero validation/storage failure handling, and command tests in `src/calorie_tracker/cli.py` and `tests/cli/test_target_commands.py`.  
  **Covers**: AC-010, AC-011, AC-021  
  **Done when**: `uv run pytest tests/cli/test_target_commands.py` passes valid paired target and invalid-value cases in the same file.

### Automated Acceptance Tests

- [x] T017 [US2] Add target acceptance tests named `test_tc010_ac010_...`, `test_tc011_ac011_...`, and `test_tc012_ac012_...` in `tests/integration/test_target_acceptance.py`; assert rejected partial/invalid target input leaves the target history unchanged.  
  **Covers**: AC-010, AC-011, AC-012  
  **Supports**: P-3  
  **Done when**: `uv run pytest tests/integration/test_target_acceptance.py` passes all paired target, bound, precision, and historical-effective-date cases.

## Phase 5: User Story 3 — View Daily Progress (Priority: P1)

**Goal**: View consumed totals for one local calendar day and, when available, the applicable target comparison.

**Independent Test**: View a selected date with and without meals/targets, then verify totals, remaining values, and tolerance-based statuses.

### Implementation

- [x] T018 [US3] Implement progress calculation in `src/calorie_tracker/service.py`: aggregate only the selected date, default to local today, look up the latest effective target, calculate signed remaining tenths, and apply calorie/protein tolerances of 50/10 tenths.  
  **Covers**: AC-013, AC-014, AC-015, AC-016, AC-017, AC-018, AC-019  
  **Done when**: `uv run python -m compileall src/calorie_tracker/service.py` succeeds; acceptance behavior is verified in T020.

- [x] T019 [US3] Add the `progress` argparse command and CLI tests; render one-decimal totals, show `no target set` without remaining/status when no target applies, otherwise show target, signed remaining, and each status in `src/calorie_tracker/cli.py` and `tests/cli/test_progress_command.py`.  
  **Covers**: AC-013, AC-014, AC-015, AC-016, AC-017, AC-018, AC-019  
  **Done when**: `uv run pytest tests/cli/test_progress_command.py` passes targeted-date, no-meal/no-target, and target progress output tests in that file.

### Automated Acceptance Tests

- [x] T020 [US3] Add progress acceptance tests named `test_tc013_ac013_...` through `test_tc019_ac019_...` in `tests/integration/test_progress_acceptance.py`, including exact target, both sides of both tolerance boundaries, and over-target negative remaining values.  
  **Covers**: AC-013, AC-014, AC-015, AC-016, AC-017, AC-018, AC-019  
  **Done when**: `uv run pytest tests/integration/test_progress_acceptance.py` passes all selected-day and progress calculation cases.

## Phase 6: Cross-Cutting Validation, Documentation, and Evidence

**Purpose**: Complete acceptance coverage and the project's required learning/demonstration artifacts.

- [x] T021 Add the end-to-end safe-failure test `test_tc020_ac020_rejected_mutations_leave_all_data_unchanged` in `tests/integration/test_safe_failure.py`, covering rejected meal creation, target setting, and unknown deletion with pre-existing records.  
  **Covers**: AC-020  
  **Supports**: P-3  
  **Done when**: `uv run pytest tests/integration/test_safe_failure.py` confirms errors are clear and meals/targets remain unchanged.

- [x] T022 Build `docs/traceability-matrix.md` mapping every AC-001 through AC-021 (with AC-006a and AC-006b replacing AC-006) to its automated test name and mapping FR-001 through FR-014 to the implementing module/task.  
  **Covers**: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006a, AC-006b, AC-007, AC-008, AC-009, AC-010, AC-011, AC-012, AC-013, AC-014, AC-015, AC-016, AC-017, AC-018, AC-019, AC-020, AC-021  
  **Supports**: P-1, P-2  
  **Done when**: The matrix contains exactly 22 acceptance-criterion rows, all with test links, and all 14 FR IDs have a component mapping.

- [ ] T023 Write the root `README.md` with the project purpose, Python/uv setup, test command, CLI command examples, and expected behavior linked to `specs/001-calorie-nutrition-tracker/contracts/cli.md` and `quickstart.md`; do not document out-of-scope capabilities.  
  **Covers**: AC-001, AC-009, AC-010, AC-013, AC-021  
  **Supports**: P-1, P-4, P-6  
  **Done when**: Every command documented in `README.md` matches the CLI contract and the setup/test instructions in `specs/001-calorie-nutrition-tracker/quickstart.md`.

- [ ] T024 Write `docs/validation-plan.md` with a field-by-field invalid/boundary test checklist and unchanged-data assertion for each rejected mutation, linked to the validation and integration tests.  
  **Covers**: AC-003, AC-006b, AC-007, AC-011, AC-020  
  **Supports**: P-3  
  **Done when**: Every invalid condition in BR-12 has a named automated test and an explicit persisted-data unchanged check.

- [ ] T025 Run the full test suite and save the exact command and successful output as `screenshots/test-run-output.txt`; capture a CLI demo showing add, set-targets, progress, and delete in `screenshots/cli-demo.png`.  
  **Covers**: AC-001, AC-009, AC-010, AC-013, AC-021  
  **Supports**: P-2, P-7  
  **Done when**: `uv run pytest` exits successfully, `screenshots/test-run-output.txt` records that run, and the CLI demo visibly shows the four required commands with successful outcomes.

- [ ] T026 Complete the quickstart validation from `specs/001-calorie-nutrition-tracker/quickstart.md` and record any deviations in `docs/prompt-log.md`; make no scope changes without updating the spec and review record first.  
  **Covers**: AC-001, AC-003, AC-009, AC-010, AC-012, AC-013, AC-017, AC-018, AC-019, AC-020  
  **Supports**: P-1, P-7  
  **Done when**: Every quickstart scenario has a recorded pass result and any AI-assisted changes are logged with prompt, output, decision, and reasoning in `docs/prompt-log.md`.

## Acceptance-Criterion Coverage Check

All 22 criteria are assigned at least one task:

| Criterion | Task(s) |
|---|---|
| AC-001 | T003, T004, T008, T010, T011, T022, T023, T025, T026 |
| AC-002 | T008, T010, T011, T022 |
| AC-003 | T006, T008, T010, T012, T022, T024, T026 |
| AC-004 | T003, T008, T010, T011, T022 |
| AC-005 | T010, T011, T022 |
| AC-006a | T004, T008, T010, T012, T022 |
| AC-006b | T006, T008, T010, T012, T022, T024 |
| AC-007 | T006, T008, T012, T022, T024 |
| AC-008 | T008, T012, T022 |
| AC-009 | T005, T009, T010, T013, T022, T023, T025, T026 |
| AC-010 | T003, T004, T015, T016, T017, T022, T023, T025, T026 |
| AC-011 | T006, T015, T016, T017, T022, T024 |
| AC-012 | T005, T015, T017, T022, T026 |
| AC-013 | T005, T018, T019, T020, T022, T023, T025, T026 |
| AC-014 | T005, T018, T019, T020, T022 |
| AC-015 | T003, T018, T019, T020, T022 |
| AC-016 | T018, T019, T020, T022 |
| AC-017 | T018, T019, T020, T022, T026 |
| AC-018 | T018, T019, T020, T022, T026 |
| AC-019 | T018, T019, T020, T022, T026 |
| AC-020 | T005, T006, T012, T017, T021, T022, T024, T026 |
| AC-021 | T010, T014, T016, T022, T023, T025 |

**Coverage result**: 22/22 acceptance criteria covered. No task is untraced; every task names at least one AC or constitution principle.

## Dependencies and Execution Order

### Phase Dependencies

- Setup (Phase 1) precedes all implementation.
- Foundational (Phase 2) follows setup and provides models, persistence, validation, and local error/path handling.
- User Stories 1–3 follow the foundation; story phases are sequenced by user-facing flow, with targets before progress because progress consumes target history.
- Cross-cutting docs/evidence follow working CLI flows and acceptance tests.

### User Story Dependencies

- **US1 — Record and Remove Meals**: Begins after foundational tasks. Its tests and CLI can be completed independently after meal services.
- **US2 — Set Daily Targets**: Begins after foundational tasks; target persistence is separate but shares validation and CLI infrastructure.
- **US3 — View Daily Progress**: Depends on the repository and service foundations and is most meaningful after meal and target flows are available.

### Parallel Opportunities

- T001 and T002 may run in parallel.
- After setup, T003 and initial test-directory scaffolding in T001 are independent.
- After shared repository foundation, US1 and US2 implementation/tests can be worked on in parallel; the plan lists them sequentially for learning flow.
- Story acceptance test tasks T011–T014, T017, and T020 may be split by test file after the corresponding CLI/service contracts are fixed.
- T022 (matrix skeleton) and T023 (README draft) can be started independently once the CLI contract is stable.
- Evidence capture T025 must wait until all implementation and tests are complete.

## Suggested MVP

Complete Phase 1, Phase 2, and Phase 3 (US1) first. This provides meal capture and deletion, which are the smallest independently useful slice. Then implement US2 targets and US3 progress before considering the feature complete.

## Task Format Validation

Every implementation task has a checkbox, sequential ID, exact file path, and a concrete “Done when” check. Story-phase tasks carry a `[US#]` label; setup, foundational, and polish tasks do not. Every task includes `Covers:` and/or `Supports:` traceability.
