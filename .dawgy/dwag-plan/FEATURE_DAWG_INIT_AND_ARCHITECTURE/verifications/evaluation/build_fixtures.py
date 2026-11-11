import json
from pathlib import Path
import subprocess
import sys


root = Path(sys.argv[1]).resolve()
if root.exists() and any(root.iterdir()):
    raise SystemExit(f"Refusing to overwrite nonempty directory: {root}")
root.mkdir(parents=True, exist_ok=True)
fixtures = json.loads(Path(__file__).with_name("fixtures.json").read_text())
for name, fixture in fixtures.items():
    project = root / name
    project.mkdir()
    for relative, content in fixture["files"].items():
        target = project / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    if name == "mature":
        for command in (
            ["git", "init", "-q", "-b", "main"],
            ["git", "add", "."],
            ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "baseline"],
        ):
            subprocess.run(command, cwd=project, check=True)
    for group in ("dirty_changes", "untracked"):
        for relative, content in fixture.get(group, {}).items():
            (project / relative).write_text(content)
    print(f"{name}: {project}\nRequest: {fixture['request']}")
