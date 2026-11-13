Title: Fix empty daily summaries returning an error

Committed scope: main merge-base `3550b821faa436389688c9d5b45101b4fbb39033` → `85dde0f8bc9e3929e56443088ebb842f6398a614`.

# Problem

Empty daily reports crash when `average([])` divides by zero; the recorded requirement calls for an average of 0.

# Fix

Return 0 for empty input. `daily_summary([])` now returns `{"average": 0}`. Nonempty input retains the existing calculation in source.

# Blast radius

Changes `average()` and its direct `daily_summary()` consumer's empty-input behavior. Callers expecting `ZeroDivisionError` now receive 0; the existing legacy check exposes that compatibility change. No dependency or configuration changes appear in this diff. Impact on consumers outside the inspected repository is unverified.

# Verified / tested

Recorded author results in `verification/records.json`, whose tested source hashes match the committed files:

- `/usr/bin/python3 -B check_empty.py`: PASS, exit 0; covers empty daily summary.
- `/usr/bin/python3 -B check_legacy.py`: FAIL, exit 1; still expects `ZeroDivisionError`. That expectation needs reconciliation with the new contract.
- `/usr/bin/python3 -B check_nonempty.py`: historical PASS on base `3550b82`; its tested implementation hash differs from this change. No applicable current execution evidence for nonempty behavior was found; rerun is still needed.

This drafting session inspected committed source and evidence; it did not rerun tests. Staged, unstaged and untracked changes are excluded.
