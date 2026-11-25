# GRA-6 pre-delivery verification

This snapshot covers the candidate built on `f855c25e12804c5953821bb12f34d3649c371482`, which includes GRA-5's lint guidance. Two separate builds of `dawg-0.13.0.zip` produced SHA-256 `e1fcd90b6342c9405427bd1eac28d64db7300d934c3cafd8682c574e714ac402`.

| Check | Observed result |
| --- | --- |
| Build and static checks | Four JSON manifests, Python compilation, whitespace checks, and six skill entrypoints passed. The archive contains a root entrypoint and 38 canonical files. |
| OpenBot validation and install | The upstream validator accepted the ZIP. Clean workspaces found six skills in both provider directories, with matching names, links, file hashes and executable flags under one lock entry. |
| Update and recovery | Revisions 1 and 2 installed on the selected profiles. A controlled folder collision preserved the existing file and saved the pack revision. Retrying that revision succeeded after removing the fixture conflict. |
| Installed Codex invocation | The installed `dawg-plan` read its local references, ran Git and Java checks, and loaded TLC. OpenBot emitted distinct start and completion events for Astra/high and Sol/high. |
| Native catalogs | Both native installs discovered five skills. Claude Code strict validation passed and enumerated all four native phase agents. |
| Bounded model check | The author and two independent reviewers each checked the same final inputs with TLC. Each run passed six invariants and three progress branches across 2,683 distinct states, with zero states left. Both semantic reviews approved. |

The first live candidate run reached both pinned workers and omitted the Git probe. The harness was updated to require successful Git commands and separate worker paths. The rerun passed.

Claude Code SDK initialization found all six OpenBot commands. It exposed zero native Dawg phase agents with user settings off and all four qualified native types with the plugin installed and user settings on. The definitions retain their effort pins. No Claude phase dispatched. This run exercised installed Codex delegation for the planner and primary review pins. The Codex dependency probe identified the additional review and implementation pins, and the repository task used its own independent reviewer and implementer contexts. Public OpenBot availability requires approval of a submitted Marketplace version.

Run the build and native checks from the candidate repository root. Use separate fresh temporary provider configurations for the install checks.

```sh
python scripts/build_openbot_pack.py --output "$DAWG_TMP/first"
python scripts/build_openbot_pack.py --output "$DAWG_TMP/second"
cmp "$DAWG_TMP/first/dawg-0.13.0.zip" "$DAWG_TMP/second/dawg-0.13.0.zip"
git diff --check
python -m py_compile scripts/build_openbot_pack.py
codex plugin marketplace add "$PWD"
codex plugin add pdawgy-skills@pdawgy-skills
codex plugin list --marketplace pdawgy-skills
claude plugin validate --strict .
claude plugin validate --strict plugins/pdawgy-skills
claude plugin marketplace add "$PWD"
claude plugin install --scope user pdawgy-skills@pdawgy-skills
claude plugin details pdawgy-skills@pdawgy-skills
```

The isolated OpenBot run used the local skill tool dispatcher and live Codex test adapter from OpenBot source revision `be7160839d309a005396c696390dd7326a76a500`. The case runner and full raw receipts are saved in the GRA-6 plan evidence. [OpenBot skill-pack contract](https://github.com/nightly-labs/openbot/blob/55160bd404b76459a5a2f434c490a97eca85212e/docs/architecture/skills-and-plugins.md#local-skill-library)
