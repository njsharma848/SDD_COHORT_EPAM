# Traceability Matrix

Maps every Acceptance Criterion to its Functional/Business Rule
source, implementing task, and the test(s) that verify it. All
listed tests pass as of the latest full run (87/87, 2026-11-05).

| AC | FR | BR | Task(s) | Test function(s) | Result |
|---|---|---|---|---|---|
| AC-001 | FR-001, FR-002 | BR-01, BR-02 | T008, T010 | `test_tc001_ac001_meal_without_date_defaults_to_today`, `test_tc001_ac001_cli_add_meal_defaults_date_and_reports_id` | PASS |
| AC-002 | FR-002 | BR-02 | T008 | `test_tc002_ac002_meal_recorded_for_past_date`, `test_tc002_ac002_meal_recorded_for_present_date` | PASS |
| AC-003 | FR-002 | BR-02, BR-12 | T008 | `test_tc003_ac003_future_date_rejected_and_data_unchanged` | PASS |
| AC-004 | FR-003 | BR-03 | T008 | `test_tc004_ac004_meal_values_stored_rounded_to_one_decimal` | PASS |
| AC-005 | FR-003 | BR-03 | T008 | `test_tc005_ac005_zero_calories_and_protein_accepted` | PASS |
| AC-006a | FR-004 | BR-03 | T008 | `test_tc006a_ac006a_meal_exactly_at_maximum_accepted` | PASS |
| AC-006b | FR-004 | BR-03, BR-12 | T008 | `test_tc006b_ac006b_meal_above_maximum_rejected_and_data_unchanged` | PASS |
| AC-007 | FR-013 | BR-12 | T008 | `test_tc007_ac007_missing_name_rejected_and_data_unchanged`, `test_tc007_ac007_non_numeric_calories_rejected_and_data_unchanged`, `test_tc007_ac007_negative_protein_rejected_and_data_unchanged`, `test_tc007_ac007_too_many_decimal_places_rejected_and_data_unchanged` | PASS |
| AC-008 | FR-006 | BR-05 | T008 | `test_tc008_ac008_meal_recorded_successfully_with_no_target_set` | PASS |
| AC-009 | FR-005 | BR-04 | T009, T010, T014 | `test_tc009_ac009_delete_known_meal_removes_it_from_totals`, `test_tc009_ac009_delete_unknown_id_reports_error_and_leaves_data_unchanged`, `test_tc009_ac009_cli_delete_meal_removes_it` | PASS |
| AC-010 | FR-006 | BR-05 | T015, T016 | `test_tc010_ac010_set_paired_targets_together`, `test_tc010_ac010_set_paired_targets_at_maximum` | PASS |
| AC-011 | FR-006 | BR-12 | T015 | `test_tc011_ac011_missing_target_value_rejected_and_history_unchanged`, `test_tc011_ac011_negative_target_rejected_and_history_unchanged`, `test_tc011_ac011_above_maximum_target_rejected_and_history_unchanged`, `test_tc011_ac011_too_many_decimal_places_rejected_and_history_unchanged`, `test_tc011_ac011_rejecting_one_field_leaves_prior_valid_target_unchanged` | PASS |
| AC-012 | FR-007 | BR-06 | T015 | `test_tc012_ac012_target_change_preserves_past_effective_dates` | PASS |
| AC-013 | FR-008 | BR-08 | T018, T020 | `test_tc013_ac013_progress_aggregates_only_meals_on_the_selected_date` | PASS |
| AC-014 | FR-009 | BR-08 | T018, T020 | `test_tc014_ac014_zero_totals_on_a_day_with_no_meals` | PASS |
| AC-015 | FR-008, FR-011, FR-012 | BR-10, BR-11 | T018, T020 | `test_tc015_ac015_consumption_exactly_equals_target_is_met_with_zero_remaining` | PASS |
| AC-016 | FR-012 | BR-11 | T018, T020 | `test_tc016_ac016_more_than_tolerance_below_target_is_under` | PASS |
| AC-017 | FR-012 | BR-11 | T018, T020 | `test_tc017_ac017_met_tolerance_boundary_on_the_under_side`, `test_tc017_ac017_met_tolerance_boundary_on_the_over_side` | PASS |
| AC-018 | FR-012 | BR-11 | T018, T020 | `test_tc018_ac018_more_than_tolerance_above_target_is_over` | PASS |
| AC-019 | FR-010 | BR-09 | T018, T020 | `test_tc019_ac019_no_target_shows_consumed_totals_and_no_target_set` | PASS |
| AC-020 | FR-013 | BR-12 | T021 | `test_tc020_ac020_invalid_meal_and_target_inputs_leave_all_data_unchanged`, `test_tc020_ac020_rejecting_a_target_field_leaves_the_prior_target_fully_intact` | PASS |
| AC-021 | FR-014 | NFR: "The feature is limited to one user and a command-line interface." | T010, T014, T016, T019 | `test_tc021_ac021_cli_usable_without_account_or_login`, plus `test_set_targets_usable_without_login`, `test_progress_usable_without_account_or_login` | PASS |



*Note: AC-021 traces to a Non-Functional Requirement/Constraint (spec.md's NFR section) rather than a Business Rule, since the single-user/no-auth guarantee isn't expressed as a numbered BR.*

## Coverage summary

- 22/22 Acceptance Criteria have at least one passing test.
- 87/87 tests passing as of the last full run (`uv run pytest -q`, 2026-11-05).
- Supporting (non-AC-tagged) test files — `test_repository.py`, `test_repository_schema.py`, `test_models.py`, `test_validation.py` — cover the underlying units (repository functions, schema constraints, dataclasses, field-level validation rules) that the AC-tagged acceptance tests build on, satisfying constitution P-2's test-coverage requirement beyond just the acceptance layer.