# Shared independent walkthrough

Read the two authored skills in `plugins/pdawgy-skills/skills/` and use the requests
and raw source from `fixtures.json`. Keep evaluations inside your own `/tmp`
project roots. Use the preserved builder to reconstruct the inputs:

```sh
python .dawgy/dwag-plan/FEATURE_DAWG_INIT_AND_ARCHITECTURE/verifications/evaluation/build_fixtures.py /tmp/dawg-init-<reviewer>-eval
```

Use a fresh output root if the target already exists; do not overwrite results.
The builder creates a local Git baseline only for the mature scenario, then
applies the saved dirty/untracked changes. The other scenarios have no Git.

For each request, perform init's investigation and propose the guidance artifacts
under an `evaluation-output/` directory outside the scenario project. Do not
execute the nested dawg-plan reviewer cycle or claim that initialization passed
that gate. Label all init artifacts as proposals; no cleanup approval is supplied.
Report any material question instead of fabricating the answer.

Then run only the architecture maintenance workflow on the mature and empty
scenario roots. It may edit their `ARCHITECTURE.md` under `/tmp`; no other target
file is authorized for maintenance edits. Run maintenance a second time against
the mature scenario and compare bytes. Record what was read/changed, questions,
preserved-file hashes or diffs, and limitations. Do not spawn subagents.

## Evaluation observations

These are inspection oracles, not instructions to invent project facts.

| Scenario | Concrete observations required |
| --- | --- |
| mature init | Preserve standard-library-only rule, stable public names, `python -m unittest discover -s tests`, nested no-filesystem-side-effects scope, dirty `store.py`, and untracked `scratch-notes.txt`. Propose missing CLAUDE delegation to AGENTS. Source reveals `ledgerbox.plugins` is dynamically imported by `load_plugin.py`; do not delete it or infer it is unused. Any other cleanup stays proposed/pending. New code guidance uses simple code and no new explanatory comments while preserving functional directives. |
| claude-existing init | Preserve the unique `python release_check.py` and owner-maintained-release-file instructions. No blind pointer-only replacement. Report conflicting decisions if any, without inventing a different release workflow. |
| mature architecture | Replace the false all-in-main claim: `main.py` invokes `ledgerbox/service.py`, which delegates aggregation to `ledgerbox/store.py`; `load_plugin.py` dynamically loads `ledgerbox.plugins`. Cite source paths. Preserve the in-memory-demo rationale while avoiding a claim of persistent storage. Second run leaves document bytes unchanged unless genuinely new evidence arises. |
| empty init/architecture | Do not initialize Git, choose a stack/framework, create pretend commands, or claim production components. Ask about intended product/stack when needed for init readiness. Architecture may record only the verified empty-directory baseline and explicitly unresolved decisions; its absence must not trigger init recursion. |

Save your report and proposed outputs outside the inputs. Include a read-only
design review of the authored skills. Return actual observations and any findings
with severity and source references. A proposed init walkthrough and text-based
architecture execution do not prove real user approval or future model behavior.
