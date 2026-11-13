# Failures: repair until green

Plan: [../PLAN.md](../PLAN.md). Checks: [verification.md](verification.md).
Open / in-progress / blocked issues: 0.
Current phase: implementation; model/plan revision1 unchanged.

## F1 — Integration patch rejected

- Status: RESOLVED
- Affects: T2, V2 source integration and packaging validation.
- Expected: apply the reviewed Git/TLA/caller/docs/version changes atomically.
- Actual: apply_patch rejected duplicate update operations for README.md; nothing
  from that failed patch was applied.
- Reproduction: submit a single patch with two Update File operations targeting
  the same README.md. The patch tool rejects that structure.
- Cause: duplicate README target stanzas in the prepared patch.
- Correction / next action: combine its hunks under one update, apply again,
  inspect resulting scope and run affected packaging/link/whitespace checks.
- Exit criteria: corrected patch applies and the intended source integration,
  both skill validators, links, JSON and whitespace checks pass on current files.
- Resolution: corrected patch applied; both skill validators and current JSON/UI/link/whitespace/scope checks pass. See [validation.log](validation.log) and tested-source.json. Failed attempt retained.

| Attempt | Input / operation | Actual outcome | Evidence | Next action |
| --- | --- | --- | --- | --- |
| F1-1 | T2 integration patch | rejected, duplicate README target | [F1-patch-attempt-1.txt](attempts/F1-patch-attempt-1.txt) | combine target hunks and retry |
| F1-2 | corrected patch/current source | applied; affected checks pass | [validation.log](validation.log) | resolved on recorded current source hashes |

Expected negative/witness model probes are distinct from this actual tool error.
No old failure evidence has been overwritten.

## F2 — Recovery paragraph interrupted the Included skills list

- Status: RESOLVED
- Affects: T2, V2 README source/rendering inspection.
- Expected: three parallel skill entries remain one list, with recovery guidance
  as a separate paragraph after that list.
- Actual: the inserted paragraph split the list and ran into the next bullet.
- Cause: integration insertion point was immediately after the dawg-plan item.
- Correction / next action: move the paragraph after all three entries; inspect
  resulting CommonMark spacing and rerun affected links/whitespace checks.
- Exit criteria: contiguous three-entry list and separately spaced recovery prose;
  current link/whitespace checks pass.
- Resolution: contiguous skill list and separate recovery paragraph inspected; current local links/whitespace checks pass. See [validation.log](validation.log) and tested-source.json.

| Attempt | Input / operation | Actual outcome | Evidence | Correction / next action |
| --- | --- | --- | --- | --- |
| F2-1 | README included-skills source inspection | recovery prose interrupted list | [F2-readme-before.txt](attempts/F2-readme-before.txt) | move prose after all three entries |
| F2-2 | corrected current README | layout inspected; links/whitespace pass | [validation.log](validation.log) | resolved on recorded current source hashes |

All observed actual issues are resolved. Both final behavioral/source reviews passed. No future delivery is claimed here.

## F3 — Final evidence update used stale patch context

- Status: RESOLVED
- Affects: final plan/checklist metadata and delivery readiness, not tested source.
- Expected: update the completed-check evidence without changing implementation.
- Actual: apply_patch rejected an unmatched expected PLAN.md text block; no edits applied.
- Cause: assumed line wrapping instead of matching the current document.
- Correction / next action: read actual current sections, update them against exact
  content, and inspect final plan/checklist/status links and failure counts.
- Exit criteria: current metadata accurately records completed checks, links resolve,
  F3 is resolved with evidence, source fingerprints/formal inputs remain unchanged.
- Resolution: exact current metadata updated, plan/checklist/review/evidence links resolve, and all 14 tested implementation hashes remain unchanged. See F3-2 evidence.

| Attempt | Input / operation | Actual outcome | Evidence | Next action |
| --- | --- | --- | --- | --- |
| F3-1 | final metadata patch | unmatched PLAN context, rejected | [F3-evidence-update-attempt-1.txt](attempts/F3-evidence-update-attempt-1.txt) | inspect exact text and correct metadata |
| F3-2 | exact inspected metadata | updated; links/current source fingerprints verified | [F3-evidence-update-attempt-2.txt](attempts/F3-evidence-update-attempt-2.txt) | resolved |
