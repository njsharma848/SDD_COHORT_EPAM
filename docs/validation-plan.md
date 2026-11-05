# Validation Plan

**Note on process:** this plan was assembled after implementation,
by cataloguing the acceptance tests actually written during T008–T021,
rather than fully upfront before coding (the ideal Phase-8 order).
Each row below reflects a real test that has run and passed — not a
planned/未written case.

Legend: N = Normal, I = Invalid, B = Boundary, E = Edge.

| TC-ID | AC | Type | Input | Expected outcome | Test ref | Actual | Result |
|---|---|---|---|---|---|---|---|
| TC-001 | AC-001 | N | Meal name/calories/protein, no date | Recorded with today's local date | `test_meal_acceptance.py::test_tc001_ac001_meal_without_date_defaults_to_today` | Recorded with today's date | PASS |
| TC-001-CLI | AC-001 | N | Same, via CLI `add-meal` | Prints meal ID and today's date | `test_meal_commands.py::test_tc001_ac001_cli_add_meal_defaults_date_and_reports_id` | ID and date printed | PASS |
| TC-002a | AC-002 | N | Meal with a past date | Recorded for that past date | `test_meal_acceptance.py::test_tc002_ac002_meal_recorded_for_past_date` | Recorded correctly | PASS |
| TC-002b | AC-002 | N | Meal with today's date | Recorded for today | `test_meal_acceptance.py::test_tc002_ac002_meal_recorded_for_present_date` | Recorded correctly | PASS |
| TC-003 | AC-003 | I | Meal with a future date | Clear error, no data change | `test_meal_acceptance.py::test_tc003_ac003_future_date_rejected_and_data_unchanged` | Rejected, unchanged | PASS |
| TC-004 | AC-004 | B | Calories/protein with 1 decimal place | Stored/displayed rounded to 1 decimal | `test_meal_acceptance.py::test_tc004_ac004_meal_values_stored_rounded_to_one_decimal` | Rounded correctly | PASS |
| TC-005 | AC-005 | E | Calories = 0, protein = 0 | Accepted | `test_meal_acceptance.py::test_tc005_ac005_zero_calories_and_protein_accepted` | Accepted | PASS |
| TC-006a | AC-006a | B | Calories = 10,000, protein = 1,000 (exact max) | Accepted | `test_meal_acceptance.py::test_tc006a_ac006a_meal_exactly_at_maximum_accepted` | Accepted | PASS |
| TC-006b | AC-006b | B/I | Calories or protein above max | Rejected, no data change | `test_meal_acceptance.py::test_tc006b_ac006b_meal_above_maximum_rejected_and_data_unchanged` | Rejected, unchanged | PASS |
| TC-007a | AC-007 | I | Missing meal name | Clear error, no data change | `test_meal_acceptance.py::test_tc007_ac007_missing_name_rejected_and_data_unchanged` | Rejected, unchanged | PASS |
| TC-007b | AC-007 | I | Non-numeric calories (`"abc"`) | Clear error, no data change | `test_meal_acceptance.py::test_tc007_ac007_non_numeric_calories_rejected_and_data_unchanged` | Rejected, unchanged | PASS |
| TC-007c | AC-007 | I | Negative protein | Clear error, no data change | `test_meal_acceptance.py::test_tc007_ac007_negative_protein_rejected_and_data_unchanged` | Rejected, unchanged | PASS |
| TC-007d | AC-007 | I | Value with 2+ decimal places | Clear error, no data change | `test_meal_acceptance.py::test_tc007_ac007_too_many_decimal_places_rejected_and_data_unchanged` | Rejected, unchanged | PASS |
| TC-008 | AC-008 | N | Valid meal, no target ever set | Meal recorded successfully | `test_meal_acceptance.py::test_tc008_ac008_meal_recorded_successfully_with_no_target_set` | Recorded | PASS |
| TC-009a | AC-009 | N | Delete a known meal ID | Removed; excluded from totals | `test_meal_acceptance.py::test_tc009_ac009_delete_known_meal_removes_it_from_totals` | Removed, totals updated | PASS |
| TC-009b | AC-009 | I | Delete an unknown meal ID | Clear error, no data change | `test_meal_acceptance.py::test_tc009_ac009_delete_unknown_id_reports_error_and_leaves_data_unchanged` | Rejected, unchanged | PASS |
| TC-009c | AC-009 | N | CLI `delete-meal` on known ID | Confirms deletion | `test_meal_commands.py::test_tc009_ac009_cli_delete_meal_removes_it` | Deleted | PASS |
| TC-010a | AC-010 | N | Valid calorie + protein target together | Both accepted, rounded, effective immediately | `test_target_acceptance.py::test_tc010_ac010_set_paired_targets_together` | Accepted | PASS |
| TC-010b | AC-010 | B | Target at exact maximum (10,000/1,000) | Accepted | `test_target_acceptance.py::test_tc010_ac010_set_paired_targets_at_maximum` | Accepted | PASS |
| TC-011a | AC-011 | I | Missing target value | Clear error, history unchanged | `test_target_acceptance.py::test_tc011_ac011_missing_target_value_rejected_and_history_unchanged` | Rejected, unchanged | PASS |
| TC-011b | AC-011 | I | Negative target | Clear error, history unchanged | `test_target_acceptance.py::test_tc011_ac011_negative_target_rejected_and_history_unchanged` | Rejected, unchanged | PASS |
| TC-011c | AC-011 | B/I | Target above maximum | Clear error, history unchanged | `test_target_acceptance.py::test_tc011_ac011_above_maximum_target_rejected_and_history_unchanged` | Rejected, unchanged | PASS |
| TC-011d | AC-011 | I | Target with 2+ decimal places | Clear error, history unchanged | `test_target_acceptance.py::test_tc011_ac011_too_many_decimal_places_rejected_and_history_unchanged` | Rejected, unchanged | PASS |
| TC-011e | AC-011 | E | One field invalid, one valid, submitted together | Whole operation rejected; prior target untouched | `test_target_acceptance.py::test_tc011_ac011_rejecting_one_field_leaves_prior_valid_target_unchanged` | Rejected, prior target intact | PASS |
| TC-012 | AC-012 | N | Target changed after a past day already had one | Past day keeps its old target; new target applies from change day forward | `test_target_acceptance.py::test_tc012_ac012_target_change_preserves_past_effective_dates` | Correct history preserved | PASS |
| TC-013 | AC-013 | N | Meals on multiple dates; view one date | Totals include only that date's meals | `test_progress_acceptance.py::test_tc013_ac013_progress_aggregates_only_meals_on_the_selected_date` | Correct aggregation | PASS |
| TC-014 | AC-014 | E | No meals on selected day | Consumed totals shown as zero | `test_progress_acceptance.py::test_tc014_ac014_zero_totals_on_a_day_with_no_meals` | Zero totals | PASS |
| TC-015 | AC-015 | B | Consumption exactly equals target | Zero remaining, "met" for both nutrients | `test_progress_acceptance.py::test_tc015_ac015_consumption_exactly_equals_target_is_met_with_zero_remaining` | Met, zero remaining | PASS |
| TC-016 | AC-016 | N | Consumption more than tolerance below target | Positive remaining, "under" status | `test_progress_acceptance.py::test_tc016_ac016_more_than_tolerance_below_target_is_under` | Under, positive remaining | PASS |
| TC-017a | AC-017 | B | Consumption exactly 5 kcal / 1 g below target | "met" status (inclusive boundary) | `test_progress_acceptance.py::test_tc017_ac017_met_tolerance_boundary_on_the_under_side` | Met | PASS |
| TC-017b | AC-017 | B | Consumption exactly 5 kcal / 1 g above target | "met" status (inclusive boundary) | `test_progress_acceptance.py::test_tc017_ac017_met_tolerance_boundary_on_the_over_side` | Met | PASS |
| TC-018 | AC-018 | N | Consumption more than tolerance above target | Negative remaining, "over" status | `test_progress_acceptance.py::test_tc018_ac018_more_than_tolerance_above_target_is_over` | Over, negative remaining | PASS |
| TC-019 | AC-019 | E | No target set for selected day | Consumed totals + "no target set"; no remaining/status | `test_progress_acceptance.py::test_tc019_ac019_no_target_shows_consumed_totals_and_no_target_set` | "No target set" shown | PASS |
| TC-020a | AC-020 | I/E | Battery of 10 different invalid meal/target/delete operations | All rejected; entire data state (both days' totals, target) unchanged | `test_safe_failure.py::test_tc020_ac020_invalid_meal_and_target_inputs_leave_all_data_unchanged` | State unchanged throughout | PASS |
| TC-020b | AC-020 | I/E | Set-targets with one invalid field after a valid target already exists | Rejected; prior target fully intact | `test_safe_failure.py::test_tc020_ac020_rejecting_a_target_field_leaves_the_prior_target_fully_intact` | Prior target intact | PASS |
| TC-021 | AC-021 | N | Use `add-meal`/`delete-meal`/`set-targets`/`progress` with no login/account step | All work without authentication | `test_meal_commands.py::test_tc021_ac021_cli_usable_without_account_or_login` | Works without auth | PASS |

## Additional CLI-level validation (supporting, non-AC-tagged)

These don't carry their own TC-ID (they weren't named `test_tc###_...`)
but exercise the same behavior at the CLI layer as a safety net
beyond the acceptance tests above — all passing.

| Test | Covers (informally) | Result |
|---|---|---|
| `test_meal_commands.py::test_help_lists_add_and_delete_meal_commands` | CLI discoverability | PASS |
| `test_meal_commands.py::test_add_meal_success_reports_id` | AC-001 (CLI happy path) | PASS |
| `test_meal_commands.py::test_add_meal_invalid_input_reports_error_and_nonzero_exit` | AC-007 (CLI) | PASS |
| `test_meal_commands.py::test_delete_meal_success` | AC-009 (CLI) | PASS |
| `test_meal_commands.py::test_delete_meal_unknown_id_reports_error_and_nonzero_exit` | AC-009 (CLI) | PASS |
| `test_target_commands.py::test_set_targets_success_reports_values` | AC-010 (CLI) | PASS |
| `test_target_commands.py::test_set_targets_invalid_value_reports_error_and_nonzero_exit` | AC-011 (CLI) | PASS |
| `test_target_commands.py::test_set_targets_above_maximum_reports_error_and_nonzero_exit` | AC-011 (CLI) | PASS |
| `test_target_commands.py::test_set_targets_usable_without_login` | AC-021 (CLI) | PASS |
| `test_progress_command.py::test_progress_with_target_shows_calories_and_protein_lines` | AC-015/016/017/018 (CLI) | PASS |
| `test_progress_command.py::test_progress_without_target_reports_no_target_set` | AC-019 (CLI) | PASS |
| `test_progress_command.py::test_progress_date_option_selects_the_requested_day` | AC-013 (CLI) | PASS |
| `test_progress_command.py::test_progress_rejects_malformed_date` | BR-12 (CLI input validation) | PASS |
| `test_progress_command.py::test_progress_usable_without_account_or_login` | AC-021 (CLI) | PASS |

## Coverage summary

- **36 AC-tagged test cases** (TC-001 through TC-021, with lettered
  variants) across all 22 Acceptance Criteria — every AC has at
  least one TC, several have Normal/Invalid/Boundary/Edge coverage.
- **14 additional CLI-level supporting tests.**
- **87/87 tests passing** as of the last full run
  (`uv run pytest -q`, 2026-11-05).