#!/usr/bin/env python3
"""Validate the cross-agent plugin manifests and bundled skill layout."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


PLUGIN_NAME = "design-system"
REQUIRED_FILES = (
    "plugin.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    ".cursor-plugin/marketplace.json",
    ".github/plugin/marketplace.json",
    ".agents/plugins/marketplace.json",
    "agents/openai.yaml",
    "assets/icon.svg",
    "assets/logo.svg",
    "commands/design-system.md",
    "commands/design-system-validate.md",
    "commands/design-system-export.md",
    "skills/design-system/SKILL.md",
    "skills/design-system/scripts/validate_design_system.py",
    "skills/design-system/scripts/export_tokens.py",
    "scripts/validate_plugin.py",
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "Makefile",
    ".github/workflows/ci.yml",
)
JSON_MANIFESTS = (
    "plugin.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    ".cursor-plugin/marketplace.json",
    ".github/plugin/marketplace.json",
    ".agents/plugins/marketplace.json",
)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")


@dataclass(frozen=True)
class Issue:
    code: str
    message: str


@dataclass
class Report:
    errors: list[Issue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def error(self, code: str, message: str) -> None:
        self.errors.append(Issue(code, message))


def load_manifest(root: Path, relative_path: str, report: Report) -> dict[str, Any] | None:
    path = root / relative_path
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.error("missing-file", f"Missing manifest: {relative_path}")
        return None
    except json.JSONDecodeError as error:
        report.error("invalid-json", f"Invalid JSON in {relative_path}: {error}")
        return None
    if not isinstance(data, dict):
        report.error("invalid-manifest", f"{relative_path} must contain a JSON object.")
        return None
    return data


def check_name(data: dict[str, Any], location: str, report: Report) -> None:
    if data.get("name") != PLUGIN_NAME:
        report.error("plugin-name", f"{location} must declare name '{PLUGIN_NAME}'.")


def check_entry_path(root: Path, manifest: dict[str, Any], key: str, location: str, report: Report) -> None:
    value = manifest.get(key)
    if not isinstance(value, str) or not value:
        report.error("missing-entry-path", f"{location} must declare a {key} path.")
        return
    target = (root / value.removeprefix("./")).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        report.error("unsafe-entry-path", f"{location} {key} path escapes the repository.")
        return
    if not target.exists():
        report.error("missing-entry-path", f"{location} {key} path does not exist: {value}.")


def check_marketplace(
    manifest: dict[str, Any], location: str, report: Report
) -> None:
    plugins = manifest.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        report.error("missing-marketplace-plugin", f"{location} must list a plugin.")
        return
    if not any(
        isinstance(plugin, dict) and plugin.get("name") == PLUGIN_NAME
        for plugin in plugins
    ):
        report.error("missing-marketplace-plugin", f"{location} does not list '{PLUGIN_NAME}'.")


def check_skill_links(root: Path, report: Report) -> None:
    skill_file = root / "skills" / PLUGIN_NAME / "SKILL.md"
    if not skill_file.is_file():
        return
    for target in LINK_RE.findall(skill_file.read_text(encoding="utf-8")):
        if target.startswith(("https://", "http://", "mailto:", "#")):
            continue
        local_path = (skill_file.parent / target.split("#", 1)[0]).resolve()
        try:
            local_path.relative_to(root.resolve())
        except ValueError:
            report.error("unsafe-skill-link", f"Skill link escapes repository: {target}")
            continue
        if not local_path.exists():
            report.error("broken-skill-link", f"Skill link target does not exist: {target}")


def validate_plugin(root: Path) -> Report:
    report = Report()
    root = root.resolve()

    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).is_file():
            report.error("missing-file", f"Missing required file: {relative_path}")

    manifests = {
        path: load_manifest(root, path, report)
        for path in JSON_MANIFESTS
    }

    root_manifest = manifests.get("plugin.json")
    if root_manifest:
        check_name(root_manifest, "plugin.json", report)
        if not root_manifest.get("description"):
            report.error("missing-description", "plugin.json must include a description.")

    versioned_manifests = (
        ".claude-plugin/plugin.json",
        ".codex-plugin/plugin.json",
        ".cursor-plugin/plugin.json",
    )
    versions: set[str] = set()
    for location in versioned_manifests:
        manifest = manifests.get(location)
        if not manifest:
            continue
        check_name(manifest, location, report)
        version = manifest.get("version")
        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            report.error("invalid-version", f"{location} must use a semantic version.")
        else:
            versions.add(version)
    if len(versions) > 1:
        report.error("version-mismatch", "Agent plugin manifests must use the same version.")

    codex = manifests.get(".codex-plugin/plugin.json")
    if codex:
        check_entry_path(root, codex, "skills", ".codex-plugin/plugin.json", report)
    cursor = manifests.get(".cursor-plugin/plugin.json")
    if cursor:
        check_entry_path(root, cursor, "skills", ".cursor-plugin/plugin.json", report)
        check_entry_path(root, cursor, "commands", ".cursor-plugin/plugin.json", report)

    for location in (
        ".claude-plugin/marketplace.json",
        ".cursor-plugin/marketplace.json",
        ".github/plugin/marketplace.json",
        ".agents/plugins/marketplace.json",
    ):
        manifest = manifests.get(location)
        if manifest:
            check_marketplace(manifest, location, report)

    agent_config = root / "agents" / "openai.yaml"
    if agent_config.is_file():
        content = agent_config.read_text(encoding="utf-8")
        if "display_name:" not in content or "$design-system" not in content:
            report.error("invalid-agent-config", "agents/openai.yaml must describe the design-system skill.")

    check_skill_links(root, report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate design-system plugin structure.")
    parser.add_argument("root", nargs="?", type=Path, default=Path("."), help="Plugin repository root")
    args = parser.parse_args(argv)

    report = validate_plugin(args.root)
    if report.ok:
        print(f"Plugin structure validation: PASS ({args.root})")
        return 0

    print(f"Plugin structure validation: FAIL ({len(report.errors)} error(s))")
    for issue in report.errors:
        print(f"  - [{issue.code}] {issue.message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
