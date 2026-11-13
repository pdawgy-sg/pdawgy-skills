# Pdawgy Skills

A personal Codex skills repository, distributed through a repo marketplace.

This repository defines one plugin, `pdawgy-skills`, using the supported Codex
manifest layout.

## Included skills

- **dawg-plan** — Understand features and fixes, ask about missing requirements,
  diagram their state transitions, and break work into small verifiable tasks.
  Every plan includes a TLA+ model/config and completed TLC runs by the parent,
  `gpt-6-astra`, and `gpt-6.1-sol`, with both reviewers at high effort independently
  checking model meaning and execution. Missing/stale/incomplete runs block
  readiness; bounded model checks complement implementation tests. Features/fixes use a dedicated Git worktree
  and task branch; non-Git directories require initialization consent. After
  authorized implementation passes checks, the workflow creates a Conventional
  Commit and pushes the task branch with remote confirmation. Planning-only
  requests do not commit or push. Invoke it with `$dawg-plan`.
- **dawg-init** — Inspect an existing repository or new directory, run
  `dawg-plan`, and create/update shared coding guidance. Keeps `AGENTS.md`
  focused on coding, creates missing `CLAUDE.md` delegation, and maintains
  source-grounded `ARCHITECTURE.md`. Proposes concrete redundancy cleanup and
  applies it only after approval. Invoke it with `$dawg-init`.
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
bundle them. Material formal-input/requirement changes require all three reruns.
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
├── .gitignore
├── README.md
└── plugins/
    └── pdawgy-skills/
        ├── .codex-plugin/
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

The marketplace catalog points to `./plugins/pdawgy-skills`, relative to the
repository root. The plugin manifest points to its own `./skills/` directory.

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
entries. Update the plugin version when releasing changes.

## Register the marketplace locally

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
an entry to `.agents/plugins/marketplace.json` pointing to that directory.

## Reference

[OpenAI plugin packaging and marketplace documentation](https://developers.openai.com/plugins/build/plugins)
