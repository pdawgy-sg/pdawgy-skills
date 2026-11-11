# <FIX|FEATURE>: <Plan name>

Status: DRAFT | BLOCKED | READY | IMPLEMENTING | VERIFIED
Project root: <absolute target project path>
Plan revision: <revision/date; update after material changes>

## Intent and scope

- User outcome and confirmed decisions: <concrete goal>
- Current behavior: <observed baseline; reproduction for a fix>
- Desired behavior: <observable change>
- Scope, constraints, and exclusions: <boundaries>
- Assumptions: <low-impact choices and their rationale>
- Open questions or blockers: <unresolved material decisions; none when ready>

## Acceptance criteria

| ID | Observable success condition | Verification IDs |
| --- | --- | --- |
| AC1 | <specific result> | V1 |

## State machine

Replace the illustrative states with the feature's actual behavior. Include
relevant failure and recovery transitions. Show the completed diagram in chat.

```mermaid
stateDiagram-v2
    [*] --> Input: TR1 receive input
    Input --> Accepted: TR2 valid input / apply effect
    Input --> Rejected: TR3 invalid input / explain error
    Accepted --> [*]: TR4 finish
    Rejected --> [*]: TR5 finish
```

| Transition | From → to | Trigger / guard / effect | Verification IDs |
| --- | --- | --- | --- |
| TR1 | <states> | <observable behavior> | V1 |

Invariants: <properties that must hold across transitions and how they are checked>

## Implementation tasks

### T1: <small deliverable>

- Deliverable and code locations: <specific change>
- Dependencies: <task IDs or none>
- Covers: <acceptance IDs, transition IDs, invariants>
- Verification: <verification IDs; exact command or concrete procedure>
- Expected result: <observable pass condition>
- Evidence: <relative path inside verifications/>

Repeat for the smallest useful remaining tasks. Keep shared verification under
one ID when it proves multiple tasks or transitions.

## Independent design reviews

| Reviewer | Model / effort | Plan revision reviewed | Findings and disposition | Record |
| --- | --- | --- | --- | --- |
| Astra | gpt-6-astra / high | <revision> | <pending or actual outcome> | verifications/design-review-astra.md |
| Sol | gpt-6.1-sol / high | <revision> | <pending or actual outcome> | verifications/design-review-sol.md |

Readiness: <both completed, material findings resolved, material questions closed>

## Verification and handoff

Checklist: [verifications/verification.md](verifications/verification.md)

- Implementation authorization: <planning only, or existing user authorization>
- Completion rule: all required checks passed with evidence; both design reviews
  cover the final design. Design approval alone does not prove implementation.
- Current result: <plan readiness, execution status, outstanding limitations>
