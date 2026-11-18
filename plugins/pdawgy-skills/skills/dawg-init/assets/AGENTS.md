# Coding in <project>

## Commands

<Keep only setup, development, build, lint, and test commands verified in this
repository. State where to run them and any prerequisites. Do not invent missing
commands or mark a command executed unless it was actually run.>

## Repository conventions

<Preserve and describe observed language/tool conventions and applicable scoped
rules. Keep this section about writing and checking code, not module inventories.>

## Dawg standards

- Use `dawg-plan` for features, fixes and refactors. Resolve material uncertainty,
  keep work in small parts, and record enough verification/evidence for each part. Include
  a meaningful TLA+ model/config and completed author plus every required reviewer
  TLC check on identical final inputs. Use coordinator-scheduled phase workers
  in the same mapped worktree. For Codex, use `gpt-6.2-astra`/high for planning
  and author TLC, `gpt-6.2-sol`/high alone for small review, a separate
  `gpt-6.2-astra`/high reviewer in addition for large review, and
  `gpt-6.2-sol`/medium for authorized implementation and verification after
  readiness. In Claude Code, use the pinned Opus 5.5/high planner, Sonnet 5.5/high
  reviewer alone for small work, an additional distinct Opus 5.5/high reviewer
  for large work, and the pinned Opus 5.5/medium implementer when ready and
  authorized. Record host, tier and rationale. Follow dawg-plan's dispatch and
  model/effort evidence rules, ask when host is unknown and reassess growth or
  host changes before readiness. Require the selected profile's current receipts.
  State bounds and assumptions, retain implementation tests and rerun formal
  checks after material model or requirement changes. Use its
  dedicated Git worktree/task branch and preserve selected subdirectory scope.
  Outside Git, ask before initialization and wait. After authorized implementation
  passes required checks, create a task-only Conventional Commit and push normally
  to that task branch; confirm the remote commit. Preserve planning-only
  limits and unrelated staged/dirty work; report delivery blockers honestly.
- Record observed failures/blockers and every attempt in the plan's persistent
  failure register. Diagnose, repair and rerun failed/affected checks until current
  required results are green; reopen recurrences and retain failed history.
  Invalidate stale passes. Ask for genuine outside dependencies and continue
  independent work, without weakening checks or claiming unresolved work complete.
- Keep local `.dawgy/` planning artifacts ignored. Preserve existing ignore rules
  and do not force-add ignored plans/evidence. Report already tracked artifacts;
  untracking or deletion requires separately approved cleanup.
- Keep code as simple as possible; add complexity only for a concrete requirement.
- Do not add explanatory code comments. Express intent through clear names and
  simple code. Retain required license notices, interpreter/tool directives, and
  functional annotations. Do not mass-delete existing comments.
- Follow the project's established tools. Keep verification proportionate; avoid
  tests that only mirror implementation or add a framework without a real need.
- Before redundancy cleanup, present the exact changes and ask for approval.
  Preserve uncommitted/untracked work and scoped instructions.
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for design context. At task
  completion, check whether implemented structure or behavior changed. Use
  `dawg-architecture-maintain` in the same task for changes to component boundaries,
  interfaces, dependencies, data flow, or deployment; preserve an accurate document
  on a no-op. If a required skill is unavailable, report the blocker.

<Remove all template prompts from the final document. Add only repo-specific
coding instructions that agents need; keep architecture prose in ARCHITECTURE.md.>
