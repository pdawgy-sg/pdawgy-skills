# Recovered addition issue register

Current phase: isolated implementation verification. V1 PASS, checked.
Open issues: 0. Nested TLA/planning/review gates explicitly deferred by the bounded
evaluation; no real task feature or Git delivery is being performed.

## F1 — Addition contract fails

- Status: RESOLVED (second episode closed by attempt4)
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
- Resolution: attempt2 exit 0 on calc SHA256 1c3eafab9aa411fd3674bb233f9447d5e0d8b808c79c2b22fe7d721729c30f46; assertion unchanged; attempt1 retained. Fresh pass meets exit criteria.

| Attempt | Input identity | Actual outcome | Evidence | Next action |
| --- | --- | --- | --- | --- |
| attempt1 | d5ef0469661a81c7af6a7e032965e51bd28e2bbf43146a95ae7166027df65a79 | FAIL, exit 1 | attempt1.log; attempt1.json | fix wrong operator and rerun |
| attempt2 | 1c3eafab9aa411fd3674bb233f9447d5e0d8b808c79c2b22fe7d721729c30f46 | PASS, exit 0 | attempt2.log; attempt2.json | resolved on current inputs |

### F1 recurrence — current issue is open

The same addition contract failed again after the deliberate regression changed
calc.py to return a + b + 1. Attempt2's earlier pass is stale, not current green.
Observed attempt3 exits 1 / AssertionError. Preserve both failed logs and the
unchanged check. Next authorized correction: remove the extra + 1, then rerun V1.
Current resolution: NONE until a fresh pass on the corrected current identity.
The previous Resolution field above is historical evidence for the first episode.

| attempt3 | 136acdc87813c2312f86224b9e23f654383aadcbe10b339bfaf6295bdb98c285 | FAIL, exit 1 | attempt3.log; attempt3.json | reopened F1; remove extra + 1 |

### F1 final current resolution

Current F1 status is RESOLVED; V1 PASS, checked, on current calc SHA256
1c3eafab9aa411fd3674bb233f9447d5e0d8b808c79c2b22fe7d721729c30f46. Attempt4 exited 0 with unchanged assertion SHA256
7d0c670e9481f4d5b18b81ccf4c93dea331a0f0442d2a9a766ae116311bc07ae. Both original failed logs remain byte-identical to their
capture hashes. The earlier recurrence section is historical and is superseded
only for current status by this fresh evidence, not erased. There are no unresolved
issues in the recovered-addition case. No unrelated check was removed or weakened.

| attempt4 | 1c3eafab9aa411fd3674bb233f9447d5e0d8b808c79c2b22fe7d721729c30f46 | PASS, exit 0 | attempt4.log; attempt4.json | final current resolution |
