---
name: tasks
description: >-
  Read, add, validate, publish, and synchronize a task set. Use when a user
  mentions a task, reminder, deadline, due date, calendar item, commitment,
  outstanding work, or asks to put something on a list.
---

# Tasks

## One source, many views

Keep a single structured task file as the source of truth. Calendar entries,
reminders, a wiki task page, and dashboard views are generated outputs. Never
edit a generated view directly: it will either be overwritten or drift from
the other views.

The portable row shape is `title<TAB>due<TAB>note`. `due` is `YYYY-MM-DD` or
empty. The note identifies the source of a stated date, or says `DERIVED, not
agreed` with its basis when a date was computed.

## Intake rule

Never invent a due date. If a request does not state one, leave it empty. An
expired target stays recorded as expired; do not replace it with a plausible
new date. Before adding a task, search for the same commitment. If one exists,
update its note only when new evidence is explicit; do not create a competitor.

## Workflow

1. Read `priorities.md` and the authoritative task file.
2. Extract title, stated due date, source note, and whether the request is a
   task rather than background information.
3. Validate row format and deduplicate by normalized title plus due date.
4. Add or update the authoritative row.
5. Publish the wiki task view.
6. Synchronize optional reminder/calendar views only when the user connected
   them and authorized the write.
7. Inspect the result summary. Report `SUCCESS`, `PARTIAL`, or `BLOCKED`; do
   not call a run successful solely because the command exited.
8. Append an activity-log entry describing the change and resulting views.

## Validation and delegation

- Every title is non-empty and dates parse or are empty.
- Synchronization may add or update but never silently delete, complete, or
  reopen an item.
- If one connected surface fails, report the exact partial state and preserve
  the authoritative file for retry.
- A model may classify candidate tasks or draft notes. It must not assign a
  date, decide a vague aspiration is a commitment, delete tasks, or resolve
  conflicting duplicates.
