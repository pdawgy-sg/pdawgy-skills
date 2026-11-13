# Recovered addition issue register

Current phase: isolated implementation verification. V1 FAIL, unchecked.
Open issues: 1. Nested TLA/planning/review gates explicitly deferred by the bounded
evaluation; no real task feature or Git delivery is being performed.

## F1 — Addition contract fails

- Status: OPEN
- Affects: V1, ordinary integer addition; calc.py.
- First observation: attempt1, Python 3.14.8, calc SHA256 d5ef0469661a81c7af6a7e032965e51bd28e2bbf43146a95ae7166027df65a79.
- Expected: `add(2, 3) == 5`, check.py exits 0.
- Actual: exit 1 / AssertionError. Evidence: attempt1.log and attempt1.json.
- Reproduction: from recovered/, run `python -B check.py`.
- Cause: `add` returns `a - b`, violating ordinary addition.
- Authorized correction: change only calc.py's operator to `+`; do not alter assertion.
- Next action: apply that minimal correction, rerun V1 and inspect unchanged check input.
- Exit criteria: fresh V1 exit 0 on corrected current source, unchanged check SHA256
  7d0c670e9481f4d5b18b81ccf4c93dea331a0f0442d2a9a766ae116311bc07ae, preserved attempt1 log, no unresolved addition issue.
- Resolution: none; no correction or rerun yet.

| Attempt | Input identity | Actual outcome | Evidence | Next action |
| --- | --- | --- | --- | --- |
| attempt1 | d5ef0469661a81c7af6a7e032965e51bd28e2bbf43146a95ae7166027df65a79 | FAIL, exit 1 | attempt1.log; attempt1.json | fix wrong operator and rerun |
