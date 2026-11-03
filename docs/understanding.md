\# Understanding — Calorie and Nutrition Tracker



\## Problem

People who want to manage their nutrition often have no simple way to see,

day by day, whether what they're eating lines up with what they intend to

eat. This project builds a small tracker that lets a person record meals as

they eat them, and see at a glance how today's calories and protein compare

to the targets they've set for themselves.



\## Users

A single individual tracking their own meals and nutrition goals. There is

no indication in the business request of multiple users sharing data, coaches

or admins managing other people's data, or any social/sharing feature — this

is treated as a single-user, personal tracking tool unless the mentor says

otherwise.



\## In scope (from the business request)

\- Recording meals with their nutrition information (at minimum: calories and

&#x20; protein).

\- Tracking total calories and protein consumed on a given day.

\- Setting daily targets for calories and protein.

\- Comparing recorded intake against targets and showing daily progress.



\## Out of scope for this fundamentals assignment (tentative — to confirm)

\- Micronutrients (fat, carbs, vitamins, fiber, etc.) — only calories and

&#x20; protein are mentioned in the request.

\- A food/nutrition database or barcode scanning — nutrition values are

&#x20; assumed to be entered manually per meal.

\- Multiple users, accounts, or authentication.

\- Exercise or calorie-burn tracking.

\- Weight tracking or long-term trend/history views beyond "today."

\- Editing or deleting past meals, unless confirmed necessary.



\## Success looks like

A user can, in a single sitting:

1\. Set a daily calorie and protein target.

2\. Record one or more meals, each with a name and its calories/protein.

3\. View a summary for the current day showing calories consumed, protein

&#x20;  consumed, each target, and how far they are from each target (under,

&#x20;  met, or over).

4\. Get a clear, correct error instead of a crash or silent bad data if they

&#x20;  enter something invalid (e.g. negative calories, missing required

&#x20;  fields).



This is the baseline behavior the specification, plan, and tests will be

built against. Every "to confirm" item above becomes a clarification

question in Phase 3 before the spec is finalized.

