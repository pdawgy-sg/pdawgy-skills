# Required Git workflow

Apply this workflow to every feature/fix, including planning-only requests.
Implementation authorization includes automatic verified commit/push under this
workflow unless the user explicitly limits delivery. Planning alone never
authorizes implementation, committing, or pushing.

## Preflight and scope

Use Git to detect context: `git rev-parse --is-inside-work-tree` and
`git rev-parse --show-toplevel`. A linked worktree's `.git` is usually a file, so
testing whether `.git` is a directory is insufficient. A bare repository is not
an editable project checkout; ask for a working checkout/worktree rather than
initializing over it.

If the selected directory is outside a Git working tree, ask whether to initialize
it, naming the exact target, and wait before creating plan files or implementing.
Do not infer consent from an init/planning request. After consent, initialize
only that target. If HEAD is unborn, explain that a committed base is required
and get approval for a concrete initial snapshot (or empty baseline for an empty
project). Never sweep preexisting files into a baseline without approval. Preserve
declined or unanswered choices as blockers.

Inspect `git status --short --branch`, staged and unstaged diffs, untracked files,
`git worktree list --porcelain`, current branch/HEAD, and remotes. Record:

- Original repository root and selected target path relative to it.
- Committed base revision, task branch, and worktree repository root.
- Mapped project directory: worktree root plus that same target-relative path.
- Implementation/delivery authorization and chosen remote/destination branch.

Keep a subdirectory request inside its mapped subdirectory. Read applicable
ancestor/nested instructions there. Git operations use the worktree repository
root; project changes, commands and plan artifacts use the mapped project unless
the task explicitly authorizes broader scope. Return both paths to callers such
as dawg-init so they do not write guidance into the original checkout or expand
an initialization to a whole monorepo.

## Create or resume the task worktree

Use `codex/feature/<kebab-case-slug>` for a feature or
`codex/fix/<kebab-case-slug>` for a fix unless the user specifies another name.
The branch must remain separate from the base branch even with a custom name.
Choose a distinct worktree path outside the source checkout, within allowed
workspace locations. From the repository, use supported worktree tooling or:

```sh
git worktree add -b "$DAWG_BRANCH" "$DAWG_WORKTREE_PATH" "$DAWG_BASE"
```

Set those task-specific variables from recorded, inspected values. Check branch
and path collisions first. Do not overwrite an existing branch/directory or reuse
an unrelated task. For a resumed task, verify its existing worktree/root, branch,
base and change ownership, then reuse it instead of nesting another worktree.
Confirm the actual new Git root/branch before writing plans or code.

A new worktree starts from committed history; it does not include uncommitted
source-checkout changes. If task-critical changes are only present there, ask
about a deliberate scoped transfer or prerequisite commit. Do not blanket stash,
copy, reset, or commit unrelated user work. Record and preserve existing staged,
unstaged, and untracked work in a reused task worktree as well.

## Verify before committing

Complete the reviewed plan's required checks with enough observable evidence to
prove intended behavior and a relevant regression boundary. Keep checks focused;
no new framework or broad Git failure simulator is required. Failed, blocked or
unrun required checks stop commit/push. Apply the
[recovery loop](recovery-loop.md): record observed failures and attempts, diagnose,
repair within scope, and rerun failed/affected checks until current required
results are green with no unresolved implementation issues. Do not finish merely
at the first red result. A plan-only task stops at its reviewed
plan, with no automatic implementation commit/push.

Save implementation evidence under the mapped project's plan `verifications/`.
Identify tested source using revision and file/diff fingerprints. If source or
generated outputs change after checking, rerun affected checks. Review the final
source and evidence together before delivery.

Before staging, committing or pushing, recheck the actual Git root and current
branch against the recorded task worktree/branch; stop on a mismatch or detached
HEAD rather than delivering from the base checkout.

Inspect the entire existing index (`git diff --cached`) and working changes before
staging. A normal commit includes preexisting staged entries, not just newly
staged task paths. If there are unrelated staged files or mixed unrelated hunks
within a task file, block delivery until ownership is resolved or the user
authorizes deliberate isolation. Never silently unstage/reset their index, discard
their content, or use blanket `git add .`/`git add -A`.

Stage explicit task-owned paths only when every hunk is in scope; otherwise use
an explicitly authorized selective approach. Include the task's plans, maintained
documentation and verification evidence as appropriate. Inspect the whole staged
diff and file list, not only selected-file hashes, to confirm no unrelated work
will enter the commit. Check Git identity; ask for missing name/email and use
repository-local settings if configuration is authorized. Do not invent an
identity or change global Git settings.

## Conventional Commit and normal task-branch push

Create the commit automatically once implementation verification and the staged
scope checks pass. Use `feat: <summary>` for features or `fix: <summary>` for fixes,
optionally with a meaningful scope, for example
`feat(planner): require isolated worktrees`. Respect the repository's established
Conventional Commit rules. Do not bypass hooks. Hook failures block delivery;
hook-modified source must be reverified before pushing.

Inspect the complete created commit delta (`git show --format= HEAD`) and confirm
it matches the reviewed task change and tested source fingerprints. Unexpected
content stops push; do not automatically amend/reset a user's commit to hide it.

Use the user-specified remote, a matching resumed task upstream, or an unambiguous
configured remote. If uncertain/missing, ask for the remote URL/name. Do not guess
a publishing destination or silently change remotes. Always push to the current
task branch name, even when the base branch has a different upstream:

```sh
git push --set-upstream "$DAWG_REMOTE" "HEAD:refs/heads/$DAWG_BRANCH"
git rev-parse HEAD
git ls-remote "$DAWG_REMOTE" "refs/heads/$DAWG_BRANCH"
```

Require a successful push and exact remote task-ref/local-HEAD OID match. Honor
required repository checks/CI; if a required gate runs after push, delivery remains
pending until its outcome is verified. No force push, implicit main/base merge,
hook bypass, or automated worktree removal. On authentication, permission,
non-fast-forward or other failures, preserve the commit/worktree, report the exact
blocker in the same persistent failure register, work through authorized remedies,
request needed outside input, and resume safely after resolution. Keep independent
work moving while genuinely blocked. Do not claim remote delivery merely
because a local commit exists.

Commit the implementation verification snapshot before delivery. Report final
commit hash, branch, remote OID confirmation, and required gate outcomes in chat;
do not churn commits trying to save a receipt containing its own commit ID or
proof of its own future push. Label that committed ledger as a pre-delivery
snapshot, and distinguish implementation VERIFIED from delivery PENDING,
COMMITTED, PUSHED, or BLOCKED in the handoff. Keep later user edits out of claims
about the tested/committed revision.
