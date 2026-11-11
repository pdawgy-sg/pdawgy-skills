# Astra final-source review and bounded Git walkthrough

Reviewer: gpt-6-astra / high. Baseline: approved FEATURE_DAWG_PLAN_GIT_WORKFLOW plan revision 2. Date: 2026-11-12.

## Design result

No material findings in the authored change. Reviewed dawg-plan main instructions, required Git reference, both templates and UI metadata; dawg-init handoff and AGENTS asset; root AGENTS, README, ARCHITECTURE; and plugin manifest version 0.3.0. The eleven reviewed file hashes are saved in evidence/reviewed-source-hashes.json.

The source preserves exact dual reviewers and user-intent/verification requirements while enforcing linked worktrees, selected-target mapping, non-Git/unborn consent, and explicit delivery limits. The required reference checks actual root/branch again before delivery, rejects bare repositories as editable project roots, blocks unresolved unrelated index/mixed-hunk state, checks the full created commit, and requires normal task-branch push plus exact OID confirmation. dawg-init adopts the mapped target and delegates delivery without a duplicate plan cycle. Routine architecture synchronization remains focused. Templates distinguish verified implementation from pre-delivery evidence and a later chat receipt.

The reviewed remedies from revision 2 are present: source/target-relative/worktree/mapped roots remain separate, and the whole index and mixed changes are guarded rather than relying on path staging alone.

## Executed bounded success path

All fixture Git operations and the sole push stayed under `/tmp/dawg-git-astra-eval`, using its local bare remote. The baseline used exactly calc.py, config.txt and packages/app/README.md from the shared walkthrough, with repository-local fixture identity. The source retained dirty config.txt (`mode=user-wip`) and untracked notes.txt (`keep this note`).

Created a linked worktree at task-worktree on `codex/feature/subtract` from committed baseline. Confirmed its `.git` is a file, actual Git root/branch match recorded values, source uncommitted changes were absent from the task checkout, and no existing task branch/path was overwritten.

Added subtract while preserving add. Executed Python with bytecode writes disabled and actual assertions `add(2, 3) == 5` and `subtract(7, 4) == 3`; exit 0. Checked whitespace, the entire index, worktree changes, identity, staged path set and content. Staged only calc.py. Inspected the whole staged delta before committing.

Created `feat(calc): add subtraction`. Inspected the entire created delta and verified that only calc.py changed and its committed blob and SHA-256 matched the tested source. Normally pushed `HEAD:refs/heads/codex/feature/subtract` with upstream tracking to the local remote, exit 0. Local HEAD exactly matched the remote branch OID, and this was the remote's only branch. The source's file hashes, dirty diff/status, index and main HEAD remained unchanged; there was no main push or merge. The task worktree was clean immediately after delivery.

Fixture delivered commit: `9889934fade11f02bcf46693ddd905d0545fec6c`.

The fixture has no required CI. No hook bypass, force push, reset, clean, or implicit worktree removal was used. The receipt is outside both versioned fixture repositories, so it does not require a commit containing its own ID.

## Preserved evaluation failure and correction

One evaluation assertion initially compared the complete text of unstaged and staged diffs. Host Git uses mnemonic prefixes: the same content appeared with i/w prefixes before staging and c/i prefixes afterward. This presentation-sensitive comparison failed; no commit or push occurred until it was resolved. The full staged patch showed no unexpected content. Replaced that comparison with staged blob identity, tested-source SHA-256, exact changed-path checking, and full-delta inspection. Those checks passed before commit.

This is an evaluator check correction, not a product failure or a hidden bypass. evidence/verification-history.json preserves the failure and resolution; commands.jsonl retains the actual differing outputs. The feature behavior assertion passed and the tested source did not change.

## Executed resumed-worktree blocker

After successful delivery, explicitly seeded preexisting user work for the required probe: unrelated config.txt and add-function edits in the index, plus a separate unstaged subtraction edit in the same calc.py path. This setup staging is distinguishable from the subsequent skill response.

Reused and inspected the existing task worktree/root/branch rather than creating another. The authored whole-index/mixed-hunk rule identified unresolved ownership and blocked further delivery. No isolation/discard authorization was supplied. After that decision, no staging, unstaging, reset, commit or push was performed.

Before/after HEAD, full cached diff, working diff, index entries, worktree file hashes, original source hashes, and remote task OID were identical. The deliberate dirty state remains in place; it is not falsely described as the verified/pushed revision. The earlier successful remote commit remains unchanged.

## Selected-subdirectory probe

Read-only mapping for an init request at source/packages/app yields task-worktree/packages/app as mapped project, with artifacts under that directory's `.dawgy/dwag-plan/FEATURE_INITIALIZE_APP/` and guidance files directly in the mapped app directory. Git operations use the worktree repository root; project commands use the mapped app directory. No root-level init files were created.

Checked mapped repository/package/app ancestor instruction locations: this tiny fixture has no AGENTS.md files. The workflow requires reading applicable ancestors and nested scopes when present. No fictitious instruction scope was invented. This is path inspection only; a genuinely separate init task still needs its own matching task branch/worktree and cannot appropriate the subtraction task merely because the path exists.

## Policy-only probes

Read the required Git reference and callers against these scenarios; the following are instruction-review results, not invented execution:

- Non-Git: ask about the exact target and wait before plans/implementation. An init request is not inferred Git consent.
- Bare/unborn: request a working checkout for bare repositories; require separately approved baseline contents before using an unborn repository.
- Planning-only: use the required worktree/planning path, but do not implement, commit or push automatically.
- Failed/blocked/unrun implementation checks: stop delivery and retain truthful status; source changes require affected revalidation.
- Missing identity or unknown remote: ask for concrete configuration, do not invent identity or a destination, and avoid global settings.
- Authentication/non-fast-forward/hook rejection: preserve the commit/worktree, report the blocker, and do not bypass hooks or force-push. Hook-induced source changes require revalidation; required post-push CI leaves delivery pending.
- Root/branch mismatch or detached HEAD: stop rather than delivering from another checkout/branch.
- Receipt: commit the implementation evidence snapshot; report final commit, remote OID and required gate outcomes separately in chat, without chasing a self-referential receipt.

## Evidence and limits

Archive only this REPORT.md and the `evidence/` directory; raw Git worktrees and the bare object database are unnecessary. Evidence contains exact cwd/argv/exit/stdout/stderr records, code snapshot/hashes, commit/delivery records, before/after source and resume snapshots, scoped mapping, and the preserved evaluator correction.

Nested fixture plan reviews were explicitly deferred by the evaluation request. This proves the bounded Git execution path and blocker response, not the complete nested plan-review ceremony. No real GitHub delivery, credential rejection, hook mutation, remote rejection or required CI was simulated. Real source packaging validation was reported by the parent and was not rerun here. No source repository edits or extra agents were made.
