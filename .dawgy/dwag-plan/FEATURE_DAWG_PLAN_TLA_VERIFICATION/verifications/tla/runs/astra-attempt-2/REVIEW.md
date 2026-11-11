# Astra independent TLA+ design review

Reviewer: gpt-6-astra / high. Reviewed plan/model revision: **1**. Date: 2026-11-12.

**Approved: no material design/model findings.** Approval is bounded to the specified model/configuration identities and semantic contract below. Authored-skill implementation and its tests remain pending.

## Independent execution and environmental history

Read the actual PLAN.md, verification.md, PlanGate.tla, all four individually identified configurations, and run_tlc.py. Copied the runner and five formal input files byte-for-byte into `/tmp/dawg-tla-astra-inputs-1`; verified original and copied SHA-256 before and after execution. The copy confines any TLC-generated trace artifacts to /tmp and does not change the evaluated content.

Executed the documented runner independently with explicit Java/JAR, using private state directories and logs:

```sh
python /tmp/dawg-tla-astra-inputs-1/run_tlc.py --java /home/chy/.local/share/mise/installs/java/temurin-25.0.5+8.0.LTS/bin/java --jar /home/chy/.local/share/mise/installs/http-tla2tools/1.7.4/tla2tools.jar --output /tmp/dawg-tla-astra-attempt-1
```

Attempt 1 is preserved: all four configurations parsed but exited 255 because the sandbox denied TLC's local RMI monitoring socket (`java.net.SocketException: Operation not permitted`). No model counterexample or completed check was claimed. The runner correctly returned failure for all four, including the expected-negative cases.

Repeated the same command with fresh output `/tmp/dawg-tla-astra-attempt-2` under approved local execution. This independently executed all four configurations and the runner exited 0. No external service was used. I inspected all four raw logs and their traces/coverage rather than accepting the parent's summary. Attempt 1 was not overwritten.

| Configuration | Exit | Distinct states | Queue left | Observed result |
| --- | --- | --- | --- | --- |
| PlanGate.cfg | 0 | 210 | 0 | Completed; all configured safety invariants hold |
| PlanOnly.cfg | 0 | 202 | 0 | Completed; all configured safety invariants hold |
| MissingReview.cfg | 12 | 18 | 15 | ReadinessSound named trace |
| ReachReady.cfg | 12 | 198 | 21 | NoReadyReached named trace |

Nonempty queues for the two intentional invariant-violation probes are expected because TLC stops on the requested witness/counterexample. They are not production completion results. Both production checks have completion messages and empty queues.

## Model and requirement assessment

The model describes this feature's readiness/verification workflow, rather than pretending to model arbitrary project code. `ReadinessSound` requires a current successful parent run, both current reviewer passes, and both semantic approvals for every ready-or-later phase. `Revise` advances the bounded revision and clears parent/reviewer receipt identities, approvals, and implementation verification before returning to draft. A reviewer rerun also clears that reviewer's approval. This aligns with the stated invalidation policy; actual content hashing and truthful tool execution remain implementation obligations.

`ImplementAuthorized` is checked both TRUE and FALSE. `DeliverySound` requires authorization, passed implementation verification, and current formal/reviewer checks before committed/delivered states. `PlanningOnlySafe` prevents the planning-only configuration from reaching implementation or delivery. AC1–AC3's gate maps meaningfully to these actions/invariants; Git mechanics, tool honesty, and code/model refinement are explicitly outside the abstract model and belong to source/runtime verification.

The finite domain is exactly two reviewers and revisions 0 and 1. There are no fairness assumptions or liveness properties. CHECK_DEADLOCK is enabled in every configuration. `Hold` is limited to ready and delivered; retry/failure actions elsewhere may also self-loop. Thus no TLC deadlock was found, but this does not assert that real tools, external decisions, or approvals eventually progress. The lack of a liveness guarantee is accurately disclosed.

## Anti-vacuity and probe audit

The production authorized run's coverage shows two successful MarkReady transitions, revision activity, and successful Implement/Verify/Commit/Push transitions. The planning-only coverage shows ready is reachable, while Implement/Verify/Commit/Push have zero successors. The safety checks therefore do not merely pass because the relevant downstream states are universally unreachable.

MissingReview.cfg alone disables EnforceReviewChecks. Its concrete three-state trace is Init → CheckParent(pass) → MarkReady, with both reviewer results still pending and approvals empty; ReadinessSound is the named violation. This tests sensitivity to missing independent reviews without weakening production configurations.

ReachReady.cfg keeps the production review gate enabled and intentionally asserts NoReadyReached. Its seven-state trace includes parent pass, both reviewer passes, both approvals, and readiness. The named violation is the expected valid-readiness witness. Neither negative result is a syntax error, runtime exception, or ordinary production-property failure disguised as success.

## Runner and identity audit

Audited the runner's commands, timeout handling, fresh state directories, exit checks, raw-log saving and state-statistic extraction. Production success requires exit 0, TLC's completion message, a nontrivial state count and an empty queue. Expected-negative success requires a nonzero exit, the exact named invariant message and a behavior trace; I additionally checked the actual exit 12 and trace contents manually. The runner is suitable for these fixed inputs; its summary alone would not establish semantic coverage or replace this audit.

Parent and independent reviewer receipts match module/config identities, Java/JAR identities, tool version, and expected outcomes. Original and copied inputs remained unchanged through checking. Model imports are standard modules from the pinned JAR; their member hashes are recorded in audit.json. No custom module dependency was omitted.

Input SHA-256:

- `run_tlc.py`: `08aef3139ab1c5f9b1006a973b0c303be38ef141064109cdc00d54a0f573e460`
- `tla/PlanGate.tla`: `3cf6163591753c3786e82bf1f7fe936aba9ea2330056ece4b867f53e43b3d4de`
- `tla/PlanGate.cfg`: `326538716e53e3a88bce5c91dbe2fd58f6377c9c1996e109718476f4eda79d60`
- `tla/PlanOnly.cfg`: `bf4957471308effbcf93257f4a1882b6807a27e4785870e0238f06362c1f4947`
- `tla/MissingReview.cfg`: `1f1b29ebf4d90a02da8c0727ede127db1e63e9fb618a45686fe25444d73e6563`
- `tla/ReachReady.cfg`: `d5412f4e5f518e3abdfcddff3ffd22b0a9150e7eaae7ac80bf69432ea98e5cc3`

Tool identities:

- Java: Temurin 25.0.5+8-LTS, binary SHA-256 `1bf1aaef01e4f8d7c85d913c60fb2ee4624cbe54d4053254c59657b7ea913b25`.
- tla2tools JAR: SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`.
- Raw TLC version: 2.19 of 08 August 2024, rev 5a47802.

## Evidence and limits

- Successful run: `/tmp/dawg-tla-astra-attempt-2/`, including this REVIEW.md, receipt.json, audit.json and all four raw .log files.
- Preserved environmental failure: `/tmp/dawg-tla-astra-attempt-1/`.
- Exact private runner/model/config copies: `/tmp/dawg-tla-astra-inputs-1/`.

These are completed finite safety checks for the configured abstraction, plus deliberately separated sensitivity/reachability probes. They are not an unbounded theorem, liveness guarantee, proof of arbitrary implementation code, proof of future agent compliance, or verification of filesystem/Git effects. Real implementation tests remain mandatory and proportionate. Material changes to behavior, model/config/dependencies, bounds, assumptions, properties or fairness invalidate this approval and require the parent and both reviewers to recheck the final identity. No source files were modified and no subagents were spawned.
