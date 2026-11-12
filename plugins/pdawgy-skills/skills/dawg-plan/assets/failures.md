# Failures: <Plan name>

Plan: [../PLAN.md](../PLAN.md)
Checks: [verification.md](verification.md)
Open / in-progress / blocked issues: <actual count; zero if none observed>
Current phase and tested input identity: <planning, implementation or delivery; revision/hashes>

Do not invent failures for unattempted planned work. Preserve observed failures
and every attempt after repair. Link all affected check/case IDs.

## F1 — <observed issue; create only after observation>

- Status: OPEN | IN PROGRESS | BLOCKED | RESOLVED
- Affects: <task/check/case IDs; reopen the same issue if it recurs>
- First observed: <source/config revision and relevant environment>
- Expected / actual: <observable result, exact failure/exit>
- Reproduction: <runnable command/procedure and prerequisites>
- Cause and correction: <evidence-backed diagnosis and applied action, or unknown>
- Next action / blocker: <what will be tried or exact outside input needed>
- Exit criteria: <fresh failed-case and affected-check passes required>
- Resolution: <actual final revision/attempt/evidence, not just a proposed patch>

| Attempt | Input identity / command | Actual outcome / exit | Evidence | Correction / next action |
| --- | --- | --- | --- | --- |
| <unique ID> | <revision/hash; command> | <actual observed result> | <unique log path> | <diagnosis/action> |

Remove unused prompts from the final register. If nothing failed, record that
plainly and keep no invented F1. Close only with evidence; never overwrite failed
logs or delete closed history to make the register look green.
