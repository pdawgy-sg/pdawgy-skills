# Record, repair, and rerun until green

During implementation and verification, keep working on observed non-green
results until the required checks for that phase pass on current inputs and
their issues meet recorded exit criteria. Reporting a failure alone is not task
completion. This includes tests, formal checks, source/artifact checks, hooks,
required CI and delivery verification when those stages apply.

## Record promptly and preserve attempts

Use the plan's `verifications/verification.md` checklist and persistent
`verifications/failures.md` register. Initialize the register without invented
failures. Give each observed issue a stable F ID, link its affected task/check or
case IDs, and save evidence before proceeding with correction/retry. Multiple
cases with one cause may share an issue if every failed case remains traceable.

For every issue record its first observation, expected/actual behavior, command or
reproduction steps, exit/error, tested source/configuration identity and relevant
environment. Keep cause, corrective action, current status, next action or blocker,
exit criteria and resolution evidence. Statuses are OPEN, IN PROGRESS, BLOCKED,
or RESOLVED. Reopen a recurring issue under the same ID when it is the same problem.

Keep a chronological attempt table and unique raw-output/evidence paths, including
failures and successful reruns. Never replace an old failed log with a pass, erase
the issue, or claim a command ran when it could not. Redact credentials/private
data while preserving useful diagnostics. If recording is itself blocked, preserve
the observation in an available authorized location/chat, report the storage
blocker, and restore the durable record when access returns.

A planned later check stays NOT RUN/unchecked in the verification checklist; it
is not an invented defect merely because execution has not reached that phase.
At the applicable gate, required unrun, stale, incomplete or blocked checks remain
non-green, with their reasons and next actions recorded.

## Diagnose and correct, then verify the correction

Investigate a reproducible cause using the failure output and relevant source or
environment. Make the smallest justified correction within scope, then rerun the
failed check and the checks affected by that correction. Use existing task
authorization; do not request permission for every ordinary fix or rerun.

If code, behavior, configuration or relevant inputs change, invalidate affected
prior passes and check the new input identity. Material formal/requirement changes
also require parent and every required reviewer to rerun/review as the TLA+ workflow says.
Verification log updates alone do not change the tested implementation.

Do not endlessly rerun an unchanged failing command without diagnosis or changed
conditions. Do not delete/skip checks, relax assertions, suppress errors, exclude
bad states, or change expected behavior merely to turn output green. A genuinely
incorrect test/model requires evidence of the intended contract; record the
reason and obtain required clarification/review for material expectation changes.

Do not cherry-pick a flaky pass. Investigate the instability and record enough
fresh evidence to support the resolution. Preexisting or apparently unrelated
failures are still recorded, investigated and kept non-green; their origin is
not a waiver. If remediation exceeds scope or authority, request a concrete scope
decision instead of silently dropping the check or changing unrelated behavior.

## Handle real blockers while continuing useful work

When progress needs missing credentials, permission, user intent, external service
state or unavailable tooling, record the exact dependency, evidence and requested
action. Ask early and continue useful independent authorized tasks. Keep the issue
BLOCKED and checks unchecked; resume after resolution. Do not pretend all-green,
bypass approval, remove user work, or claim completion because further progress
requires another party. There is no arbitrary retry-count rule that converts a
self-correctable failure into a successful handoff.

## Close only with current evidence

Resolve an issue only when its actual exit criteria are met: fresh passing results
for the failed case and affected checks, with source/config identity and evidence
links. Writing a fix, receiving design approval, or observing an old pass is not
resolution. Preserve the full failed history after closure.

Green is phase-specific:

- Plan readiness: current parent/all-required-reviewer formal runs and semantic approvals;
  future implementation tests remain planned, not falsely executed.
- Implementation completion: all required implementation/artifact checks are PASS
  on current inputs and no implementation failure/blocker remains unresolved.
- Commit/push/delivery: existing scoped Git gates, hook and required CI/remote
  confirmations apply. Record and work through failures while preserving the
  existing commit/worktree; no force, bypass, or false delivery claim.

Declared negative/witness probes are checked against their exact expected outcome.
An expected named counterexample can make that probe successful; a parser crash,
timeout or a different violation cannot. Keep these probes distinct from required
production checks so their preserved error output is not hidden or mislabeled.

Before completion, inspect the whole phase checklist and failure register. Zero
unresolved issues plus current passing required checks is the gate. Retain the
plan-only and explicit delivery limits. Final commit/push receipts stay in chat
as specified by the Git workflow; do not churn a verified commit to embed its own
future delivery receipt.
