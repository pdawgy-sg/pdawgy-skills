---
name: dawg-init
description: Initialize or improve a repository's coding-agent guidance using dawg-plan, shared Dawg coding standards, AGENTS.md, CLAUDE.md delegation, and source-grounded architecture documentation. Use when preparing an existing repository or new directory for coding agents.
---

# Dawg Init

Make the current project easier for coding agents to work in. Learn the project
first, preserve its valid standards, and make Dawg the shared workflow.

## Inspect before prescribing

Resolve the user's intended target directory. Inspect Git state when Git exists,
including staged, unstaged, and untracked work; an ordinary directory needs no
Git initialization. Do not silently expand a subdirectory request to an entire
monorepo. Read applicable ancestor and nested instructions before proposing edits.

Inspect existing `AGENTS.md`, `CLAUDE.md`, `ARCHITECTURE.md`, README, manifests,
scripts, CI, representative source, and relevant tests. Identify actual language,
entry points, module boundaries, build/test commands, and established conventions.
Inspect enough code to understand the project; do not infer its architecture
from directory names alone. Preserve local work and nested instruction scope.

Ask focused questions about material missing intent, conflicting standards, or
unclear target boundaries. Resolve repository facts yourself. For an empty
directory, ask about the intended project when needed; do not choose a stack or
invent commands/components. Established facts do not need repeated confirmation.

## Run dawg-plan before initialization writes

Read and execute the bundled [dawg-plan workflow](../dawg-plan/SKILL.md) for the
initialization. Reuse a matching current plan when continuing the same task;
update it instead of creating a nested or duplicate plan. Include the intended
instruction changes, architecture work, and any separately gated cleanup in its
scope. Save its plan, state diagrams, checklist, and evidence in the target
project's `.dawgy/dwag-plan/FEATURE_<PLAN_NAME>/` directory.

Honor the full workflow, including `gpt-6-astra` and `gpt-6.1-sol` design reviews
at high effort. Do not write the target guidance files before the plan is ready.
If the sibling skill or required reviewers are unavailable, report the blocker;
continue inspection and drafting but do not invent a substitute review. Running
the skill authorizes requested guidance creation/updates; it does not authorize
the cleanup described below. Preserve any planning-only limit from the user.

## Establish shared, repository-specific guidance

Use the [AGENTS starting point](assets/AGENTS.md),
[CLAUDE delegation](assets/CLAUDE.md), and
[architecture starting point](assets/ARCHITECTURE.md). Adapt them to observed
facts; remove template prompts and unsupported sections from finished documents.

- **AGENTS.md:** The canonical coding guide for its scope. Include verified
  setup/check commands, code conventions, relevant scope-specific rules, small
  verifiable changes, and the Dawg workflow below. Keep architecture descriptions,
  feature inventories, plans, and historical evidence in their own documents.
  Preserve valid existing requirements; ask about conflicts instead of silently
  choosing a winner. Keep nested instructions scoped rather than copying local
  exceptions into a universal root rule.
- **CLAUDE.md:** When absent, create the small delegation file referring to the
  applicable `AGENTS.md`. When present, inspect and preserve its unique rules and
  workflow. Add a useful relative reference where compatible. Propose migration
  or deduplication separately; do not replace an existing file with a pointer and
  discard its content. Resolve contradictory instructions with the user first.
- **ARCHITECTURE.md:** Run the bundled
  [architecture maintenance workflow](../dawg-architecture-maintain/SKILL.md)
  against the chosen project, using the starting point where helpful. Document
  implemented structure and flows with source paths and supported rationale.
  Preserve unresolved decisions explicitly. Architecture maintenance must not
  recursively run initialization or restart the same plan.

Encode these Dawg coding standards in `AGENTS.md`:

- Use `dawg-plan` for features and fixes; clarify material uncertainty and keep
  tasks small with enough verification/evidence to prove they work.
- Keep code as simple as the behavior permits. Add complexity only for a concrete
  requirement. Do not add explanatory code comments; use clear names and code.
  Retain required license notices, interpreter/tool directives, and functional
  annotations. Existing comments are not an automatic deletion target.
- Use the repository's established tools and conventions. Do not invent commands
  or add frameworks merely to initialize agent guidance.
- Read `ARCHITECTURE.md` for design context. Use `dawg-architecture-maintain` in
  the same task whenever implemented changes affect components, interfaces,
  dependencies, data flow, or deployment. Check for relevance at feature/fix
  completion; an unchanged architecture needs no cosmetic edit. Report missing
  required skills rather than claiming their workflows ran.

## Identify cleanup automatically; apply it only after approval

During investigation, identify possible redundant files, instructions, code,
comments, or configuration. Check references, exports, dynamic loading, scripts,
tests, and user work before calling something redundant. A search with no matches
does not prove an item is unused.

In the plan, show a bounded cleanup proposal with exact paths/edits, supporting
evidence, expected impact, checks, and a recovery method. Present a concrete diff
where feasible, then ask the user to approve that list. Do not delete, move,
consolidate away, or mass-strip existing material on the strength of the initial
init request. Already approved exact changes do not need another approval.
Declined or unanswered cleanup remains pending; continue independent authorized
documentation work. Reassess changed candidates before applying approved edits.
Never use blanket reset/clean commands or remove dirty/untracked work as cleanup.

## Verify and hand off

Use the initialization plan's verification ledger. Inspect document diffs and
relative links; confirm project commands exist in source/configuration and label
anything not run. Check that useful original rules and nested scope survived,
CLAUDE delegation reaches AGENTS, and architecture claims match source. Rerunning
init should make no cosmetic changes to already accurate guidance. If approved
cleanup changes code, run only relevant focused checks and preserve results.

Save evidence under that plan's `verifications/`; follow dawg-plan's screenshot
save/share rules when screenshots are relevant. Link the plan, checklist, and
changed documents in chat. Report initialization, verification, and cleanup
approval/execution statuses separately so pending cleanup is visible.
