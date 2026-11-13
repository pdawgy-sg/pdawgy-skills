# Astra formal design review

Model: gpt-6-astra; effort high; existing explicitly configured reviewer reused.
Plan/model revision1: approved, no material findings. Independently ran/audited
all four configs, raw logs, runner and identity. Production: exit0, 178 distinct
states, queue0. MissingRecord/RedCompletion/RecoveryWitness each produced its
named expected trace, exit12. Model/config/tool hashes match parent. No source
edits or additional agents.

Scope is bounded protocol safety; filesystem durability, real repairs, and
phase/blocker behavior require concrete/source checks. Full report/audit/logs:
[tla/runs/astra-attempt-1/](tla/runs/astra-attempt-1/).

Final source/behavioral review: approved without material findings against
revision1. Actual fixture exits 1/0/1/0, durable recording before repair,
invalidation/reopening, fresh resolution, and preserved failure logs/assertion.
Separate unavailable-tool case stayed explicitly blocked while independent
inspection continued. Current formal hashes match executed inputs; no duplicate
formal run needed. Actual task F1/F2 records and corrected source inspected.
Full report and evidence: [evaluation/astra/REPORT.md](evaluation/astra/REPORT.md).
Nested fixture planning/reviews were deferred; no source edits, extra agents or
GitHub mutations. F3 was a later parent-only metadata repair, not a source change.
