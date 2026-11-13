# Sol formal design review

Model: gpt-6.1-sol; effort high; existing explicitly configured reviewer reused.
Plan/model revision1: approved, no material findings. Independently executed and
audited production and three sensitivity/witness configs: 178 production distinct
states, queue0, exit0; three named expected traces exit12. Raw witness contains
record, Repair, fresh passing Run and completion with preserved history. Current
input/tool hashes match parent. No source edits or additional agents.

Phase/authority boundaries and concrete durability/correctness remain separate
checks; no unconditional liveness proof. Full report/audit/logs:
[tla/runs/sol-attempt-1/](tla/runs/sol-attempt-1/).

Final source/behavioral review: approved without material findings against
revision1. Actual fixture exits 1/0/1/0, durable recording before repair,
invalidation/reopening, fresh resolution, and preserved failure logs/assertion.
Separate unavailable-tool case stayed explicitly blocked while independent
inspection continued. Current formal hashes match executed inputs; no duplicate
formal run needed. Actual task F1/F2 records and corrected source inspected.
Full report and evidence: [evaluation/sol/REPORT.md](evaluation/sol/REPORT.md).
Nested fixture planning/reviews were deferred; no source edits, extra agents or
GitHub mutations. F3 was a later parent-only metadata repair, not a source change.
