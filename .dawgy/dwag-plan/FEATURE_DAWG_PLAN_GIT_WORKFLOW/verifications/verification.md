# Verification: Git worktree delivery

Plan: [../PLAN.md](../PLAN.md)
Working directory: worktree root recorded in PLAN.md.
Execution: V1/V2 PASS. Implementation: VERIFIED. Delivery: PENDING (pre-delivery snapshot).

- [x] V1 — Two exact design reviews, source/UI/templates/links and validators (T1/T2; AC1–AC5; all transitions inspected).
- [x] V2 — Independent Git workflow evaluations using disposable local remotes (T1/T2; AC1–AC4; all transitions inspected and practical Git path exercised).
- [ ] V3 — Actual task verification, scoped commit and remote task branch OID (T3; AC3/AC5; TR12–TR20).

## V1 — Design and packaging

Both reviewers read revision 1 plan/checklist and current source, then after
implementation inspect changed skill, required Git reference, templates, caller
handoff and docs. Save returned findings/revisions/dispositions. A required review
failure blocks plan readiness; material remediation is reviewed by both.

Run from this worktree with installed skill-creator and existing temporary PyYAML:

```sh
for skill in dawg-plan dawg-init; do
  PYTHONPATH=/tmp/dawg-plan-validation-deps python /home/chy/.codex/skills/.system/skill-creator/scripts/quick_validate.py "plugins/pdawgy-skills/skills/$skill" || exit 1
 done
python -m json.tool .agents/plugins/marketplace.json > /dev/null
python -m json.tool plugins/pdawgy-skills/.codex-plugin/plugin.json > /dev/null
git diff --check
```

Parse changed agents/openai.yaml with PyYAML; resolve Markdown resource links from
their owning document and inspect paths in adapted templates at their target root.
Confirm manifest version 0.3.0 and current UI prompt/discovery consistency. Inspect
all new files for whitespace. Hash tested implementation files and save commands,
exits and results in validation.log. Check git diff --name-only against the task
scope and confirm no tracked historical .dawgy file changed.
Expected: valid skills/metadata, grounded documentation, unchanged earlier evidence.
Actual: both required reviewers approved revision 2 and final authored source
without material findings. Both validators and diff checks exit 0. UI YAML,
resource/root-document links, marketplace, version 0.3.0 and exact source scope
pass; no tracked historical evidence changed. All 11 implementation files have
recorded SHA-256 fingerprints.
Status: PASS. Evidence: validation.log, tested-source.json and both review records.

## V2 — Independent scenario execution

Each reviewer uses its own fresh /tmp root. The concrete shared request and
baseline/expected behavior are in [git-walkthrough.md](git-walkthrough.md).
Initialize an empty bare local remote
and a normal source fixture using git init --bare <root>/remote.git and git init
-b main <root>/source. For the fixture only, use local name/email `Dawg Fixture` /
`fixture@example.invalid`. Commit a tiny calc.py (`def add(a, b): return a + b`),
add origin pointing to the local bare repo, then leave unrelated tracked changes
and an untracked note in the source checkout. Create a task branch worktree from
committed HEAD, inspect its .git file/root/branch, implement a tiny bounded change,
run an actual assertion of its behavior, stage only task paths, commit with a
feat/fix Conventional Commit, and normally push that task branch. Compare
`git rev-parse HEAD` with `git ls-remote <remote> refs/heads/<task-branch>`.
Inspect source fixture bytes/status to prove dirty/untracked work was preserved.

Use the authored skill/reference to choose the sequence, not a separate invented
workflow. Review gates are already provided by this task; do not recursively
spawn fixture reviewers. Do not push to GitHub or change the real source repo.
Record exact executed commands and actual outputs in a report, plus code hashes.

Also inspect the authored instructions against these probes without fabricating
execution/approval: a new non-Git directory; an unborn repo with preexisting files;
a planning-only request; failed required check; missing identity; unknown or denied
remote; non-fast-forward rejection; existing task worktree resume with unrelated
staged files and mixed same-file hunks; caller init switching roots while mapping
a selected subdirectory to the same relative path; and final metadata receipt
without infinite commit recursion. Inspect the full proposed/created commit delta
and preserve any preexisting unrelated index entries rather than silently unstaging.
Expected: ask/wait on unapproved init or baseline, no broad staging/dirty loss,
no source-checkout implementation, no commit/push before passed checks, no force
or hook skip, no implicit main merge, correct final task branch remote OID. Record
limits and any material findings. A small local Git fixture and focused assertions
are enough; do not add a test framework or comprehensive Git failure simulator.
Actual: both reviewers executed the concrete isolated Git success path and
matched remote task OID to their Conventional Commit. Source dirty/untracked work
was preserved; resumed staged/mixed changes blocked delivery with index, HEAD,
working bytes and remote unchanged. Both verified selected-subdirectory mapping.
Astra corrected a diff-prefix comparison in its harness and retained the failed
attempt. No source defect was found. Nested fixture reviews and policy-only
failure branches were not executed or claimed.
Status: PASS. Evidence: evaluation/astra/REPORT.md and evidence/;
evaluation/sol/REPORT.md and evidence/.

## V3 — Actual feature delivery

Record worktree root, base, task branch and chosen origin. Run required V1/V2
checks. Stage only explicit task paths and this feature plan/evidence, inspect
`git diff --cached --stat` and `git diff --cached`, then commit using the message
in PLAN.md. Confirm tested implementation file hashes match committed contents.
No hook-induced changes may bypass revalidation. Push normally:

```sh
git push --set-upstream origin HEAD:refs/heads/codex/feature/dawg-plan-git-workflow
git rev-parse HEAD
git ls-remote origin refs/heads/codex/feature/dawg-plan-git-workflow
git status --short --branch
```

Expected: successful conventional feature commit, matching remote task branch OID,
clean task worktree, unchanged original checkout, no main push/merge. Implementation
logs are committed; final delivery receipt (commit/branch/remote confirmation) is
reported in chat rather than modifying tracked evidence after its own commit.
Actual checkpoint: correct worktree/branch/base/origin are recorded in
git-context.json. V1/V2 pass and GitHub push authentication dry-run exited 0.
Status: delivery PENDING until actual commit/push. Final actual receipt follows
in chat; the committed ledger remains an honest pre-delivery snapshot rather
than claiming its own future commit or push has already happened.
