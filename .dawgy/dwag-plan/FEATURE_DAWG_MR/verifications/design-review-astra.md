# Dawg MR independent design review — Astra

Reviewer: gpt-6-astra, high effort. Reviewed initial design revision (2026-11-13); immutable plan/checklist and formal-input identities are recorded in [audit.json](tla/runs/astra-01/audit.json).

Verdict: APPROVED. No material findings.

## Intent and scope

The plan implements the requested quick committed-change MR-message draft: Problem, Fix, Blast radius, Verified/tested. Runtime remains read-only drafting in chat, without invoking dawg-plan/TLA/review ceremonies, launching tests, publishing, or mutating Git. Explicit scope wins; otherwise material base ambiguity blocks drafting. Pinned committed blobs, merge-base comparison, and rejection of same-feature upstream as integration base address dirty-checkout and wrong-range risks. Source/direct-consumer inspection supports blast-radius statements; commands/results/revision/provenance qualify verification claims. Existing templates may be used without losing the four topics.

## Formal semantic audit

MrDraft.tla is a small abstract input/output protocol: 32 initial combinations from known/unknown base, nonempty/empty changes, four evidence classes, and clean/dirty checkout. Resolve implements the blocked/empty/inspect split. Draft classifies current passes, failures, and unverified stale/absent evidence and emits all four topic labels. NewRequest resets output and allows later resolution; terminal Hold explicitly permits stuttering. ScopeSound, EvidenceSound, UnknownExplicit and FourTopics match their documented mappings; TypeOK bounds the state domain.

The dirty flag is intentionally non-influential once evidence applicability is classified. A current-pass input assumes inspected evidence already applies to the pinned clean committed revision. The model does not establish that classification, interpret Git/prose, represent mixed evidence items, or prove filesystem read-only behavior. Those responsibilities are explicitly assigned to the practical forward evaluation; each concrete claim must be classified independently. This is an appropriate bounded model for this small drafting workflow, not an arbitrary-code proof.

Production uses CHECK_DEADLOCK TRUE, no constraints/reductions/fairness or liveness property. Resolve/Draft are enabled in their phases; terminal Hold/NewRequest avoid artificial deadlocks. No claim of eventual draft or guaranteed external clarification is made. Production coverage includes 8 Draft outputs across all four evidence classes and both dirty values; 32 scope resolutions and 1024 NewRequest successor evaluations. The explicit NoDraft witness reaches a three-state valid draft path. The evidence mutation reaches a stale-pass falsely classified as passed and is caught by EvidenceSound. Thus checked output properties are exercised rather than vacuous.

## Actual independent TLC execution

Inspected run_tlc.py, each configuration, parent-02 raw logs/receipt, and all independent raw logs/traces/coverage. Executed from the plan root:

```sh
python3 verifications/run_tlc.py --java /home/chy/.local/share/mise/installs/java/temurin-25.0.5+8.0.LTS/bin/java --jar /home/chy/.local/share/mise/installs/http-tla2tools/1.7.4/tla2tools.jar --output verifications/tla/runs/astra-01
```

Local monitoring-socket escalation was authorized. Runner exit: 0.

| Configuration | Actual result | States generated / distinct / queued |
| --- | --- | --- |
| MrDraft.cfg | exit 0, completed without errors | 1128 / 72 / 0 |
| EvidenceFault.cfg | exit 12, exact EvidenceSound violation and trace | 859 / 67 / 7 |
| DraftWitness.cfg | exit 12, exact NoDraft violation and trace | 857 / 65 / 7 |

Runner accepts production only with exit 0, completion text, more than one distinct state and empty queue. Negative probes require nonzero exit plus their named violation and behavior trace; raw audit confirms actual TLC exit 12 and intended counterexamples, not parser/tool failures. Negative queues are expected because these runs stop on the intended violation. Fresh output and per-run temporary metadata prevent prior-state reuse. Before/after runner/module/config hashes match; module/config/tool identities match parent-02 and the current inputs. Tool versions and exact commands/hashes are in [receipt.json](tla/runs/astra-01/receipt.json).

## Verification and limits

Small tasks and targeted validation/source inspection plus isolated dirty-range/evidence/empty/ambiguity evaluations are proportionate; no new runtime dependency or test framework is proposed. The authoring process's formal review and Git delivery requirements remain separate from the skill's quick runtime. Implementation and actual-skill behavioral evaluation have not run and are not approved by this design receipt. Preserve concrete fixture inputs, commands, drafts and before/after state when executing V3 so those observations are independently inspectable. This is an execution evidence expectation, not a new product requirement.

No source/model changes, subagents, network actions or Git mutations were performed. Only the requested review and independent evidence files were written.
