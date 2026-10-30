---
description: Export design.json tokens to CSS, Tailwind, or flat JSON
argument-hint: Path to design.json, output directory, or export format
---

# Export Design Tokens

Load the `design-system` skill for the token contract.

Host arguments: `$ARGUMENTS`

Resolve `scripts/export_tokens.py` relative to the installed skill. Export from the user's `design.json` without modifying it. If no format is specified, export CSS variables, a Tailwind theme, and flat JSON. Write generated files to `dist/` unless the user specifies another output directory.

For a checkout of this repository:

```bash
python3 skills/design-system/scripts/export_tokens.py --tokens design.json --out dist --format all
```

Report the generated file paths and surface validation or export errors; do not silently substitute defaults for invalid tokens.
