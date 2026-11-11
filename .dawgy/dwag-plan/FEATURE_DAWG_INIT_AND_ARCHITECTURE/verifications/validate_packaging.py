import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys

import yaml


root = Path(__file__).resolve().parents[4]
plugin = root / "plugins/pdawgy-skills"
validator = Path(sys.argv[1]).resolve()
manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
catalog = json.loads((root / ".agents/plugins/marketplace.json").read_text())
entry = next(item for item in catalog["plugins"] if item["name"] == manifest["name"])
assert (root / entry["source"]["path"]).resolve() == plugin
assert manifest["version"] == "0.2.0"
assert (plugin / manifest["skills"]).resolve() == plugin / "skills"
lines = [f"Python: {platform.python_version()}; PyYAML: {yaml.__version__}"]
files = [root / "README.md", plugin / ".codex-plugin/plugin.json"]
for name in ("dawg-plan", "dawg-init", "dawg-architecture-maintain"):
    skill = plugin / "skills" / name
    command = [sys.executable, str(validator), str(skill)]
    result = subprocess.run(command, capture_output=True, text=True)
    lines.extend([f"Command: {' '.join(command)}", f"Exit: {result.returncode}", result.stdout.strip(), result.stderr.strip()])
    assert result.returncode == 0, result.stdout + result.stderr
    ui = yaml.safe_load((skill / "agents/openai.yaml").read_text())
    assert f"${name}" in ui["interface"]["default_prompt"]
    assert 25 <= len(ui["interface"]["short_description"]) <= 64
    assert ui.get("policy", {}).get("allow_implicit_invocation", True)
    for target in re.findall(r"\]\(([^)]+)\)", (skill / "SKILL.md").read_text()):
        if not target.startswith(("https:", "http:")):
            resolved = (skill / target).resolve()
            assert resolved.is_relative_to(plugin) and resolved.is_file(), target
    assert name in (root / "README.md").read_text()
    files.extend(path for path in skill.rglob("*") if path.is_file())
for path in files:
    result = subprocess.run(["git", "diff", "--no-index", "--check", "/dev/null", str(path)], capture_output=True, text=True)
    assert result.returncode in (0, 1) and not result.stdout and not result.stderr, result.stdout + result.stderr
lines.append("PASS: marketplace discovery, UI invocation, resource/dependency links, README integration, and new-file whitespace.")
lines.append("Revision: uncommitted repository on main. Tested file SHA-256:")
lines.extend(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(root)}" for path in files)
output = "\n".join(line for line in lines if line) + "\n"
Path(__file__).with_name("validation.log").write_text(output)
print(output, end="")
