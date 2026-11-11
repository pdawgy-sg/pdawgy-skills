# Coding

## Repository conventions and release workflow

Use Python standard library only. Before a release, run `python release_check.py`
from the project root. Release files are maintained by the owner. These release
rules are retained from the existing CLAUDE.md; `release_check.py` exists, and the
command was not executed during this documentation walkthrough. No other check
command is established by the observed project files.

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
