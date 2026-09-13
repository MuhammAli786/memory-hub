# Windows Task Scheduler Template

Create separate tasks for the model router, embedding server, graph refresh,
and container health/backup work. Use a dedicated interactive or service account
selected by the operator; different GPU drivers may have different session
requirements.

For every task configure:

1. An absolute launcher path owned by the operator.
2. A working directory under the local clone.
3. Output and error logs under ignored `local-data/logs/`.
4. A bounded restart policy.
5. A trigger appropriate to its ownership: boot for persistent local services,
   hourly for graph work, daily for backups.
6. An overlap rule: do not start a new graph or ingest run if the prior one is
   still active.

After registration, run the task manually, inspect its log, then wait for one
scheduled execution. A task marked running is not proof that its child process
is healthy; verify its expected health signal.
