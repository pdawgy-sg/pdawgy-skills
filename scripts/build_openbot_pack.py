import argparse
import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "pdawgy-skills"
PACK_ROOT = ROOT / "packaging" / "openbot" / "SKILL.md"
CHILD_NAME = re.compile(r"dawg-[a-z0-9]+(?:-[a-z0-9]+)*")
VERSION = re.compile(
    r"(?:0|[1-9][0-9]*)(?:\.(?:0|[1-9][0-9]*)){2}"
    r"(?:-[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)?"
    r"(?:\+[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)?"
)
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
UNSUPPORTED_FILE = re.compile(r"^\.env|private.*key|\.(?:zip|tar|tgz|gz|7z|rar)$", re.IGNORECASE)
MAX_FILES = 200
MAX_BYTES = 10 * 1024 * 1024
IGNORED_ENTRIES = {
    ".git", ".DS_Store", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
}


def package_version():
    codex, claude = (
        json.loads((PLUGIN / f".{host}-plugin" / "plugin.json").read_text(encoding="utf-8"))
        for host in ("codex", "claude")
    )
    version = codex.get("version")
    if version != claude.get("version") or not isinstance(version, str) or not VERSION.fullmatch(version):
        raise ValueError("Codex and Claude plugin manifests must have the same valid package version")
    return version


def validate_entrypoint(content, expected_name, path):
    frontmatter = FRONTMATTER.match(content.decode("utf-8"))
    if not frontmatter:
        raise ValueError(f"Missing frontmatter in {path}")
    metadata = frontmatter.group(1)
    names = re.findall(r"^name:[ \t]*([^\r\n]*)", metadata, re.MULTILINE)
    descriptions = re.findall(r"^description:[ \t]*([^\r\n]*)", metadata, re.MULTILINE)
    if len(names) != 1 or names[0].strip() not in (expected_name, f"'{expected_name}'", f'"{expected_name}"'):
        raise ValueError(f"Expected frontmatter name '{expected_name}' in {path}")
    if len(descriptions) != 1 or not descriptions[0].strip(" \t'\""):
        raise ValueError(f"Expected a frontmatter description in {path}")


def skill_files(directory):
    for path in sorted(directory.iterdir()):
        if path.name in IGNORED_ENTRIES:
            continue
        if "\\" in path.name:
            raise ValueError(f"Unsupported skill pack path: {path}")
        if path.is_symlink():
            raise ValueError(f"Symlinks are unsupported in the skill pack: {path}")
        if path.is_dir():
            yield from skill_files(path)
        elif path.is_file():
            if UNSUPPORTED_FILE.search(path.name):
                raise ValueError(f"Unsupported skill pack path: {path}")
            yield path
        else:
            raise ValueError(f"Expected a regular skill pack file: {path}")


def pack_files(version):
    root = PACK_ROOT.read_bytes()
    validate_entrypoint(root, "dawg", PACK_ROOT)
    if root.count(b"@PACKAGE_VERSION@") != 1:
        raise ValueError(f"Expected one package version placeholder in {PACK_ROOT}")
    files = {"SKILL.md": (root.replace(b"@PACKAGE_VERSION@", version.encode("ascii")), 0o644)}
    skills = PLUGIN / "skills"
    for child in sorted(skills.iterdir()):
        if child.name in IGNORED_ENTRIES:
            continue
        if not CHILD_NAME.fullmatch(child.name) or len(child.name) > 64 or child.is_symlink() or not child.is_dir():
            raise ValueError(f"Invalid OpenBot child skill directory: {child}")
        entry = child / "SKILL.md"
        if entry.is_symlink() or not entry.is_file():
            raise ValueError(f"Missing regular child entrypoint: {entry}")
        validate_entrypoint(entry.read_bytes(), child.name, entry)
        for path in skill_files(child):
            name = "skills/" + path.relative_to(skills).as_posix()
            files[name] = (path.read_bytes(), 0o644 | (path.stat().st_mode & 0o111))
    if len(files) == 1:
        raise ValueError(f"No OpenBot child skills found in {skills}")
    if len(files) > MAX_FILES or sum(len(content) for content, _ in files.values()) > MAX_BYTES:
        raise ValueError(f"OpenBot packs support at most {MAX_FILES} files and {MAX_BYTES} expanded bytes")
    return files


def build(output):
    if output.exists() or output.is_symlink():
        raise ValueError(f"Choose a fresh output directory: {output}")
    if any(output.resolve().is_relative_to(source) for source in (PLUGIN, PACK_ROOT.parent)):
        raise ValueError("Choose an output directory outside the skill and pack source trees")
    version = package_version()
    files = pack_files(version)
    archive_name = f"dawg-{version}.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output.parent) as scratch:
        result = Path(scratch) / "pack"
        result.mkdir()
        zip_path = result / archive_name
        with ZipFile(zip_path, "w") as archive:
            for name, (content, mode) in sorted(files.items()):
                entry = ZipInfo(name)
                entry.create_system = 3
                entry.external_attr = (0o100000 | mode) << 16
                archive.writestr(entry, content)
                staged = result / "dawg" / name
                staged.parent.mkdir(parents=True, exist_ok=True)
                staged.write_bytes(content)
                staged.chmod(mode)
        if zip_path.stat().st_size > MAX_BYTES:
            raise ValueError(f"OpenBot pack ZIP exceeds {MAX_BYTES} bytes")
        result.rename(output)
    return output / "dawg", output / archive_name


def main():
    parser = argparse.ArgumentParser(description="Build the Dawg OpenBot skill pack from the canonical plugin.")
    parser.add_argument("--output", type=Path, required=True, help="Fresh directory for the staged pack and versioned ZIP.")
    args = parser.parse_args()
    try:
        for path in build(args.output):
            print(path)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
