import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import yaml

root = Path(__file__).resolve().parents[4]
v = Path(__file__).resolve().parent
skill = root / 'plugins/pdawgy-skills/skills/dawg-mr'
command = [sys.executable, '/home/chy/.codex/skills/.system/skill-creator/scripts/quick_validate.py', str(skill)]
result = subprocess.run(command, cwd=root, capture_output=True, text=True)
print('Command:', command, '\nExit:', result.returncode, '\n' + result.stdout + result.stderr)
assert result.returncode == 0
manifest = json.loads((root / 'plugins/pdawgy-skills/.codex-plugin/plugin.json').read_text())
catalog = json.loads((root / '.agents/plugins/marketplace.json').read_text())
assert manifest['version'] == '0.6.0'
assert (root / catalog['plugins'][0]['source']['path']).is_dir()
plugin = root / 'plugins/pdawgy-skills'
assert (plugin / manifest['skills']).is_dir()
ui = yaml.safe_load((skill / 'agents/openai.yaml').read_text())['interface']
assert all(isinstance(value, str) for value in ui.values())
assert 25 <= len(ui['short_description']) <= 64
assert '$dawg-mr' in ui['default_prompt']
for name in ['README.md', 'ARCHITECTURE.md', 'AGENTS.md', 'CLAUDE.md']:
    owner = root / name
    for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', owner.read_text()):
        if '://' not in link and not link.startswith('#'):
            assert (owner.parent / link.split('#')[0]).exists(), (name, link)
print('PASS: frontmatter/UI, JSON discovery/version and root Markdown resource paths')
source = ['README.md', 'ARCHITECTURE.md', 'plugins/pdawgy-skills/.codex-plugin/plugin.json',
          'plugins/pdawgy-skills/skills/dawg-mr/SKILL.md',
          'plugins/pdawgy-skills/skills/dawg-mr/agents/openai.yaml']
for command in [['git', 'diff', '--check'], *[
        ['git', 'diff', '--no-index', '--check', '/dev/null', name] for name in source[3:]]]:
    result = subprocess.run(command, cwd=root, capture_output=True, text=True)
    print('Command:', command, 'Exit:', result.returncode, result.stdout + result.stderr)
    assert result.returncode in (0, 1) and not result.stdout and not result.stderr
(v / 'tested-source.json').write_text(json.dumps({
    name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in source
}, indent=2) + '\n')
print('PASS: whitespace and current source fingerprints')
