# Pdawgy Skills

A shared collection of skills for Codex, Claude Code, and OpenBot.

One `pdawgy-skills` plugin contains the five canonical skills. The native Codex
and Claude Code catalogs point to it. OpenBot installs the same skills as one
`dawg` pack.

## Install in OpenBot

Use Python 3.9 or later. From the checkout you want to install, set
`DAWG_WORKSPACE` to the absolute path of the selected OpenBot agent's workspace.
Build into a fresh directory within that workspace.

```sh
DAWG_WORKSPACE=/absolute/path/to/agent/workspace
python scripts/build_openbot_pack.py --output "$DAWG_WORKSPACE/candidate"
```

The builder prints the staged folder and the versioned ZIP paths. From that
agent's chat, ask OpenBot to run `create_skill` once with
`sourcePath: "candidate/dawg"`. This saves the pack in the shared local library
and installs it on the calling agent. If it's already in the library, use
`install_local_skill` once with its `skillId` and `revision`. Supply `agentId`
to install it on another selected agent.

To update, build into a fresh workspace directory and get the current library
revision with `read_local_skill`. On the agent with the installed pack, ask
OpenBot to run `revise_skill` with the same `skillId`, that `expectedRevision`,
and the workspace-relative `sourcePath` of the new staged `dawg` folder.
Other agents update when you install the new revision on each of them. If
OpenBot reports that it saved a revision but could not install it, fix the
reported problem and retry `install_local_skill` for the saved ID and revision.

Verify that OpenBot discovers `dawg` and the five names in the invocation table.
The selected workspace has those six folders in both `.agents/skills/` and
`.claude/skills/`, with one pack entry at the requested revision in
`.openbot/skills-lock.json`. OpenBot assigns integer library revisions. The
package version in `dawg/SKILL.md` and the ZIP filename comes from the aligned
native plugin manifests.

In OpenBot, invoke a child by its canonical name, for example `$dawg-plan`, or
use `$dawg` to choose a workflow. Planning and initialization require Git,
Java/TLC, and the active provider's pinned delegation and model access shown
below. For Claude Code, also install the separate native plugin using the next
section and enable **Use my Claude Code setup** so OpenBot can load that user
configuration. Verify the session exposes the applicable native agent types
before starting a phase. They are `pdawgy-skills:dawg-planner`,
`pdawgy-skills:dawg-review-sonnet`, `pdawgy-skills:dawg-review-opus`, and
`pdawgy-skills:dawg-implementer`. The pack provides skill files. If the session
lacks a required agent type, pinned model or effort, or tool, the workflow
reports the missing capability and stops that phase.

For public distribution, submit the generated ZIP to the OpenBot Skills
Marketplace for review. Marketplace listings expose an approved version.

## Install in Claude Code

Use these commands to install the version published on `main`.

```sh
claude plugin marketplace add 'https://github.com/pdawgy-sg/pdawgy-skills.git#main'
claude plugin install pdawgy-skills@pdawgy-skills
```

To test an unpublished feature branch, replace `#main` in the first command
with that branch name. The plugin install ID stays the same. A local checkout
of the desired branch also works, using the commands below.

The explicit ref avoids relying on the repository's default branch. Choose one
source for this marketplace name. Confirm installation with `claude plugin list`
and inspect the five skills and four phase agents with
`claude plugin details pdawgy-skills`. Start a new session to use them.

To try an unpublished change from a checkout, run these from the repository root
instead of adding the GitHub source:

```sh
claude plugin marketplace add "$PWD"
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
  and task branch; non-Git directories require initialization consent. Planning
  records applicable lint and static checks from project guidance, tooling and CI,
  or explains why none apply. During authorized implementation, run those checks
  in the task worktree and rerun failed and affected checks after repairs. The
  coordinator checks current evidence before Conventional Commit and again before
  pushing the task branch with remote confirmation. Planning-only requests do
  not commit or push. Invoke it with `$dawg-plan`.
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
  the agent says. Planning starts with web research (project, location,
  comparables, buyers, competitors' reels, platform craft) and a creative brief
  with the client, from Classic to Experimental. Builds an editable FilmCraft
  project headlessly through `filmcraft-cli` (with an ffmpeg-only fallback),
  from bundled Python scripts, a per-project config, research and brief guides,
  a style guide and a worked example. Invoke it with
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
├── packaging/openbot/SKILL.md
├── scripts/build_openbot_pack.py
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
