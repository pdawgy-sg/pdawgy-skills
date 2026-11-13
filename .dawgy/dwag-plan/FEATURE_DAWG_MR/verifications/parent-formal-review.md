# Parent formal inspection — design revision 1

Executed `run_tlc.py` with the absolute Java and JAR paths recorded in
`tla/runs/parent-02/receipt.json`. Inspected source/configs and raw outputs.
Module SHA256 db3c6030a23d837c85992514d4df4959a32f70425fca346708b8e60aa03dc40c.

Production: 32 initial states, 1128 generated / 72 distinct / queue 0, exit 0;
TypeOK, ScopeSound, EvidenceSound, UnknownExplicit, FourTopics enabled.
Resolve covers blocked/empty/inspect; Draft has eight distinct output cases
(4 evidence classes times dirty/clean), with current pass, failed and unverified
outcomes. NewRequest supports resolving unknown scope without removing failures.
Deadlock checking enabled; valid terminals explicitly Hold. No fairness,
constraints, reductions or liveness claims. Finite domains are in PLAN.md.

EvidenceFault exits 12 specifically at EvidenceSound: stale-pass input becomes
passed in a three-state trace. DraftWitness exits 12 specifically at NoDraft,
showing reachable complete output with all four topics. These are expected
probes, not errors in the required model. Initial parent-01 runtime error is
preserved and resolved in F1; neither probe is treated as a substitute for the
successful exhaustive required configuration.

Abstraction assumes classification of current evidence is correct; real
Git/source/provenance interpretation and read-only execution are implementation
evaluation responsibilities. This does not prove prose quality, arbitrary code,
or a future agent's honest use of the instructions.
