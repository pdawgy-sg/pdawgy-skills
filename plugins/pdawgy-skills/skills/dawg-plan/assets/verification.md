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
Failure register: [failures.md](failures.md)
Current phase / green gate: <required checks for this phase; open F IDs>
Execution host / evidence: <Codex or Claude Code; trusted context, unresolved host blocks>
Review tier / rationale / required models: <Codex gpt-6.2-sol/high; add separate gpt-6.2-astra/high for large; Claude Code Sonnet 5.5/high; add separate Opus 5.5/high for large>

## Project lint and static checks

- Inspected sources: <applicable instructions, tooling/scripts/configuration and CI paths>
- If none apply: <why the inspected sources yield no applicable check for this scope>

| Check ID | Requirement source and applicability | Exact command | Working directory in the task worktree |
| --- | --- | --- | --- |
| <V ID> | <path and why this check applies> | <command> | <absolute mapped path> |

List applicable checks here and record runs, tested inputs, and failure or
blocker evidence under their check IDs below. Use the absence rationale when
the inventory is empty. A missing prerequisite for a required command is BLOCKED.
Keep required tests and CI in the coverage checklist.

## Coverage checklist

- [ ] FORMAL — author and every tier-required exact reviewer independently completed TLC on
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
- Issue and attempt history: <linked F IDs, preserved failed attempts, correction,
  affected-check reruns, final tested identity; no invented failures>

Repeat for each verification ID. Record failed attempts and reruns rather than
replacing a failure with an unexplained pass. Store logs, screenshots, and other
proof in this directory; redact private data and credentials.

An observed non-green result must enter failures.md promptly, then be diagnosed,
corrected within authorization and rerun along with affected checks until green.
Reopen recurrences; preserve failed logs after closure. Changed relevant inputs
invalidate affected old passes. Record real blockers and needed input, ask early,
continue independent work, and do not claim completion while required issues stay
unresolved. Keep later planned phases and exact expected negative probes distinct.

## Phase identity and review evidence

- Codex phases when applicable: <gpt-6.2-astra/high planner and author,
  gpt-6.2-sol/high independent reviewer, separate gpt-6.2-astra/high reviewer for
  large work, gpt-6.2-sol/medium implementer if ready and authorized. Record each
  context, explicit dispatch arguments and available trusted effective metadata
  or its limits. Report known mismatches.>
- Claude phases when applicable: <qualified planner/reviewer(s)/implementer types;
  requested and effective full model IDs/effort; overrides checked; distinct sibling
  contexts; Opus 5.5/high author, Sonnet 5.5/high small review only, separate
  Opus 5.5/high additional review for large; authorized ready implementation by
  Opus 5.5/medium; plan-only skips implementer; material gaps re-plan/re-review>

- Author TLC: <revision/input/tool hashes; exact command; configs; completed
  outcomes/state counts; tla/runs/...; not run until actually executed>
- Primary host reviewer: <gpt-6.2-sol/high in Codex or Sonnet 5.5/high in Claude Code;
  host-specific design-review file, requested and available effective identity/effort, own current
  TLC hashes/logs/results and semantic review on final inputs>
- Additional host reviewer (large only): <gpt-6.2-astra/high in Codex or Opus 5.5/high in
  Claude Code; own current TLC/semantic review and actual identity; for small
  explicitly mark not required, never fabricate execution>
- Formal limits/probes: <finite bounds, assumptions, fairness/deadlock choices,
  actual nominal reachability; expected negative traces separate from failures>

Changed behavior/model/config/dependencies/bounds/assumptions/fairness invalidate
the author and all required reviewer receipts.
Scope growth requires the host-specific large-tier set before readiness. Host
changes revoke readiness/reselect the profile; wrong-provider receipts do not count. Missing, failed, stale or incomplete required executions block
readiness. These checks validate a bounded abstraction; implementation verification
and source correspondence remain required.

## Completion

- Required checks: <passed / total; blocked or failing IDs>
- Remaining limitations: <specific items, or none>
- All-green evidence: <current phase's required checks PASS on current inputs,
  zero unresolved relevant F IDs, failed history retained; blocked is not complete>
- Evidence shared in chat: <plan/checklist links and screenshot embeds, if any>
- Coordinator audit before commit and before push: <current passing required
  checks, lint/static evidence or justified non-applicability, entire existing
  index/task hunks in scope, complete commit delta matches tested source, identity/remote>
- Delivery handoff: <actual Conventional Commit, task branch and remote OID
  confirmation in chat; distinguish local commit, push and required CI outcomes>
