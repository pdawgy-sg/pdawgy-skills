# Verification: <Plan name>

Plan: [../PLAN.md](../PLAN.md)
Execution status: NOT RUN | IN PROGRESS | VERIFIED | BLOCKED | FAILED
Tested revision and uncommitted changes: <commit/diff reference, or not run>
Environment and prerequisites: <relevant runtime, fixtures, services, tools>
Working directory: <absolute path>

## Coverage checklist

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

- Astra: <pending or link to design-review-astra.md; model, effort, plan revision>
- Sol: <pending or link to design-review-sol.md; model, effort, plan revision>

These reviews validate the design, not the implementation.

## Completion

- Required checks: <passed / total; blocked or failing IDs>
- Remaining limitations: <specific items, or none>
- Evidence shared in chat: <plan/checklist links and screenshot embeds, if any>
