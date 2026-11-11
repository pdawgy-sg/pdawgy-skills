# Design review invocation

Two existing independent reviewers were reused with their original explicit
model/effort selections: `gpt-6-astra` high and `gpt-6.1-sol` high. Both originally
used `fork_turns: none`. Follow-up tasks preserve that configuration.

Both received revision 1 PLAN.md and verification.md, the user requirements,
confirmed `dawg-architecture-maintain` spelling, and this shared request:

Review intent alignment, meaningful state machines, scope/approval boundaries,
proportional task verification, dependency recursion, and design-document
consistency. Read-only; no implementation, source edits, or new subagents. Return
actionable findings with severity and file references or no material issues.
Material remediation must be reviewed again. Authored-skill walkthroughs follow
plan readiness.

Both revision 1 reviewers identified reproducibility gaps. Both then received
revision 2 with saved validation script, exact invocation, full raw fixtures,
deterministic fixture builder, and shared case-specific walkthrough observations.
Both independently confirmed P2 resolved and plan ready. Individual returned
findings and limits are preserved in the sibling design-review files.

The authored-skill evaluation uses WALKTHROUGH.md and the same raw inputs for
both reviewers, with separate /tmp roots. It deliberately defers nested init
reviews and labels init output as proposed, while architecture sync may actually
edit only the isolated ARCHITECTURE.md files.
