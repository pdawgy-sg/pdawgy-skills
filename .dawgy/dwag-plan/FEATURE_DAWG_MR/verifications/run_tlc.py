import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--java', required=True, type=Path)
    parser.add_argument('--jar', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    models = Path(__file__).resolve().parent / 'tla'
    module = models / 'MrDraft.tla'
    outcomes = []
    cases = [('MrDraft.cfg', None), ('EvidenceFault.cfg', 'EvidenceSound'),
             ('DraftWitness.cfg', 'NoDraft')]
    java_version = subprocess.run([str(args.java), '-version'], capture_output=True, text=True, check=True)
    for name, expected_violation in cases:
        config = models / name
        with tempfile.TemporaryDirectory(prefix='dawg-tlc-states-') as state_dir:
            command = [str(args.java), '-XX:+UseParallelGC', '-Xmx512m', '-cp', str(args.jar),
                       'tlc2.TLC', '-workers', '1', '-coverage', '1', '-metadir', state_dir,
                       '-config', str(config), str(module)]
            try:
                result = subprocess.run(command, cwd=models, capture_output=True, text=True, timeout=120)
                output = result.stdout + result.stderr
                code = result.returncode
            except subprocess.TimeoutExpired as error:
                output = (error.stdout or b'').decode(errors='replace') + (error.stderr or b'').decode(errors='replace')
                output += '\nBLOCKED: model check timed out after 120 seconds.\n'
                code = None
        (args.output / (config.stem + '.log')).write_text(output)
        if expected_violation:
            passed = (code is not None and code != 0
                      and f'Invariant {expected_violation} is violated' in output
                      and 'The behavior up to this point is:' in output)
        else:
            passed = code == 0 and 'Model checking completed. No error has been found.' in output
        states = re.findall(r'(\d+) states generated, (\d+) distinct states found, (\d+) states left on queue', output)
        if not expected_violation:
            passed = passed and bool(states) and int(states[-1][1]) > 1 and int(states[-1][2]) == 0
        outcome = {'config': name, 'module_sha256': digest(module), 'config_sha256': digest(config),
                   'command': command, 'exit_code': code, 'expected_violation': expected_violation,
                   'states': states[-1] if states else None, 'expected_outcome_observed': bool(passed)}
        outcomes.append(outcome)
        print(name, 'PASS' if passed else 'FAIL/BLOCKED', 'exit', code, 'states', outcome['states'], flush=True)
    receipt = {'java_version': java_version.stderr.strip(), 'java_binary': str(args.java),
               'java_sha256': digest(args.java.resolve()), 'tlc_jar': str(args.jar),
               'tlc_jar_sha256': digest(args.jar), 'outcomes': outcomes,
               'all_expected_outcomes_observed': all(item['expected_outcome_observed'] for item in outcomes)}
    (args.output / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    if not receipt['all_expected_outcomes_observed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
