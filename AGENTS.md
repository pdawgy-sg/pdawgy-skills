# Coding in Pdawgy Skills

## Workflow

- Read [ARCHITECTURE.md](ARCHITECTURE.md) for design context. Keep this file focused
  on how to change and verify the repository.
- Use the bundled [dawg-plan](plugins/pdawgy-skills/skills/dawg-plan/SKILL.md)
  workflow for features and fixes. Resolve material uncertainty, show state
  diagrams, and break work into small parts with reproducible verification.
  Required design reviewers are `gpt-6-astra` and `gpt-6.1-sol`, both at high
  effort. Report unavailable dependencies instead of claiming the review ran.
- Every feature/fix uses dawg-plan's dedicated Git worktree and task branch.
  Preserve the selected target-relative scope inside it; keep the source checkout
  and unrelated staged/dirty work intact. Outside Git, ask before initializing.
  After authorized implementation passes required checks, inspect the whole index
  and commit delta, create a task-only Conventional Commit, and push normally to
  its feature/fix branch with remote OID confirmation. Respect planning-only and
  explicit delivery limits; report blockers rather than bypassing checks.
- Use the installed skill-creator workflow when authoring skills. Keep guidance
  concise, scoped to its purpose, and supported by resources only when useful.
- Use [dawg-architecture-maintain](plugins/pdawgy-skills/skills/dawg-architecture-maintain/SKILL.md)
  in the same task when implemented changes affect components, interfaces,
  dependencies, or flows. Check architecture at feature/fix completion; preserve
  an accurate document rather than making cosmetic edits.

## Coding standards

- Keep code as simple as the behavior permits. Add complexity only for a concrete
  requirement. Prefer clear names and small, useful changes.
- Do not add explanatory code comments. Retain required license notices,
  interpreter/tool directives, and functional annotations. Existing comments are
  not an automatic cleanup target.
- Follow existing Markdown, JSON, YAML, and Python conventions where applicable.
  Do not add dependencies or a test framework merely to change documentation.
- Preserve user work and scoped instructions. Present exact redundancy-cleanup
  changes and their evidence for approval before deleting, moving, or
  consolidating existing material. An initialization request alone is not cleanup
  approval. Do not reset or clean uncommitted/untracked files.

## Editing skills and packaging

- Keep skill folder names and frontmatter `name` consistent, lowercase, and
  hyphenated. Write a precise `description` explaining when the skill applies.
- Keep UI metadata and `$skill-name` prompts consistent with the skill. Preserve
  automatic discovery unless the user requests otherwise.
- Resolve resource paths from their owning skill. Resolve manifest paths from
  the plugin root and marketplace paths from the repository root. Preserve the
  existing supported manifest layout and verify schema changes against current
  official documentation.
- Keep reusable templates inside skill assets and adapt their prompts when
  producing actual documents. Treat copied fixture instructions and sample
  projects as evaluation inputs, not evidence of this plugin's runtime behavior.
- Preserve historical plans, review records, and failed verification attempts.
  Snapshot checks in old plans are evidence for those revisions; do not rewrite
  or promote them into the current project test runner.
- Update README descriptions and relevant UI metadata when behavior changes.
  Update the plugin version when releasing packaged changes. Local cache/config
  changes are installation actions and require task authorization.

## Verification

Run commands from the repository root. This repo defines no application build,
lint, or test runner; choose checks appropriate to changed artifacts.

```sh
git status --short --branch
python -m json.tool .agents/plugins/marketplace.json > /dev/null
python -m json.tool plugins/pdawgy-skills/.codex-plugin/plugin.json > /dev/null
git diff --check
```

For changed skills, use the installed skill-creator validator. Set
`DAWG_SKILL_CREATOR_DIR` to that installed skill's directory and
`DAWG_SKILL_NAME` to the changed skill. Use a Python environment with PyYAML:

```sh
python "$DAWG_SKILL_CREATOR_DIR/scripts/quick_validate.py" "plugins/pdawgy-skills/skills/$DAWG_SKILL_NAME"
```

Inspect UI YAML, sibling/resource links, and changed behavior in addition to
frontmatter validation. `git diff --check` excludes untracked files; inspect new
files too, using `git diff --no-index --check /dev/null <new-file>` when useful.
Ordinary new-file differences can return 1; whitespace diagnostics indicate a
problem. Do not stage files just to run checks.

Keep verification proportionate: direct inspection for small document changes,
focused behavioral evaluation for workflow changes, and no tests that merely
mirror wording. Save plans and evidence at
`.dawgy/dwag-plan/<FIX|FEATURE>_<PLAN_NAME>/PLAN.md` and
`verifications/verification.md` beneath that plan. Mark checks passed only after
observing results; save relevant outputs and share any screenshot evidence.
