#!/usr/bin/env python3
"""Validate a DESIGN-SYSTEM.md artifact and an optional design.json token file."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

ARTIFACT_RE = re.compile(r"<!--\s*design-system:artifact\s+([^>]*?)-->")
SECTION_RE = re.compile(r"<!--\s*design-system:section\s+([^>]*?)-->")
COMPONENT_RE = re.compile(r"<!--\s*design-system:component\s+([^>]*?)-->")
COUNTS_RE = re.compile(r"<!--\s*design-system:counts\s+([^>]*?)-->")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
PLACEHOLDER_RE = re.compile(
    r"\b(?:TODO|TBD|FIXME)\b|\[insert\b|<insert\b|\[placeholder\b|<placeholder\b|lorem ipsum",
    re.IGNORECASE,
)
SECRET_RE = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|"
    r"AKIA[0-9A-Z]{16}|"
    r"(?:sk|pk|ghp|gho|glpat|xox[baprs])[-_][A-Za-z0-9]{16,}|"
    r"(?:password|passwd|secret|api[_-]?key)\s*[:=]\s*[\"'][^\"']{8,}[\"']",
    re.IGNORECASE,
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
QUESTION_RE = re.compile(r"^###\s+(Q-\d{3})\s*$", re.MULTILINE)
COMPONENT_ID_RE = re.compile(r"^CMP-(\d{3})$")
A11Y_ID_RE = re.compile(r"\bA11Y-(\d{3})\b")
AUDIT_ID_RE = re.compile(r"\bAUDIT-(\d{3})\b")
AUDIT_ROW_RE = re.compile(r"(?m)^\|\s*(AUDIT-\d{3})\s*\|")
PRIN_ID_RE = re.compile(r"\bPRIN-\d{3}\b")
ALIAS_RE = re.compile(r"^\{[^{}]+\}$")

REQUIRED_SECTIONS = (
    "context",
    "principles",
    "tokens",
    "typography",
    "spacing",
    "radius",
    "elevation",
    "motion",
    "accessibility",
    "components",
    "governance",
    "adoption",
    "qa",
    "traceability",
    "dod",
)

REQUIRED_METADATA = (
    "status",
    "date",
    "owner",
    "artifact language",
    "version",
    "mode",
    "platforms",
)
ALLOWED_STATUS = ("draft", "in review", "approved", "superseded")
ALLOWED_MODES = ("create", "audit", "evolve")
ALLOWED_COMPONENT_STATUS = ("stable", "beta", "deprecated")
ALLOWED_AUDIT_SEVERITY = ("high", "medium", "low")
AUDIT_VIEWPORTS = ("320px", "768px", "1024px", "1280px", "200%")
COMPONENT_LABELS = (
    "Anatomy",
    "Variants",
    "States",
    "Usage",
    "Accessibility",
    "Tokens",
)

REQUIRED_PRIMITIVE_CATEGORIES = (
    "color",
    "font",
    "space",
    "radius",
    "shadow",
    "duration",
    "easing",
    "breakpoint",
    "grid",
)
REQUIRED_SEMANTIC_CATEGORIES = (
    "color",
    "typography",
    "spacing",
    "radius",
    "elevation",
    "motion",
    "layout",
)

EXPECTED_COMPONENT_NAMESPACES = {
    "button": "Button",
    "iconbutton": "Icon Button",
    "input": "Input",
    "select": "Select",
    "checkbox": "Checkbox",
    "radio": "Radio Group",
    "switch": "Switch",
    "badge": "Badge",
    "card": "Card",
    "modal": "Modal",
    "toast": "Toast",
    "tabs": "Tabs",
}

CONTRAST_PAIRS = (
    (("semantic", "color", "foreground", "default"), ("semantic", "color", "background", "default"), 4.5, "body text"),
    (("semantic", "color", "foreground", "muted"), ("semantic", "color", "background", "default"), 4.5, "muted text"),
    (("semantic", "color", "foreground", "subtle"), ("semantic", "color", "background", "default"), 4.5, "subtle text"),
    (("semantic", "color", "foreground", "brand"), ("semantic", "color", "background", "default"), 4.5, "brand text"),
    (("semantic", "color", "foreground", "danger"), ("semantic", "color", "background", "default"), 4.5, "danger text"),
    (("semantic", "color", "foreground", "success"), ("semantic", "color", "background", "default"), 4.5, "success text"),
    (("semantic", "color", "foreground", "warning"), ("semantic", "color", "background", "default"), 4.5, "warning text"),
    (("semantic", "color", "foreground", "inverse"), ("semantic", "color", "background", "inverse"), 4.5, "inverse text"),
    (
        ("semantic", "color", "action", "primary", "foreground", "default"),
        ("semantic", "color", "action", "primary", "background", "default"),
        4.5,
        "primary action label",
    ),
    (("semantic", "color", "border", "default"), ("semantic", "color", "background", "default"), 3.0, "control border"),
    (("semantic", "color", "focus", "ring"), ("semantic", "color", "background", "default"), 3.0, "focus ring"),
)


class Issue:
    def __init__(self, level: str, code: str, message: str, location: str = "") -> None:
        self.level = level
        self.code = code
        self.message = message
        self.location = location

    def to_dict(self) -> dict[str, str]:
        return {
            "level": self.level,
            "code": self.code,
            "message": self.message,
            "location": self.location,
        }


@dataclass
class Report:
    errors: list[Issue] = field(default_factory=list)
    warnings: list[Issue] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)

    def error(self, code: str, message: str, location: str = "") -> None:
        self.errors.append(Issue("error", code, message, location))

    def warning(self, code: str, message: str, location: str = "") -> None:
        self.warnings.append(Issue("warning", code, message, location))

    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": "pass" if self.ok() else "fail",
            "stats": self.stats,
            "errors": [issue.to_dict() for issue in self.errors],
            "warnings": [issue.to_dict() for issue in self.warnings],
        }


def parse_attributes(raw: str) -> dict[str, str]:
    attributes: dict[str, str] = {}
    for match in re.finditer(r"([A-Za-z_][A-Za-z0-9_-]*)=(\"[^\"]*\"|'[^']*'|\S+)", raw):
        value = match.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        attributes[match.group(1)] = value
    return attributes


def strip_comments(text: str) -> str:
    return HTML_COMMENT_RE.sub("", text)


def marker_positions(text: str, pattern: re.Pattern[str]) -> list[tuple[int, int, dict[str, str]]]:
    return [(match.start(), match.end(), parse_attributes(match.group(1))) for match in pattern.finditer(text)]


def section_bodies(text: str, report: Report | None = None) -> dict[str, str]:
    markers = marker_positions(text, SECTION_RE)
    bodies: dict[str, str] = {}
    for index, (start, end, attributes) in enumerate(markers):
        section_id = attributes.get("id", "")
        if report is not None and not section_id:
            report.error("section-missing-id", "A section marker is missing its id.", str(start))
            continue
        if section_id in bodies:
            if report is not None:
                report.error("duplicate-section", f"Duplicate section marker id={section_id}.", section_id)
            continue
        next_start = markers[index + 1][0] if index + 1 < len(markers) else len(text)
        bodies[section_id] = text[end:next_start]
    return bodies


def content_lines(body: str) -> list[str]:
    cleaned = strip_comments(body)
    return [line.strip() for line in cleaned.splitlines() if line.strip()]


def label_line(body: str, label: str) -> str:
    pattern = re.compile(r"(?im)^\s*(?:\*\*)?%s\b[^\n]*" % re.escape(label))
    match = pattern.search(body)
    return match.group(0).strip() if match else ""


def header_metadata(text: str) -> dict[str, str]:
    first_section = SECTION_RE.search(text)
    header = text[: first_section.start()] if first_section else text[:4000]
    metadata: dict[str, str] = {}
    for match in re.finditer(r"(?m)^\s*[-*]\s*([^:\n]+):\s*(.+?)\s*$", header):
        metadata[match.group(1).strip().lower()] = match.group(2).strip()
    return metadata


def component_specs(section_body: str) -> list[tuple[dict[str, str], str]]:
    markers = marker_positions(section_body, COMPONENT_RE)
    specs: list[tuple[dict[str, str], str]] = []
    for index, (_start, end, attributes) in enumerate(markers):
        next_start = markers[index + 1][0] if index + 1 < len(markers) else len(section_body)
        specs.append((attributes, section_body[end:next_start]))
    return specs


def is_alias(value: Any) -> bool:
    return isinstance(value, str) and bool(ALIAS_RE.match(value.strip()))


def get_node(root: Any, path: tuple[str, ...]) -> Any:
    node = root
    for key in path:
        if not isinstance(node, dict) or key not in node:
            return None
        node = node[key]
    return node


def resolve_value(value: Any, root: Any, depth: int = 0) -> Any:
    if depth > 30:
        raise ValueError("alias cycle or excessive alias depth")
    if isinstance(value, dict):
        if "$value" in value:
            return resolve_value(value["$value"], root, depth + 1)
        return value
    if is_alias(value):
        path = tuple(part for part in value.strip()[1:-1].split(".") if part)
        node = get_node(root, path)
        if node is None:
            raise KeyError(".".join(path))
        return resolve_value(node, root, depth + 1)
    return value


def collect_aliases(value: Any) -> Iterator[str]:
    if is_alias(value):
        yield value.strip()
    elif isinstance(value, dict):
        for item in value.values():
            yield from collect_aliases(item)
    elif isinstance(value, list):
        for item in value:
            yield from collect_aliases(item)


def iter_tokens(node: Any, path: tuple[str, ...] = (), inherited_type: str | None = None) -> Iterator[tuple[tuple[str, ...], Any, str | None]]:
    if isinstance(node, dict):
        node_type = node.get("$type", inherited_type)
        if "$value" in node:
            yield path, node["$value"], node_type
            return
        for key, value in node.items():
            if key.startswith("$"):
                continue
            yield from iter_tokens(value, path + (key,), node_type)
    else:
        yield path, node, inherited_type


def parse_px(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, dict):
        raw = value.get("value")
        unit = value.get("unit", "px")
        if isinstance(raw, (int, float)):
            factor = 16.0 if unit in ("rem", "em") else 1.0
            return float(raw) * factor
        return None
    if not isinstance(value, str):
        return None
    match = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*(px|rem|em)?\s*$", value)
    if not match:
        return None
    number = float(match.group(1))
    unit = match.group(2) or "px"
    if unit in ("rem", "em"):
        number *= 16.0
    return number


def parse_color(value: Any) -> tuple[float, float, float] | None:
    if not isinstance(value, str):
        return None
    raw = value.strip()
    if raw.startswith("#"):
        hex_part = raw[1:]
        if len(hex_part) in (3, 4):
            hex_part = "".join(char * 2 for char in hex_part)
        if len(hex_part) == 8:
            hex_part = hex_part[:6]
        if len(hex_part) != 6:
            return None
        try:
            return tuple(int(hex_part[index : index + 2], 16) / 255.0 for index in (0, 2, 4))  # type: ignore[return-value]
        except ValueError:
            return None
    match = re.match(r"rgba?\(([^)]+)\)", raw, re.IGNORECASE)
    if match:
        parts = [part for part in re.split(r"[,\s/]+", match.group(1).strip()) if part]
        if len(parts) < 3:
            return None
        try:
            channels = [float(part) for part in parts[:3]]
        except ValueError:
            return None
        if any(channel > 1 for channel in channels):
            channels = [channel / 255.0 for channel in channels]
        return tuple(min(max(channel, 0.0), 1.0) for channel in channels)  # type: ignore[return-value]
    return None


def relative_luminance(color: tuple[float, float, float]) -> float:
    def linear(channel: float) -> float:
        if channel <= 0.04045:
            return channel / 12.92
        return ((channel + 0.055) / 1.055) ** 2.4

    red, green, blue = (linear(channel) for channel in color)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(first: tuple[float, float, float], second: tuple[float, float, float]) -> float:
    light = max(relative_luminance(first), relative_luminance(second))
    dark = min(relative_luminance(first), relative_luminance(second))
    return (light + 0.05) / (dark + 0.05)


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> None:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_merge(base[key], value)
        else:
            base[key] = copy.deepcopy(value)


def token_root_for_theme(data: dict[str, Any], theme_name: str) -> dict[str, Any]:
    root = copy.deepcopy(data)
    themes = data.get("themes", {})
    theme = themes.get(theme_name, {}) if isinstance(themes, dict) else {}
    override = theme.get("semantic", {}) if isinstance(theme, dict) else {}
    if isinstance(override, dict) and isinstance(root.get("semantic"), dict):
        deep_merge(root["semantic"], override)
    return root


def normalize_key(key: str) -> str:
    return re.sub(r"[\s_-]+", "", key.lower())


def validate_markdown(
    text: str,
    report: Report,
    min_components: int,
    min_questions: int,
    min_a11y: int,
    min_audit: int = 1,
    require_audit: bool = False,
) -> None:
    artifact = ARTIFACT_RE.search(text)
    if not artifact:
        report.error("artifact-missing", "Missing artifact marker: <!-- design-system:artifact type=design-system version=1 -->")
    else:
        attributes = parse_attributes(artifact.group(1))
        if attributes.get("type") != "design-system":
            report.error("artifact-type", "Artifact marker type must be design-system.", "artifact")
        if attributes.get("version") != "1":
            report.error("artifact-version", "Artifact marker version must be 1.", "artifact")

    metadata = header_metadata(text)
    for key in REQUIRED_METADATA:
        if key not in metadata or not metadata[key]:
            report.error("metadata-missing", f"Missing required metadata: {key.title()}.")
    status = metadata.get("status", "").strip().lower()
    if status and status not in ALLOWED_STATUS:
        report.error("metadata-status", f"Status must be one of: {', '.join(ALLOWED_STATUS)}.", "Status")
    date = metadata.get("date", "").strip()
    if date and not DATE_RE.match(date):
        report.error("metadata-date", "Date must use YYYY-MM-DD.", "Date")
    version = metadata.get("version", "").strip()
    if version and not VERSION_RE.match(version):
        report.error("metadata-version", "Version must use semantic versioning, for example 1.0.0.", "Version")
    mode = metadata.get("mode", "").strip().lower()
    if mode and mode not in ALLOWED_MODES:
        report.error("metadata-mode", f"Mode must be one of: {', '.join(ALLOWED_MODES)}.", "Mode")
    audit_required = require_audit or mode == "audit"

    bodies = section_bodies(text, report)
    for section in REQUIRED_SECTIONS:
        if section not in bodies:
            report.error("section-missing", f"Missing required section id={section}.", section)
            continue
        if not content_lines(bodies[section]):
            report.error("section-empty", f"Required section id={section} is empty.", section)

    if "principles" in bodies:
        principles = PRIN_ID_RE.findall(bodies["principles"])
        if len(set(principles)) < 3:
            report.error("principles-count", "At least three PRIN-### principles are required.", "principles")

    if "tokens" in bodies:
        tokens_body = bodies["tokens"].lower()
        for term in ("primitive", "semantic", "component"):
            if term not in tokens_body:
                report.error("tokens-layer", f"The tokens section must describe the {term} layer.", "tokens")
        if not re.search(r"\{category\}|color\.background\.|component\.button\.", bodies["tokens"]):
            report.error("tokens-naming", "The tokens section must show the naming convention, for example color.background.primary.default.", "tokens")
        if "design.json" not in bodies["tokens"]:
            report.error("tokens-source", "The tokens section must name design.json as the machine-readable source of truth.", "tokens")

    if "typography" in bodies:
        typography = bodies["typography"]
        if "16px" not in typography and "1rem" not in typography:
            report.error("typography-base", "The typography section must state the 16px or 1rem base size.", "typography")
        if not re.search(r"1\.2(?:0|5)?0?|1\.25", typography):
            report.error("typography-ratio", "The typography section must state a modular ratio such as 1.200 or 1.250.", "typography")
        if "size(n)" not in typography and "formula" not in typography.lower():
            report.error("typography-formula", "The typography section must show the size(n) formula.", "typography")
        if len(re.findall(r"\d+(?:\.\d+)?px", typography)) < 4:
            report.error("typography-values", "The typography section must list at least four px values.", "typography")

    if "spacing" in bodies:
        spacing = bodies["spacing"]
        if "4px" not in spacing:
            report.error("spacing-grid", "The spacing section must state the 4px base grid.", "spacing")
        if "space(n)" not in spacing and "formula" not in spacing.lower():
            report.error("spacing-formula", "The spacing section must show the space(n) formula.", "spacing")
        if len(re.findall(r"\d+(?:\.\d+)?px", spacing)) < 4:
            report.error("spacing-values", "The spacing section must list at least four px values.", "spacing")
        layout = spacing.lower()
        anchors = [pos for pos in (layout.find("responsive layout"), layout.find("breakpoint")) if pos != -1]
        layout_block = layout[min(anchors):] if anchors else ""
        required_layout_terms = {
            "breakpoint": "breakpoint tiers",
            "mobile": "mobile tier",
            "tablet": "tablet tier",
            "desktop": "desktop tier",
            "wide": "wide tier",
            "column": "grid columns",
            "gutter": "grid gutters",
            "margin": "side margins",
        }
        for term, label in required_layout_terms.items():
            if term not in layout_block:
                report.error("layout-term", f"The spacing section must cover responsive {label} ({term}).", "spacing")
        if "full-width" not in layout_block and "full width" not in layout_block:
            report.error("layout-adaptation", "The layout subsection must state that buttons become full-width on mobile.", "spacing")
        if not re.search(r"\btable\b", layout_block) or "card" not in layout_block:
            report.error("layout-table", "The layout subsection must document the table-to-card or table-scroll fallback.", "spacing")
        tier_lines = "\n".join(
            line for line in layout_block.splitlines()
            if re.search(r"\b(?:mobile|tablet|desktop|wide)\b", line, re.IGNORECASE)
        )
        if len(set(re.findall(r"\d+(?:\.\d+)?(?:px|rem)", tier_lines))) < 4:
            report.error(
                "layout-breakpoint-values",
                "The layout subsection must list at least four distinct breakpoint values with units.",
                "spacing",
            )

    if "accessibility" in bodies:
        accessibility = bodies["accessibility"]
        lowered = accessibility.lower()
        required_terms = {
            "4.5:1": "normal text contrast",
            "3:1": "large text and UI contrast",
            "44": "touch target",
            "200%": "text resize",
            "prefers-reduced-motion": "reduced motion",
            "keyboard": "keyboard operability",
            "focus": "focus visibility",
        }
        for term, label in required_terms.items():
            if term not in lowered:
                report.error("accessibility-term", f"The accessibility section must cover {label} ({term}).", "accessibility")
        a11y_ids = set(A11Y_ID_RE.findall(accessibility))
        if len(a11y_ids) < min_a11y:
            report.error(
                "accessibility-count",
                f"At least {min_a11y} unique A11Y-### rules are required; found {len(a11y_ids)}.",
                "accessibility",
            )
        ratio_rows = re.findall(r"\d+(?:\.\d+)?:1", accessibility)
        if len(ratio_rows) < 4:
            report.error("accessibility-contrast", "The accessibility section must include a contrast pair matrix with measured ratios.", "accessibility")

    component_count = 0
    component_ids: list[str] = []
    if "components" in bodies:
        specs = component_specs(bodies["components"])
        component_count = len(specs)
        if component_count < min_components:
            report.error(
                "components-count",
                f"At least {min_components} component markers are required; found {component_count}.",
                "components",
            )
        for attributes, body in specs:
            component_id = attributes.get("id", "")
            name = attributes.get("name", "")
            status = attributes.get("status", "")
            layer = attributes.get("layer", "")
            if not COMPONENT_ID_RE.match(component_id):
                report.error("component-id", f"Invalid component id '{component_id}'. Use CMP-###.", component_id or "components")
            else:
                component_ids.append(component_id)
            if not name:
                report.error("component-name", f"{component_id or 'A component'} is missing its name attribute.", component_id)
            if status not in ALLOWED_COMPONENT_STATUS:
                report.error("component-status", f"{component_id or 'A component'} status must be stable, beta, or deprecated.", component_id)
            if not layer:
                report.error("component-layer", f"{component_id or 'A component'} is missing its layer attribute.", component_id)
            for label in COMPONENT_LABELS:
                if not label_line(body, label):
                    report.error("component-label", f"{component_id or 'A component'} is missing the {label} line.", component_id)
            states_line = label_line(body, "States").lower()
            for state in ("default", "hover", "focus", "disabled"):
                if state not in states_line:
                    report.error("component-states", f"{component_id or 'A component'} states must mention {state.title()}.", component_id)
            if "loading" not in states_line and "n/a" not in states_line:
                report.error("component-loading", f"{component_id or 'A component'} states must mention Loading or N/A.", component_id)
            if "error" not in states_line and "n/a" not in states_line:
                report.error("component-error", f"{component_id or 'A component'} states must mention Error or N/A.", component_id)
            usage_line = label_line(body, "Usage").lower()
            if usage_line and not re.search(r"\b(do not use|don't use|avoid|not use)\b", usage_line):
                report.warning("component-usage", f"{component_id or 'A component'} should state when not to use it.", component_id)
            accessibility_line = label_line(body, "Accessibility").lower()
            if accessibility_line and not re.search(r"aria|role|keyboard|focus|screen reader|accessible name|target", accessibility_line):
                report.warning("component-a11y", f"{component_id or 'A component'} should state its accessibility behavior.", component_id)
            tokens_line = label_line(body, "Tokens")
            if tokens_line and "component." not in tokens_line:
                report.error("component-tokens", f"{component_id or 'A component'} must reference component.* tokens.", component_id)
            if tokens_line and "semantic." not in tokens_line:
                report.warning("component-semantic-tokens", f"{component_id or 'A component'} should also reference semantic.* tokens.", component_id)

        if component_ids:
            numeric_ids = sorted(int(COMPONENT_ID_RE.match(component_id).group(1)) for component_id in component_ids)  # type: ignore[union-attr]
            expected = list(range(1, len(numeric_ids) + 1))
            if numeric_ids != expected:
                report.error(
                    "component-ids",
                    "Component IDs must be unique and sequential from CMP-001.",
                    "components",
                )

    if "qa" in bodies:
        questions = QUESTION_RE.findall(bodies["qa"])
        if len(questions) < min_questions:
            report.error(
                "questions-count",
                f"At least {min_questions} Q-### questions are required; found {len(questions)}.",
                "qa",
            )
        for question_id in questions:
            pattern = re.compile(r"###\s+%s\b(.*?)(?=###\s+Q-\d{3}\b|\Z)" % re.escape(question_id), re.DOTALL)
            match = pattern.search(bodies["qa"])
            if match:
                block = match.group(1).lower()
                if "question" not in block or "answer" not in block:
                    report.warning("question-format", f"{question_id} should include Question and Answer lines.", question_id)

    if "governance" in bodies:
        governance = bodies["governance"].lower()
        for term, label in (
            ("version", "versioning"),
            ("deprecat", "deprecation"),
            ("contribut", "contribution"),
            ("release", "release process"),
        ):
            if term not in governance:
                report.error("governance-term", f"The governance section must cover {label}.", "governance")

    if "adoption" in bodies:
        adoption = bodies["adoption"].lower()
        for term, label in (
            ("pilot", "a pilot"),
            ("migration", "migration"),
            ("documentation", "documentation"),
            ("metric", "adoption metrics"),
        ):
            if term not in adoption:
                report.error("adoption-term", f"The adoption section must cover {label}.", "adoption")

    if "audit" not in bodies:
        if audit_required:
            report.error(
                "audit-section",
                "Mode Audit (or --require-audit) requires a section id=audit with AUDIT-### findings.",
                "audit",
            )
    else:
        audit_body = bodies["audit"]
        audit_rows = AUDIT_ROW_RE.findall(audit_body)
        unique_audit = set(audit_rows)
        if audit_required and len(unique_audit) < max(1, min_audit):
            report.error(
                "audit-count",
                f"At least {max(1, min_audit)} AUDIT-### findings are required; found {len(unique_audit)}.",
                "audit",
            )
        for line in audit_body.splitlines():
            if not AUDIT_ROW_RE.match(line):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            audit_id = cells[0]
            if len(cells) < 8:
                report.error(
                    "audit-row",
                    f"{audit_id} must include route, viewport, evidence, severity, remediation, owner, and status.",
                    audit_id,
                )
                continue
            severity = cells[4].lower()
            if not any(level in severity for level in ALLOWED_AUDIT_SEVERITY):
                report.error("audit-severity", f"{audit_id} severity must be High, Medium, or Low.", audit_id)
            status = cells[7].lower()
            if "high" in severity and status.startswith("open"):
                report.warning(
                    "audit-high-open",
                    f"{audit_id} is a High finding still open; fix it before release or record a compensating control.",
                    audit_id,
                )
        lowered_audit = audit_body.lower()
        for viewport in AUDIT_VIEWPORTS:
            if viewport not in audit_body:
                report.error("audit-viewport", f"The layout audit must include evidence at {viewport}.", "audit")
        if "pattern map" not in lowered_audit:
            report.error("audit-pattern-map", "The layout audit must include a target pattern map.", "audit")
        if "migration sequence" not in lowered_audit and "migration plan" not in lowered_audit:
            report.error("audit-migration", "The layout audit must include a migration sequence.", "audit")
        if "pilot" not in lowered_audit:
            report.warning("audit-pilot", "The layout audit should name the pilot screen.", "audit")
        if "acceptance" not in lowered_audit:
            report.warning("audit-acceptance", "The layout audit should state acceptance criteria.", "audit")
        if "rollback" not in lowered_audit:
            report.warning("audit-rollback", "The layout audit should state the rollback plan.", "audit")
        report.stats["audit_findings"] = len(unique_audit)

    if "traceability" in bodies and component_ids:
        for component_id in component_ids:
            if component_id not in bodies["traceability"]:
                report.error("traceability-missing", f"{component_id} is missing from the traceability section.", "traceability")

    if "dod" in bodies:
        checkboxes = re.findall(r"(?m)^\s*-\s*\[[ xX]\]", bodies["dod"])
        if len(checkboxes) < 5:
            report.error("dod-checklist", "The definition of done must include at least five checklist items.", "dod")

    counts = COUNTS_RE.search(text)
    a11y_count = len(set(A11Y_ID_RE.findall(bodies.get("accessibility", ""))))
    question_count = len(QUESTION_RE.findall(bodies.get("qa", "")))
    if not counts:
        report.error("counts-missing", "Missing counts marker: <!-- design-system:counts components=12 a11y=8 questions=6 -->")
    else:
        attributes = parse_attributes(counts.group(1))
        expected = {
            "components": component_count,
            "a11y": a11y_count,
            "questions": question_count,
        }
        for key, actual in expected.items():
            raw = attributes.get(key)
            if raw is None:
                report.error("counts-key", f"The counts marker is missing {key}.", "counts")
                continue
            try:
                declared = int(raw)
            except ValueError:
                report.error("counts-value", f"The counts marker value for {key} must be an integer.", "counts")
                continue
            if declared != actual:
                report.error(
                    "counts-mismatch",
                    f"Counts marker says {key}={declared}, but the artifact contains {actual}.",
                    "counts",
                )

    if PLACEHOLDER_RE.search(text):
        report.error("placeholder", "The artifact contains a TODO, TBD, FIXME, or placeholder.")
    if SECRET_RE.search(text):
        report.error("secret", "The artifact appears to contain a secret, credential, or private key.")

    report.stats.update(
        {
            "components": component_count,
            "a11y_rules": a11y_count,
            "questions": question_count,
            "mode": mode or "unknown",
        }
    )


def validate_tokens(data: dict[str, Any], report: Report, min_components: int, require_themes: bool) -> None:
    for key in ("meta", "primitive", "semantic", "component"):
        if key not in data:
            report.error("tokens-top-level", f"design.json is missing the top-level '{key}' object.", "design.json")
    if not all(key in data for key in ("meta", "primitive", "semantic", "component")):
        return

    meta = data.get("meta", {})
    if not isinstance(meta, dict):
        report.error("tokens-meta", "design.json meta must be an object.", "meta")
        meta = {}
    for key in ("name", "version", "baseFontSize", "scaleRatio", "spacingGrid"):
        if key not in meta:
            report.error("tokens-meta-key", f"design.json meta is missing '{key}'.", "meta")
    base_font = str(meta.get("baseFontSize", ""))
    if base_font and "16" not in base_font:
        report.warning("tokens-base-font", "The recommended base font size is 16px.", "meta.baseFontSize")
    ratio = meta.get("scaleRatio")
    try:
        ratio_value = float(ratio)
    except (TypeError, ValueError):
        ratio_value = None
        report.error("tokens-ratio", "meta.scaleRatio must be a number.", "meta.scaleRatio")
    if ratio_value is not None and not 1.1 <= ratio_value <= 1.6:
        report.warning("tokens-ratio-range", "meta.scaleRatio is outside the usual 1.1 to 1.6 range.", "meta.scaleRatio")
    spacing_grid = str(meta.get("spacingGrid", ""))
    if spacing_grid and "4" not in spacing_grid and "8" not in spacing_grid:
        report.warning("tokens-spacing-grid", "The spacing grid is usually 4px or 8px.", "meta.spacingGrid")

    primitive = data.get("primitive", {})
    semantic = data.get("semantic", {})
    component = data.get("component", {})
    if not isinstance(primitive, dict):
        report.error("tokens-primitive", "primitive must be an object.", "primitive")
        primitive = {}
    if not isinstance(semantic, dict):
        report.error("tokens-semantic", "semantic must be an object.", "semantic")
        semantic = {}
    if not isinstance(component, dict):
        report.error("tokens-component", "component must be an object.", "component")
        component = {}

    for category in REQUIRED_PRIMITIVE_CATEGORIES:
        if category not in primitive:
            report.error("tokens-primitive-category", f"primitive is missing the '{category}' category.", "primitive")
        elif not isinstance(primitive[category], dict):
            report.error("tokens-primitive-category", f"primitive.{category} must be an object.", f"primitive.{category}")
    for category in REQUIRED_SEMANTIC_CATEGORIES:
        if category not in semantic:
            report.error("tokens-semantic-category", f"semantic is missing the '{category}' category.", "semantic")
        elif not isinstance(semantic[category], dict):
            report.error("tokens-semantic-category", f"semantic.{category} must be an object.", f"semantic.{category}")

    breakpoint_tokens = list(iter_tokens(primitive.get("breakpoint", {}), ("breakpoint",)))
    if len(breakpoint_tokens) < 4:
        report.error(
            "tokens-breakpoints",
            "primitive.breakpoint must contain at least four breakpoint steps.",
            "primitive.breakpoint",
        )
    for path, value, _token_type in breakpoint_tokens:
        if parse_px(value) is None:
            report.error(
                "tokens-breakpoint-value",
                f"Breakpoint token {'.'.join(path)} must be a px or rem dimension.",
                ".".join(path),
            )

    grid_primitive = primitive.get("grid", {})
    if not isinstance(grid_primitive, dict):
        grid_primitive = {}
    grid_columns = list(iter_tokens(grid_primitive.get("columns", {}), ("grid", "columns")))
    if len(grid_columns) < 4:
        report.error(
            "tokens-grid-columns",
            "primitive.grid.columns must contain at least four tiers.",
            "primitive.grid.columns",
        )
    for path, value, _token_type in grid_columns:
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 1 <= value <= 24:
            report.error(
                "tokens-grid-column",
                f"Grid column token {'.'.join(path)} must be a number from 1 to 24.",
                ".".join(path),
            )
    for key in ("gutter", "margin"):
        grid_tokens = list(iter_tokens(grid_primitive.get(key, {}), ("grid", key)))
        if len(grid_tokens) < 4:
            report.error(
                "tokens-grid-spacing",
                f"primitive.grid.{key} must contain at least four tiers.",
                f"primitive.grid.{key}",
            )
        for path, value, _token_type in grid_tokens:
            if parse_px(value) is None:
                report.error(
                    "tokens-grid-value",
                    f"Grid {key} token {'.'.join(path)} must be a px or rem dimension.",
                    ".".join(path),
                )

    layout_semantic = semantic.get("layout", {})
    if isinstance(layout_semantic, dict):
        for key in ("breakpoint", "container", "grid"):
            if not isinstance(layout_semantic.get(key), dict):
                report.error(
                    "tokens-layout-role",
                    f"semantic.layout.{key} must be an object.",
                    f"semantic.layout.{key}",
                )
        layout_breakpoints = list(iter_tokens(layout_semantic.get("breakpoint", {}), ("layout", "breakpoint")))
        if len(layout_breakpoints) < 4:
            report.error(
                "tokens-layout-breakpoints",
                "semantic.layout.breakpoint must expose at least four tiers.",
                "semantic.layout.breakpoint",
            )
        layout_grid = layout_semantic.get("grid", {})
        if isinstance(layout_grid, dict):
            for key in ("columns", "gutter", "margin"):
                layout_tokens = list(iter_tokens(layout_grid.get(key, {}), ("layout", "grid", key)))
                if len(layout_tokens) < 4:
                    report.error(
                        "tokens-layout-grid",
                        f"semantic.layout.grid.{key} must expose at least four tiers.",
                        f"semantic.layout.grid.{key}",
                    )

    actual_namespaces = {normalize_key(key): key for key in component.keys() if not key.startswith("$")}
    missing_namespaces = [
        label for key, label in EXPECTED_COMPONENT_NAMESPACES.items() if key not in actual_namespaces
    ]
    if missing_namespaces:
        report.error(
            "tokens-component-namespaces",
            f"design.json is missing component namespaces: {', '.join(missing_namespaces)}.",
            "component",
        )
    namespace_count = len(actual_namespaces)
    if namespace_count < min_components:
        report.error(
            "tokens-component-count",
            f"At least {min_components} component namespaces are required; found {namespace_count}.",
            "component",
        )

    primitive_tokens = list(iter_tokens(primitive))
    semantic_tokens = list(iter_tokens(semantic))
    component_tokens = list(iter_tokens(component))

    for path, value, token_type in primitive_tokens:
        dotted = ".".join(path)
        if token_type == "color" and parse_color(value) is None:
            report.error("tokens-primitive-color", f"Primitive color {dotted} must be a hex, rgb, or hsl color.", dotted)
        if path[:1] == ("space",):
            px = parse_px(value)
            if px is None:
                report.warning("tokens-spacing-value", f"Spacing token {dotted} is not a simple dimension.", dotted)
            elif px % 2 != 0:
                report.error("tokens-spacing-grid", f"Spacing token {dotted} is not on the 2px half-step grid.", dotted)
            elif px > 128:
                report.warning("tokens-spacing-large", f"Spacing token {dotted} is larger than 128px.", dotted)

    font_sizes: list[float] = []
    for path, value, _token_type in primitive_tokens:
        if path[:2] == ("font", "size"):
            px = parse_px(value)
            if px is not None:
                font_sizes.append(px)
    if len(font_sizes) < 6:
        report.error("tokens-font-scale", "primitive.font.size must contain at least six steps.", "primitive.font.size")
    if not any(abs(px - 16.0) < 0.01 for px in font_sizes):
        report.error("tokens-font-base", "primitive.font.size must contain a 16px base step.", "primitive.font.size")

    for path, value, token_type in semantic_tokens:
        dotted = ".".join(path)
        if token_type == "color":
            if not is_alias(value):
                report.error("tokens-semantic-alias", f"Semantic color {dotted} must alias a primitive token.", dotted)
            elif not value.strip()[1:-1].startswith("primitive."):
                report.error(
                    "tokens-semantic-layer",
                    f"Semantic color {dotted} must reference primitive.*, not {value.strip()[1:-1]}.",
                    dotted,
                )
        if token_type == "typography" and isinstance(value, dict):
            for key in ("fontFamily", "fontSize", "fontWeight", "lineHeight", "letterSpacing"):
                if key not in value:
                    report.warning("tokens-typography-composite", f"Typography token {dotted} is missing {key}.", dotted)

    for path, value, _token_type in component_tokens:
        dotted = ".".join(path)
        if not is_alias(value):
            report.error("tokens-component-alias", f"Component token {dotted} must alias a semantic token.", dotted)
            continue
        target = value.strip()[1:-1]
        if not target.startswith("semantic."):
            report.error(
                "tokens-component-layer",
                f"Component token {dotted} must reference semantic.*, not {target}.",
                dotted,
            )

    for path, value, _token_type in semantic_tokens + component_tokens:
        for alias in collect_aliases(value):
            try:
                resolve_value(alias, data)
            except (KeyError, ValueError) as error:
                report.error(
                    "tokens-alias-target",
                    f"{'.'.join(path)} references a missing or invalid alias: {error}.",
                    ".".join(path),
                )

    themes = data.get("themes")
    if not isinstance(themes, dict):
        if require_themes:
            report.error("tokens-themes", "design.json must contain a themes object with light and dark.", "themes")
        else:
            report.warning("tokens-themes", "design.json has no themes object; theme coverage cannot be verified.", "themes")
    else:
        for theme_name in ("light", "dark"):
            if theme_name not in themes:
                if require_themes:
                    report.error("tokens-theme-missing", f"themes.{theme_name} is required.", "themes")
                else:
                    report.warning("tokens-theme-missing", f"themes.{theme_name} is missing.", "themes")
            elif not isinstance(themes[theme_name], dict):
                report.error("tokens-theme-type", f"themes.{theme_name} must be an object.", f"themes.{theme_name}")

        for theme_name, theme in themes.items():
            if not isinstance(theme, dict):
                continue
            for key in theme:
                if key != "semantic" and not key.startswith("$"):
                    report.error(
                        "tokens-theme-layer",
                        f"themes.{theme_name}.{key} is not allowed; themes override semantic tokens only.",
                        f"themes.{theme_name}",
                    )
            override = theme.get("semantic", {})
            if not isinstance(override, dict):
                report.error(
                    "tokens-theme-semantic",
                    f"themes.{theme_name}.semantic must be an object.",
                    f"themes.{theme_name}.semantic",
                )
                continue
            theme_root = token_root_for_theme(data, theme_name)
            for path, value, _token_type in iter_tokens(override, ("semantic",)):
                for alias in collect_aliases(value):
                    try:
                        resolve_value(alias, theme_root)
                    except (KeyError, ValueError) as error:
                        report.error(
                            "tokens-theme-alias",
                            f"{'.'.join(path)} in themes.{theme_name} references a missing or invalid alias: {error}.",
                            f"themes.{theme_name}",
                        )

    contrast_checks = 0
    contrast_failures = 0
    contrast_min: float | None = None
    theme_names = ["light"]
    if isinstance(themes, dict) and isinstance(themes.get("dark"), dict):
        theme_names.append("dark")
    for theme_name in theme_names:
        root = token_root_for_theme(data, theme_name)
        for foreground_path, background_path, threshold, label in CONTRAST_PAIRS:
            foreground = resolve_value(get_node(root, foreground_path), root) if get_node(root, foreground_path) is not None else None
            background = resolve_value(get_node(root, background_path), root) if get_node(root, background_path) is not None else None
            if foreground is None or background is None:
                report.warning(
                    "tokens-contrast-missing",
                    f"Cannot check {label} in {theme_name}: missing {'.'.join(foreground_path if foreground is None else background_path)}.",
                    theme_name,
                )
                continue
            foreground_color = parse_color(foreground)
            background_color = parse_color(background)
            if foreground_color is None or background_color is None:
                report.warning(
                    "tokens-contrast-format",
                    f"Cannot check {label} in {theme_name}: unsupported color format.",
                    theme_name,
                )
                continue
            ratio = contrast_ratio(foreground_color, background_color)
            contrast_checks += 1
            contrast_min = ratio if contrast_min is None else min(contrast_min, ratio)
            if ratio + 0.005 < threshold:
                contrast_failures += 1
                report.error(
                    "tokens-contrast",
                    f"{label} in {theme_name} has {ratio:.2f}:1, below the required {threshold}:1 "
                    f"({'.'.join(foreground_path)} on {'.'.join(background_path)}).",
                    theme_name,
                )

    report.stats.update(
        {
            "primitive_tokens": len(primitive_tokens),
            "semantic_tokens": len(semantic_tokens),
            "component_tokens": len(component_tokens),
            "component_namespaces": namespace_count,
            "breakpoints": len(breakpoint_tokens),
            "grid_tiers": len(grid_columns),
            "contrast_checks": contrast_checks,
            "contrast_failures": contrast_failures,
            "contrast_min": round(contrast_min, 2) if contrast_min is not None else None,
        }
    )


def print_report(report: Report, artifact: Path, tokens: Path | None) -> None:
    status = "PASS" if report.ok() else "FAIL"
    print(f"Design system validation: {status}")
    print(f"Artifact: {artifact}")
    if tokens is not None:
        print(f"Tokens: {tokens}")
    if report.stats:
        stats = ", ".join(f"{key}={value}" for key, value in report.stats.items())
        print(f"Stats: {stats}")
    print(f"Errors: {len(report.errors)}")
    for issue in report.errors:
        location = f" [{issue.location}]" if issue.location else ""
        print(f"  - {issue.code}{location}: {issue.message}")
    print(f"Warnings: {len(report.warnings)}")
    for issue in report.warnings:
        location = f" [{issue.location}]" if issue.location else ""
        print(f"  - {issue.code}{location}: {issue.message}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate DESIGN-SYSTEM.md and design.json.")
    parser.add_argument("artifact", type=Path, help="Path to DESIGN-SYSTEM.md")
    parser.add_argument("--tokens", type=Path, help="Path to design.json")
    parser.add_argument("--min-components", type=int, default=12, help="Minimum number of component specifications (default: 12)")
    parser.add_argument("--min-questions", type=int, default=6, help="Minimum number of answered questions (default: 6)")
    parser.add_argument("--min-a11y", type=int, default=6, help="Minimum number of A11Y rules (default: 6)")
    parser.add_argument("--min-audit", type=int, default=1, help="Minimum number of AUDIT findings when a layout audit is present (default: 1)")
    parser.add_argument("--require-audit", action="store_true", help="Require a layout audit section with AUDIT-### findings")
    parser.add_argument("--require-themes", action="store_true", help="Require light and dark themes in design.json")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable report")
    args = parser.parse_args(argv)

    report = Report()
    if not args.artifact.exists():
        report.error("artifact-not-found", f"Artifact not found: {args.artifact}")
    else:
        text = args.artifact.read_text(encoding="utf-8")
        validate_markdown(
            text,
            report,
            args.min_components,
            args.min_questions,
            args.min_a11y,
            args.min_audit,
            args.require_audit,
        )

    tokens_data: dict[str, Any] | None = None
    if args.tokens is not None:
        if not args.tokens.exists():
            report.error("tokens-not-found", f"Token file not found: {args.tokens}")
        else:
            try:
                tokens_data = json.loads(args.tokens.read_text(encoding="utf-8"))
            except json.JSONDecodeError as error:
                report.error("tokens-json", f"design.json is not valid JSON: {error}", str(args.tokens))
            if tokens_data is not None:
                if not isinstance(tokens_data, dict):
                    report.error("tokens-json-root", "design.json must contain a JSON object.", str(args.tokens))
                else:
                    validate_tokens(tokens_data, report, args.min_components, args.require_themes)
    else:
        report.warning("tokens-skipped", "No --tokens file was provided; token and contrast checks were skipped.")

    if args.strict:
        for warning in report.warnings:
            report.errors.append(Issue("error", warning.code, warning.message, warning.location))

    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print_report(report, args.artifact, args.tokens)

    return 0 if report.ok() else 1


if __name__ == "__main__":
    sys.exit(main())
