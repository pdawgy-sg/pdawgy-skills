# Ledgerbox architecture

## Purpose and current scope

Ledgerbox is a local Python demo with in-process aggregation and display. The
existing documentation states that keeping storage in memory is deliberate
because this is a local demo. The inspected implementation performs aggregation
in memory and contains no persistence mechanism.

## Components and boundaries

- `main.py` is an executable entry point. It calls `ledgerbox/service.py`'s
  `summarize([1, 2, 3])` and prints the returned text.
- `ledgerbox/service.py` provides `summarize(values)`: it delegates aggregation
  to `ledgerbox/store.py`'s `total(values)` and formats `Total: RESULT`.
- `ledgerbox/store.py` supplies aggregation. The current uncommitted working
  version filters out `None` values before summing; it does not read or write
  files or provide persistent storage.
- `load_plugin.py` is a separate executable entry point. It uses
  `importlib.import_module("ledgerbox.plugins")`, then prints the module's
  `label()` result. `ledgerbox/plugins.py` is therefore dynamically referenced.

## Entry points and flows

`main.py` → `ledgerbox/service.py:summarize` → `ledgerbox/store.py:total` → formatted
text → stdout. `load_plugin.py` → dynamic import of `ledgerbox.plugins` → `label()`
→ stdout. The sources establish no connection between these two entry points.

## Runtime context and open decisions

`pyproject.toml` specifies Python >=3.11. The inspected source uses the Python
standard library and local modules; no external service or deployment setup is
present in these fixtures. `tests/test_service.py` checks normal integer summary
behavior. The dirty filtering change and `scratch-notes.txt` show investigation
of `None` handling; the intended stable contract for that case remains unresolved.
This document records current working code, not approval of that change.
