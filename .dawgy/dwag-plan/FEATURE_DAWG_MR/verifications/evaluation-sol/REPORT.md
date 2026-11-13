# Independent Sol authored-source review and forward evaluation

Reviewer: gpt-6.1-sol / high. Approved design/model: revision 1.
Decision: **Approve final authored source; no material findings.**

## Source review and formal correspondence

Read actual dawg-mr/SKILL.md and UI, manifest 0.6.0, README and ARCHITECTURE.
Reviewed source hashes in evidence/approved-source-hashes.json match the parent's
frozen tested-source.json. Current model/config hashes equal my actually executed
sol-01 receipt; no material formal contract changed, so no redundant rerun was
performed. Evidence/formal-input-identity.json records that comparison.

Actual skill requires pinned scope and merge-base for branch summaries, committed
blob/template/evidence inspection despite dirty work, material-base clarification,
source/direct-consumer tracing, evidence provenance and honest failed/stale/absent
outcomes. It drafts four requested topics proportionately and explicitly avoids
runtime planning/model/review/test/publication/mutation ceremonies. This matches
ScopeSound/EvidenceSound/UnknownExplicit/FourTopics without pretending the finite
model proves Git operations or prose quality. UI and repository docs accurately
add the fourth skill; manifest version is consistent.

## Real forward use

User request for the shipping fixture: “Use $dawg-mr to quickly draft an MR message
for these committed changes.” Runtime followed the authored skill rather than
merely checking its wording. Exact runtime Git argv/cwd/exits/stdout/stderr are
in evidence/runtime-readonly-commands.log; actual output is draft.md.

Committed AGENTS establishes main as MR target and the committed GitLab template
supplies the four headings. Pinned merge-base is `4fee0028ef162896cfc02a7af4ab00137a17c7d4`;
head is `7ff8c71ea4473d82d999dd2eca399bcfebfdda83`. Inspected the actual scoped log/stat/diff,
shipping.py, direct cli.py consumer, README contract, added checks, and committed
verification JSON through git show. No runtime application/test command ran.

The observed change fixes fractional-weight undercharging: int truncation billed
1.2 kg at 5 despite a per-started-kilogram contract; ceil bills it at 10. The draft
covers that behavior, relevant CLI caller and unchanged signature/rate/positive
validation without inventing deployment or broad compatibility guarantees.

Evidence was classified from committed records, not their filenames alone:

- A genuine setup quote-check pass has matching committed relevant source/check
  fingerprints and narrow fractional/whole-weight scope.
- A genuine recorded CLI-label failure has matching relevant fingerprints and
  remains visible: actual `10` versus expected `Shipping: 10`.
- The old integer-only pass fingerprints pre-fix shipping.py and is explicitly
  stale for the change.
- All setup runs preceded the commit. The draft explicitly reports that provenance
  and does not promote them into proof of a clean-HEAD execution; no current clean
  checkout rerun is established. Matching-input recorded results are distinguished
  from independent runtime execution. Evidence applicability hashes are in
  evidence/evidence-applicability.json.
- Dirty shipping.py returning 999, staged operator notes, untracked notes and an
  untracked fake all-pass record never contaminate the scoped draft.

## Empty and ambiguous scope outputs

empty-output.md responds to an explicit head..head range with no committed changes;
no problem/fix was invented from staged or dirty files.

ambiguous-output.md asks which target to compare against: main, develop or another
base. The separate fixture has divergent main/develop and a feature branch, no
MR guidance or upstream. Its actual refs/config/tree/graph were inspected. No
HEAD-parent guess, silent fetch or speculative MR message was made.

## Read-only preservation and self-contained artifacts

Both runtime before/after snapshots match exactly for HEAD, all refs, full status,
raw index-file SHA-256 and every non-Git file. No Git commit, switch, staging,
worktree creation, test execution, network, push, MR publication or nested review
occurred during drafting. Git optional locks were disabled for read-only status.
Setup-only operations are separately logged in evidence/setup-commands.log.

Committed base/head file snapshots and working-file snapshots are under evidence/;
raw fixture inputs, setup writes, actual verification runs, identities and runtime
outputs are archived, excluding .git databases. A setup import-path invocation
failed before correction to module execution; its raw error and resolution remain
in setup log and SETUP_NOTES.md. It is not concealed or treated as a skill defect.

## Bounds

This is a small concrete shipping fix and three requested runtime cases, not an
exhaustive Git/evidence/prose-quality proof. There was no network/remote refresh,
GitLab/GitHub mutation or actual project-source edit. Setup tests exist to create
real records; none was launched to fill the runtime message. Formal bounded
safety remains distinct from actual draft quality and provenance judgment.
Packaging/actual task delivery are the parent's separate checks. No screenshot
applies. Approval covers evidence/approved-source-hashes.json.
