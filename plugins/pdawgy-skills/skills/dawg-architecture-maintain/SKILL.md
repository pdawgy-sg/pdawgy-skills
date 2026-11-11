---
name: dawg-architecture-maintain
description: Create or synchronize ARCHITECTURE.md with implemented repository structure and flows. Use when documenting architecture drift or completing changes to components, interfaces, dependencies, data flow, or deployment.
---

# Dawg Architecture Maintain

Keep `ARCHITECTURE.md` accurate as code evolves. Document what exists and why;
leave coding instructions in `AGENTS.md`.

## Establish the current architecture

Resolve the requested repository/directory scope and read applicable instructions,
existing architecture/design documentation, and relevant source. Inspect Git
changes when available, including staged, unstaged, and untracked code; do not
discard user work. In a directory without Git, inspect files directly. A diff
can guide investigation but is not a substitute for tracing actual boundaries.

Follow entry points, imports and calls, public interfaces, storage, external
dependencies, configuration, and deployment where relevant. Verify paths and
claims against code/configuration. Separate implemented facts, supported design
rationale, inferences, and future proposals. Existing documentation is evidence
of stated intent, not proof that the implementation still matches it.

Ask about material design ambiguity or conflicting intent before presenting it
as settled. Do not ask the user to resolve facts already visible in code. A
missing stack or empty directory is not permission to invent a product design.
Record the verified baseline and open decisions; ask what is needed for further
specificity.

## Update the architecture document

Create `ARCHITECTURE.md` if absent. Keep only useful sections: current purpose,
major components with source paths, boundaries/interfaces, significant control
and data flows, dependencies/runtime context, constraints, and supported design
decisions. Omit unsupported or irrelevant sections. Add a diagram only when it
clarifies a real flow. Keep the document useful to the next coding agent rather
than turning it into an exhaustive file inventory.

When updating an existing document, preserve accurate rationale and intentional
scope. Correct stale descriptions using observed implementation. If code and a
documented design conflict materially, surface the discrepancy; describe current
code without inventing intent, and ask before declaring the old decision obsolete.
Keep unresolved intent visible. Keep plans and proposed architecture separate
from implemented descriptions. Do not rewrite code to make it match the document.

Routine synchronization is the authorized documentation task: it does not need
a fresh dawg-plan cycle, background watcher, repository initialization, or new
infrastructure. When called by `dawg-init` or an implementation task, reuse its
scope, plan, and evidence directory; do not invoke init or recursively restart
planning. If the user is requesting a new feature/refactor rather than a factual
documentation sync, run the bundled [dawg-plan workflow](../dawg-plan/SKILL.md)
for that change and keep the proposal out of implemented architecture until built.

Edit only architecture documentation in scope. Moving/deleting other documents,
removing purportedly redundant code, or consolidating away unique material needs
a concrete proposal and user approval. A routine correction of stale architecture
facts is part of the requested synchronization, not a new cleanup campaign.

## Verify and keep it current

Read the completed document against source. Check referenced paths, important
interfaces and flows, and any diagrams. Explain which claims changed and what
supports them. Do not run broad application tests solely for a documentation
edit; use source inspection and relevant existing doc checks when sufficient.

If the document is already accurate, preserve its bytes and report a verified
no-op. Avoid timestamps or cosmetic rewrites just to show activity. Repeated runs
against unchanged evidence should not produce churn. Ask about genuine new
uncertainty instead of guessing to force completion.

Use a calling task's verification ledger when one exists; record inspected
source, changed claims, checks, and remaining questions there. For a standalone
sync, report those observations directly in chat without creating a planning
ceremony. Link the architecture document and any saved evidence. Save/share
screenshots under the calling plan's `verifications/` when applicable.

Architecture stays current through this skill's use in relevant coding tasks and
the maintenance rule in generated `AGENTS.md`. Do not claim an unattended process
was installed or that future documentation updates happen without agent work.
