# Astra final source and recovery review

Reviewed by gpt-6-astra/high against approved plan/model revision 1. Authored plugin version: 0.5.0. Verdict: APPROVED; no material source findings.

The dawg-plan main instructions, recovery reference, failure-register asset, plan/checklist templates and UI consistently require observed failures to be recorded, diagnosed, corrected within authorization, and freshly rechecked before closure. Git/TLA integrations and dawg-init/generated AGENTS guidance retain the same rules. Root AGENTS, README and ARCHITECTURE describe the implemented instructions. No new formal contract mismatch was found.

The current phase governs green status. Future implementation checks do not block planning-only readiness. Exact named negative/witness outcomes remain distinct from unexpected failures; parser errors/timeouts/different violations do not pass. Unrelated/preexisting failures still require recording and investigation; scope decisions and genuine external blockers remain explicit. The source forbids weakened checks, unchanged blind retries, lucky flaky passes and false completion. Current input changes invalidate affected passes; material formal changes invalidate all three formal/reviewer receipts.

## Executed bounded recovery case

Actual command for all four attempts: `/usr/bin/python3 -B check.py`, cwd `/tmp/dawg-green-astra-eval/addition`. The assertion `add(2, 3) == 5` was unchanged throughout.

| Attempt | Source behavior | Actual result | Issue outcome |
| --- | --- | --- | --- |
| 1 | `a - b` | AssertionError, exit 1 | F1 recorded OPEN before correction |
| 2 | `a + b` | exit 0 | F1 resolved only after fresh pass |
| 3 | `a + b + 1` | AssertionError, exit 1 | old pass marked stale before rerun; same F1 reopened and recorded before repair |
| 4 | `a + b` | exit 0 | F1 resolved on current source and fresh evidence |

Both failed logs retain their original SHA-256 and bytes. They have equal hashes because the unchanged assertion produced the same traceback, but are distinct preserved files with distinct source snapshots and attempt identities. The final source matches attempt4; the assertion hash matches every attempt. Chronological events and pre-repair ledger snapshots establish the recording-before-repair sequence.

## Separate expected blocked case

The uniquely nonexistent `/tmp/dawg-green-astra-eval/blocked/required-verifier-2cc09c93-nonexistent --verify` was actually attempted. It raised FileNotFoundError errno 2 before process creation; its receipt correctly has no process exit code. B1 remains unchecked/BLOCKED, with required executable/path or authorized installation recorded as the dependency. No installation, bypass, fake pass or unchanged retry occurred. Independent B2 read-only AST inspection continued and passed; it does not satisfy B1. This intentionally blocked scenario remains incomplete and separate from the recovered addition case.

## Formal identity and actual-task records

Recomputed all six formal input hashes (runner, Recovery module and four configurations) and matched my prior independently executed receipt/audit exactly. Authored source corresponds to that approved protocol, so no redundant TLC rerun was required. Prior actual production run: exit 0, 178 distinct states, queue 0. MissingRecord, RedCompletion and RecoveryWitness each exited 12 with their exact intended named invariant violation. See evidence/formal-identity-check.json and evidence/prior-independent-tlc-receipt.json; full independent logs remain in `/tmp/dawg-green-astra-attempt-1/` and the parent's archived copy.

Reviewed the actual task's F1 duplicate-patch rejection and F2 README list-layout issue, their preserved old evidence, corrected README and current validation.log/tested-source.json. Records retain both issues as resolved with current-source checks. F2's current list is contiguous and recovery prose separately spaced. Fresh authored-file hashes match the current validation manifest exactly. Parent-run packaging/link/metadata checks were inspected, not independently rerun in this bounded source evaluation.

## Artifacts and limits

Archive this REPORT.md and the entire focused evidence/ directory. Key evidence: addition/attempt1–4.{json,log}, addition/attempt1–4-calc.py, immutable pre-repair/resolved ledger snapshots, addition/failures.md and verification.md, blocked/attempt1.{json,log}, blocked/failures.md and verification.md, blocked/independent-inspection.json, events.jsonl, final-audit.json, source-hashes.json, formal-identity-check.json, prior-independent-tlc-receipt.json and runner.py. The runner helper supports the actual check command; ledger/source transitions are independently recorded in the chronological evidence.

Nested fixture planning/TLA/reviews were explicitly deferred; this is a bounded recovery walkthrough, not a full nested dawg-plan run. No new agents, repository edits, GitHub mutations or application feature work occurred. The finite formal model establishes bounded protocol safety, not filesystem durability, correctness of arbitrary programs or unconditional eventual success. The concrete fixture confirms this small assertion/recovery sequence only. No screenshots are relevant.
