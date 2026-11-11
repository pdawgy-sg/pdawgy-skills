# Verification: Mandatory TLA+ planning

Plan: [../PLAN.md](../PLAN.md). Source/model revision: 1.
Working directory: the mapped worktree recorded in PLAN.md.
Implementation: VERIFIED. Delivery: PENDING (pre-delivery snapshot).

- [x] V1 — Parent and both exact reviewers run TLC, inspect model/requirements/probes and current hashes (T1; AC1–AC3, formal transitions/invariants).
- [x] V2 — Both final-source reviews and standard skill/metadata/link checks (T1/T2; AC1–AC5 outside abstract model).
- [ ] V3 — Scoped Conventional Commit/push with exact tested tree and remote OID (T3; AC5).

## V1 — Reproducible TLC execution

Installed tooling: explicit Java 25.0.5 binary and tla2tools 1.7.4 (TLC 2.19).
Use the exact run below with a fresh output directory for each agent/attempt:

```sh
python .dawgy/dwag-plan/FEATURE_DAWG_PLAN_TLA_VERIFICATION/verifications/run_tlc.py --java /home/chy/.local/share/mise/installs/java/temurin-25.0.5+8.0.LTS/bin/java --jar /home/chy/.local/share/mise/installs/http-tla2tools/1.7.4/tla2tools.jar --output /tmp/dawg-tla-REVIEWER-attempt-N
```

The runner records exact argv, model/config/JAR/Java hashes, Java version, exit
status and state statistics for all four configurations. TLC output records its
version and coverage; fresh metadata dirs are temporary. Each reviewer must also
inspect the runner, enabled properties/configuration and raw logs to avoid relying
only on its summary. Local socket capability may require approved execution;
record environmental blockers, not fake counterexamples. Do not write into or
overwrite the parent's run; save reviewer outputs in separate directories and
copy them into tla/runs/<reviewer>/ after completion. No new subagents are needed.

Expect production configs completed exit 0, nontrivial reachable states and empty
queues; negative/witness configs nonzero with the specific expected invariant and
trace. Expected violations are separate probes, not required-property failures.
Check model/config/dependency hashes agree across parent and reviewers. Assess
assumptions, bounds, requirement mapping, deadlock/liveness choices, vacuity,
invalidation on revision changes, and implementation abstraction limitations.

Actual parent: attempt 1 BLOCKED by local socket restrictions (exit 255); attempt
2 complete with expected outcomes: 210/202 positive distinct states, both queue 0;
negative/witness traces exit 12. Both exact reviewers independently ran/audited
all four configs with matching final inputs/tools and approved semantic review.
Their first socket-blocked attempts and fresh successful attempts are preserved.
Evidence: tla/runs/{primary,astra,sol}-attempt-{1,2}/, both design review records,
run_tlc.py and validation.log input-identity check. Status: PASS within stated scope.

## V2 — Authored skills and packaging

After implementation, both reviewers inspect changed source against this plan,
formal model and current receipts. Rerun TLC/review if the formal contract changes;
an unchanged model/config identity may reuse its same-revision executed receipts.
Run from this worktree with existing isolated PyYAML:

```sh
for skill in dawg-plan dawg-init; do
  PYTHONPATH=/tmp/dawg-plan-validation-deps python /home/chy/.codex/skills/.system/skill-creator/scripts/quick_validate.py "plugins/pdawgy-skills/skills/$skill" || exit 1
done
python -m json.tool .agents/plugins/marketplace.json > /dev/null
python -m json.tool plugins/pdawgy-skills/.codex-plugin/plugin.json > /dev/null
git diff --check
```

Parse UI YAML; confirm automatic discovery/invocation, manifest 0.4.0, relative
resource/document links and exact intended task file set. Inspect new reference
and evidence whitespace, model syntax and TLC logs. Hash tested source files in
validation.log/tested-source.json; confirm no prior tracked .dawgy artifact edits.
Manual source reviews verify mandatory concrete models, both independent runs,
blocked/incomplete/stale behavior, preserved implementation tests, Git gates and
caller consistency. This does not prove future agent compliance.
Actual: both final-source reviewers approved with no material findings and
confirmed unchanged formal input/runner/evidence identity. Both changed skills
validate; UI YAML, invocation, JSON, links, manifest0.4.0, source scope and whitespace
checks pass. All three actual formal receipt identities match current inputs/tools.
No tracked historical evidence changed. Source fingerprints saved for 11 changed
implementation files.
Evidence: final-review-{astra,sol}.md, final-source-hashes-{astra,sol}.json,
validation.log and tested-source.json. Status: PASS.

## V3 — Actual delivery

Only stage explicit task paths and this new plan/evidence after V1/V2 pass. Verify
all index entries/hunks task-owned, record intended index tree and source hashes,
create the Conventional Commit in PLAN.md, then compare the entire commit tree
and delta with that inspected index and tested fingerprints. A mutation stops push.

```sh
git push --set-upstream origin HEAD:refs/heads/codex/feature/dawg-plan-tla-verification
git rev-parse HEAD
git ls-remote origin refs/heads/codex/feature/dawg-plan-tla-verification
git status --short --branch
```

Expected: normal task-branch push with exact remote/local OID match and clean
worktree; no base-branch mutation. Final commit/push receipt in chat, with this
ledger remaining a truthful pre-delivery snapshot. Actual checkpoint: V1/V2 pass;
commit/push receipt follows in chat after actual execution. No future success is
claimed here. Status: delivery pending.
