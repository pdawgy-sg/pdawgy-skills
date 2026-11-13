# Dawg MR final source and independent forward evaluation

Reviewer: gpt-6-astra/high. Baseline: approved design revision 1. Authored package version: 0.6.0. Verdict: APPROVED; no material findings.

## Source and model correspondence

Reviewed the actual dawg-mr SKILL.md and agents/openai.yaml, plugin manifest, README and ARCHITECTURE. The instructions implement pinned committed scope, material ambiguity handling, committed blob/template/evidence reads, direct-consumer impact analysis, four requested message topics, and provenance-qualified pass/failure/unverified claims. They expressly separate runtime drafting from authoring dawg-plan/TLA/reviews, test execution, worktree/commit/push and MR publication. The UI is consistent and docs identify four skills. Version is 0.6.0.

All five formal-input hashes (runner, module, three configurations) still match my actual astra-01 execution. No material contract/model change was found, so those receipts remain applicable; no redundant TLC rerun was performed. The current-pass classification precondition is realized through evidence/source-identity checks. Practical Git preservation and prose fidelity remain outside the finite model and were examined below.

## Actual bounded invocation

Request: “Use $dawg-mr to quickly draft an MR message for these committed changes.” I followed the actual authored skill as the drafting agent. Local setup created a small average/summary example; test commands were actually executed during fixture preparation to generate truthful evidence, then committed. Setup and runtime commands are separated in the evidence.

The repository instruction selects main. I pinned base 3550b821faa436389688c9d5b45101b4fbb39033 and head 85dde0f8bc9e3929e56443088ebb842f6398a614, calculated merge-base, inspected log/stat/diff and committed source/template/records. Runtime never executed tests. The checkout held a staged return999 change, unstaged secret_feature consumer, and untracked unsupported “ALL TESTS PASSED” claim. None entered the actual draft.

Actual output is draft.md, following the four committed template headings. It describes empty input returning zero, identifies the direct summary consumer and the exception-to-zero compatibility change, and distinguishes:

- Current empty-summary check: real recorded exit 0; source/test hashes match committed blobs.
- Current legacy-exception check: real recorded exit 1; failure retained explicitly, not repaired or waived by this drafting task.
- Historical nonempty check: real exit 0 on the prior implementation; stale hash identified, no current passing claim. Remaining check is stated without running it.

The draft separates recorded author execution from current source/evidence inspection. evidence-applicability.json contains actual hash comparisons and commands.

## Empty and ambiguous cases

empty.md is the actual no-change response for explicitly identical pinned base/head. It reports no committed changes, does not invent problem/fix content, and excludes dirty work.

ambiguous.md is the actual focused clarification for a separate repository with release-a and release-b producing materially different scopes and no target guidance/remote. No draft or HEAD^ fallback is produced. The question names the alternatives and concrete difference. An initial two-branch fixture had identical target commits, so it was inadequate to establish material scope ambiguity; its observations were preserved and a fresh ambiguous-material fixture was created. Only the latter is claimed as the material-ambiguity test. This fixture refinement is not a discovered skill defect.

## Preservation and evidence

Full file-content fingerprints, including .git index, refs, objects, logs and config, match before/after/final for both evaluated scenarios. Captured status, staged/unstaged diffs and complete committed/working-copy snapshots show distractor preservation. No plugin implementation source was edited; no network, MR/push, nested agents/reviews, or runtime test execution occurred. Local fixture setup commits are outside runtime and task source.

Files: draft.md, empty.md, ambiguous.md; evidence/setup-commands.json, runtime-commands.json, ambiguous-material-setup/runtime.json, evidence-applicability.json, snapshot-read-commands.json, *-before/after/final.json, fixtures/ committed and working-copy snapshots, and approved-source-hashes.json. The small setup/read scripts are preserved for reproducibility; no framework or plugin dependency was introduced.

Limits: one reviewer interpretation of the authored instructions on small controlled fixtures, not a guarantee across all future agents/repositories. Real Git state and current/stale/failed evidence were exercised; publishing/network integration was intentionally outside scope. Formal checks prove the bounded abstract protocol, not arbitrary Git interpretation or prose. Packaging validation is parent-owned and not independently rerun here.
