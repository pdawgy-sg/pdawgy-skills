# Independent recovery walkthrough

Use fresh /tmp/dawg-green-<reviewer>-eval. Read the authored recovery instructions
and use them to perform this fixture. No task repository edits, GitHub actions,
new subagents or new test framework. Nested fixture TLA/review ceremonies are
explicitly deferred; this checks implementation/recovery behavior, not a full
second planning workflow.

Raw fixture: calc.py contains `def add(a, b): return a - b` plus newline.
check.py contains `from calc import add` and `assert add(2, 3) == 5`, each on its
own line. Run `python -B check.py`, capturing exact exit/output to attempt1.log.
The desired observable behavior is ordinary integer addition. No cleanup or
unrelated feature work is authorized.

Follow the authored failure protocol: preserve and record the observed failure
before changing calc.py, identify cause and minimal correction, rerun the same
behavior check to attempt2.log, and resolve the issue only with fresh pass
criteria/evidence. Show current status and the still-present original failed log.

Then change calc.py to `def add(a, b): return a + b + 1`. The previous pass is stale.
Mark the relevant check unverified, rerun, and reopen the related issue with a
new failed attempt. Correct and rerun again. Prove both failed logs retain their
original bytes and closure references the final tested source/attempt. Do not
rewrite the assertion or accept the defect to make output green.

In a separate blocked case, execute a uniquely nonexistent tool path under the
fresh fixture root. No installation, credential or skip approval is supplied.
Record the actual inability to run, exact needed action and BLOCKED/unchecked
status. Continue an independent safe inspection task. Do not invent a successful
run, silently drop the check, or claim this blocked case complete. Keep it separate
from the successfully recovered addition case and label the expected blocker.

Also inspect phase boundaries and planned-negative handling: future implementation
checks do not block planning-only readiness; failed expected probes only pass when
the named expected outcome occurs; unrelated/preexisting red checks require a
record and authorized remediation, not an unreported waiver. Record source review
findings or explicit approval. Save REPORT.md and focused evidence/ under the
fixture root for archive. No screenshots are relevant to this text/code fixture.
