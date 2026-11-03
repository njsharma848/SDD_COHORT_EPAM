# Data Model: Calorie and Nutrition Tracker

This model implements BR-01–BR-12 for the reviewed v1.0 baseline. Numeric values are stored as integer tenths so that permitted one-decimal-place values remain exact.

## Meal

Represents one recorded meal.

| Field | SQLite type | Unit / meaning | Constraints |
|---|---|---|---|
| `id` | `INTEGER` | Stable meal identifier | Primary key; generated when inserted. |
| `name` | `TEXT` | User-provided meal name | Required. |
| `calories_tenths` | `INTEGER` | Tenths of a kilocalorie; `123` means `12.3 kcal` | Required; 0–100,000 inclusive; integer storage ensures at most one decimal place. |
| `protein_tenths` | `INTEGER` | Tenths of a gram; `123` means `12.3 g` | Required; 0–10,000 inclusive. |
| `meal_date` | `TEXT` | Local calendar date, ISO `YYYY-MM-DD` | Required; valid calendar date; cannot be after today's local date. |

### Meal operations

- Add creates a new row after complete input validation.
- Delete removes a matching `id`; a missing row is an error and makes no change.
- Editing is not supported. Correcting a mistake means deleting and adding.
- No target row is required to add a meal.

## Daily Target History

Represents the pair of daily nutrition goals effective from a given local date onward.

| Field | SQLite type | Unit / meaning | Constraints |
|---|---|---|---|
| `effective_date` | `TEXT` | First local calendar day this pair applies, ISO `YYYY-MM-DD` | Primary key; required valid ISO date. |
| `calories_tenths` | `INTEGER` | Tenths of kcal per day | Required; 0–100,000 inclusive. |
| `protein_tenths` | `INTEGER` | Tenths of protein grams per day | Required; 0–10,000 inclusive. |

Both nutrient targets are set together. A target history row applies to its effective date and later dates until the next row. If changed again on the same day, the pair for that date is replaced; entries for earlier dates are retained.

## Daily Progress (Derived Result)

Progress is calculated for one requested date; it is not a separately persisted entity.

| Value | Meaning |
|---|---|
| `day` | Selected local calendar date. |
| `consumed_calories_tenths` | Sum of meal calorie tenths for exactly that date; zero if none. |
| `consumed_protein_tenths` | Sum of meal protein tenths for exactly that date; zero if none. |
| `target` | Latest target pair whose effective date is on or before `day`, or absent. |
| `remaining_tenths` | Target tenths minus consumed tenths, preserving sign. Absent if no target exists. |
| `status` | `under`, `met`, or `over`; absent if no target exists. |

## Validation and Integrity

- Validation rejects missing values, non-numeric values, negative meal/target values, more than one fractional digit, meal values above 10,000 kcal / 1,000 g, target values above the same v1.0 limits, malformed dates, and future meal dates.
- Validate both target fields before changing either.
- Convert validated decimal input to integer tenths before persistence.
- SQLite `CHECK` constraints enforce numeric bounds as a final integrity guard. Application validation remains responsible for field-specific error messages.
- All mutations use a transaction. Validation errors occur before mutation; database failures roll back.

## Relationships and Queries

- Meals do not require a corresponding target.
- For progress on day `D`, aggregate meals where `meal_date = D`.
- For the target on day `D`, select the row with the greatest `effective_date <= D`; if there is none, no target is set for that day.
- Deleting a meal changes only the meal row; subsequent progress totals reflect its removal.
