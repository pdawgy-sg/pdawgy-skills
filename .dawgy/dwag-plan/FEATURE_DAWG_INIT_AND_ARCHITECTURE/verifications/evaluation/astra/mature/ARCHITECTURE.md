# Ledgerbox architecture

## Current scope and rationale

Ledgerbox is a small local Python demo. The existing documented decision is to keep storage in memory for that purpose. The inspected code operates on values in memory and has no implemented persistence layer; `store.py` aggregates values rather than storing them durably.

## Components and flows

- [main.py](main.py) passes `[1, 2, 3]` to `ledgerbox.service.summarize` and prints its return value.
- [ledgerbox/service.py](ledgerbox/service.py) formats `Total: ...` using the result of `ledgerbox.store.total`.
- [ledgerbox/store.py](ledgerbox/store.py) sums its input. The current uncommitted implementation skips `None` values; this is an observed local change, not a confirmed permanent interface contract.
- [load_plugin.py](load_plugin.py) dynamically imports `ledgerbox.plugins`, calls its `label()` function, and prints the result. [ledgerbox/plugins.py](ledgerbox/plugins.py) supplies the string `ledgerbox`; it is used despite having no static import from the main entry point.

The aggregation path is `main.py → ledgerbox/service.py → ledgerbox/store.py`. The plugin example is a separate entry point. Formatting and aggregation therefore do not all live in `main.py`.

## Runtime and open decisions

[pyproject.toml](pyproject.toml) declares Python >=3.11. The inspected runtime imports are internal modules and the Python standard library. No external service, deployment configuration, or persistent datastore appears in the inspected fixture.

The desired handling of `None` values remains unresolved: [scratch-notes.txt](scratch-notes.txt) says it is under investigation. This document records current behavior without settling that decision. The existing in-memory-demo rationale remains relevant; no contrary implementation was found.
