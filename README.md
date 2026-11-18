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
and inspect the four skills and four phase agents with `claude plugin details pdawgy-skills`. Start a
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
| Property motion video edit | `$dawg-video-property-motion-edit` | `/pdawgy-skills:dawg-video-property-motion-edit` |

`dawg-plan` and `dawg-init` share one coordinator-led workflow with these defaults:

| Host | Planning and author TLC | Small review | Large review | Authorized implementation and verification |
| --- | --- | --- | --- | --- |
| Codex | GPT-6.2 Astra / high | GPT-6.2 Sol / high only | GPT-6.2 Sol + separate GPT-6.2 Astra, both high | GPT-6.2 Sol / medium |
| Claude Code | Opus 5.5 / high | Sonnet 5.5 / high only | Sonnet 5.5 + separate Opus 5.5, both high | Opus 5.5 / medium |

The coordinator launches distinct sibling workers in the same mapped task
worktree, handles user clarifications and readiness, and audits Git delivery.
Codex uses explicit model and effort on each spawn. Claude Code uses four native
agent definitions with full model and effort pins. The planner runs author TLC
and each required reviewer independently runs TLC and assesses the design.
Planning-only requests end at the reviewed plan. Material design gaps return
to the planner and required reviewers before implementation resumes.

Plans record host, size/risk rationale, worker contexts and model/effort evidence.
Unknown hosts require clarification. Scope growth and host changes trigger a
readiness reassessment. Unavailable required execution and known model or effort
mismatches block the phase. Codex records explicit dispatch and checks effective
identity when trusted runtime metadata is available. Claude Code checks the
definition pins, runtime metadata and applicable overrides.

Java/TLC is still required for formal planning checks. Installation supplies
instructions, not model entitlements or external tooling. `dawg-mr` drafts from
committed changes without requiring the planning review cycle. See Claude Code's
[subagent model/effort rules](https://code.claude.com/docs/en/sub-agents).

## Included skills

- **dawg-plan** — Understand features, fixes and refactors, ask about missing requirements,
  diagram their state transitions, and break work into small verifiable tasks.
  Every plan includes a TLA+ model/config and completed author plus required
  reviewer TLC runs under the phase assignments above. Record an impact/risk
  rationale, reassess growth and obtain current runs and semantic approval from
  the required set. Missing, stale or incomplete runs block
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
- **dawg-video-property-motion-edit** — Edit raw property-agent footage into a
  vertical reel: the tour plays full-screen while infographics, a location map
  card, floor plans, captions and CEA-compliant agent details land on the words
  the agent says. Bundles ffmpeg/ImageMagick Python scripts, a per-project
  config, a style guide and a worked example. Invoke it with
  `$dawg-video-property-motion-edit`.

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
Formal specifications, configurations and author/reviewer logs live under that
directory's `tla/`. Java and TLC are external authoring tools; the plugin does not
bundle them. Material formal-input/requirement changes require the author and all required
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
        ├── agents/
        │   ├── dawg-planner.md
        │   ├── dawg-review-sonnet.md
        │   ├── dawg-review-opus.md
        │   └── dawg-implementer.md
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
            ├── dawg-mr/
            │   ├── SKILL.md
            │   └── agents/openai.yaml
            └── dawg-video-property-motion-edit/
                ├── SKILL.md
                ├── agents/openai.yaml
                ├── references/
                └── scripts/
```

Both marketplace catalogs point to `./plugins/pdawgy-skills`, relative to the
repository root. Codex declares `./skills/` in its manifest; Claude Code discovers
the same standard `skills/` directory and its native `agents/` definitions.
Codex continues discovering shared skills through its declared skills path.
Keep both manifest versions aligned.

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
