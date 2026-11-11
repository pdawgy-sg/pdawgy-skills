# Ledgerbox coding

## Commands and conventions

Use Python standard library only. Keep public function names stable.
From the project root, run `python -m unittest discover -s tests` with Python
>=3.11 (per `pyproject.toml`). The test command is established in the existing
AGENTS.md and its test directory exists; it was not run during this documentation
walkthrough. Respect `ledgerbox/AGENTS.md` within that package; keep its local
no-filesystem-side-effects rule scoped there.

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
