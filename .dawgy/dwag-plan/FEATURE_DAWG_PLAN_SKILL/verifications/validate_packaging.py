"""Reproduce the packaging checks recorded for this skill feature.

Usage: python validate_packaging.py /absolute/path/to/quick_validate.py
Requires PyYAML in the invoking Python environment.
"""

import hashlib
import json
import platform
import re
import subprocess
import sys
from pathlib import Path

import yaml


def main():
    root = Path(__file__).resolve().parents[4]
    skill = root / "plugins/pdawgy-skills/skills/dawg-plan"
    validator = Path(sys.argv[1]).resolve()
    command = [sys.executable, str(validator), str(skill)]
    result = subprocess.run(command, capture_output=True, text=True)
    lines = [
        f"Python: {platform.python_version()}",
        f"PyYAML: {yaml.__version__}",
        f"Validator command: {' '.join(command)}",
        f"Exit: {result.returncode}",
        result.stdout.strip(),
        result.stderr.strip(),
    ]
    assert result.returncode == 0, result.stderr or result.stdout

    catalog = json.loads((root / ".agents/plugins/marketplace.json").read_text())
    entry = next(p for p in catalog["plugins"] if p["name"] == "pdawgy-skills")
    plugin = (root / entry["source"]["path"]).resolve()
    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    assert (plugin / manifest["skills"]).resolve() == skill.parent
    assert manifest["name"] == entry["name"]
    ui = yaml.safe_load((skill / "agents/openai.yaml").read_text())
    assert "$dawg-plan" in ui["interface"]["default_prompt"]
    assert 25 <= len(ui["interface"]["short_description"]) <= 64
    assert ui.get("policy", {}).get("allow_implicit_invocation", True)
    for reference in re.findall(
        r"\]\((assets/[^)]+)\)", (skill / "SKILL.md").read_text()
    ):
        assert (skill / reference).is_file(), reference
    assert not (skill.parent / ".gitkeep").exists()
    readme = (root / "README.md").read_text()
    assert "$dawg-plan" in readme and "No skills are bundled yet" not in readme
    lines.append(
        "PASS: parsed marketplace -> plugin -> skill discovery, UI metadata, "
        "invocation, template references, and README integration."
    )

    files = sorted(skill.rglob("*")) + [
        root / "README.md",
        root / ".agents/plugins/marketplace.json",
        plugin / ".codex-plugin/plugin.json",
    ]
    for file in files:
        if file.is_file():
            check = subprocess.run(
                ["git", "diff", "--no-index", "--check", "/dev/null", str(file)],
                capture_output=True,
                text=True,
            )
            assert check.returncode in (0, 1) and not check.stdout and not check.stderr
    lines.append("PASS: whitespace checks include new, untracked skill files.")
    lines.append("Revision: main has no commits; all files uncommitted. SHA-256:")
    for file in files:
        if file.is_file():
            digest = hashlib.sha256(file.read_bytes()).hexdigest()
            lines.append(f"{digest}  {file.relative_to(root)}")
    output = "\n".join(line for line in lines if line) + "\n"
    (Path(__file__).parent / "validation.log").write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
