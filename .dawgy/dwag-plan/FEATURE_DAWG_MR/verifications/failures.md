# Failure register

## F1 — TLC cannot enumerate primed Init (T1/V1)

Status: RESOLVED. Corrected rerun `tla/runs/parent-02/` passed: production 72 distinct states, queue 0; EvidenceSound and NoDraft probes each exited 12 with the exact violation and trace. Original failed logs/input preserved. Environment: Java 25.0.5, TLC 2.19.
Attempt: `tla/runs/parent-01/` raw three logs/receipt and exact input snapshot.
Expected: full production exploration and named negative/witness violations.
Actual: all configurations exit 75 with undefined `phase` while evaluating `Init'`
in NewRequest; 64 states generated, queue 31. This is a model execution error,
not an expected negative violation. Input/tool/config hashes are in receipt.json.
Cause: TLC cannot enumerate this primed state predicate as an action generator.
Correction: expand reset into explicit primed assignments/membership generators,
retaining the same finite input relation. No requirements or properties weakened.
Exit criterion: rerun all configs; complete production plus exact probe traces.
Both reviewers will execute the corrected final inputs independently.

## F2 — initial ambiguity fixture did not create distinct scopes (T2/V3)

Status: RESOLVED in Astra's final evaluation. This was an evaluation-input gap,
not a skill defect. Expected: two plausible targets with materially different
committed scopes. Actual: initial two-branch fixture pointed to identical target
commits, so it could not establish that condition. Original observations and
fingerprints remain in `evaluation-astra/evidence/ambiguous-*` and the report.
Correction: created a fresh `ambiguous-material` fixture with genuinely different
release-a/release-b scopes; preserved its setup/runtime commands and snapshots.
Exit criterion met: actual output `evaluation-astra/ambiguous.md` asks the focused
target question without guessing or mutating Git; final byte fingerprints match.

Intentional fixture application failures and stale logs are test inputs: V3
passes only when the MR draft accurately reports them. They are not unresolved
failures of this plugin or permission to repair the summarized target repository.

## F3 — fixture setup import invocation failed (T2/V3)

Status: RESOLVED. Sol fixture setup `python -B checks/check_integer.py` failed
with ModuleNotFoundError because checks/ rather than repository root was on
sys.path. Raw attempt is preserved in evaluation-sol/evidence/setup-commands.log
and SETUP_NOTES.md. Correction: explicit checks package and module invocation
`python -B -m checks.check_integer`. Baseline command then passed; subsequent
records use module commands. Expected baseline result observed before runtime
began. Setup-only correction; no plugin defect, runtime test run, or erased error.

All observed authoring/evaluation issues are resolved. Required implementation
checks passed on the current source; final commit/push remain delivery steps.
