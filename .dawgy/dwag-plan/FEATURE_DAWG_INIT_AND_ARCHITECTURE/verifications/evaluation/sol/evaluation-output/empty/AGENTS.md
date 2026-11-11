# Coding guidance proposal — pending project intent

No language, framework, commands, or application components were established by
the empty-directory inspection. This is a language-neutral proposal only; clarify
product and stack intent before treating initialization as ready. Do not create
Git metadata or choose tools without an applicable user request.

## Dawg workflow

- Use `dawg-plan` for features and fixes. Clarify material uncertainty, keep tasks
  small, and save proportionate verification/evidence.
- Keep code as simple as possible; add complexity only for a concrete requirement.
  Do not add explanatory code comments. Retain required notices, interpreter/tool
  directives, and functional annotations. Do not mass-delete existing comments.
- Keep the established project tools; do not add a framework for agent guidance.
- Propose exact redundancy cleanup changes and obtain approval before applying
  them. Preserve uncommitted/untracked work and scoped instructions.
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for design context. At feature/fix
  completion, check architecture relevance; use `dawg-architecture-maintain` in
  the same task for changes to component boundaries, interfaces, dependencies,
  data flow, or deployment. Preserve accurate documentation on a no-op. Report
  missing required skills rather than claiming their workflows ran.
