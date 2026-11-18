---
name: dawg-plan
description: Plan features, fixes and refactors in Git worktrees with TLA+ checks, state diagrams and host-aware independent review (Sol/Astra in Codex, Sonnet/Opus in Claude Code; one reviewer for small work, two for large work). During authorized implementation, record failures and repair/reverify until required checks are green before Conventional Commit and push. Use when planning a feature, fix or refactor or explicitly asked to use dawg-plan.
---

# Dawg Plan

Understand what the user is building before choosing an implementation. Produce a
plan another coding agent can execute and verify with inspectable evidence.

## Require Git and a task worktree

Read and follow [the Git workflow](references/git-workflow.md) on every invocation.
It defines required preflight, worktree/scope mapping, and verified delivery.
Before creating plan artifacts or implementing a feature/fix/refactor, confirm Git context
and create or reuse its dedicated task worktree and branch. Outside Git, ask the
user to initialize and wait for consent; do not silently initialize or proceed.
Preserve an originally selected subdirectory by mapping it into the worktree.
Tell callers the worktree repository root and mapped project directory, and use
that mapped project for subsequent work. Do not implement in the source checkout.

## Route phases through the active host

Identify the host from trusted session context and the active delegation API.
If the host remains unknown, ask before dispatch. The calling agent coordinates
all phases, including Git preflight, worktree mapping, user clarifications,
readiness and audited Git delivery. It launches distinct sibling workers in the
same mapped task worktree. Each worker follows its assigned phase and returns to
the coordinator without recursively routing the workflow or spawning workers.

| Phase | Codex model | Effort |
| --- | --- | --- |
| Planning and author TLC | `gpt-6.2-astra` | high |
| Primary independent review | `gpt-6.2-sol` | high |
| Additional review, large only | `gpt-6.2-astra` | high |
| Authorized implementation and verification | `gpt-6.2-sol` | medium |

In Codex, the coordinator uses `collaboration.spawn_agent` for each worker with
explicit `model`, `reasoning_effort` and `fork_turns: "none"`. Include the phase
role in the task and use separate contexts for planner, reviewers and implementer,
including when two roles use the same model.

| Phase | Claude Code qualified agent type | Model | Effort |
| --- | --- | --- | --- |
| Planning and author TLC | `pdawgy-skills:dawg-planner` | `claude-opus-5-5` | high |
| Primary independent review | `pdawgy-skills:dawg-review-sonnet` | `claude-sonnet-5-5` | high |
| Additional review, large only | `pdawgy-skills:dawg-review-opus` | `claude-opus-5-5` | high |
| Authorized implementation and verification | `pdawgy-skills:dawg-implementer` | `claude-opus-5-5` | medium |

In Claude Code, select these exact native `Agent` types as non-fork siblings.
Omit per-invocation `model` and `effort` overrides so their definition pins apply.
A per-call family alias can replace a full-version pin. Verify requested and
effective model/effort using host metadata (including `/tasks` when available)
and applicable overrides. Record provider-specific equivalent IDs only with
evidence they resolve to the same 5.5 model. See the
[subagent model/effort rules](https://code.claude.com/docs/en/sub-agents).

For each handoff, supply the complete user requirements, confirmed decisions,
applicable instructions, role, worktree root and mapped project, source scope,
constraints, current plan/revision and evidence paths. Record the distinct worker
context, requested identity/effort and supporting dispatch evidence. In Codex,
check effective identity/effort against any available trusted runtime metadata.
If no separate effective values are exposed, record the successful explicit
dispatch and the metadata limit without claiming independent confirmation.
A forced fallback, known model/effort mismatch, missing required definition or
unavailable required execution blocks the affected phase. Keep inherited
permissions and use the shared worktree without extra isolation, provider bridges
or user-global setting changes.

The planner authors the plan and checklist, runs author TLC and returns artifacts,
questions and findings. The coordinator relays material questions to the user and
returns answers to the planner. After the author checks pass, the coordinator
dispatches the size-required independent reviews, each with its own TLC run.
The planner's author run does not count as a review. A coordinator run cannot
substitute for the planner's author run or a reviewer's run.

Planning-only requests stop at the reviewed plan. After readiness and
authorization, the coordinator dispatches a separate implementer. Callers such
as dawg-init reuse the same workers and coordination cycle.

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
    ├── verification.md
    ├── failures.md
    └── tla/
        ├── <Module>.tla
        ├── <Model>.cfg
        └── runs/
```

Use `FIX_` for a bug fix and `FEATURE_` for new behavior or a refactor, followed by a concise
uppercase underscore-separated name, for example `FIX_RETRY_DUPLICATE_SUBMIT`.
The directory is deliberately spelled `dwag-plan`; the skill is `dawg-plan`.
Use `verifications/` consistently for all evidence, including screenshots.
Reuse the matching plan when continuing the same work. Inspect existing artifacts
before editing; never overwrite an unrelated plan or discard existing evidence.
Choose a distinguishing suffix for a different task with a colliding name.

Read and adapt [the plan template](assets/PLAN.md) and
[the verification template](assets/verification.md). Replace template prompts
with concrete content. Keep the plan and checklist synchronized as scope changes.
Create `verifications/failures.md` from [the failure register](assets/failures.md)
when implementation/verification begins; leave it honestly empty if no failures
are observed. Link issue IDs to tasks and checks, preserving all attempt evidence.
If project-root access is unavailable, report the blocker and provide a draft;
do not claim the artifacts were saved.

## Model the feature, fix or refactor as a state machine

Every plan includes at least one fenced Mermaid `stateDiagram-v2` diagram in
`PLAN.md`, also shown in chat so the user can inspect the proposed flow.

Model the actual product or system behavior, not just the agent's work stages.
Identify initial and terminal states, triggers, guards, effects, failure states,
and recovery paths where applicable. Cover cancellation, retries, concurrency,
and authorization only when relevant to the feature, fix or refactor. For stateless work,
model observable input, validation, and outcome states instead of inventing a
persistent state store. Multiple diagrams are useful only for distinct flows.

Give transitions stable IDs (`TR1`, `TR2`, ...) in the diagram labels and a short
transition table. State invariants that must remain true. Map each transition
and acceptance criterion to a verification item. One meaningful check may cover
several transitions; do not create a separate test merely for every arrow.

## Verify every plan with TLA+

Read and follow [the required TLA+ workflow](references/tla-verification.md).
Every plan includes a concrete TLA+ model/configuration of the requested behavior,
mapped acceptance criteria/actions/properties, stated assumptions and finite bounds,
and completed TLC checks. Keep diagrams and the model consistent. The author and every required
reviewer must actually run the same final model/configuration; an opinion or
inspection of someone else's log does not satisfy independent execution.

Save reproducible logs, tool/input identities, state statistics, and relevant
counterexamples under `verifications/tla/`. Missing tools, incomplete exploration,
required-property violations, or stale/missing runs block readiness. Report bounded
model-checking results separately from implementation tests; neither a diagram nor
a generic process model proves an unrelated product feature works.

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

## Select independent reviewers by host and change size

Before reviewer delegation, confirm the active execution host and classify the
fix, feature or refactor as **small** or **large**. Record the host, tier, concrete
rationale and required model/effort set in `PLAN.md`.

- **Small:** A narrow, well-understood behavioral change with limited impact and
  straightforward focused verification. Repeating one policy across documentation
  or templates does not by itself make a change large.
- **Large:** Interacting changes across components, broad refactoring, or meaningful
  architecture, public-interface, data/migration, security, concurrency, or
  deployment risk. Judge impact and uncertainty, not just file/line counts.
  Investigate unclear scope; use the large tier when material size/risk uncertainty
  remains. Resolve unclear product intent through the normal questions workflow.

| Active host | Small work | Large work |
| --- | --- | --- |
| Codex | `gpt-6.2-sol` / high only | `gpt-6.2-sol` + independent `gpt-6.2-astra`, both high |
| Claude Code | Sonnet 5.5 / high only | Sonnet 5.5 + independent Opus 5.5, both high |

Use only the host's primary reviewer for small work. Add its second reviewer for
large work, concurrently when supported. An explicit user reviewer choice
supersedes these defaults when the required execution is available. Reassess
scope/risk growth: revoke readiness and add Astra in Codex or Opus in Claude Code
before proceeding. Do not silently drop a required reviewer or downgrade merely
to avoid review. A host change also revokes readiness. Repeat planning, author
TLC and the required reviews using the new profile. Previous-provider receipts cannot satisfy it.

After the planner returns the concrete plan, checklist, TLA+ inputs and passing
author TLC results, the coordinator spawns the selected reviewers.
Use the host's phase dispatch and identity rules above. Each reviewer must be
independent of the planner and all other reviewer contexts.
Give every required reviewer the same current requirements, confirmed decisions,
repository context, plan/checklist, formal inputs and author evidence. Each
independently reviews intent, transitions/invariants, task boundaries, acceptance
coverage, reproducibility and excessive testing/scope.

Every required reviewer must actually run TLC with fresh private state/log paths,
audit enabled properties/raw outputs, and assess abstraction, assumptions, bounds,
relevant liveness/deadlocks, reachability and requirement mapping. Require its own
tool/input hashes, commands, results and actionable findings or no material findings.
Keep project source unchanged and preserve separate reviewer evidence. Do not treat
another agent's log or a shared runner summary as independent execution/review.

Wait for every required review. Save model/effort, reviewed revision and findings
in host-specific records: Codex uses `verifications/design-review-sol.md` and,
for large work, `design-review-astra.md`; Claude Code uses `design-review-sonnet.md`
and, for large work, `design-review-opus.md`, all under `verifications/`. For small
work mark the additional host reviewer not required, not missing/pending, and do
not claim it ran. Record findings/dispositions in
`PLAN.md`; resolve material findings and return missing product decisions to the
user. Reuse required reviewers for reassessment after material design changes.

Material requirement, behavior, model/dependency, config/property/bound/assumption
or fairness changes invalidate the author's and every required reviewer's receipts:
rerun/review on identical final inputs. If only the required set expands and
reviewed inputs are unchanged, retain valid current receipts and obtain the
missing host-specific reviewer execution and semantic review. Readiness requires the current author
run, every tier-required reviewer's current run and semantic approval, and no
unresolved material findings.

Unavailable required models/effort/delegation/TLC execution block readiness;
record the exact dependency and tell the user. Missing the optional second
reviewer does not block small work. Do not silently switch host profiles,
substitute models or invent reviews. Continue independent
drafting/investigation while a genuine required dependency remains blocked.

## Preserve evidence through implementation

Planning alone does not authorize implementation. If the user has already
authorized implementation, proceed after the plan is ready without requesting
redundant approval. Otherwise deliver the reviewed plan and checklist.
The coordinator dispatches the host's medium-effort implementation worker with
the ready plan, mapped worktree, source scope, authorization and evidence paths.
That worker implements, verifies and repairs within scope, then returns the
current evidence and source changes for the coordinator to audit and deliver. A
material design gap pauses implementation. The coordinator returns the gap to
the high-effort planner, revokes readiness and obtains fresh author TLC and
required independent TLC runs and semantic approvals before resuming implementation. Ordinary in-scope
repairs stay with the implementer.

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
are failing, blocked, or not run. If checks expose a design gap, return it to
the coordinator for renewed planning and review before proceeding.

## Record and repair until green

Follow [the recovery loop](references/recovery-loop.md) during implementation and
verification. An observed non-green check is work to resolve, not a completed
handoff: promptly record the failure/blocker and evidence, diagnose its cause,
apply an authorized correction, rerun the failed and affected checks, and repeat
until the current phase's required checks pass with no unresolved issues.

Preserve stable failure IDs and failed attempts; reopen recurrences. A patch or a
single lucky rerun does not establish resolution. Invalidate affected old passes
when tested inputs change. Do not weaken, skip, waive or overwrite checks/history
to manufacture green. Apply the gate to the current phase: planning-only requests
do not require tests for unimplemented features, and declared negative probes pass
only on their exact expected outcomes.

Use existing authorization for ordinary repairs and reruns. For a genuine missing
permission, user decision or external dependency, record what is needed, ask early,
and continue independent authorized work. Keep unresolved checks visibly blocked;
do not claim completion or delivery, bypass authority, or blindly repeat an
unchanged failing command. Resume the loop when the dependency is resolved.

## Commit and push verified implementation

After the authorized implementer returns current verification evidence and source
changes, the coordinator follows [the Git workflow](references/git-workflow.md).
Audit required checks and inspect the entire index and proposed commit. Create a
task-only Conventional Commit,
confirm its delta/source matches the verified change, and push normally to the
task branch. Confirm the remote branch equals local HEAD. Preserve
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
Report the TLA+ properties/bounds, actual run outcomes and formal limitations
alongside implementation evidence and delivery, without claiming a general proof
of code correctness.
