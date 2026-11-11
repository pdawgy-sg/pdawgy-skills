# Verification: COPY_TEXT_DRY_RUN

Plan: [../PLAN.md](../PLAN.md)
Execution status: NOT RUN
Tested revision and uncommitted changes: not run; record target code SHA-256,
runtime, and exact diff when executing after implementation. This evaluation
does not implement the feature or run its proposed checks.
Environment and prerequisites: Python 3 standard library; writable temporary
directory; completed implementation at /tmp/dawg-plan-sol-eval/copy_text.py.
Drafting environment observed Python 3.14.8. No service or third-party dependency.
Working directory: /tmp/dawg-plan-sol-eval

## Coverage checklist

- [ ] V1 — functional dry-run and normal-copy behavior; T1; AC1, AC2, AC4; TR1, TR3, TR5, TR6, TR7, TR9, TR10; I1, I3.
- [ ] V2 — shared source failures, mandatory read, no dry-run effects, retained destination failure; T1; AC1, AC3, AC4; TR1–TR8 except TR7, plus TR11; I1, I2, I3.
- [ ] V3 — focused code/dependency inspection; T1; AC5; I4.

Evidence paths below are planned, not saved. Each command redirects output to a
log without a pipeline so assertion failures preserve a nonzero command status.
If a command fails, preserve its log with an attempt suffix before rerunning and
record exit status and code revision for every attempt. Do not check boxes until
actual execution passes.

## V1 — Functional command behavior

- Covers: T1; AC1, AC2, AC4; TR1, TR3, TR5, TR6, TR7, TR9, TR10; I1, I3.
- Procedure: from the working directory run the following exact command after
  implementation. The evaluation-specific evidence directory already exists.

```bash
python - <<'PY' > /tmp/dawg-plan-sol-eval/.dawgy/dwag-plan/FEATURE_COPY_DRY_RUN/verifications/v1-functional.log 2>&1
from pathlib import Path
import hashlib
import subprocess
import sys
import tempfile

script = Path.cwd() / 'copy_text.py'
print('python:', sys.version, flush=True)
print('script sha256:', hashlib.sha256(script.read_bytes()).hexdigest(), flush=True)

def run(source, destination, dry=False):
    argv = [sys.executable, str(script)]
    if dry:
        argv.append('--dry-run')
    argv += [str(source), str(destination)]
    result = subprocess.run(argv, capture_output=True, text=True)
    print('command:', argv, 'exit:', result.returncode,
          'stdout:', repr(result.stdout), 'stderr:', repr(result.stderr), flush=True)
    expected = f'{"Would copy" if dry else "Copied"} {source} -> {destination}\n'
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, '')

def snapshot(root):
    return {str(p.relative_to(root)): None if p.is_dir() else p.read_bytes()
            for p in root.rglob('*')}

with tempfile.TemporaryDirectory(prefix='copy-dry-eval-') as temporary:
    root = Path(temporary)
    source = root / 'source.txt'
    source.write_text('hello\nsecond line\n')
    missing_destination = root / 'missing' / 'nested' / 'destination.txt'
    before = snapshot(root)
    run(source, missing_destination, dry=True)
    assert snapshot(root) == before, 'dry run created filesystem entries'
    existing = root / 'existing.txt'
    existing.write_text('sentinel\n')
    before = snapshot(root)
    run(source, existing, dry=True)
    assert snapshot(root) == before, 'dry run changed existing content'
    run(source, missing_destination)
    assert missing_destination.read_bytes() == source.read_bytes()
    run(source, existing)
    assert existing.read_bytes() == source.read_bytes(), 'normal overwrite changed'
print('PASS: dry-run side effects and normal copy compatibility', flush=True)
PY
```

- Expected: exit 0; PASS line; exact CLI diagnostics asserted; temporary
  filesystem snapshots unchanged after both dry runs; real copies create missing
  parents and overwrite sentinel text.
- Actual: not run.
- Evidence: planned `v1-functional.log`; add command exit status and attempt/revision
  metadata to this ledger when run.
- Status: NOT RUN
- Blocker / next action: implement only after readiness and authorization.
- Cleanup: TemporaryDirectory removes all fixtures, including on assertion failure.

## V2 — Source validation, required read, and error behavior

- Covers: T1; AC1, AC3, AC4; TR1–TR8 except TR7, plus TR11; I1–I3.
- Procedure: run from the same working directory after implementation. Missing
  and directory sources are real subprocess cases. Standard-library mocks make
  read/write errors reproducible without relying on Unix permission bits or root
  behavior. No fixture code is changed.

```bash
python - <<'PY' > /tmp/dawg-plan-sol-eval/.dawgy/dwag-plan/FEATURE_COPY_DRY_RUN/verifications/v2-errors.log 2>&1
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import patch
import hashlib
import runpy
import subprocess
import sys
import tempfile

script = Path.cwd() / 'copy_text.py'
print('python:', sys.version, flush=True)
print('script sha256:', hashlib.sha256(script.read_bytes()).hexdigest(), flush=True)
main = runpy.run_path(str(script))['main']

def invoke(source, destination, dry):
    out, err = StringIO(), StringIO()
    argv = [str(script)] + (['--dry-run'] if dry else []) + [str(source), str(destination)]
    with patch.object(sys, 'argv', argv), redirect_stdout(out), redirect_stderr(err):
        status = main()
    return status, out.getvalue(), err.getvalue()

with tempfile.TemporaryDirectory(prefix='copy-errors-eval-') as temporary:
    root = Path(temporary)
    source = root / 'source.txt'
    source.write_text('hello\n')
    destination = root / 'absent-parent' / 'destination.txt'
    for invalid in [root / 'missing.txt', root]:
        for dry in [False, True]:
            argv = [sys.executable, str(script)] + (['--dry-run'] if dry else [])
            result = subprocess.run(argv + [str(invalid), str(destination)],
                                    capture_output=True, text=True)
            assert (result.returncode, result.stdout, result.stderr) == (
                1, '', 'Source must be a file\n')
            assert not destination.parent.exists()
            print('PASS: non-file source', invalid, 'dry:', dry, flush=True)
    for dry in [False, True]:
        with patch.object(Path, 'read_text', side_effect=PermissionError('injected read failure')) as read, \
             patch.object(Path, 'mkdir') as mkdir, patch.object(Path, 'write_text') as write:
            result = invoke(source, destination, dry)
            assert result == (1, '', 'injected read failure\n'), result
            read.assert_called_once_with()
            mkdir.assert_not_called()
            write.assert_not_called()
        print('PASS: shared read failure; dry:', dry, flush=True)
    with patch.object(Path, 'read_text', return_value='hello\n') as read, \
         patch.object(Path, 'mkdir') as mkdir, patch.object(Path, 'write_text') as write:
        result = invoke(source, destination, True)
        assert result == (0, f'Would copy {source} -> {destination}\n', ''), result
        read.assert_called_once_with()
        mkdir.assert_not_called()
        write.assert_not_called()
    for failing_effect in ['mkdir', 'write_text']:
        with patch.object(Path, 'mkdir') as mkdir, patch.object(Path, 'write_text') as write:
            (mkdir if failing_effect == 'mkdir' else write).side_effect = OSError('injected destination failure')
            result = invoke(source, destination, False)
            assert result == (1, '', 'injected destination failure\n'), result
        print('PASS: retained destination error from', failing_effect, flush=True)
    assert not destination.parent.exists()
print('PASS: source/error paths and dry-run effect boundary', flush=True)
PY
```

- Expected: exit 0 and final PASS; both modes retain missing/non-file and read
  OSError diagnostics; dry run actually reads but never invokes destination
  effects; normal copy retains both destination-error paths.
- Actual: not run.
- Evidence: planned `v2-errors.log`; record command exit status and attempt/revision
  metadata in this ledger when run.
- Status: NOT RUN
- Blocker / next action: implementation pending; checks do not depend on chmod
  behavior or a writable destination during dry run.
- Cleanup: mocks restore original methods; TemporaryDirectory removes fixtures.

## V3 — Proportionate scope and dependency inspection

- Covers: T1; AC5; I4.
- Procedure: from the working directory, save the source and runtime metadata:

```bash
python - <<'PYCODE' > /tmp/dawg-plan-sol-eval/.dawgy/dwag-plan/FEATURE_COPY_DRY_RUN/verifications/v3-diff-review.txt
from pathlib import Path
import hashlib
import sys
p = Path('copy_text.py')
print('python:', sys.version)
print('script sha256:', hashlib.sha256(p.read_bytes()).hexdigest())
for number, line in enumerate(p.read_text().splitlines(), 1):
    print(f'{number:4}: {line}')
PYCODE
```

  Inspect the captured source: imports should still be only `argparse`, `Path`
  from `pathlib`, and `sys`; no external package should be referenced. Compare
  against the baseline described in the plan: one parser with two positional
  Paths, is_file rejection, read_text inside the OSError handler, mkdir/write,
  normal Copied output. The only behavior addition should be flag parsing and a
  preview return after reading, before mkdir/write. Record inspection result and
  source line references in this ledger. This human inspection is separate from
  the automatic behavior assertions; a source capture alone is not a PASS.
- Expected: only argparse flag and post-read preview behavior change, with any
  directly necessary formatting; no speculative safety feature or dependency.
- Actual: not run.
- Evidence: planned `v3-diff-review.txt` containing the exact source and SHA-256;
  add actual inspection observations to this ledger before marking PASS.
- Status: NOT RUN
- Blocker / next action: implementation pending, then capture and inspect source.
- Cleanup: none; retain captured source as evidence.

## Design review evidence

- Astra: pending; required gpt-6-astra / high; draft 1; record path planned
  `design-review-astra.md`.
- Sol: pending; required gpt-6.1-sol / high; draft 1; record path planned
  `design-review-sol.md`.

These reviews validate the design, not the implementation. Evaluation instructions
explicitly defer nested review execution; no substitute reviewer was used.

## Completion

- Required checks: 0 / 3 passed; V1–V3 NOT RUN.
- Remaining limitations: feature unimplemented; reviews pending; no implementation
  evidence exists. This plan is not READY and work is not VERIFIED.
- Evidence shared in chat: only draft plan/checklist links are available. No
  screenshot is necessary for this CLI; if any is taken, save it under this
  directory and embed it in chat using its absolute local path.
