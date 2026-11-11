> PROPOSED INIT OUTPUT ONLY. Required dawg-plan reviews are deferred in this evaluation; this file has not been applied to the project.

# Coding guidance

The user has not chosen a stack or product architecture. Do not choose either on their behalf. No project-specific setup, test, build, or release commands are established. Do not initialize Git merely to create guidance.

## Dawg coding standards

- Use `dawg-plan` for features and fixes. Clarify material uncertainty, keep tasks small, and record proportionate verification and evidence.
- Keep code as simple as possible. Add complexity only for a concrete requirement.
- Do not add explanatory code comments. Use clear names and simple code. Preserve required license notices, interpreter/tool directives, and functional annotations; existing comments are not automatically cleanup targets.
- Follow established project tools. Do not add frameworks or tests that merely duplicate the implementation.
- Propose exact redundancy cleanup with evidence and ask for approval before applying it. Preserve dirty/untracked work and scoped instructions.
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for design context. At feature/fix completion, check architecture relevance. Use `dawg-architecture-maintain` in the same task when implemented changes affect components, interfaces, dependencies, data flow, or deployment. Preserve accurate architecture on a no-op; report missing required skills rather than claiming they ran.
