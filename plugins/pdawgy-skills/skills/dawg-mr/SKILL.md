---
name: dawg-mr
description: Quickly review committed Git changes and draft a merge request or pull request message covering the problem, fix, blast radius, and verification evidence. Use when asked to write an MR/PR description or summarize committed work for review.
---

# Dawg MR

Produce a concise, copy-ready MR message grounded in committed changes. This is
read-only drafting: preserve the checkout, index, refs and files. Do not initialize
Git, create a worktree, commit, push, or create/update an MR unless separately
requested. Do not invoke dawg-plan, model checking, reviewers, or tests merely to
write the message.

## Establish the committed scope

Read applicable repository instructions and any relevant MR/PR template. Confirm
Git context and available commits. Honor a user-specified base/head, range, or
commit selection; resolve refs to immutable commit IDs before inspection.

For a branch summary, use the established MR target, repository guidance, or an
unambiguous integration branch as the comparison base. Compute its merge-base
with the selected head (default `HEAD`) and review that committed diff and log.
An upstream tracking the same feature branch is not an integration base. If the
base is materially ambiguous or required commits are unavailable, ask a focused
question instead of guessing `HEAD^`. Report when local refs may be stale; do
not silently fetch or change refs. If there are no committed changes in scope,
say so without inventing a problem or fix.

Identify the pinned comparison/head briefly with the draft. Exclude staged,
unstaged and untracked work. Use the committed diff and `git show <commit>:<path>`
for relevant source, templates and evidence so dirty files cannot contaminate the
summary. Commit subjects provide context, not proof of behavior or test results.

## Inspect changes and evidence

Start with the scoped log, diff stat and actual diff; follow relevant entry points
and direct consumers only as needed to understand the behavior and impact. Avoid
an exhaustive repository audit. Describe the aggregate change, including removals
and compatibility effects, rather than narrating every commit or file.

Inspect available verification records for this change. For each material claim,
identify the command/check, observed result, tested revision or source identity,
and evidence source. Distinguish recorded CI/agent/author results from checks
independently run in the current session. Added test code is not evidence it ran.
A passing historical log, copied fixture, unrelated check, or dirty-checkout run
does not establish that the committed change passes. Explain its scope or mark
it stale/unconfirmed. Preserve known failures, skipped checks and blockers in the
message; do not turn absent evidence into a passing claim. If no applicable run
is evidenced, say `Not run / no applicable execution evidence found` and identify
useful checks still needed. Do not launch a test suite just to fill this section.

## Draft the message

Follow the repository's MR template when present while covering all four topics.
Otherwise provide a short title and these sections:

- **Problem** — The concrete limitation, failure or user need motivating the
  change. Mark inferred intent as inference; ask only if missing intent materially
  changes the message and cannot be resolved from the committed artifacts.
- **Fix** — What changed and the resulting behavior, using a before/after example
  when useful. Summarize the final implementation, not the development history.
- **Blast radius** — Affected components, callers and interfaces, plus relevant
  compatibility, data/configuration, dependency or deployment effects. Ground
  impact in the diff and inspected consumers. State meaningful unknowns; do not
  promise no impact or claim unrelated areas were verified.
- **Verified / tested** — Actual checks and outcomes with concise evidence or
  command pointers and revision/provenance. Include failures and testing gaps;
  distinguish inspection from execution and record when nothing was rerun.

Keep it proportional to the change and ready to paste. Link relevant evidence
when available, omit unsupported claims, and return the message in chat. Drafting
alone does not authorize publishing or modifying an existing MR.
