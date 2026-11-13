# Verification ledger

Pre-delivery snapshot: implementation VERIFIED; delivery PENDING. Final whole
staged-tree/commit comparison and push receipt belong in chat. No screenshot applies.

| ID | Task / criteria | Actual procedure and result | Status / evidence |
| --- | --- | --- | --- |
| V1 | T1 / AC2-5 / TR1-5 | Parent and both exact high-effort reviewers independently ran run_tlc.py with Java25.0.5/TLC2.19; required configuration exit0, 1128 generated/72 distinct/queue0; both probes exit12 at exact named invariant with trace. All final model/config hashes match. Both semantic reviews approved revision1. | PASS; tla/runs/parent-02/, astra-01/, sol-01/; parent-formal-review.md and design-review-{astra,sol}.md |
| V2 | T2-3 / AC1/6 | From repository root: `PYTHONPATH=/tmp/dawg-plan-validation-deps python .dawgy/dwag-plan/FEATURE_DAWG_MR/verifications/check_structure.py`. Validator exit0; JSON/UI metadata, discovery/version0.6, Markdown links and source whitespace pass. Frozen source matches both reviewers. | PASS; structure-01.log, check_structure.py, tested-source.json |
| V3 | T2 / AC2-5 / TR1-5 | Both reviewers actually followed the authored skill on independent isolated Git fixtures. Four-topic drafts trace real changes/consumers and preserve current failures, stale/absent evidence limitations and provenance. Dirty/staged/untracked distractors excluded. Empty range reports no changes; materially ambiguous base asks a focused question. Runtime did not launch tests or mutate Git/files. Before/after fingerprints match. | PASS; evaluation-astra/REPORT.md and evaluation-sol/REPORT.md, actual drafts and raw setup/runtime/evidence snapshots |
| V4 | T4 / all | Verified current branch/root/base, empty existing index and frozen reviewed source. Whole staged-tree audit and Conventional Commit/push with exact remote OID confirmation are delivery steps after this snapshot; no claim they already ran. | Preflight PASS; delivery PENDING; final receipt in chat |
| V5 | T3 / AC1/6 | Refreshed previously installed local plugin using temporary marketplace source override. All 18 package files byte-identical to version0.6 cache, plugin enabled, persistent source remains original checkout. | PASS; installation.json |

## Evidence scope

Real setup commands generated fixture application pass/fail logs; expected
application failures are input data to verify truthful drafting, not plugin
failures to repair. No tests ran merely to write the runtime MR messages.
Formal checks cover a bounded evidence/scope protocol, not arbitrary Git, prose,
or future agent correctness. Practical fixtures complement that abstraction.
F1 model-generator error, F2 insufficient ambiguity fixture, F3 setup import error
are resolved with old attempts retained in failures.md and linked evidence.

Reproduce formal runs from plan root using `python verifications/run_tlc.py
--java /home/chy/.local/share/mise/installs/java/temurin-25.0.5+8.0.LTS/bin/java
--jar /home/chy/.local/share/mise/installs/http-tla2tools/1.7.4/tla2tools.jar
--output <fresh-directory>` as one command. Java needs a permitted local monitoring
socket. Each receipt records exact commands, Java/JAR identities and input hashes.
