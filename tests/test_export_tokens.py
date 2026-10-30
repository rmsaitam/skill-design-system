import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "design-system"
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

import export_tokens  # noqa: E402


class TokenExportTests(unittest.TestCase):
    def test_all_formats_are_written_from_the_starter_tokens(self):
        data = json.loads(
            (SKILL_ROOT / "assets" / "design.example.json").read_text(encoding="utf-8")
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            written = export_tokens.export(data, output, {"css", "tailwind", "json"}, "--ds-")

            self.assertEqual(
                {"tokens.css", "tailwind.tokens.json", "tailwind.tokens.js", "tokens.flat.json"},
                {path.name for path in written},
            )
            css = (output / "tokens.css").read_text(encoding="utf-8")
            self.assertIn(":root {", css)
            self.assertIn('[data-theme="dark"]', css)
            self.assertIn("--ds-", css)
            flat_tokens = json.loads(
                (output / "tokens.flat.json").read_text(encoding="utf-8")
            )
            self.assertIn("tokens", flat_tokens)
            self.assertIn("themes", flat_tokens)
            json.loads((output / "tailwind.tokens.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
