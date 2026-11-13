# Addition failures

Current phase: bounded implementation recovery. Open issues: 1.

## F1 — Addition returns an incorrect value

- Status: OPEN.
- Affects: T1, V1, `add(2, 3) == 5`.
- First observed: attempt1, Python 3.14.8, fixture source SHA-256 `d5ef0469661a81c7af6a7e032965e51bd28e2bbf43146a95ae7166027df65a79`.
- Expected: ordinary integer addition gives 5 and the assertion command exits 0.
- Actual: assertion failed, exit 1; source currently subtracts.
- Reproduction: from `/tmp/dawg-green-astra-eval/addition`, run `/usr/bin/python3 -B check.py`.
- Cause: `add` returns `a - b`; inspect this operator before the minimal correction.
- Correction: not yet applied. Next action is changing subtraction to addition and rerunning the same unchanged assertion.
- Exit criteria: fresh exit 0 for V1 on the corrected source, unchanged assertion, and preserved failed output.
- Resolution: none; writing a proposed fix is not closure.

| Attempt | Source identity | Outcome | Evidence | Next action |
| --- | --- | --- | --- | --- |
| 1 | `d5ef0469661a81c7af6a7e032965e51bd28e2bbf43146a95ae7166027df65a79` | FAIL, exit 1 | attempt1.log; attempt1.json; attempt1-calc.py | diagnose and correct operator |
