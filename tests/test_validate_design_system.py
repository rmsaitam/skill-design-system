import contextlib
import copy
import io
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "design-system"
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

import validate_design_system as validator  # noqa: E402

EXAMPLE_ARTIFACT = SKILL_ROOT / "assets" / "DESIGN-SYSTEM.example.md"
EXAMPLE_TOKENS = SKILL_ROOT / "assets" / "design.example.json"
TEMPLATE = SKILL_ROOT / "references" / "design-system-template.md"


def example_text() -> str:
    return EXAMPLE_ARTIFACT.read_text(encoding="utf-8")


def report_for(text: str, **overrides) -> validator.Report:
    options = {
        "min_components": 12,
        "min_questions": 6,
        "min_a11y": 6,
        "min_audit": 1,
        "require_audit": True,
    }
    options.update(overrides)
    report = validator.Report()
    validator.validate_markdown(text, report, **options)
    return report


def error_codes(report: validator.Report) -> set[str]:
    return {issue.code for issue in report.errors}


def without_audit_section(text: str) -> str:
    start = text.index("<!-- design-system:section id=audit -->")
    end = text.index("<!-- design-system:section id=qa -->")
    return text[:start] + text[end:]


def template_artifact() -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    start = text.index("```markdown") + len("```markdown\n")
    end = text.index("\n```", start)
    return text[start:end]


class ExampleArtifactTests(unittest.TestCase):
    def test_example_passes_strict_layout_audit_gate(self):
        report = report_for(example_text())
        self.assertEqual([], [issue.code for issue in report.errors])
        self.assertEqual([], [issue.code for issue in report.warnings])
        self.assertEqual(2, report.stats["audit_findings"])
        self.assertEqual("create", report.stats["mode"])

    def test_template_artifact_matches_example(self):
        self.assertEqual(
            example_text().rstrip("\n"),
            template_artifact().rstrip("\n"),
        )


class AuditGateTests(unittest.TestCase):
    def test_example_passes_without_audit_section_when_not_required(self):
        report = report_for(without_audit_section(example_text()), require_audit=False)
        self.assertNotIn("audit-section", error_codes(report))

    def test_audit_mode_requires_audit_section(self):
        text = example_text().replace("- Mode: Create", "- Mode: Audit")
        report = report_for(without_audit_section(text), require_audit=False)
        self.assertIn("audit-section", error_codes(report))

    def test_require_audit_flag_rejects_missing_section(self):
        report = report_for(without_audit_section(example_text()), require_audit=True)
        self.assertIn("audit-section", error_codes(report))

    def test_invalid_mode_is_rejected(self):
        text = example_text().replace("- Mode: Create", "- Mode: Rework")
        report = report_for(text)
        self.assertIn("metadata-mode", error_codes(report))

    def test_invalid_severity_is_rejected(self):
        text = example_text().replace(
            "| High | Off-canvas filters;",
            "| Critical | Off-canvas filters;",
        )
        report = report_for(text)
        self.assertIn("audit-severity", error_codes(report))

    def test_missing_viewport_evidence_is_rejected(self):
        text = example_text().replace("`1280px`, and `200%` zoom", "`1281px`, and `200%` zoom")
        report = report_for(text)
        self.assertIn("audit-viewport", error_codes(report))

    def test_missing_pattern_map_is_rejected(self):
        text = example_text().replace("Target pattern map:", "Patterns:")
        report = report_for(text)
        self.assertIn("audit-pattern-map", error_codes(report))

    def test_missing_migration_sequence_is_rejected(self):
        text = example_text().replace("Migration sequence:", "Order:")
        report = report_for(text)
        self.assertIn("audit-migration", error_codes(report))

    def test_missing_acceptance_criteria_is_warned(self):
        text = example_text().replace("Acceptance:", "Done when:")
        report = report_for(text)
        self.assertIn("audit-acceptance", {issue.code for issue in report.warnings})

    def test_counts_mismatch_is_rejected(self):
        text = example_text().replace("questions=6", "questions=5")
        report = report_for(text)
        self.assertIn("counts-mismatch", error_codes(report))


class TokenValidationTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(EXAMPLE_TOKENS.read_text(encoding="utf-8"))

    def validate(self, data):
        report = validator.Report()
        validator.validate_tokens(data, report, 12, True)
        return report

    def test_example_tokens_pass(self):
        report = self.validate(self.data)
        self.assertEqual([], [issue.code for issue in report.errors])
        self.assertEqual([], [issue.code for issue in report.warnings])

    def test_component_raw_value_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["component"]["button"]["primary"]["background"]["default"]["$value"] = "#ffffff"
        report = self.validate(data)
        self.assertIn("tokens-component-alias", error_codes(report))

    def test_component_primitive_reference_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["component"]["button"]["primary"]["background"]["default"]["$value"] = "{primitive.color.blue.600}"
        report = self.validate(data)
        self.assertIn("tokens-component-layer", error_codes(report))

    def test_semantic_raw_color_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["semantic"]["color"]["foreground"]["default"]["$value"] = "#111111"
        report = self.validate(data)
        self.assertIn("tokens-semantic-alias", error_codes(report))


class CommandLineTests(unittest.TestCase):
    def test_cli_passes_example_with_strict_audit_gate(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = validator.main(
                [
                    str(EXAMPLE_ARTIFACT),
                    "--tokens",
                    str(EXAMPLE_TOKENS),
                    "--min-components",
                    "12",
                    "--min-questions",
                    "6",
                    "--require-audit",
                    "--min-audit",
                    "1",
                    "--strict",
                ]
            )
        self.assertEqual(0, exit_code, output.getvalue())
        self.assertIn("Design system validation: PASS", output.getvalue())


if __name__ == "__main__":
    unittest.main()
