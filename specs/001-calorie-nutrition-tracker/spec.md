# Feature Specification: Calorie and Nutrition Tracker

**Status**: Draft
**Source**: User-provided feature decisions A-01 through A-14

## Users / Actors

* **User**: One individual who records meals, sets personal daily calorie and protein targets, and views progress through a command-line interface. Accounts and authentication are not part of this feature.

## Scope

### In Scope

* Recording meals with a name, calories, protein in grams, and a date.
* Deleting a meal by its ID; corrections are made by deleting and re-adding.
* Setting daily calorie and protein targets.
* Viewing consumed totals and progress for one selected day, including today.
* Validating input and reporting invalid input without changing existing data.

### Out of Scope

* Micronutrients such as fat, carbohydrates, fiber, and vitamins.
* Food or nutrition databases and barcode lookup.
* Exercise or calorie-burn tracking.
* Weight tracking.
* Multiple users, accounts, authentication, or sharing.
* Editing meals or viewing multi-day history, weekly summaries, or trends.

## Business Rules

* **BR-01 — Meal details**: A meal has a name, calorie amount, protein amount in grams, and date.
* **BR-02 — Meal date**: A meal date defaults to today. The user may select any past or present date, but not a future date.
* **BR-03 — Meal nutrition values**: Calories and protein may be zero. Values are numeric, support up to one decimal place, and are rounded to one decimal place for storage and display. A meal may not exceed 10,000 kcal or 1,000 g protein.
* **BR-04 — Meal deletion**: A meal may be deleted by its ID. If the ID does not identify a recorded meal, the system reports a clear error and leaves data unchanged. Editing is not supported; a correction requires deleting and re-adding the meal.
* **BR-05 — Daily targets**: The user sets or changes daily calorie and protein targets together. A target does not have to exist before meals can be logged. Each target is numeric, has no more than one decimal place, is rounded to one decimal place for storage and display, and must be between zero and a daily maximum of 20,000 kcal or 2,000 g protein. These daily maximums are independent of, and intentionally larger than, the per-meal maximums in BR-03.
* **BR-06 — Target history**: A changed target applies starting on the day it is changed. Past days retain the target that was active on those days.
* **BR-07 — Day boundary**: A day is the period from midnight to midnight in local system time.
* **BR-08 — Daily totals**: Daily consumed totals are the sum of meal calories and protein for the selected day only. With no meals for that day, both totals are zero.
* **BR-09 — No target**: When no target exists for a day, show consumed totals and “no target set”; do not show remaining amounts or status labels.
* **BR-10 — Remaining amounts**: When targets exist, remaining calories and protein equal target minus consumed amount. A negative remaining amount is shown when consumption is over target.
* **BR-11 — Progress status**: Each nutrient has a status of “under”, “met”, or “over”. A difference within 5 kcal of the calorie target or within 1 g of the protein target, including the boundary, counts as “met”.
* **BR-12 — Invalid input**: Missing required fields, negative meal calories or protein, non-numeric input, values above the meal or target maximums, values with more than one decimal place, future meal dates, and targets below zero are rejected with a clear error. Rejection leaves existing data unchanged and performs no partial write.

## Functional Requirements

* **FR-001**: The system MUST let the single user record a meal with a name, calories, protein in grams, and date.
* **FR-002**: The system MUST default a meal date to today and allow any past or present date, while rejecting future dates.
* **FR-003**: The system MUST accept zero for meal calories and protein, accept values to one decimal place, and store and display them rounded to one decimal place.
* **FR-004**: The system MUST reject a meal with calories above 10,000 kcal or protein above 1,000 g.
* **FR-005**: The system MUST let the user delete a meal by its ID, report a clear error without changing data if the ID is unknown, and MUST NOT provide meal editing.
* **FR-006**: The system MUST let the user set or change daily calorie and protein targets together, each from zero through 20,000 kcal or 2,000 g protein respectively and to no more than one decimal place, round them to one decimal place for storage and display, and MUST allow meal logging when no target is set.
* **FR-007**: The system MUST apply a changed target from its effective day forward while preserving the target applicable to each past day.
* **FR-008**: The system MUST show, for one selected day, total calories and protein consumed and, if a target exists, that day's targets, remaining amounts, and status labels.
* **FR-009**: The system MUST show zero consumed totals when a day has no meals.
* **FR-010**: The system MUST show “no target set” instead of remaining amounts or status labels when no target exists for the selected day.
* **FR-011**: The system MUST calculate remaining amounts as target minus consumed amount, showing a negative number when over target.
* **FR-012**: The system MUST classify each nutrient as “under”, “met”, or “over”, with “met” including differences within 5 kcal or 1 g of its respective target.
* **FR-013**: The system MUST reject invalid input with a clear error and leave existing data unchanged, without partial writes or silent corrections.
* **FR-014**: The system MUST be usable by one user through a command-line interface without accounts or authentication.

## Non-Functional Requirements / Constraints

* The feature is limited to one user and a command-line interface.
* A “day” uses the local system's midnight-to-midnight boundary.
* The specification defines observable behavior only; it does not prescribe implementation technology or architecture.

## Glossary

* **Day**: Midnight-to-midnight period according to local system time.
* **Meal**: A named food-intake entry with calorie and protein amounts and a date.
* **Target**: The user's daily desired amount of calories or protein.
* **Progress**: The selected day's consumed totals and, when a target exists, target comparison, remaining amount, and status.

## Acceptance Criteria

* **AC-001 — Record a meal with today's default date**  
**Given** the user supplies a valid meal name, calories, and protein without a date, **When** the user records the meal, **Then** the meal is recorded with today's local date and its supplied nutrition values.
* **AC-002 — Record meals for past and present dates**  
**Given** the user supplies a valid meal and a past or present date, **When** the user records it, **Then** the meal is recorded for that date.
* **AC-003 — Reject a future meal date**  
**Given** the user supplies a future date for a meal, **When** the user attempts to record it, **Then** the system gives a clear error and existing data remains unchanged.
* **AC-004 — Accept and display meal values to one decimal place**  
**Given** the user supplies valid calorie and protein values with no more than one decimal place, **When** the meal is recorded and viewed in daily totals, **Then** those values are stored and displayed rounded to one decimal place.
* **AC-005 — Accept zero meal values**  
**Given** the user supplies zero for calories, protein, or both, **When** the meal is recorded, **Then** the system accepts the values.
* **AC-006 — Enforce meal maximums**  
**Given** a meal has 10,000 kcal and 1,000 g protein, **When** it is recorded, **Then** the system accepts it. **Given** either value exceeds its maximum, **When** the user attempts to record it, **Then** the system rejects it with a clear error and leaves existing data unchanged.
* **AC-007 — Reject missing, non-numeric, or negative meal input**  
**Given** a required meal field is missing, a calorie or protein value is non-numeric or negative, or a meal value has more than one decimal place, **When** the user attempts to record the meal, **Then** the system gives a clear error and existing data remains unchanged.
* **AC-008 — Record a meal without a target**  
**Given** no daily target has been set, **When** the user records a valid meal, **Then** the meal is recorded successfully.
* **AC-009 — Delete a meal by ID**  
**Given** a recorded meal with an ID, **When** the user deletes that meal by ID, **Then** it is removed and no longer contributes to that day's consumed totals. **Given** an ID that does not identify a recorded meal, **When** the user attempts deletion, **Then** the system reports a clear error and leaves existing data unchanged.
* **AC-010 — Set calorie and protein targets together**  
**Given** the user supplies both targets with values from zero through 20,000 kcal and zero through 2,000 g protein, each to no more than one decimal place, **When** the user sets or changes the targets, **Then** both are accepted, rounded to one decimal place for storage and display, and available for progress on their effective day.
* **AC-011 — Reject invalid targets safely**  
**Given** either required target is missing, non-numeric, below zero, above its maximum, or has more than one decimal place, **When** the user attempts to set or change targets, **Then** the system gives a clear error and leaves the existing target and other data unchanged.
* **AC-012 — Preserve past targets after a change**  
**Given** a target was active on a past day and is later changed, **When** the user views progress for the past day and for the change day, **Then** the past day retains its previously active target and the changed target applies from the change day forward.
* **AC-013 — Calculate totals for only the selected day**  
**Given** meals exist on multiple dates, **When** the user views progress for one date, **Then** the consumed calorie and protein totals include only meals dated on that selected day.
* **AC-014 — Show zero totals on a day without meals**  
**Given** no meals are recorded for a selected day, **When** the user views its progress, **Then** consumed calories and protein are both shown as zero.
* **AC-015 — Show progress when a target exists**  
**Given** a target exists for a selected day and consumption exactly equals each target, **When** the user views progress, **Then** the system shows consumed totals, targets, zero remaining amounts, and “met” status for both.
* **AC-016 — Show under-target progress**  
**Given** consumption is more than the applicable tolerance below a target, **When** the user views progress, **Then** the system shows a positive remaining amount and “under” status for that nutrient.
* **AC-017 — Apply the met tolerance at its boundaries**  
**Given** consumption differs from its target by no more than 5 kcal or 1 g, on either side and including the respective boundary, **When** the user views progress, **Then** that nutrient's status is “met”.
* **AC-018 — Show over-target progress**  
**Given** consumption exceeds a target by more than its applicable tolerance, **When** the user views progress, **Then** the system shows a negative remaining amount and “over” status for that nutrient.
* **AC-019 — Show progress without a target**  
**Given** no target exists for a selected day, **When** the user views progress, **Then** the system shows consumed totals and “no target set”, without remaining amounts or status labels.
* **AC-020 — Reject invalid input without partial changes**  
**Given** existing meals or targets are present, **When** any invalid input covered by BR-12 is submitted, **Then** the system reports an error and all existing meals, targets, and totals remain unchanged.
* **AC-021 — Use the tracker without an account**  
**Given** the single user starts the tracker, **When** they access its meal, target, or progress functions through the command-line interface, **Then** they can use them without creating an account or authenticating.

