---
name: dawg-plan
description: Plan software features and fixes in dedicated Git worktrees with clarifying questions, state diagrams, verifiable tasks, and independent reviews. After authorized implementation, verify, conventionally commit, and push the task branch. Use when planning a feature or fix or explicitly asked to use dawg-plan.
---

# Dawg Plan

Understand what the user is building before choosing an implementation. Produce a
plan another coding agent can execute and verify with inspectable evidence.

## Require Git and a task worktree

Read and follow [the Git workflow](references/git-workflow.md) on every invocation.
It defines required preflight, worktree/scope mapping, and verified delivery.
Before creating plan artifacts or implementing a feature/fix, confirm Git context
and create or reuse its dedicated task worktree and branch. Outside Git, ask the
user to initialize and wait for consent; do not silently initialize or proceed.
Preserve an originally selected subdirectory by mapping it into the worktree.
Tell callers the worktree repository root and mapped project directory, and use
that mapped project for subsequent work. Do not implement in the source checkout.

## Understand the intended behavior

1. Read the request, applicable repository instructions, and relevant code or
   documentation. Identify the user's goal, current behavior, desired behavior,
   affected users and entry points, constraints, and boundaries.
2. Resolve facts available in the repository yourself. Ask the user focused,
   concrete questions about missing intent, conflicting requirements, or choices
   that change observable behavior, acceptance criteria, or architecture. Keep
   asking follow-ups until these material gaps are resolved; do not silently
   guess. Continue independent investigation while awaiting answers.
3. Restate the intended outcome and define observable acceptance criteria with
   stable IDs (`AC1`, `AC2`, ...). Record confirmed decisions, relevant constraints,
   and explicit exclusions. A fix includes a reproducible failure or an honest
   description of why reproduction is currently blocked.
4. Separate harmless implementation choices from unresolved product decisions.
   Record reasonable low-impact assumptions. Do not add speculative requirements
   or ask the user to confirm facts already established in the session. A draft
   with unresolved material questions stays blocked, not ready for execution.

## Save the plan in the target project

Always create these artifacts under the mapped project directory in the task
worktree, not in the source checkout or installed skill's directory:

```text
.dawgy/dwag-plan/<FIX|FEATURE>_<PLAN_NAME>/
├── PLAN.md
└── verifications/
    └── verification.md
```

Use `FIX_` for a bug fix and `FEATURE_` for new behavior, followed by a concise
uppercase underscore-separated name, for example `FIX_RETRY_DUPLICATE_SUBMIT`.
The directory is deliberately spelled `dwag-plan`; the skill is `dawg-plan`.
Use `verifications/` consistently for all evidence, including screenshots.
Reuse the matching plan when continuing the same work. Inspect existing artifacts
before editing; never overwrite an unrelated plan or discard existing evidence.
Choose a distinguishing suffix for a different task with a colliding name.

Read and adapt [the plan template](assets/PLAN.md) and
[the verification template](assets/verification.md). Replace template prompts
with concrete content. Keep the plan and checklist synchronized as scope changes.
If project-root access is unavailable, report the blocker and provide a draft;
do not claim the artifacts were saved.

## Model the feature or fix as a state machine

Every plan includes at least one fenced Mermaid `stateDiagram-v2` diagram in
`PLAN.md`, also shown in chat so the user can inspect the proposed flow.

Model the actual product or system behavior, not just the agent's work stages.
Identify initial and terminal states, triggers, guards, effects, failure states,
and recovery paths where applicable. Cover cancellation, retries, concurrency,
and authorization only when relevant to the feature or fix. For stateless work,
model observable input, validation, and outcome states instead of inventing a
persistent state store. Multiple diagrams are useful only for distinct flows.

Give transitions stable IDs (`TR1`, `TR2`, ...) in the diagram labels and a short
transition table. State invariants that must remain true. Map each transition
and acceptance criterion to a verification item. One meaningful check may cover
several transitions; do not create a separate test merely for every arrow.

## Break work into small, verifiable parts

Define bounded tasks (`T1`, `T2`, ...) in dependency order. Each task specifies:

- The behavior or artifact delivered, relevant code locations, and dependencies.
- Its acceptance criteria and relevant transitions or invariants.
- The smallest sufficient verification: an exact runnable command, concrete UI
  procedure, or artifact inspection, with expected observable results.
- Where to save evidence under `verifications/` and what proves completion.

Prefer existing focused tests and tooling. Add regression tests when needed to
demonstrate a fix or protect meaningful behavior. Use direct checks or a short
manual flow for low-impact changes when sufficient. Avoid tests that mirror
implementation details, arbitrary coverage goals, duplicate checks, or new test
frameworks without a concrete need. Include realistic failure behavior and a
relevant regression boundary, without inventing irrelevant edge cases.

Specify prerequisites, working directory, fixtures, and any cleanup needed to
rerun checks. A plan must be independently executable; instructions like "test
it" or "verify it works" are insufficient. Use repository-supported commands;
label a command that cannot yet be confirmed and explain what must resolve it.

## Require two independent design reviews for every plan

After drafting the concrete plan and checklist, spawn exactly two design review
subagents, concurrently when supported:

- `gpt-6-astra` at `high` reasoning effort.
- `gpt-6.1-sol` at `high` reasoning effort.

Use the runtime's subagent tool with explicit model and effort selections. If
using `collaboration.spawn_agent`, set `fork_turns: "none"` so the overrides can
be applied. Give each reviewer the same user requirements, confirmed decisions,
relevant repository context, and paths to the draft plan and checklist. Ask each
to independently inspect intent alignment, state transitions and invariants,
task boundaries, acceptance coverage, reproducibility of evidence, and excessive
testing or scope. Require actionable findings with severity and file references,
or an explicit statement that no material issues were found. Reviewers should
read and report without editing project files or running unsafe checks.

Wait for both reviews. Save each returned review, its model and effort, and the
reviewed plan revision under `verifications/design-review-astra.md` and
`verifications/design-review-sol.md`. Record findings and their dispositions in
`PLAN.md`. Resolve material findings; return product decisions to the user when
needed. After a material design change, have both reviewers reassess the updated
design; reuse the two reviewers rather than spawning additional reviewers.
Keep review records current with the final design. Readiness requires both
reviews completed and no unresolved material findings.

If either exact model, effort selection, or delegation is unavailable, record
which requirement is blocked and tell the user. Do not substitute models, invent
reviews, or mark the plan ready. Continue independent drafting and investigation
that do not depend on the unavailable review.

## Preserve evidence through implementation

Planning alone does not authorize implementation. If the user has already
authorized implementation, proceed after the plan is ready without requesting
redundant approval. Otherwise deliver the reviewed plan and checklist.

Use `verifications/verification.md` as the execution ledger. Each verification
has a stable ID (`V1`, `V2`, ...), linked tasks and acceptance criteria/transitions,
procedure, expected result, actual result, evidence paths, and status. Use
`NOT RUN`, `PASS`, `FAIL`, or `BLOCKED`; leave checklist boxes unchecked until
the actual check passes. Planned evidence paths and a successful design review
are not implementation evidence. Preserve failed results and rerun history.

When executing authorized work, run the planned checks and save relevant output,
observed behavior, or screenshots under `verifications/`. Record the tested code
revision (and uncommitted changes when present), environment, command/procedure,
and exit status or observed result so another agent can reproduce the finding.
Exclude credentials and private data from saved evidence. Do not claim a check
ran when a tool or environment prevented it. Mark it blocked with a concrete
reason and next action. Keep the overall work unverified while required checks
are failing, blocked, or not run. If checks expose a design gap, update the plan
and obtain the required updated reviews before proceeding on the changed design.

## Commit and push verified implementation

After authorized implementation, automatically follow the delivery steps in
[the Git workflow](references/git-workflow.md): pass all required checks, inspect
the entire index and proposed commit, create a task-only Conventional Commit,
confirm its delta/source matches the verified change, and push normally to the
task feature/fix branch. Confirm the remote branch equals local HEAD. Preserve
planning-only and explicit no-commit/no-push limits. Never deliver while required
checks fail or remain blocked; report commit/push blockers separately from
implementation verification. Final commit/remote receipts belong in the chat
handoff, avoiding a tracked receipt that would need to contain its own commit ID.

On completion, link `PLAN.md`, the checklist, and relevant evidence in chat.
Summarize passed checks and any limitations. If evidence includes screenshots,
save them inside `verifications/` and display them in chat with Markdown image
embeds using absolute local paths. For large sets, group screenshots in multiple
messages so each is shared. Distinguish a ready plan from verified implementation;
also distinguish committed work from confirmed remote delivery. Include the
worktree path, task branch, verification results, Conventional Commit hash, remote
branch confirmation, and any outstanding blocker. Retain the worktree and branch
for review; do not implicitly merge into the base branch or remove the worktree.
