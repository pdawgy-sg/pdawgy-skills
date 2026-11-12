# Verification: repair until green

Plan: [../PLAN.md](../PLAN.md). Revision1. Working directory: mapped worktree in plan.
Implementation: VERIFIED. Delivery: PENDING (pre-delivery snapshot).
Failures: [failures.md](failures.md). No actual unexpected failure currently open.

- [x] V1 — Parent and both exact reviewers run/audit current TLA configs and semantic mapping (T1; AC1/AC2/AC4).
- [x] V2 — Concrete red/green/reopen/blocked fixture and independent final-source/packaging checks (T1/T2; AC1–AC5).
- [ ] V3 — Task-only Conventional Commit and normal push with exact remote OID (T3; AC4/AC5).

## V1 — Formal runs

Use installed Java25.0.5 and tla2tools1.7.4 (TLC2.19), fresh outputs per role/attempt:

```sh
python .dawgy/dwag-plan/FEATURE_DAWG_PLAN_GREEN_VERIFICATION/verifications/run_tlc.py --java /home/chy/.local/share/mise/installs/java/temurin-25.0.5+8.0.LTS/bin/java --jar /home/chy/.local/share/mise/installs/http-tla2tools/1.7.4/tla2tools.jar --output /tmp/dawg-green-ROLE-attempt-N
```

TLC requires an approved local monitoring socket; use available authorized
execution rather than claim a blocked run passed. Read runner, configs, properties,
raw outputs and exact hashes. Required Recovery.cfg must complete exit0, nontrivial
states/queue0, all enabled properties pass. Other configs must produce the exact
expected named invariant and trace; parse/runtime failures do not satisfy them.
Parent and both exact reviewers independently observed 178 distinct states and
the three named expected probe traces, then approved matching current inputs.
All raw runs/audits are preserved under tla/runs/. Material model/contract
changes require all three actual reruns. No liveness/code-durability proof claimed.

## V2 — Bounded behavioral fixture and packaging

After authoring, each reviewer reads the actual skill and shared
[recovery-walkthrough.md](recovery-walkthrough.md), uses its own /tmp root, and
applies the recovery instructions to the raw fixture. Nested model/reviewer gates
are explicitly deferred in that isolated fixture; do not fabricate their execution.
Save exact commands/exits, raw failed/pass logs, issue ledger, statuses, source
identities, preserved failed-log hashes and observations. An intentionally blocked
fixture must remain visibly blocked; that expected response is not an unresolved
product failure in this task. Both final-source reviewers must confirm the policy
matches the approved TLA abstraction, finite limits and Git/phase boundaries.

Run real packaging checks in this task worktree:

```sh
for skill in dawg-plan dawg-init; do
  PYTHONPATH=/tmp/dawg-plan-validation-deps python /home/chy/.codex/skills/.system/skill-creator/scripts/quick_validate.py "plugins/pdawgy-skills/skills/$skill" || exit 1
done
python -m json.tool .agents/plugins/marketplace.json > /dev/null
python -m json.tool plugins/pdawgy-skills/.codex-plugin/plugin.json > /dev/null
git diff --check
```

Parse changed UI YAML, inspect new assets/reference and local Markdown links,
manifest0.5.0, intended source diff and no prior .dawgy edits. Save exact commands,
results and final implementation hashes in validation.log/tested-source.json.
Any actual failed attempt gets F ID in failures.md before correction/rerun; close
only with evidence. Expected outcome: current checks pass, both final reviews
approve, no unresolved actual issue, meaningful fixture behavior recorded.

## V3 — Delivery checkpoint

Only after phase-relevant V1/V2 checks and actual issue exit criteria pass, stage
explicit task paths and current plan artifacts. Inspect entire index/file set,
record intended tree, create the Conventional Commit in PLAN.md, compare the full
created tree/delta and tested fingerprints, then push normally:

```sh
git push --set-upstream origin HEAD:refs/heads/codex/feature/dawg-plan-green-verification
git rev-parse HEAD
git ls-remote origin refs/heads/codex/feature/dawg-plan-green-verification
git status --short --branch
```

Final actual receipt in chat; this committed ledger remains pre-delivery. A push/
hook/remote-check error is recorded and worked through within authorization; no
force, bypass, false green, implicit main merge or unrelated changes.

## Observed V2 results

Both final-source reviews approved revision1 without material findings. Each
reviewer's real fixture exits were 1/0/1/0: record before repair, fresh resolution,
invalidate/reopen on regression, repair/rerun again, failed logs and assertion
unchanged. The separate missing-tool case remains BLOCKED/unchecked while an
independent inspection passed. That is a declared expected-response test, not an
unresolved actual product defect. Reports/evidence: evaluation/astra/ and
 evaluation/sol/. Formal input identities remain unchanged. Source validators,
JSON/UI/resources/links/whitespace/scope checks pass with hashes for all 14 source
files in validation.log/tested-source.json. Actual F1/F2 resolutions preserve
failed observations; F3 final metadata correction passed the actual link/fingerprint checks; its failed attempt is preserved. V1/V2 PASS; zero actual issues unresolved.
