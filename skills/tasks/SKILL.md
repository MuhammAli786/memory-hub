---
name: tasks
description: Maintain a single task source and publish consistent task views without inventing deadlines.
---

# Tasks

Maintain one task file as the source of truth. Derived views—calendar, reminders, wiki task page, or a private task adapter—must be generated from it rather than edited independently.

Each task has a title, optional due date, and note. Add a date only when a source states it. If a checkpoint is calculated from a known date, label it derived and name the basis. Never transform an absent date into a plausible one.

Before synchronizing, validate that every due date uses `YYYY-MM-DD`, that titles are non-empty, and that no duplicate task has conflicting dates. Synchronization may add or update views but must not silently delete, complete, or reopen tasks.
