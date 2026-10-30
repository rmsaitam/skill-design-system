# Design System

[![skills.sh](https://skills.sh/b/rmsaitam/skill-design-system)](https://skills.sh/rmsaitam/skill-design-system)

Design System is a reusable design-systems skill and agent plugin. It guides teams through creating, auditing, and evolving a pragmatic, accessible design system and produces two validated artifacts:

- `DESIGN-SYSTEM.md`: foundations, responsive behavior, accessibility, component specifications, governance, and traceability.
- `design.json`: the machine-readable design-token source of truth with primitive, semantic, and component layers.

## Supported agents

| Agent | Integration |
| --- | --- |
| Claude Code | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and `commands/` |
| Codex | `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, and `agents/openai.yaml` |
| Antigravity | Root `plugin.json` |
| Cursor | `.cursor-plugin/plugin.json`, `.cursor-plugin/marketplace.json`, and `commands/` |
| GitHub Copilot CLI | Root `plugin.json` and `.github/plugin/marketplace.json` |
| skills.sh | `skills/design-system/SKILL.md` |

All integrations share the same skill, references, examples, validator, and token exporter.

## Install

### skills.sh

```bash
# Select compatible agents interactively
npx skills add rmsaitam/skill-design-system

# Install globally without prompts
npx skills add rmsaitam/skill-design-system -g -y

# List available skills
npx skills add rmsaitam/skill-design-system --list
```

### Claude Code

```text
/plugin marketplace add rmsaitam/skill-design-system
/plugin install design-system@design-system
```

For a local checkout, replace the repository with its absolute path.

### Codex

```bash
codex plugin marketplace add rmsaitam/skill-design-system
codex plugin install design-system@design-system
```

### Antigravity

Install the repository root as a plugin; it contains the Antigravity `plugin.json` manifest.

### Cursor

Install this repository as a plugin from a marketplace or use the local plugin directory. Cursor reads `.cursor-plugin/plugin.json`, `skills/`, and `commands/`.

### GitHub Copilot CLI

```bash
copilot plugin marketplace add rmsaitam/skill-design-system
copilot plugin install design-system@design-system
```

Plugin marketplace and command syntax may vary by agent version. When a CLI command is unavailable, install the repository through that agent's plugin UI.

## Usage

Create or evolve a design system:

```text
/design-system Create a design system for our analytics dashboard
```

Validate existing artifacts:

```text
/design-system-validate DESIGN-SYSTEM.md
```

Export tokens to CSS, Tailwind, and flat JSON:

```text
/design-system-export design.json
```

The workflow inspects existing project context, interviews the user about missing requirements, and asks for approval before generating or changing artifacts. It does not implement application components unless separately requested.

## Artifact contract

### `DESIGN-SYSTEM.md`

The specification covers the approved product and brand direction, a three-layer token architecture, mathematically justified scales, responsive layout rules, WCAG 2.1 AA accessibility, 12 essential component specifications, governance, adoption, and traceability. Stable markers, IDs, and required fields make it auditable and machine-checkable.

### `design.json`

Tokens use exactly three layers:

1. `primitive` — raw values.
2. `semantic` — intent and theme-aware roles.
3. `component` — scoped aliases to semantic tokens.

The validator checks the Markdown artifact contract and token structure, alias resolution, themes, and contrast. The skill workflow keeps both artifacts aligned.

## Validation and token export

The scripts use only Python's standard library. From a repository checkout:

```bash
python3 skills/design-system/scripts/validate_design_system.py \
  DESIGN-SYSTEM.md --tokens design.json --min-components 12 --min-questions 6

python3 skills/design-system/scripts/export_tokens.py \
  --tokens design.json --out dist --format all

python3 scripts/validate_plugin.py .
```

The exporter supports `css`, `tailwind`, `json`, and `all` formats. For installed skills, resolve each bundled script relative to the installed `skills/design-system/SKILL.md`.

## References

The skill includes focused guides for the interview, token architecture, typography and spacing, responsive layout, layout audits, accessibility, component specifications, artifact templates, and manual validation. Complete starter artifacts are in `skills/design-system/assets/`.

## Development

Requirements: Python 3.10 or newer. No runtime or development dependencies are required.

```bash
make test
make validate
make check
```

`make check` runs the unit suite and validates the cross-agent plugin layout.

## License

MIT. See [LICENSE](LICENSE).
