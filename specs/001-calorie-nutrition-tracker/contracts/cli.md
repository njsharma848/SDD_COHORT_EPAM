# CLI Contract: Calorie and Nutrition Tracker

The CLI is the only user-facing interface. It uses four commands and reports expected validation/domain errors clearly without writing partial data.

## Commands

### Add a meal

```text
calorie-tracker add-meal --name NAME --calories VALUE --protein VALUE [--date YYYY-MM-DD]
```

- `--name`, `--calories`, and `--protein` are required.
- `--date` is optional and defaults to today's local date.
- On success, report that the meal was recorded and include its ID.
- Reject invalid values and future meal dates with a clear error; do not change stored data.

### Delete a meal

```text
calorie-tracker delete-meal --id ID
```

- A matching meal is deleted and success is reported.
- An unknown ID produces a clear error and leaves data unchanged.

### Set or change daily targets

```text
calorie-tracker set-targets --calories VALUE --protein VALUE
```

- Both targets are required and are set together.
- Both become effective on today's local date.
- Values must be numeric, between zero and the v1.0 maximums (10,000 kcal and 1,000 g protein), with at most one decimal place.
- On success, report both values to one decimal place.
- Any invalid field rejects the whole operation and preserves existing target history.

### View progress

```text
calorie-tracker progress [--date YYYY-MM-DD]
```

- `--date` is optional and defaults to today's local date.
- Show consumed calories and protein for only that day; show `0.0` when there are no meals.
- If no target is effective on that day, show `no target set` and omit remaining/status fields.
- Otherwise show the target pair, signed remaining values, and one status per nutrient.
- Values are displayed to one decimal place.

## Output and Exit Behavior

- Successful commands exit with status `0`.
- Invalid input, unknown meal ID, or an operation failure exits non-zero and prints a concise, actionable message to stderr.
- Progress is read-only. Rejected mutating commands leave persisted data unchanged.
- No command for editing meals, account management, or multi-day reporting is exposed.
