# Formatting helper

`format_label` normalizes whitespace between words and removes leading and trailing whitespace. See [usage.md](usage.md) and [helper.py](helper.py).

The accepted [user request](../history.json) was to create the helper and install it for local agents. During closeout on 2026-11-12 UTC, helper syntax compilation passed and the [installed helper](../installed/helper.py) matched the source byte for byte. To repeat the documented project check: `python3 -m py_compile helper.py`.

Creation and installation are complete. Closeout preserves the task source and usage in a local Git commit. Synchronization and archive execution were not requested; no follow-up is outstanding for the accepted task.
