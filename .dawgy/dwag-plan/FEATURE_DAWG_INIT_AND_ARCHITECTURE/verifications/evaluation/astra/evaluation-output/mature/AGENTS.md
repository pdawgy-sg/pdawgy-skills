> PROPOSED INIT OUTPUT ONLY. Required dawg-plan reviews are deferred in this evaluation; this file has not been applied to the project.

# Ledgerbox coding

## Commands

Use Python >=3.11 as declared in `pyproject.toml`. From the project root run `python -m unittest discover -s tests`. The command is grounded in existing AGENTS.md and the tests directory; it was not executed during this documentation evaluation.

## Repository conventions

Use Python standard library only. Keep public function names stable.
Respect [ledgerbox/AGENTS.md](ledgerbox/AGENTS.md) when editing that package; its service-function restriction remains scoped there.
Preserve existing dirty changes and untracked notes. Do not finalize the in-progress `None` handling policy without resolving its intended behavior when a change depends on it.

## Dawg coding standards

- Use `dawg-plan` for features and fixes. Clarify material uncertainty, keep tasks small, and record proportionate verification and evidence.
- Keep code as simple as possible. Add complexity only for a concrete requirement.
- Do not add explanatory code comments. Use clear names and simple code. Preserve required license notices, interpreter/tool directives, and functional annotations; existing comments are not automatically cleanup targets.
- Follow established project tools. Do not add frameworks or tests that merely duplicate the implementation.
- Propose exact redundancy cleanup with evidence and ask for approval before applying it. Preserve dirty/untracked work and scoped instructions.
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for design context. At feature/fix completion, check architecture relevance. Use `dawg-architecture-maintain` in the same task when implemented changes affect components, interfaces, dependencies, data flow, or deployment. Preserve accurate architecture on a no-op; report missing required skills rather than claiming they ran.
