#!/usr/bin/env python3
"""Build or check the local skill archive; no installation or network access."""

import argparse
import hashlib
import json
from pathlib import Path
import posixpath
import re
import sys
from zipfile import BadZipFile, ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "codex-lazier"
VERSION = "0.4.0"
ARCHIVE = ROOT / "dist" / f"codex-lazier-{VERSION}.zip"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def source_paths():
    return {
        "codex-lazier/SKILL.md": SKILL / "SKILL.md",
        "codex-lazier/agents/openai.yaml": SKILL / "agents/openai.yaml",
        "codex-lazier/references/policy.md": SKILL / "references/policy.md",
        "codex-lazier/references/codex.md": SKILL / "references/codex.md",
        "codex-lazier/references/web.md": SKILL / "references/web.md",
        "codex-lazier/LICENSE": ROOT / "LICENSE",
    }


def source_files():
    files = source_paths()
    for name, source in files.items():
        require(source.is_file() and not source.is_symlink(), f"Missing or symlinked input: {name}")
    return {name: source.read_bytes() for name, source in files.items()}


def validate_sources():
    content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n(.+)\Z", content, re.S)
    require(match is not None, "Missing manifest frontmatter or body")
    # Accept a restricted subset of plain YAML strings, not general YAML syntax.
    fields = {}
    for line in match[1].splitlines():
        key, separator, value = line.partition(": ")
        require(separator and key not in fields and value.strip() and line.isprintable(),
                "Invalid or duplicate metadata field")
        value = value.strip()
        require(re.match(r"[A-Za-z]", value)
                and ":" not in value and "#" not in value
                and value.lower() not in {"null", "true", "false", "yes", "no", "on", "off", "y", "n"},
                "Metadata values must be plain single-line strings starting with an ASCII letter, without ':' or '#'")
        fields[key] = value
    name = fields.get("name", "")
    require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) and len(name) <= 64,
            "Invalid skill name")
    require(name == SKILL.name, "Skill name must match its directory")
    require(0 < len(fields.get("description", "")) <= 1024, "Invalid description length")
    require(set(fields) == {"name", "description", "license"}, "Unexpected manifest fields")
    require(fields["license"] == "MIT", "License must match the bundled license")
    metadata = (SKILL / "agents/openai.yaml").read_text(encoding="utf-8")
    interface = re.fullmatch(
        r'interface:\n'
        r'  display_name: ("[^\n]*")\n'
        r'  short_description: ("[^\n]*")\n'
        r'  default_prompt: ("[^\n]*")\n'
        r'\npolicy:\n  allow_implicit_invocation: true\n', metadata,
    )
    require(interface is not None, "Required interface metadata or implicit invocation policy is missing")
    # JSON-quoted strings are a YAML subset; validate values without duplicating UI text.
    require(all(json.loads(value).strip() for value in interface.groups()),
            "Interface metadata strings must not be empty")

    files = source_files()
    packaged_paths = {source: name for name, source in source_paths().items()}
    for source in ROOT.rglob("*.md"):
        if ".git" in source.relative_to(ROOT).parts:
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            if source in packaged_paths:
                # Bundled guidance must link only to files available after installation.
                member = posixpath.normpath(posixpath.join(
                    posixpath.dirname(packaged_paths[source]), target.split("#", 1)[0]))
                require(member in files,
                        f"Broken package link in {packaged_paths[source]}: {target}")
                continue
            resolved = (source.parent / target.split("#", 1)[0]).resolve()
            require(resolved.is_relative_to(ROOT) and resolved.is_file(),
                    f"Broken or external local link in {source.relative_to(ROOT)}: {target}")


def build(files):
    ARCHIVE.parent.mkdir(exist_ok=True)
    with ZipFile(ARCHIVE, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(files.items()):
            info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, content, compresslevel=9)
    digest = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    ARCHIVE.with_suffix(".sha256").write_text(f"{digest}  {ARCHIVE.name}\n", encoding="utf-8")


def validate_archive(files):
    with ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) and set(names) == set(files),
                "Archive entries differ from the allowed distribution files")
        require(archive.testzip() is None, "Archive CRC validation failed")
        for name, expected in files.items():
            require(archive.read(name) == expected, f"Stale archive content: {name}")
            require(archive.getinfo(name).external_attr >> 16 == 0o100644,
                    f"Unexpected file type or permissions: {name}")
    digest = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    require(ARCHIVE.with_suffix(".sha256").read_text(encoding="utf-8") == f"{digest}  {ARCHIVE.name}\n",
            "Archive checksum mismatch")
    print(f"PASS: metadata, local links, {len(files)} archive files, CRCs, source identity, SHA-256\n{digest}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true", help="Rebuild only the ZIP and checksum in dist/")
    parser.add_argument("--tag", help="Require an exact v<package version> release tag")
    args = parser.parse_args()
    if args.tag is not None:
        require(args.tag == f"v{VERSION}",
                f"Release tag mismatch: expected v{VERSION}, got {args.tag}")
    validate_sources()
    files = source_files()
    if args.build:
        build(files)
    validate_archive(files)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, BadZipFile) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
