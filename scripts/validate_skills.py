#!/usr/bin/env python3
"""Validate Agent Skills packaging without executing skills or making network calls."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys instead of silently accepting the last one."""


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if not isinstance(key, str):
            raise ValueError("YAML mapping keys must be strings")
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=True)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)

NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
LINK = re.compile(r'\[[^\]\n]+\]\((?:<([^>\n]+)>|([^\s)\n]+))(?:\s+"[^"\n]*")?\)')
FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SKIP = {".git", ".venv", "__pycache__"}


def load_mapping(text: str) -> dict:
    value = yaml.load(text, Loader=UniqueKeyLoader)
    if not isinstance(value, dict):
        raise ValueError("expected a YAML mapping")
    return value


def validate_manifest(skill: Path) -> None:
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("SKILL.md must begin with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc
    data = load_mapping("\n".join(lines[1:end]))
    if set(data) - FIELDS:
        raise ValueError(f"unsupported frontmatter fields: {sorted(set(data) - FIELDS)}")
    name = data.get("name")
    if not isinstance(name, str) or len(name) > 64 or not NAME.fullmatch(name):
        raise ValueError("name must be 1-64 lowercase letters/digits with single internal hyphens")
    if name != skill.name:
        raise ValueError("manifest name must match the skill directory")
    description = data.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        raise ValueError("description must be a non-empty string of at most 1024 characters")
    if not "\n".join(lines[end + 1:]).strip():
        raise ValueError("SKILL.md needs instructions after the frontmatter")
    for field in ("license", "allowed-tools", "compatibility"):
        if field in data and (not isinstance(data[field], str) or not data[field].strip()):
            raise ValueError(f"{field} must be a non-empty string")
    if len(data.get("compatibility", "")) > 500:
        raise ValueError("compatibility exceeds 500 characters")
    if "metadata" in data and (
        not isinstance(data["metadata"], dict)
        or any(not isinstance(v, str) for v in data["metadata"].values())
    ):
        raise ValueError("metadata must map string keys to string values")

    ui_path = skill / "agents" / "openai.yaml"
    if ui_path.exists():
        ui = load_mapping(ui_path.read_text(encoding="utf-8"))
        interface = ui.get("interface", {})
        if not isinstance(interface, dict):
            raise ValueError("openai.yaml interface must be a mapping")
        for key, value in interface.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"openai.yaml interface.{key} must be a non-empty string")
        short = interface.get("short_description")
        if short is not None and not 25 <= len(short) <= 64:
            raise ValueError("openai.yaml short_description must be 25-64 characters")
        prompt = interface.get("default_prompt")
        if prompt is not None and f"${name}" not in prompt:
            raise ValueError("openai.yaml default_prompt must mention the skill invocation")


def validate_links(path: Path, boundary: Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    # Examples inside fenced code are not documentation links.
    text = re.sub(r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$", "", text)
    for match in LINK.finditer(text):
        target = match.group(1) or match.group(2)
        parsed = urlsplit(target)
        if parsed.scheme in {"https", "http", "mailto"}:
            continue
        if parsed.scheme or parsed.netloc:
            errors.append(f"{path}: unsupported link scheme: {target}")
            continue
        if not parsed.path:
            continue
        destination = (path.parent / unquote(parsed.path)).resolve()
        if not destination.is_relative_to(boundary.resolve()):
            errors.append(f"{path}: link escapes package boundary: {target}")
        elif not destination.exists():
            errors.append(f"{path}: missing link target: {target}")
    return errors


def validate_repository(root: Path, selected: str | None = None) -> tuple[int, list[str]]:
    root = root.resolve()
    skills_root = root / "skills"
    errors = []
    if skills_root.is_symlink():
        return 0, ["skills directory must not be a symlink"]
    if selected is not None:
        if not NAME.fullmatch(selected):
            return 0, ["invalid selected skill name"]
        skills = [skills_root / selected]
    else:
        skills = sorted(p for p in skills_root.iterdir() if not p.name.startswith(".")) if skills_root.is_dir() else []
    if not skills:
        return 0, ["no skill directories found"]
    for skill in skills:
        if not skill.is_dir():
            errors.append(f"{skill}: expected a skill directory")
            continue
        members = [skill, *skill.rglob("*")]
        if any(p.is_symlink() for p in members):
            errors.append(f"{skill}: symlinks are not portable skill resources")
            continue
        try:
            validate_manifest(skill)
            for path in skill.rglob("*.md"):
                errors.extend(validate_links(path, skill))
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{skill}: {exc}")
    if selected is None:
        for catalog in (root / "README.md", root / "README.pt-BR.md"):
            if not catalog.is_file():
                errors.append(f"missing catalog: {catalog}")
                continue
            contents = catalog.read_text(encoding="utf-8")
            for skill in skills:
                if f"skills/{skill.name}/SKILL.md" not in contents:
                    errors.append(f"{catalog}: missing catalog entry for {skill.name}")
        for path in root.rglob("*.md"):
            relative = path.relative_to(root)
            if relative.parts[0] == "skills" or any(part in SKIP for part in relative.parts):
                continue
            if path.is_symlink():
                errors.append(f"{path}: refusing to read a symlink")
                continue
            try:
                errors.extend(validate_links(path, root))
            except (OSError, ValueError) as exc:
                errors.append(f"{path}: {exc}")
    return len(skills), errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--skill", help="validate only this skill, without checking repository catalogs")
    args = parser.parse_args()
    count, errors = validate_repository(args.root, args.skill)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print(f"Validated {count} skill(s) and inline Markdown file links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
