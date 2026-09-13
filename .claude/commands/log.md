---
description: Append a verified activity note
argument-hint: "<note>"
---

Append a concise, factual entry with:

```sh
python3 tools/append_activity.py --log wiki/activity-log.md --message "$ARGUMENTS"
```

Do not modify existing entries. If the change updates a wiki page, update its `last-updated` date and its index entry as well.
