---
description: Validate DESIGN-SYSTEM.md and design.json against the design-system contract
argument-hint: Optional DESIGN-SYSTEM.md path and validator options
---

# Validate Design System

Load the `design-system` skill for the artifact and token contracts.

Host arguments: `$ARGUMENTS`

Use the supplied Markdown path when present; otherwise default to `DESIGN-SYSTEM.md` in the current workspace. Use `design.json` beside it unless another token path is supplied.

Resolve `scripts/validate_design_system.py` relative to the installed skill and run it with the selected artifact and token paths. For a checkout of this repository, the command is:

```bash
python3 skills/design-system/scripts/validate_design_system.py DESIGN-SYSTEM.md --tokens design.json --min-components 12 --min-questions 6
```

Use `--strict` when warnings should fail validation and `--json` for a machine-readable report. Report errors first, then warnings and validated counts. Do not edit the artifacts unless asked.
