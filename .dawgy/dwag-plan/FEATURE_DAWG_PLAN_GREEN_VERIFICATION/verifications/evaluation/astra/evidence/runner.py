from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path('/tmp/dawg-green-astra-eval')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def event(kind, details):
    with (ROOT / 'evidence/events.jsonl').open('a') as file:
        file.write(json.dumps({'time': datetime.now(timezone.utc).isoformat(), 'event': kind, 'details': details}) + '\n')

def attempt(number):
    project = ROOT / 'addition'
    evidence = ROOT / 'evidence/addition'
    argv = [sys.executable, '-B', 'check.py']
    before = {'calc.py': sha(project / 'calc.py'), 'check.py': sha(project / 'check.py')}
    result = subprocess.run(argv, cwd=project, text=True, capture_output=True)
    with (evidence / f'attempt{number}.log').open('x') as file:
        file.write(result.stdout + result.stderr)
    with (evidence / f'attempt{number}-calc.py').open('x') as file:
        file.write((project / 'calc.py').read_text())
    record = {'attempt': number, 'argv': argv, 'cwd': str(project), 'source_sha256': before, 'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr, 'log_sha256': sha(evidence / f'attempt{number}.log')}
    with (evidence / f'attempt{number}.json').open('x') as file:
        json.dump(record, file, indent=2)
        file.write('\n')
    assert before == {'calc.py': sha(project / 'calc.py'), 'check.py': sha(project / 'check.py')}
    event('check observed', record)
    print(json.dumps(record, indent=2))
    return record
