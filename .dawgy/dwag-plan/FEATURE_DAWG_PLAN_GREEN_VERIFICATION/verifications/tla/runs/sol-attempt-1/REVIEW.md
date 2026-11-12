# Sol independent formal design review — recovery revision 1

Reviewer: gpt-6.1-sol / high.
Decision: **Approve revision 1; no material design/model findings.**

## Independent execution and result audit

Executed the documented runner with explicit installed Temurin Java 25.0.5+8 and
tla2tools 1.7.4 / TLC 2.19 in fresh /tmp/dawg-green-sol-attempt-1. Approved local
execution enabled TLC's required local monitoring socket. No external service was
contacted. No source file was edited and no extra agents were spawned.

| Config | Exit | Generated / distinct / queue | Audited outcome |
| --- | --- | --- | --- |
| Recovery.cfg | 0 | 1044 / 178 / 0 | completed production finite check; enabled invariants and HistoryPreserved pass |
| MissingRecord.cfg | 12 | 4 / 4 / 2 | exact IssueRecorded violation with a real two-state trace |
| RedCompletion.cfg | 12 | 27 / 19 / 14 | exact CompletesOnlyGreen violation with a real three-state trace |
| RecoveryWitness.cfg | 12 | 410 / 123 / 44 | exact NoRecoveredCompletion violation with a real six-state recovery witness |

The three nonzero runs are labeled sensitivity/witness probes. Their nonempty
queues reflect deliberate stopping at the requested trace; they are not passing
required production invariants. The required production queue is empty.

I read the runner, each named config, enabled properties and raw logs/coverage/
trace states, and independently checked their actual exits/statistics and content.
The runner requires positive exit 0 plus explicit completion, >1 distinct state
and queue 0; negative checks require the named invariant and trace, so a parser,
monitoring-socket or runtime failure alone is not success. These actual probe
exits are TLC invariant-violation exit 12. Raw production output contains no Error.

Only after this independent execution/audit did I compare inputs/tool hashes and
outcomes with primary-attempt-1: they match. Current source model/config hashes
also match the inputs identified by my executed receipt. Exact Java commands,
versions, JAR/binary hashes, module/config hashes and outcomes are in receipt.json.
Runner/log hashes and comparison checks are in independent-audit.json; copies of
inspected inputs are in audited-inputs/. This review does not rely merely on a
summary boolean or the parent's receipt.

## Semantic review

- Recovery.tla:20–31 atomically associates a fail/blocked observation with an open
  issue, recording bit and persistent history membership. IssueRecorded checks
  that relationship. MissingRecord deliberately disables recording and its actual
  trace exposes fail plus an open issue without logged/history evidence. Real
  filesystem durability and per-attempt raw records remain concrete checks.
- A failed/blocked check cannot Run again while open unless Repair has enabled
  the retry (lines 22, 33–37). Repair represents diagnosed authorized remediation,
  not a proof that an actual patch is sufficient. The plan adds the operational
  safeguards against blind retries, weakening assertions and scope expansion.
- Run(pass) closes the corresponding issue only through the gated rerun. A later
  fail reopens it while retaining history. HistoryPreserved is enabled as an
  action-safety temporal property in every config (not a progress property).
- Invalidate advances the bounded revision, removes current pass evidence and
  repair flags, and preserves open issues/history/logged information (lines 47–54).
  Complete requires both checks passing on that revision and no open issue.
  Thus a stale pass cannot establish verified status. Initial notrun checks are
  pending work, not invented failures; completion cannot skip them.
- CompletesOnlyGreen checks the current all-green gate. RedCompletion deliberately
  removes the gate and actually reaches verified with fail/notrun and an open
  issue, showing the gate's sensitivity to red completion.
- The real RecoveryWitness trace reaches: first check pass, other check fail with
  logged/history/open state, Repair, fresh passing Run, then Complete with open
  empty and history retained. Successful recovery is reachable, so production
  safety is not explained by impossible completion.
- The model is appropriate for this requested workflow-policy feature. The plan's
  AC1/AC2/AC4 mappings correctly distinguish represented protocol safety from
  concrete artifact/implementation and phase/blocker/Git inspections. The bounded
  behavioral walkthrough preserves assertions, observes actual red/green/reopen
  outcomes, retains failed-log hashes, and separately keeps a genuine missing-tool
  case blocked. It is proportionate and needs no new framework.

## Phase, authority and claim boundaries

PLAN.md:24–45 is explicit that recovery continues through diagnose/correct/rerun,
phase-required stale/unrun checks remain non-green, scheduled future tests are not
fake defects, planning-only does not authorize implementation, and true external
or authority blockers must be recorded/asked about while independent work
continues. Source changes invalidate affected passes; material formal-contract
changes require fresh parent and both exact reviewer execution/review. Expected
negative probes pass only for their specific expected outcomes. No waiver for a
preexisting/unrelated red observation is introduced, while remediation must stay
within authorization. These operational requirements are preserved for the later
source/fixture review rather than falsely claimed fully proven by this model.

The checked finite scope is two representative checks and revisions 0/1, with
cyclic failures/repairs and no retry cap encoded. CHECK_DEADLOCK is TRUE. Hold
represents intentional verified waiting, not an arbitrary all-state deadlock
suppression. There is no fairness/progress assumption forcing external success.
HistoryPreserved is temporal safety, not unconditional liveness. No arbitrary-size,
actual-code-correctness, filesystem-durability, user/tool-truthfulness or complete
Git theorem is claimed. Aggregate history membership abstracts immutable detailed
attempt records; actual per-attempt preservation is delegated to the concrete
walkthrough/source checks as disclosed in the approved plan.

## Artifacts and next gate

All independent reviewer artifacts are under /tmp/dawg-green-sol-attempt-1:
Recovery.log, MissingRecord.log, RedCompletion.log, RecoveryWitness.log,
receipt.json, independent-audit.json, audited-inputs/, and this REVIEW.md.

Implementation, authored-source conformance, concrete recovery walkthrough,
packaging and real commit/push remain pending. This approval applies to revision 1
and the exact executed formal inputs only. A material contract/model/config change
requires correction plus fresh parent/both-reviewer runs, not receipt reuse.

## Explicit identities

- java_sha256: `1bf1aaef01e4f8d7c85d913c60fb2ee4624cbe54d4053254c59657b7ea913b25`
- tlc_jar_sha256: `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`
- runner_sha256: `d88a38daee62cf18839c4193703b40482ebafcdffdf6dcbafe00c5c470c5c2da`
- run_tlc.py: `d88a38daee62cf18839c4193703b40482ebafcdffdf6dcbafe00c5c470c5c2da`
- Recovery.tla: `68760ea28785800914c3a16ed981f5bb44eba0815a69a48ff7a70d3fe70cf33b`
- MissingRecord.cfg: `db27fb621e6de7d9b082f173b23fd3ce35c467a7210a82e7810a07c4e3e0ca9e`
- Recovery.cfg: `73caa18525f85a3534c6e95f5389d0acc03c09732fa38cfaa3a170b5a9478df4`
- RecoveryWitness.cfg: `fd6dd8cf5882237565c1363e014db3c150b542304514084c6b10f62da6b5dce5`
- RedCompletion.cfg: `311924ab7256f203433cff3f02066869f142b6b02c46e2fd3d944e61ff0afece`
