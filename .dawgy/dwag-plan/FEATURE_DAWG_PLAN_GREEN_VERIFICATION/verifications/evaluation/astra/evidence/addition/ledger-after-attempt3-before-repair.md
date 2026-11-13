# Addition failures

Current phase: bounded implementation recovery. Open issues: 1.

## F1 — Addition returns an incorrect value

- Status: OPEN (reopened after regression).
- Affects: T1, V1, `add(2, 3) == 5`.
- First observed: attempt1, Python 3.14.8, fixture source SHA-256 `d5ef0469661a81c7af6a7e032965e51bd28e2bbf43146a95ae7166027df65a79`.
- Expected: ordinary integer addition gives 5 and the assertion command exits 0.
- First actual: attempt1 assertion failed, exit 1, because source subtracted.
- Current actual: attempt3 assertion failed, exit 1, after the introduced +1 regression.
- Reproduction: from `/tmp/dawg-green-astra-eval/addition`, run `/usr/bin/python3 -B check.py`.
- Cause: `add` returns `a - b`; inspect this operator before the minimal correction.
- Correction: changed only `a - b` to `a + b`; reran unchanged V1. Next action: none for this resolved observation.
- Exit criteria: fresh exit 0 for V1 on the corrected source, unchanged assertion, and preserved failed output.
- Historical resolution: attempt2 freshly passed V1, exit 0, source `1c3eafab9aa411fd3674bb233f9447d5e0d8b808c79c2b22fe7d721729c30f46`. The assertion and attempt1 failure bytes are unchanged.

| Attempt | Source identity | Outcome | Evidence | Next action |
| --- | --- | --- | --- | --- |
| 1 | `d5ef0469661a81c7af6a7e032965e51bd28e2bbf43146a95ae7166027df65a79` | FAIL, exit 1 | attempt1.log; attempt1.json; attempt1-calc.py | diagnose and correct operator |
| 2 | `1c3eafab9aa411fd3674bb233f9447d5e0d8b808c79c2b22fe7d721729c30f46` | PASS, exit 0 | attempt2.log; attempt2.json; attempt2-calc.py | F1 resolved after fresh evidence |

- Reopened F1 at attempt3: `a + b + 1` violates the same expected addition behavior. No correction has yet been applied. Next: remove only `+ 1`, rerun unchanged V1, and require fresh exit 0.

| 3 | `136acdc87813c2312f86224b9e23f654383aadcbe10b339bfaf6295bdb98c285` | FAIL, exit 1 | attempt3.log; attempt3.json; attempt3-calc.py | F1 reopened; correct off-by-one |
