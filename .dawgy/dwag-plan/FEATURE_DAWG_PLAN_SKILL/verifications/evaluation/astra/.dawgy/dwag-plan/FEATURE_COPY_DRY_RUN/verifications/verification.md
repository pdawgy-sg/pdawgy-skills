# Verification: Copy dry run

Plan: [../PLAN.md](../PLAN.md)
Execution status: NOT RUN
Tested revision and uncommitted changes: not run; V1 will save the exact tested source snapshot and SHA-256.
Environment and prerequisites: Python 3 and Bash, standard library only. The supplied module is import-safe and exposes main(). No root privilege, service, network, or dependency installation is needed.
Working directory: `/tmp/dawg-plan-astra-eval`

## Coverage checklist

- [ ] V1 — success, nonmutation, source failures, normal regression; T1; AC1–AC4; TR1–TR11; I1–I3.
- [ ] V2 — standard-library and scope inspection; T1; AC5; I4.

## V1 — Behavior and regression in disposable fixtures

- Covers: T1, AC1–AC4, TR1–TR11, I1–I3.
- Procedure: after implementation is separately authorized and complete, run the following command from the stated directory. It creates a fresh evidence attempt directory, uses temporary synthetic files, records the exact source and interpreter, and preserves assertion failures and tracebacks. No tests have been run in this planning evaluation. The command is a proposed post-implementation check, not a claim of current feature support.

```bash
cd /tmp/dawg-plan-astra-eval
python3 - <<'PY'
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from unittest.mock import patch
import hashlib
import importlib.util
import io
import json
import platform
import subprocess
import sys
import traceback

script = Path.cwd() / 'copy_text.py'
evidence_root = Path('/tmp/dawg-plan-astra-eval/.dawgy/dwag-plan/FEATURE_COPY_DRY_RUN/verifications')
attempt = Path(mkdtemp(prefix='v1-', dir=evidence_root))
source_code = script.read_bytes()
(attempt / 'copy_text.py').write_bytes(source_code)
failed = False
with (attempt / 'results.txt').open('w') as log, redirect_stdout(log), redirect_stderr(log):
    print('Tested file:', script)
    print('SHA256:', hashlib.sha256(source_code).hexdigest())
    print('Runtime:', sys.executable, sys.version, platform.platform())
    print('Exact tested source is saved beside this log, including uncommitted edits.')
    try:
        spec = importlib.util.spec_from_file_location('copy_text_under_test', script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with TemporaryDirectory(prefix='copy-dry-run-check-') as fixture:
            root = Path(fixture)
            src = root / 'source.txt'
            src.write_text('source payload\n')
            original = src.read_bytes()
            def cli(destination, dry=False, source=src):
                argv = [sys.executable, str(script)] + (['--dry-run'] if dry else []) + [str(source), str(destination)]
                result = subprocess.run(argv, capture_output=True, text=True)
                print(json.dumps({'argv': argv, 'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}))
                return result
            def success(result, destination, dry):
                verb = 'Would copy' if dry else 'Copied'
                assert (result.returncode, result.stdout, result.stderr) == (0, f'{verb} {src} -> {destination}\n', '')

            absent = root / 'absent' / 'nested' / 'dest.txt'
            success(cli(absent, dry=True), absent, True)
            assert not (root / 'absent').exists()
            existing = root / 'existing.txt'
            existing.write_text('keep me\n')
            success(cli(existing, dry=True), existing, True)
            assert existing.read_text() == 'keep me\n'
            blocked_parent = root / 'file-parent'
            blocked_parent.write_text('not a directory')
            blocked_dest = blocked_parent / 'dest.txt'
            success(cli(blocked_dest, dry=True), blocked_dest, True)
            assert blocked_parent.read_text() == 'not a directory'
            print('PASS dry-run success and no destination mutation')

            success(cli(absent), absent, False)
            assert absent.read_bytes() == original
            success(cli(existing), existing, False)
            assert existing.read_bytes() == original
            result = cli(blocked_dest)
            assert result.returncode == 1 and result.stdout == '' and result.stderr.strip()
            print('PASS normal creation, overwrite, output, and destination failure')

            for bad_source in (root / 'missing.txt', root):
                for dry in (False, True):
                    dest = root / 'invalid-source-dest' / 'dest.txt'
                    result = cli(dest, dry=dry, source=bad_source)
                    assert (result.returncode, result.stdout, result.stderr) == (1, '', 'Source must be a file\n')
                    assert not dest.parent.exists()
            print('PASS missing and non-file sources in both modes')

            for dry in (False, True):
                argv = [str(script)] + (['--dry-run'] if dry else []) + [str(src), str(existing)]
                stdout, stderr = io.StringIO(), io.StringIO()
                with patch.object(sys, 'argv', argv), patch.object(Path, 'read_text', side_effect=OSError('synthetic read error')) as read, patch.object(Path, 'mkdir') as mkdir, patch.object(Path, 'write_text') as write, redirect_stdout(stdout), redirect_stderr(stderr):
                    code = module.main()
                read.assert_called_once()
                mkdir.assert_not_called()
                write.assert_not_called()
                assert (code, stdout.getvalue(), stderr.getvalue()) == (1, '', 'synthetic read error\n')
                print('PASS deterministic OSError read failure, dry=', dry)

                stdout, stderr = io.StringIO(), io.StringIO()
                decode_error = UnicodeDecodeError('utf-8', b'\xff', 0, 1, 'invalid start byte')
                with patch.object(sys, 'argv', argv), patch.object(Path, 'read_text', side_effect=decode_error), patch.object(Path, 'mkdir') as mkdir, patch.object(Path, 'write_text') as write, redirect_stdout(stdout), redirect_stderr(stderr):
                    try:
                        module.main()
                    except UnicodeDecodeError:
                        pass
                    else:
                        raise AssertionError('existing non-OSError propagation changed')
                mkdir.assert_not_called()
                write.assert_not_called()
                assert stdout.getvalue() == '' and stderr.getvalue() == ''
                print('PASS existing non-OSError propagation, dry=', dry)
            assert src.read_bytes() == original
            assert existing.read_bytes() == original
        assert script.read_bytes() == source_code, 'Source changed while checking; rerun against one revision'
        print('V1 PASS')
    except BaseException:
        failed = True
        traceback.print_exc()
        print('V1 FAIL')
print('Evidence:', attempt)
sys.exit(1 if failed else 0)
PY
```

- Expected: command exits 0; results.txt ends with `V1 PASS`, all named checks pass, and source snapshot/hash identifies the exact tested implementation. Injected read errors are deterministic evidence of the shared read/error path, not a claim of OS permission simulation.
- Actual: not run.
- Evidence: planned unique `v1-*/results.txt` and `v1-*/copy_text.py` under this directory.
- Status: NOT RUN
- Blocker / next action: complete required design reviews; obtain implementation authorization separately; implement T1 before executing this command.
- Cleanup: TemporaryDirectory removes all synthetic source/destination files. Retain every attempt directory, including failures. Do not reuse earlier logs as current evidence.

## V2 — Standard-library and change-boundary inspection

- Covers: T1, AC5, I4.
- Procedure: inspect the complete tested source snapshot saved by V1, compare it to the read-only original `/tmp/dawg-plan-review-fixture/copy_text.py`, and inspect the target project for added dependency manifests or frameworks. Confirm all imported modules belong to Python's standard library, no dependency was added, and the changed behavior is confined to argument parsing and the branch between source reading and destination mutation. Record the reviewed V1 attempt, source hash, actual observations, and PASS/FAIL in a fresh `v2-<unique-attempt>.txt` in this directory. This is a small concrete source review, not a separate test framework.
- Expected: standard-library-only setup preserved; no unrelated behavior added.
- Actual: not run.
- Evidence: planned `v2-<unique-attempt>.txt`.
- Status: NOT RUN
- Blocker / next action: inspect the implemented revision after V1; preserve failed inspection notes and record any corrected attempt separately.
- Cleanup: none; retain evidence.

## Design review evidence

- Astra: pending, gpt-6-astra / high, no plan revision reviewed; no record created.
- Sol: pending, gpt-6.1-sol / high, no plan revision reviewed; no record created.

These reviews validate the design, not the implementation. Nested reviews were explicitly excluded from this evaluation and must not be fabricated.

## Completion

- Required checks: 0 / 2 passed; V1 and V2 NOT RUN.
- Remaining limitations: planning-only evaluation; no implementation or nested design review. The verification procedure has been drafted, not executed against a hypothetical implementation.
- Evidence shared in chat: no executed implementation evidence or screenshots exist. Plan/checklist paths are supplied in the reviewer report. No screenshot is required for this CLI behavior.
