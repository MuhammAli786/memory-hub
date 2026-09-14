# Hook Utilities

`capture.py` is pure offline logic. It also provides a durable pending-turn outbox: save the prompt at submission, save the completed assistant reply before any external delivery attempt, then give only `replayable_pending()` records to a reviewed retry adapter. `run_capture.py` is a fail-open lifecycle wrapper: it reads one envelope from standard input, prints an accepted batch, and always succeeds so an unavailable downstream component cannot trap a session.

An integration adapter may persist the accepted batch after it has applied its own authorization, identity, and transport controls. That adapter is intentionally out of scope for this repository.

`recall_hook.py` renders reviewed persona content plus fresh L0/L1/L2 records supplied by that adapter. `sweep_sessions.py` is an offline safety-net batch producer for transcript files. `persona_manual.py` preserves exactly one human-reviewed persona block in a local document.
