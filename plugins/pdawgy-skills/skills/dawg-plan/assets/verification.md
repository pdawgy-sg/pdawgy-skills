# Verification: <Plan name>

Plan: [../PLAN.md](../PLAN.md)
Execution status: NOT RUN | IN PROGRESS | VERIFIED | BLOCKED | FAILED
Tested revision and uncommitted changes: <commit/diff reference, or not run>
Environment and prerequisites: <relevant runtime, fixtures, services, tools>
Working directory: <absolute path>
Source repository / selected relative scope: <original root; target-relative path>
Worktree repository / mapped project: <task worktree root; scoped project path>
Base commit / task branch / remote destination: <record exact values>
Delivery checkpoint: <planning-only, or verified pre-delivery snapshot>
Final commit/push receipt: <report in chat after delivery; no self-referential commit>

## Coverage checklist

- [ ] FORMAL — parent and both exact reviewers independently completed TLC on
  identical current inputs; enabled properties/assumptions/bounds reviewed;
  logs/receipts/traces under tla/; bounded claims and implementation gaps recorded.
- [ ] V1 — <observable check; task IDs; acceptance IDs; transition IDs/invariants>

List every required check. Every task, acceptance criterion, transition, and
stated invariant must map to a check; reuse checks where they provide coverage.
Keep boxes unchecked until their actual checks pass.

## V1 — <check name>

- Covers: <task IDs, acceptance IDs, transition IDs/invariants>
- Procedure: <exact command or reproducible UI/artifact inspection steps>
- Expected: <specific result or exit status and observed behavior>
- Actual: <not run, or observed result including command exit status>
- Evidence: <relative evidence filenames; label paths as planned until saved>
- Status: NOT RUN
- Blocker / next action: <if any>
- Cleanup: <if needed>

Repeat for each verification ID. Record failed attempts and reruns rather than
replacing a failure with an unexplained pass. Store logs, screenshots, and other
proof in this directory; redact private data and credentials.

## Design review evidence

- Parent TLC: <revision/input/tool hashes; exact command; configs; completed
  outcomes/state counts; tla/runs/...; not run until actually executed>
- Astra: <design-review-astra.md; gpt-6-astra/high; own TLC hashes/logs/results;
  abstraction/requirement review; matching final model identity>
- Sol: <design-review-sol.md; gpt-6.1-sol/high; own TLC hashes/logs/results;
  abstraction/requirement review; matching final model identity>
- Formal limits/probes: <finite bounds, assumptions, fairness/deadlock choices,
  actual nominal reachability; expected negative traces separate from failures>

Changed behavior/model/config/dependencies/bounds/assumptions/fairness invalidate
all three receipts. Missing, failed, stale or incomplete required executions block
readiness. These checks validate a bounded abstraction; implementation verification
and source correspondence remain required.

## Completion

- Required checks: <passed / total; blocked or failing IDs>
- Remaining limitations: <specific items, or none>
- Evidence shared in chat: <plan/checklist links and screenshot embeds, if any>
- Commit/push prerequisites: <all checks passed, entire existing index/task hunks
  in scope, complete commit delta matches intended/tested source, identity/remote>
- Delivery handoff: <actual Conventional Commit, task branch and remote OID
  confirmation in chat; distinguish local commit, push and required CI outcomes>
