# Astra independent recovery design and TLA+ review

Reviewer: gpt-6-astra / high. Reviewed revision: **1**. Date: 2026-11-12.

**Approved: no material design/model findings.** This approval concerns the stated bounded recovery protocol and planned implementation/verification; the authored policy and concrete filesystem walkthrough still require their subsequent source/behavior checks.

## Actual independent execution

Read PLAN.md, verification.md, recovery-walkthrough.md, Recovery.tla, every named configuration and run_tlc.py. Copied exactly the runner/module/config files to `/tmp/dawg-green-astra-inputs-1`, verified their hashes against source before execution, and verified both copies remain unchanged afterward.

Executed all four configurations independently with the supplied audited runner:

```sh
python /tmp/dawg-green-astra-inputs-1/run_tlc.py --java /home/chy/.local/share/mise/installs/java/temurin-25.0.5+8.0.LTS/bin/java --jar /home/chy/.local/share/mise/installs/http-tla2tools/1.7.4/tla2tools.jar --output /tmp/dawg-green-astra-attempt-1
```

Used approved local execution for TLC's local monitoring socket. No external service was contacted. Each configuration used fresh private metadata. The runner exited 0 after observing every expected outcome. I independently read the complete raw logs, coverage and concrete traces rather than trusting either the parent or runner's summary.

| Config | Exit | Distinct states | Queue left | Actual result |
| --- | --- | --- | --- | --- |
| Recovery.cfg | 0 | 178 | 0 | Completed; required safety properties hold |
| MissingRecord.cfg | 12 | 4 | 2 | IssueRecorded named trace |
| RedCompletion.cfg | 12 | 19 | 14 | CompletesOnlyGreen named trace |
| RecoveryWitness.cfg | 12 | 123 | 44 | NoRecoveredCompletion named trace |

Production generated 1,044 states and completed at depth 9, with 178 distinct states and an empty queue. The three probes deliberately stop on their named violation, so their nonempty queues are not claimed as completed production checks.

## Semantic mapping and bounded claims

In production, a failing/blocked Run atomically opens the issue, records its current observation, adds permanent history membership, and clears retry readiness. Because the issue is open and repairReady is false, that check cannot run again until Repair occurs. IssueRecorded checks every open issue has both current recording and historical membership. This is a useful protocol abstraction of record-before-repair/retry; it does not verify actual durable writes or a separate logger's ordering.

Repair is the abstract event for diagnosed corrective action. It enables a retry without closing the issue or changing its red result. A passing Run alone removes the issue from the open set, and any later failure reopens it. The model therefore distinguishes writing a patch from observing a passing rerun. Its truthfulness and substantive nature of remediation must still be checked in authored instructions and the concrete walkthrough; a Boolean flag cannot prove those real-world facts.

AllGreen requires both representative checks to pass on the current revision. Complete additionally requires an empty issue set. Invalidate increments the bounded revision, returns to working, resets results/check revisions/retry readiness, and preserves issue/history state. Prior passes therefore cannot complete a later modeled revision. Real change-impact analysis and making sure source changes trigger the appropriate invalidation remain implementation obligations.

HistoryPreserved is enabled as a temporal action-safety property: history membership never shrinks. It is not an eventual-progress property or proof that each raw filesystem attempt survives. The model deliberately abstracts repeated attempt history to a finite membership set. The planned concrete check of failed-log byte identity, stable issue/reopening and final source identity is necessary to cover those omitted durability details.

The finite domain has two checks and revision values 0/1; cyclic failure/repair/retry behavior imposes no retry-count cap. CHECK_DEADLOCK is enabled. Hold permits intentional verified waiting, while external blocked results may recur indefinitely. There is no fairness assumption or unconditional liveness/success claim. This correctly avoids promising green when tools, authority or external state cannot be obtained.

Plan-only phases, expected-negative interpretation, user/external blockers and Git delivery are not modeled as if these two representative implementation checks prove them. The plan explicitly assigns those requirements to source inspection and the later bounded walkthrough. Future implementation checks do not become invented plan-readiness defects; observed required blockers remain recorded and unverified while authorized independent work continues. The proposed prohibition on test weakening, hidden flakes and unrelated-scope changes matches the request without authorizing unsafe bypasses.

## Nonvacuity and probe audit

Production coverage exercised Run, Repair, Complete and Invalidate; Complete generated eight successor states, so the green gate is not unreachably true. The witness gives a concrete six-state path: a test passes, verification fails and is recorded, Repair enables it, verification reruns successfully, and Complete enters verified with failure history still present.

MissingRecord disables recording only in its labeled probe. Its two-state trace shows a failed check open while logged is false and history empty, violating IssueRecorded. RedCompletion disables the green gate only in its probe; its trace reaches verified with an open failed check and another unrun check, violating CompletesOnlyGreen. RecoveryWitness keeps production safeguards enabled and intentionally violates NoRecoveredCompletion after successful recovery. None is a parse/runtime error being mislabeled as the intended result.

## Runner and identity audit

The runner's required-production predicate checks exit 0, the completion message, nontrivial state count and empty queue. Expected probes require a nonzero exit, exact invariant name and a behavior trace; I checked actual exit 12 and each trace's semantics. Timeout/runtime failures would fail the appropriate expectation, not count as recovery. Raw output, per-attempt isolation and identities are preserved. The common runner does not replace the independent semantic assessment.

Current source/private input hashes, tool identities and configuration outcomes match the primary receipt. Imported standard-module member hashes from the pinned JAR are saved in audit.json. Input identities are:

- `run_tlc.py`: `d88a38daee62cf18839c4193703b40482ebafcdffdf6dcbafe00c5c470c5c2da`
- `tla/Recovery.tla`: `68760ea28785800914c3a16ed981f5bb44eba0815a69a48ff7a70d3fe70cf33b`
- `tla/Recovery.cfg`: `73caa18525f85a3534c6e95f5389d0acc03c09732fa38cfaa3a170b5a9478df4`
- `tla/MissingRecord.cfg`: `db27fb621e6de7d9b082f173b23fd3ce35c467a7210a82e7810a07c4e3e0ca9e`
- `tla/RedCompletion.cfg`: `311924ab7256f203433cff3f02066869f142b6b02c46e2fd3d944e61ff0afece`
- `tla/RecoveryWitness.cfg`: `fd6dd8cf5882237565c1363e014db3c150b542304514084c6b10f62da6b5dce5`

Java is Temurin25.0.5+8-LTS; binary SHA-256 `1bf1aaef01e4f8d7c85d913c60fb2ee4624cbe54d4053254c59657b7ea913b25`. JAR SHA-256 is `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`; raw TLC version is2.19, rev5a47802. Exact commands, Java version, state statistics and individual results are in receipt.json.

## Evidence and limits

This directory preserves REVIEW.md, receipt.json, audit.json and all four raw logs. Private exact inputs remain in `/tmp/dawg-green-astra-inputs-1/`. No unexpected failure occurred in this independent run; intentional sensitivity/witness results are correctly labeled rather than opened as product defects.

These completed checks concern bounded protocol safety, not unlimited log contents, real filesystem durability, actual program correctness, full Git behavior or future agent/tool truthfulness. No unconditional eventual success is proven. Material model/config/dependency/requirement/assumption changes invalidate this approval and require the parent and both reviewers to execute and assess the new identity. No source files were modified and no subagents were used.
