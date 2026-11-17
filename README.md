# Pdawgy Skills

A shared collection of coding-agent skills for Codex and Claude Code.

One `pdawgy-skills` plugin contains the canonical skills. Each client has its own
native marketplace catalog and manifest pointing to that same package.

## Install in Claude Code

Run these commands in your terminal to install the version published on `main`:
Unmerged feature-branch changes are not included in that version.

```sh
claude plugin marketplace add 'https://github.com/pdawgy-sg/pdawgy-skills.git#main'
claude plugin install pdawgy-skills@pdawgy-skills
```

To test an unpublished feature branch, replace `#main` in the first command
with that branch name. The plugin install ID stays the same. A local checkout
of the desired branch also works, using the commands below.

The explicit ref avoids relying on the repository's default branch. Choose one
source for this marketplace name. Confirm installation with `claude plugin list`
and inspect the four skills with `claude plugin details pdawgy-skills`. Start a
new session to use them.

To try an unpublished change from a checkout, run these from the repository root
instead of adding the GitHub source:

```sh
claude plugin marketplace add .
claude plugin install pdawgy-skills@pdawgy-skills
```

Use one source for the `pdawgy-skills` marketplace name. Claude Code's
[marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces) documents
the registration/install flow and
[Git ref support](https://code.claude.com/docs/en/plugins/host-marketplace)
explains `#main` or another branch/tag.

## Invoke skills

| Skill | Codex | Claude Code |
| --- | --- | --- |
| Planning | `$dawg-plan` | `/pdawgy-skills:dawg-plan` |
| Repository initialization | `$dawg-init` | `/pdawgy-skills:dawg-init` |
| Architecture maintenance | `$dawg-architecture-maintain` | `/pdawgy-skills:dawg-architecture-maintain` |
| MR description | `$dawg-mr` | `/pdawgy-skills:dawg-mr` |

`dawg-plan` and `dawg-init` select reviewers for the active client:

| Host | Small change | Large change |
| --- | --- | --- |
| Codex | GPT-6.1 Sol / high | Sol + GPT-6 Astra, both high |
| Claude Code | Sonnet / high | Sonnet + Opus, both high |

Claude Code uses its native `sonnet` and `opus` aliases and per-agent effort
selection. Codex retains its exact Sol/Astra model choices. Plans record host,
size/risk rationale and model identities; scope growth or host changes revoke
readiness until the required reviews are current. Unknown hosts require a focused
question, and unavailable required models/effort remain blockers. Neither client
silently falls back to the other client's reviewers.

Java/TLC is still required for formal planning checks. Installation supplies
instructions, not model entitlements or external tooling. `dawg-mr` drafts from
committed changes without requiring the planning review cycle. See Claude Code's
[subagent model/effort rules](https://code.claude.com/docs/en/sub-agents).

## Included skills

- **dawg-plan** — Understand features, fixes and refactors, ask about missing requirements,
  diagram their state transitions, and break work into small verifiable tasks.
  Every plan includes a TLA+ model/config and completed parent plus required
  reviewer TLC runs. Codex uses Sol/high and adds Astra/high for large work;
  Claude Code uses Sonnet/high and adds Opus/high for large work. Record an impact/risk rationale, reassess growth
  and obtain current runs and semantic approval from the required set. Missing/stale/incomplete runs block
  readiness; bounded model checks complement implementation tests. Features/fixes/refactors use a dedicated Git worktree
  and task branch; non-Git directories require initialization consent. After
  authorized implementation passes checks, the workflow creates a Conventional
  Commit and pushes the task branch with remote confirmation. Planning-only
  requests do not commit or push. Invoke it with `$dawg-plan`.
- **dawg-init** — Inspect an existing repository or new directory, run
  `dawg-plan`, and create/update shared coding guidance. Keeps `AGENTS.md`
  focused on coding, creates missing `CLAUDE.md` delegation, and maintains
  source-grounded `ARCHITECTURE.md`. Proposes concrete redundancy cleanup and
  applies it only after approval. Ensures `.dawgy/` is effectively ignored while
  preserving existing rules and tracked artifacts. Invoke it with `$dawg-init`.
- **dawg-architecture-maintain** — Synchronize `ARCHITECTURE.md` with implemented
  components and flows during relevant coding tasks, or check it directly.
  Preserves accurate documents without cosmetic churn. Invoke it with
  `$dawg-architecture-maintain`.

- **dawg-mr** — Quickly review committed changes and draft an MR/PR message with
  the problem, fix, blast radius, and verified/tested evidence. Labels missing or
  stale results honestly; drafts in chat without publishing or running tests.
  Invoke it with `$dawg-mr`.

During implementation and verification, Dawg records observed failures in the
plan's `verifications/failures.md`, diagnoses and repairs them, and reruns failed
and affected checks until required results are current/green. It retains failed
attempts and reopens regressions. Genuine blockers remain explicit while useful
independent work continues; unresolved issues prevent completion/delivery.

Dawg guidance favors simple code, no explanatory code comments, and proportionate
verification. Required notices and functional/tool directives remain intact.
Architecture stays current through coding-task maintenance, not a background job.

Plans are saved in the target project's
`.dawgy/dwag-plan/<FIX|FEATURE>_<PLAN_NAME>/PLAN.md`, with the checklist and
evidence in `verifications/verification.md` and the surrounding directory.
Formal specifications, configurations and parent/reviewer logs live under that
directory's `tla/`. Java and TLC are external authoring tools; the plugin does not
bundle them. Material formal-input/requirement changes require the parent and all required
reviewers to rerun.
The target project is mapped into the task worktree, preserving any selected
subdirectory. Branches default to `codex/feature/<slug>` or `codex/fix/<slug>`.
Missing identity/remotes, unresolved unrelated staging, failed checks, or rejected
pushes are explicit blockers. Main is not implicitly merged or force-pushed.
Screenshots are saved there and displayed in chat on completion. The models and
subagent tooling must be available to complete the required reviews.

## Structure

```text
pdawgy-skills/
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── .claude-plugin/
│   └── marketplace.json
├── .gitignore
├── README.md
└── plugins/
    └── pdawgy-skills/
        ├── .codex-plugin/
        │   └── plugin.json
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            ├── dawg-plan/
            │   ├── SKILL.md
            │   ├── agents/openai.yaml
            │   ├── references/git-workflow.md
            │   ├── references/tla-verification.md
            │   ├── references/recovery-loop.md
            │   └── assets/
            │       ├── PLAN.md
            │       ├── verification.md
            │       └── failures.md
            ├── dawg-init/
            │   ├── SKILL.md
            │   ├── agents/openai.yaml
            │   └── assets/
            │       ├── AGENTS.md
            │       ├── CLAUDE.md
            │       └── ARCHITECTURE.md
            ├── dawg-architecture-maintain/
            │   ├── SKILL.md
            │   └── agents/openai.yaml
            └── dawg-mr/
                ├── SKILL.md
                └── agents/openai.yaml
```

Both marketplace catalogs point to `./plugins/pdawgy-skills`, relative to the
repository root. Codex declares `./skills/` in its manifest; Claude Code discovers
the same standard `skills/` directory. Keep both manifest versions aligned.

## Add a skill

Create `plugins/pdawgy-skills/skills/<skill-name>/SKILL.md`. Give each skill a
lowercase, hyphenated name and YAML frontmatter describing when to use it:

```markdown
---
name: my-skill
description: Describe what this skill does and when Codex should use it.
---

# My Skill

Write the workflow instructions here.
```

Keep any supporting `scripts/`, `references/`, or `assets/` inside that skill's
directory. Additional skills in this plugin do not need separate marketplace
entries. Update the version in both plugin manifests when releasing changes.

## Install in Codex

From this repository's root, run:

```sh
codex plugin marketplace add .
codex plugin marketplace list
```

Restart the Codex desktop app, open the plugin directory, select **Pdawgy Skills**
as the marketplace source, and install the plugin. Test added skills in a new chat.
The scaffold itself does not register or install anything.

After publishing this repository to GitHub, it can also be registered with
`codex plugin marketplace add <owner>/pdawgy-skills --ref main`.

## Add another plugin

Create another directory under `plugins/` with its own manifest and skills. Add
entries to `.agents/plugins/marketplace.json` and `.claude-plugin/marketplace.json`
pointing to that directory.

## Reference

[OpenAI plugin packaging and marketplace documentation](https://developers.openai.com/plugins/build/plugins)

[Claude Code plugin manifest reference](https://code.claude.com/docs/en/plugins-reference)
