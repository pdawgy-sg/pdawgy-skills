# Pdawgy Skills

A personal Codex skills repository, distributed through a repo marketplace.

This repository defines one plugin, `pdawgy-skills`, using the supported Codex
manifest layout.

## Included skills

- **dawg-plan** — Understand features and fixes, ask about missing requirements,
  diagram their state transitions, and break work into small verifiable tasks.
  Every plan requires independent design reviews by `gpt-6-astra` and
  `gpt-6.1-sol`, both at high effort. Invoke it with `$dawg-plan`.
- **dawg-init** — Inspect an existing repository or new directory, run
  `dawg-plan`, and create/update shared coding guidance. Keeps `AGENTS.md`
  focused on coding, creates missing `CLAUDE.md` delegation, and maintains
  source-grounded `ARCHITECTURE.md`. Proposes concrete redundancy cleanup and
  applies it only after approval. Invoke it with `$dawg-init`.
- **dawg-architecture-maintain** — Synchronize `ARCHITECTURE.md` with implemented
  components and flows during relevant coding tasks, or check it directly.
  Preserves accurate documents without cosmetic churn. Invoke it with
  `$dawg-architecture-maintain`.

Dawg guidance favors simple code, no explanatory code comments, and proportionate
verification. Required notices and functional/tool directives remain intact.
Architecture stays current through coding-task maintenance, not a background job.

Plans are saved in the target project's
`.dawgy/dwag-plan/<FIX|FEATURE>_<PLAN_NAME>/PLAN.md`, with the checklist and
evidence in `verifications/verification.md` and the surrounding directory.
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
            │   └── assets/
            │       ├── PLAN.md
            │       └── verification.md
            ├── dawg-init/
            │   ├── SKILL.md
            │   ├── agents/openai.yaml
            │   └── assets/
            │       ├── AGENTS.md
            │       ├── CLAUDE.md
            │       └── ARCHITECTURE.md
            └── dawg-architecture-maintain/
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
