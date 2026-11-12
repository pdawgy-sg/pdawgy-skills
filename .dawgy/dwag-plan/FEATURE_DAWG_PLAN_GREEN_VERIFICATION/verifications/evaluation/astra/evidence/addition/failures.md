# Addition failures

Current phase: bounded implementation recovery. Open issues: 0.

## F1 — Addition returns an incorrect value

- Status: RESOLVED on attempt4 after reopening at attempt3.
- Affects: T1, V1, ordinary addition `add(2, 3) == 5`.
- First observed: attempt1, Python 3.14.8; full environment/command/source identities in attempt JSON.
- Expected: result 5, assertion exits 0.
- Actual history: attempt1 subtraction failed; attempt2 corrected addition passed; introduced regression invalidated that pass before attempt3; attempt3 extra +1 failed and reopened F1; attempt4 corrected addition passed.
- Reproduction: `/usr/bin/python3 -B check.py` from `/tmp/dawg-green-astra-eval/addition`.
- Causes/corrections: initially replace subtraction with addition; on recurrence remove introduced +1. Assertion unchanged in all four attempts.
- Exit criteria: fresh unchanged V1 exits 0 on corrected source; original failed logs remain intact.
- Current resolution: attempt4, exit 0, source `1c3eafab9aa411fd3674bb233f9447d5e0d8b808c79c2b22fe7d721729c30f46`. Both failed logs retain original bytes. Earlier resolved snapshot and pre-repair open snapshots remain preserved.
- Next action: none for F1; separate unavailable-tool case is not covered by this resolution.

| Attempt | Source identity | Outcome | Evidence |
| --- | --- | --- | --- |
| 1 | `d5ef0469661a81c7af6a7e032965e51bd28e2bbf43146a95ae7166027df65a79` | FAIL, exit 1 | attempt1.log; attempt1.json; attempt1-calc.py |
| 2 | `1c3eafab9aa411fd3674bb233f9447d5e0d8b808c79c2b22fe7d721729c30f46` | PASS, exit 0 | attempt2.log; attempt2.json; attempt2-calc.py |
| 3 | `136acdc87813c2312f86224b9e23f654383aadcbe10b339bfaf6295bdb98c285` | FAIL, exit 1 | attempt3.log; attempt3.json; attempt3-calc.py |
| 4 | `1c3eafab9aa411fd3674bb233f9447d5e0d8b808c79c2b22fe7d721729c30f46` | PASS, exit 0 | attempt4.log; attempt4.json; attempt4-calc.py |
