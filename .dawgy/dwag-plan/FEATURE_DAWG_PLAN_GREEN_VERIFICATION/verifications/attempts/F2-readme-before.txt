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

During implementation and verification, Dawg records observed failures in the
plan's `verifications/failures.md`, diagnoses and repairs them, and reruns failed
and affected checks until required results are current/green. It retains failed
attempts and reopens regressions. Genuine blockers remain explicit while useful
independent work continues; unresolved issues prevent completion/delivery.
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
