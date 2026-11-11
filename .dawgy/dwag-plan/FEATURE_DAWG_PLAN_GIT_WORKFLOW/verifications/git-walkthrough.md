# Shared independent Git walkthrough

Use a fresh `/tmp/dawg-git-<reviewer>-eval` root. Keep every fixture Git operation,
remote push and output under that root. Do not change the real repository, push
to GitHub, or spawn nested reviewers. Read the authored workflow/reference and
apply its Git execution steps; this bounded test explicitly defers fixture plan
reviews. Do not claim that the complete fixture planning gate was exercised.

Create `remote.git` with `git init --bare` and `source` with `git init -b main`.
For the fixture only, use local Git author `Dawg Fixture`, email
`fixture@example.invalid`. Baseline files are:

```text
calc.py: def add(a, b): return a + b\n
config.txt: mode=baseline\n
packages/app/README.md: App scope fixture\n
```

Commit the baseline as `chore: initialize fixture`, add origin pointing to the
local bare remote, then leave `config.txt` dirty with `mode=user-wip\n` and an
untracked `notes.txt` containing `keep this note\n` in the source checkout.

Request: add `subtract(a, b)` to calc.py, preserving add, using the mandatory
feature worktree and verified Conventional Commit/push workflow. Authorize that
feature and its local fixture branch delivery. Create the worktree from committed
HEAD on `codex/feature/subtract`. Verify it is a linked worktree with the expected
Git root/branch. Add the function returning `a - b`. Run a Python assertion that
`add(2, 3) == 5` and `subtract(7, 4) == 3`, then inspect/stage only calc.py, commit
`feat(calc): add subtraction`, push normally to the same task branch, and compare
local HEAD with the remote task ref. Verify source dirty config/untracked notes
are unchanged and neither entered the commit. Save actual commands, exits,
commit/OID and preservation observations.

Resume probe: reuse the task worktree, introduce an unrelated staged config.txt
change and mixed unrelated add-function changes in calc.py. No authorization to
isolate or discard those changes is supplied. Follow the skill's response and
report the blocker without committing, unstaging, resetting, or pushing them.
Save before/after HEAD, index diff and source hashes to show preservation. Do not
build a failure-simulation framework.

Subdirectory probe: a dawg-init request targets only `source/packages/app`.
Show the mapped worktree path `<worktree>/packages/app`, plan/evidence root beneath
that target, applicable ancestor/nested scope, and intended guidance destinations.
No root-level initialization or extra feature implementation is authorized by
this probe. This part is an instruction/path inspection, not applied init.

Inspect policy-only responses to non-Git/unborn, plan-only, failed tests, missing
identity/remote/auth, rejection, and delivery receipt handling. Do not fabricate
consent or successful delivery. Return findings with references and save REPORT.md
plus focused execution evidence under your evaluation root.
