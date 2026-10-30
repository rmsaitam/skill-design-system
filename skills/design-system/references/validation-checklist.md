# Validation Checklist

Use this checklist when Python is unavailable or when you need to verify a design system manually. The script `skills/design-system/scripts/validate_design_system.py` is the source of truth; this checklist mirrors its gates.

## 1. Artifact contract

- [ ] The file starts with `<!-- design-system:artifact type=design-system version=1 -->`.
- [ ] The header includes `Status`, `Date`, `Owner`, `Artifact language`, `Version`, `Mode`, and `Platforms`.
- [ ] `Status` is `Draft`, `In review`, `Approved`, or `Superseded`.
- [ ] `Mode` is `Create`, `Audit`, or `Evolve`.
- [ ] `Date` uses `YYYY-MM-DD`.
- [ ] `Version` uses semantic versioning, such as `1.0.0`.
- [ ] The counts marker exists and matches the artifact: `<!-- design-system:counts components=12 a11y=8 questions=6 -->`.
- [ ] Every required section marker is present exactly once and is not empty.
- [ ] When `Mode` is `Audit`, the optional `audit` section is present and complete.
- [ ] No `TODO`, `TBD`, `FIXME`, `[insert ...]`, or `lorem ipsum` placeholders remain.
- [ ] No secrets, private keys, credentials, customer data, or personal data are present.

Required section IDs:

```text
context, principles, tokens, typography, spacing, radius, elevation, motion,
accessibility, components, governance, adoption, qa, traceability, dod

optional: audit
```

## 2. Principles and context

- [ ] The context states the product, users, scope, and explicit out-of-scope items.
- [ ] At least three `PRIN-###` principles are present.
- [ ] Each principle states what it means in practice, not only an aspiration.
- [ ] Confirmed decisions, assumptions, and open questions are distinguishable.

## 3. Token architecture

- [ ] The tokens section names `primitive`, `semantic`, and `component`.
- [ ] The tokens section names `design.json` as the machine-readable source of truth.
- [ ] The naming convention is documented, for example `color.background.primary.default`.
- [ ] `design.json` is valid JSON with no comments or trailing commas.
- [ ] `design.json` contains `meta`, `primitive`, `semantic`, `component`, and `themes`.
- [ ] `meta` includes `name`, `version`, `baseFontSize`, `scaleRatio`, and `spacingGrid`.
- [ ] Primitive categories include `color`, `font`, `space`, `radius`, `shadow`, `duration`, `easing`, `breakpoint`, and `grid`.
- [ ] Semantic categories include `color`, `typography`, `spacing`, `radius`, `elevation`, `motion`, and `layout`.
- [ ] The component layer has a namespace for all 12 components.
- [ ] Primitive tokens are raw and theme-agnostic.
- [ ] Semantic tokens express intent and may change by theme.
- [ ] Every component token aliases a `semantic.*` token.
- [ ] No component token references `primitive.*` directly.
- [ ] No raw hex colors appear below the primitive layer.
- [ ] Every alias resolves to an existing token; there are no cycles.
- [ ] Light and dark themes exist; dark overrides semantic tokens only.

## 4. Typography and spacing

- [ ] The typography base is `16px` or `1rem`.
- [ ] The ratio is stated, normally `1.200` for product UI or `1.250` for marketing.
- [ ] The formula is stated, for example `size(n) = 16 * 1.200^n`.
- [ ] At least four concrete px values are listed.
- [ ] Line heights snap to the `4px` grid.
- [ ] Body text does not drop below `16px` on mobile web.
- [ ] The spacing grid is `4px`, with an `8px` layout rhythm.
- [ ] The spacing formula is stated, for example `space(n) = 4px * n`.
- [ ] At least four concrete spacing values are listed.
- [ ] Breakpoints are defined with px and rem values for mobile, tablet, desktop, and wide.
- [ ] Each breakpoint states columns, side margins, gutters, and maximum content width.
- [ ] The grid formula is documented.
- [ ] Component adaptation covers buttons, cards, modals, tabs, toasts, and data tables.
- [ ] The layout is tested at `320px`, `768px`, `1024px`, and `1280px`.
- [ ] New layouts document the page shell, regions, template pattern map, and per-tier reflow rules.
- [ ] No layout introduces a screen-specific breakpoint, container width, gutter, or hardcoded page margin.
- [ ] `primitive.breakpoint` and `primitive.grid` exist; `semantic.layout` exposes them.
- [ ] Radius, elevation, and motion scales include values and usage.

## 5. Accessibility

- [ ] The target is WCAG 2.1 Level AA.
- [ ] Normal text meets `4.5:1`.
- [ ] Large text, UI components, graphical objects, and focus indicators meet `3:1`.
- [ ] Touch targets are `44x44` CSS px where possible, with `24x24` as the absolute minimum.
- [ ] Text resizes to `200%` and reflows at `320px`.
- [ ] Motion respects `prefers-reduced-motion`.
- [ ] Every interactive component is keyboard operable.
- [ ] Focus is visible, not obscured, and returns after overlays close.
- [ ] Every icon-only control has an accessible name.
- [ ] Forms have visible labels, linked errors, and `aria-invalid`.
- [ ] Color is never the only signal of status or error.
- [ ] At least six unique `A11Y-###` rules are present.
- [ ] The contrast matrix includes foreground, background, usage, required ratio, measured ratio, and result.
- [ ] Every measured ratio meets or exceeds its required ratio, or has a recorded exception.

## 6. Components

- [ ] There are 12 component markers, `CMP-001` through `CMP-012`, unique and sequential.
- [ ] Each marker has `id`, `name`, `status`, and `layer`.
- [ ] Each status is `stable`, `beta`, or `deprecated`.
- [ ] Each component body contains `Anatomy:`, `Variants:`, `States:`, `Usage:`, `Accessibility:`, and `Tokens:`.
- [ ] The states line mentions Default, Hover, Focus, Disabled, and Loading or `N/A`.
- [ ] The states line mentions Error or `N/A`.
- [ ] Usage states when to use and when not to use the component.
- [ ] Accessibility states role, keyboard behavior, focus, ARIA, contrast, and target size.
- [ ] Tokens reference `component.*` and `semantic.*` tokens.
- [ ] Responsive behavior is documented per component or in the layout adaptation matrix.
- [ ] Content rules and do/don't guidance are present.
- [ ] Every `CMP-###` appears in the traceability section.

Default v1.0 set:

```text
CMP-001 Button
CMP-002 Icon Button
CMP-003 Input
CMP-004 Select / Dropdown
CMP-005 Checkbox
CMP-006 Radio Group
CMP-007 Switch
CMP-008 Badge
CMP-009 Card
CMP-010 Modal / Dialog
CMP-011 Toast / Alert
CMP-012 Tabs
```

## 7. Layout audit (existing products)

- [ ] `Mode` is `Audit`, or the artifact records why the audit section is omitted.
- [ ] The `audit` section contains at least one `AUDIT-###` finding.
- [ ] Each finding row includes route or template, viewport, evidence, severity, remediation, owner, and status.
- [ ] Severity uses High, Medium, or Low.
- [ ] Evidence covers `320px`, `768px`, `1024px`, `1280px`, and `200%` zoom.
- [ ] A target pattern map maps every legacy pattern to a target pattern and tier.
- [ ] A migration sequence names the global shell, the pilot screen, and the long tail.
- [ ] Acceptance criteria and a rollback plan are stated.
- [ ] Exceptions have an owner, reason, expiry, and compensating control.
- [ ] High findings are fixed before release or have a recorded compensating control.

## 8. Questions, governance, and adoption

- [ ] At least six `### Q-###` headings are present.
- [ ] Each question has a `Question:` line and an `Answer:` line.
- [ ] Governance covers versioning, deprecation, contribution, and release.
- [ ] Adoption covers a pilot, migration, documentation, and metrics.
- [ ] Ownership, cadence, and exception handling are explicit.

## 9. Definition of done

- [ ] The DoD contains at least five checklist items.
- [ ] The DoD covers tokens, scales, layouts, themes, contrast, accessibility, components, traceability, governance, and validation.
- [ ] The DoD mentions the layout audit when the product already exists.
- [ ] The validator passes with no errors.
- [ ] Warnings are resolved or explicitly accepted with a recorded reason.

## 10. Manual commands

```bash
python3 -m json.tool design.json > /dev/null
python3 skills/design-system/scripts/validate_design_system.py DESIGN-SYSTEM.md --tokens design.json --min-components 12 --min-questions 6
python3 skills/design-system/scripts/validate_design_system.py DESIGN-SYSTEM.md --tokens design.json --strict
python3 skills/design-system/scripts/validate_design_system.py DESIGN-SYSTEM.md --tokens design.json --require-audit --min-audit 1
python3 skills/design-system/scripts/export_tokens.py --tokens design.json --out dist --format all
```

If the validator cannot run, record the manual result and the reason the script was unavailable.
