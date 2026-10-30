import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_plugin as plugin_validator  # noqa: E402


class PluginStructureTests(unittest.TestCase):
    def test_repository_has_a_valid_cross_agent_plugin_layout(self):
        report = plugin_validator.validate_plugin(ROOT)
        self.assertTrue(report.ok, [issue.message for issue in report.errors])

    def test_missing_agent_manifest_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "plugin"
            shutil.copytree(
                ROOT,
                copy,
                ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"),
            )
            (copy / ".codex-plugin" / "plugin.json").unlink()

            report = plugin_validator.validate_plugin(copy)

        self.assertIn("missing-file", {issue.code for issue in report.errors})

    def test_invalid_manifest_json_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "plugin"
            shutil.copytree(
                ROOT,
                copy,
                ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"),
            )
            (copy / ".claude-plugin" / "plugin.json").write_text("{ invalid", encoding="utf-8")

            report = plugin_validator.validate_plugin(copy)

        self.assertIn("invalid-json", {issue.code for issue in report.errors})


if __name__ == "__main__":
    unittest.main()
