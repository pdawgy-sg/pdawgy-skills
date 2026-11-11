# Sol independent formal design review — revision 1

Reviewer: gpt-6.1-sol / high.
Decision: **Approve revision 1; no material design/model findings.**

## Independent execution and audited evidence

Executed the documented source run_tlc.py with the exact installed Java and JAR.
Attempt 1 at `/tmp/dawg-tla-sol-attempt-1` independently reproduced the local RMI
monitoring socket denial: all four configs exit 255, no state exploration. Its
raw logs and failed receipt remain preserved and are environmental blockers,
not counterexamples. A separately approved require_escalated call ran all four
again into fresh `/tmp/dawg-tla-sol-attempt-2`, enabling only the necessary local
execution capability. No external service was contacted or claimed.

Successful attempt results, read from the raw logs and independently checked
against their enabled configs rather than merely trusting the receipt:

| Config | Exit | Generated / distinct / queue | Actual interpretation |
| --- | --- | --- | --- |
| PlanGate.cfg | 0 | 2083 / 210 / 0 | completed finite production model; all four invariants hold |
| PlanOnly.cfg | 0 | 2066 / 202 / 0 | completed planning-only production model; all four invariants hold |
| MissingReview.cfg | 12 | 21 / 18 / 15 | intended ReadinessSound counterexample, with named violation and three-state trace |
| ReachReady.cfg | 12 | 1807 / 198 / 21 | intended NoReadyReached reachability witness, with seven-state trace |

Nonempty queues in the two probes are expected because exploration deliberately
stops at the named witness/counterexample. They are not completed production
checks or passing production invariants. Both positive queues are empty.

I inspected the full runner before executing, individual config contents, raw
parsing/status/coverage output, negative trace states and final state statistics.
Positive checks require exit 0, explicit completion marker, >1 distinct state and
queue 0. Negative checks require a nonzero exit plus the exact intended invariant
and a behavior trace; syntax/runtime errors alone do not meet those predicates.
The actual negative exits are TLC invariant-violation exit 12, not an unrelated
error. I additionally checked no Error marker appears in positive raw logs.
No source edit, tool substitution or skipped check was used to obtain success.

Raw logs and receipt.json preserve exact Java argv, fresh state-directory paths,
TLC versions, exit codes, statistics and input/tool hashes. independent-audit.json
adds runner and raw-log hashes, final-input identity checks, and reviewer identity.
Copies of inspected model/configs/runner are in audited-inputs/.

## Tool and input identities

Java: Temurin OpenJDK 25.0.5+8 LTS, explicit binary
`/home/chy/.local/share/mise/installs/java/temurin-25.0.5+8.0.LTS/bin/java`.
TLC: 2.19, 08 August 2024, rev 5a47802; installed tla2tools 1.7.4 JAR
`/home/chy/.local/share/mise/installs/http-tla2tools/1.7.4/tla2tools.jar`.

- Java binary SHA-256: `1bf1aaef01e4f8d7c85d913c60fb2ee4624cbe54d4053254c59657b7ea913b25`
- TLC JAR SHA-256: `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`
- run_tlc.py SHA-256: `08aef3139ab1c5f9b1006a973b0c303be38ef141064109cdc00d54a0f573e460`
- PlanGate.tla SHA-256: `3cf6163591753c3786e82bf1f7fe936aba9ea2330056ece4b867f53e43b3d4de`
- PlanGate.cfg SHA-256: `326538716e53e3a88bce5c91dbe2fd58f6377c9c1996e109718476f4eda79d60`
- PlanOnly.cfg SHA-256: `bf4957471308effbcf93257f4a1882b6807a27e4785870e0238f06362c1f4947`
- MissingReview.cfg SHA-256: `1f1b29ebf4d90a02da8c0727ede127db1e63e9fb618a45686fe25444d73e6563`
- ReachReady.cfg SHA-256: `d5412f4e5f518e3abdfcddff3ffd22b0a9150e7eaae7ac80bf69432ea98e5cc3`

After executing independently, I compared input/tool hashes and actual outcomes
with primary-attempt-2: model, each config, Java binary and JAR hashes agree;
state counts/exits agree. This comparison supplements independent execution and
semantic audit; it is not the basis for trusting the parent's receipt.

## Semantic review and requirement mapping

PlanGate.tla models the product being changed here: formal planning/review
readiness and authorized delivery gates. The abstraction is relevant to the
requested instruction-workflow change rather than an unrelated sample system.

- Init starts pending/draft. CheckParent and CheckReviewer distinguish pass,
  fail and blocked results. Approve requires the named reviewer's successful
  current-revision check. CurrentChecks requires a current successful parent and
  both distinct named reviewer checks plus both semantic approvals.
- MarkReady enforces CurrentChecks in both production configs. ReadinessSound
  checks every non-draft phase. MissingReview.cfg alone intentionally disables
  the reviewer gate: its actual trace reaches ready after only parent pass, while
  both reviewer results/approvals remain absent. This is a meaningful sensitivity
  check for the independent-review requirement, not a syntax/error proxy.
- ReachReady.cfg keeps the real reviewer gate enabled. Its trace executes parent
  pass, Astra pass, Sol pass, both approvals, then MarkReady. Readiness is therefore
  reachable; the positive safety result is not due to an impossible ready phase.
  Positive coverage also reaches Implement, Verify, Commit and Push when authorized;
  those actions have zero reached transitions in PlanOnly as intended.
- Revise increments the modeled revision and resets parent/reviewer results,
  receipt revisions, approvals and implementationPassed to pending/unverified.
  Both checked bounds include revisions 0 and 1. Reacquiring readiness after
  revision thus requires fresh parent/reviewer checks and approvals. The plan
  separately invalidates operational receipts on changes to behavior, spec,
  config, assumptions, bounds/properties and fairness (PLAN.md:36–38).
- Implement is guarded by ImplementAuthorized; Verify(TRUE) precedes Commit.
  PlanningOnlySafe and DeliverySound preserve the existing planning/delivery
  boundary. Push failure stays committed rather than claiming delivered.
- Requirement mapping in PLAN.md:77–110 accurately distinguishes abstract gate
  properties from Git/filesystem execution and source inspection requirements.
  TLA checks do not replace proportionate implementation checks.

## Finite bounds, deadlock, fairness and limitations

Exactly two named reviewers, fixed result/phase sets and MaxRevision=1 make these
configs finite. ImplementAuthorized is separately checked TRUE and FALSE. No state
constraint or symmetry reduction silently excludes the relevant readiness path.
EnforceReviewChecks is TRUE in production and is not an optional user workflow
setting. The FALSE setting belongs only to the labeled sensitivity probe.

CHECK_DEADLOCK is TRUE in every config. Hold allows intentional unchanged ready
handoff and delivered terminal states; result retry self-loops represent waiting
or blocked outcomes. Spec includes stuttering, no fairness condition and no checked
liveness/progress property. Consequently no eventual readiness/delivery or tool
availability is claimed. The successful run checks bounded safety, with TLC's
normal fingerprinting assumptions; it is not an unbounded mathematical proof.

Receipt variables abstract genuine tool outcomes. This model does not prove that
an agent really ran TLC, validate truthfulness, model delayed asynchronous stale
callbacks, or prove filesystem/Git operations, code refinement, credential behavior,
or arbitrary parameter sizes. Concrete hash/input matching, raw-log audit and
independent reviewer execution enforce the operational contract outside that
abstraction. No weakening is needed for the stated bounded claims.

This review approves design/model revision 1, not future authored skill behavior
or implementation verification. The final guide/source must preserve this formal
contract; any material contract/input change invalidates these receipts and
requires parent plus both exact reviewers to rerun and reassess. Source authoring,
packaging checks, scoped commit/push and their final review remain pending.

## Preserved artifacts

- `/tmp/dawg-tla-sol-attempt-1/`: all initial blocked raw logs/receipt.
- `/tmp/dawg-tla-sol-attempt-2/`: all four successful-attempt raw logs, receipt,
  independent-audit.json, audited-inputs/, and this REVIEW.md.

No source repository file was edited by this reviewer. All review outputs are
under /tmp. No additional agents were spawned.
