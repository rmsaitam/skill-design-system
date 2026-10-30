# Typography and Spacing

Every scale needs a base, a ratio, a formula, and a rounding rule. A scale without arithmetic is a preference, not a system.

## Modular typography scale

### Formula

```text
size(n) = base * ratio^n
```

- Base: `16px` / `1rem`, the browser default and the minimum comfortable body size.
- Product UI ratio: `1.200` (minor third), because it produces a usable `14px` step and keeps dense interfaces compact.
- Marketing ratio: `1.250` (major third), because it produces stronger display contrast for landing pages and brand surfaces.
- Rounding: round each result to the nearest even pixel, then snap line heights to the `4px` grid. Even sizes keep borders and line boxes crisp; the 4px line-height grid keeps vertical rhythm aligned with spacing.

Do not mix ratios inside one surface. Pick one ratio per product surface and document it.

### Product scale, ratio 1.200, base 16px

| Token | Step | Raw value | Rounded | rem | Line height | Usage |
| --- | --- | --- | --- | --- | --- | --- |
| `font.size.2xs` | -3 | 9.259px | 10px | 0.625rem | 16px | Legal text, dense metadata; avoid for body copy |
| `font.size.xs` | -2 | 11.111px | 12px | 0.75rem | 16px | Caption, helper text, timestamps |
| `font.size.sm` | -1 | 13.333px | 14px | 0.875rem | 20px | Dense body, labels, table cells |
| `font.size.md` | 0 | 16px | 16px | 1rem | 24px | Default body |
| `font.size.lg` | 1 | 19.2px | 20px | 1.25rem | 28px | Lead paragraph, large body |
| `font.size.xl` | 2 | 23.04px | 24px | 1.5rem | 32px | Heading 4 |
| `font.size.2xl` | 3 | 27.648px | 28px | 1.75rem | 36px | Heading 3 |
| `font.size.3xl` | 4 | 33.178px | 32px | 2rem | 40px | Heading 2 |
| `font.size.4xl` | 5 | 39.813px | 40px | 2.5rem | 48px | Heading 1 |
| `font.size.5xl` | 6 | 47.776px | 48px | 3rem | 56px | Display |
| `font.size.6xl` | 7 | 57.331px | 56px | 3.5rem | 64px | Large display |

Line-height ratios range from `1.6` at 10px to `1.143` at 56px. This is intentional: small text needs more leading for legibility, and large display text needs tighter leading to keep its shape.

### Marketing scale, ratio 1.250, base 16px

| Token | Step | Raw value | Rounded | rem | Line height | Usage |
| --- | --- | --- | --- | --- | --- | --- |
| `font.size.2xs` | -2 | 10.24px | 10px | 0.625rem | 16px | Legal text, eyebrow labels |
| `font.size.xs` | -1 | 12.8px | 12px | 0.75rem | 16px | Caption, helper text |
| `font.size.md` | 0 | 16px | 16px | 1rem | 24px | Body |
| `font.size.lg` | 1 | 20px | 20px | 1.25rem | 28px | Lead paragraph |
| `font.size.xl` | 2 | 25px | 24px | 1.5rem | 32px | Heading 4 |
| `font.size.2xl` | 3 | 31.25px | 32px | 2rem | 40px | Heading 3 |
| `font.size.3xl` | 4 | 39.063px | 40px | 2.5rem | 48px | Heading 2 |
| `font.size.4xl` | 5 | 48.828px | 48px | 3rem | 56px | Heading 1 |
| `font.size.5xl` | 6 | 61.035px | 60px | 3.75rem | 64px | Display |

The 1.250 scale has no `14px` step. If the product needs dense controls, use the 1.200 scale or add a documented `14px` dense exception; do not silently introduce an off-scale value.

### Font weights and letter spacing

| Token | Value | Usage |
| --- | --- | --- |
| `font.weight.regular` | 400 | Body, inputs, long text |
| `font.weight.medium` | 500 | Labels, navigation, emphasis |
| `font.weight.semibold` | 600 | Headings, buttons |
| `font.weight.bold` | 700 | Display, strong emphasis |

| Token | Value | Usage |
| --- | --- | --- |
| `font.letterSpacing.tight` | -0.01em | Large headings and display |
| `font.letterSpacing.normal` | 0 | Body and UI |
| `font.letterSpacing.wide` | 0.02em | Uppercase labels and eyebrows |

### Typography roles

| Role | Size | Weight | Line height | Usage |
| --- | --- | --- | --- | --- |
| `typography.display.lg` | 56px | 700 | 64px | Hero display |
| `typography.display.md` | 48px | 700 | 56px | Section display |
| `typography.heading.1` | 40px | 600 | 48px | Page title |
| `typography.heading.2` | 32px | 600 | 40px | Section title |
| `typography.heading.3` | 28px | 600 | 36px | Subsection title |
| `typography.heading.4` | 24px | 600 | 32px | Card or group title |
| `typography.body.lg` | 20px | 400 | 28px | Lead paragraph |
| `typography.body.md` | 16px | 400 | 24px | Default body |
| `typography.body.sm` | 14px | 400 | 20px | Dense body |
| `typography.label.lg` | 16px | 500 | 24px | Form labels |
| `typography.label.md` | 14px | 500 | 20px | Buttons, tabs, table headers |
| `typography.label.sm` | 12px | 500 | 16px | Compact labels |
| `typography.caption` | 12px | 400 | 16px | Helper text, metadata |
| `typography.code` | 14px | 400 | 20px | Inline code and code blocks |

### Responsive typography

- Mobile web: body is `16px`; do not go below `16px` for inputs, because iOS zooms on focus below 16px.
- Use a smaller display step on mobile: `display.lg` becomes `heading.1`, and `heading.1` becomes `heading.2`.
- Prefer fixed steps for product UI. Use `clamp()` only for marketing surfaces where fluid type is a deliberate brand choice.
- Test with 200% text zoom and with the browser's default font size increased.
- Ensure a maximum line length of roughly 45 to 75 characters for body text.

## Spacing scale

### Formula

```text
space(n) = 4px * n
```

The `4px` base grid supports the `8px` layout rhythm while allowing `2px` and `6px` half-steps for borders, icon alignment, and compact controls. Use the `8px` rhythm for layout: prefer `8`, `16`, `24`, `32`, `48`, and `64`.

| Token | Value | rem | Usage |
| --- | --- | --- | --- |
| `space.0` | 0 | 0 | Reset |
| `space.0.5` | 2px | 0.125rem | Hairline gaps, icon optical alignment |
| `space.1` | 4px | 0.25rem | Tight inline gap |
| `space.1.5` | 6px | 0.375rem | Compact control padding |
| `space.2` | 8px | 0.5rem | Default inline gap |
| `space.3` | 12px | 0.75rem | Control padding, compact stack |
| `space.4` | 16px | 1rem | Default stack, card padding |
| `space.5` | 20px | 1.25rem | Comfortable stack |
| `space.6` | 24px | 1.5rem | Section padding |
| `space.8` | 32px | 2rem | Large section gap |
| `space.10` | 40px | 2.5rem | Page block gap |
| `space.12` | 48px | 3rem | Large page block gap |
| `space.16` | 64px | 4rem | Hero spacing |
| `space.20` | 80px | 5rem | Marketing section |
| `space.24` | 96px | 6rem | Large marketing section |
| `space.32` | 128px | 8rem | Maximum page rhythm |

### Semantic spacing roles

| Role | Default | Usage |
| --- | --- | --- |
| `spacing.inline.xs` | 4px | Icon and text |
| `spacing.inline.sm` | 8px | Button icon gap |
| `spacing.inline.md` | 12px | Control groups |
| `spacing.inline.lg` | 16px | Loose inline groups |
| `spacing.stack.xs` | 4px | Label and helper text |
| `spacing.stack.sm` | 8px | Tight form fields |
| `spacing.stack.md` | 16px | Default form field gap |
| `spacing.stack.lg` | 24px | Form sections |
| `spacing.section.sm` | 24px | Compact sections |
| `spacing.section.md` | 32px | Default sections |
| `spacing.section.lg` | 48px | Major sections |
| `spacing.page.gutter` | 16px / 24px / 32px | Mobile / tablet / desktop |
| `spacing.control.height.sm` | 32px | Dense controls |
| `spacing.control.height.md` | 40px | Default controls |
| `spacing.control.height.lg` | 48px | Comfortable controls |

## Layout and breakpoints

| Token | Value | Usage |
| --- | --- | --- |
| `breakpoint.xs` | 0px / 0rem | Base mobile tier |
| `breakpoint.sm` | 640px / 40rem | Large phone |
| `breakpoint.md` | 768px / 48rem | Tablet |
| `breakpoint.lg` | 1024px / 64rem | Small desktop |
| `breakpoint.xl` | 1280px / 80rem | Desktop |
| `breakpoint.2xl` | 1536px / 96rem | Wide desktop |
| `container.sm` | 640px | Narrow content |
| `container.md` | 768px | Reading width |
| `container.lg` | 1024px | Standard app content |
| `container.xl` | 1280px | Wide app content |
| `container.full` | 100% | Full-bleed layouts |

Use mobile-first breakpoints. A layout must reflow at `320px` width without horizontal scrolling, except for intentionally scrollable data tables.

See `references/responsive-layout.md` for the per-breakpoint column grid, gutters, margins, container-query guidance, and the component adaptation matrix.

## Radius scale

| Token | Value | Usage |
| --- | --- | --- |
| `radius.none` | 0 | Sharp surfaces, data tables |
| `radius.xs` | 2px | Badges, tags, small chips |
| `radius.sm` | 4px | Checkboxes, small controls |
| `radius.md` | 8px | Buttons, inputs, default controls |
| `radius.lg` | 12px | Cards, panels |
| `radius.xl` | 16px | Modals, large surfaces |
| `radius.2xl` | 24px | Feature cards |
| `radius.full` | 9999px | Pills, avatars, switches |

Semantic aliases: `radius.control = radius.md`, `radius.surface = radius.lg`, `radius.overlay = radius.xl`, `radius.pill = radius.full`.

Do not mix radii arbitrarily. Pick a personality: sharp (`0-4px`), soft (`8-16px`), or pill (`full` for interactive chips). Document the exception when a component needs a different radius.

## Elevation and shadows

| Token | Value | Usage |
| --- | --- | --- |
| `shadow.0` | none | Flat surfaces |
| `shadow.1` | `0 1px 2px rgba(11,13,18,0.06), 0 1px 3px rgba(11,13,18,0.10)` | Cards, inputs on subtle backgrounds |
| `shadow.2` | `0 2px 4px rgba(11,13,18,0.06), 0 4px 8px rgba(11,13,18,0.08)` | Dropdowns, popovers |
| `shadow.3` | `0 4px 8px rgba(11,13,18,0.08), 0 8px 16px rgba(11,13,18,0.10)` | Modals, sticky headers |
| `shadow.4` | `0 8px 16px rgba(11,13,18,0.10), 0 16px 32px rgba(11,13,18,0.12)` | High-emphasis overlays |

Rules:

- Use borders instead of shadows for dense, flat interfaces.
- Dark themes need stronger shadows or a visible border, because dark surfaces absorb shadow contrast.
- Never use elevation as the only way to communicate interactivity.
- Keep shadows subtle. A shadow is a depth cue, not decoration.

## Motion

| Token | Value | Usage |
| --- | --- | --- |
| `duration.instant` | 0ms | Immediate state changes |
| `duration.fast` | 100ms | Hover, focus, small toggles |
| `duration.normal` | 200ms | Default transitions |
| `duration.slow` | 300ms | Modals, drawers, large surfaces |
| `duration.slower` | 500ms | Page-level choreography |

| Token | Value | Usage |
| --- | --- | --- |
| `easing.standard` | `cubic-bezier(0.2, 0, 0, 1)` | Default |
| `easing.enter` | `cubic-bezier(0, 0, 0.2, 1)` | Elements entering |
| `easing.exit` | `cubic-bezier(0.4, 0, 1, 1)` | Elements leaving |
| `easing.emphasized` | `cubic-bezier(0.2, 0, 0, 1)` | Deliberate emphasis |

Rules:

- Animate `transform` and `opacity`; avoid animating layout properties.
- Use motion to explain a change, not to delay the user.
- Respect `prefers-reduced-motion: reduce`: remove transforms and set duration to `0.01ms`.
- Never flash more than three times per second.
- Keep hover and focus feedback at or below `100ms` so the UI feels responsive.
- Do not animate focus rings in a way that hides them.

## Justification checklist

- [ ] The base size and ratio are recorded.
- [ ] The formula and rounding rule are recorded.
- [ ] Every scale step has a value, a unit, and a usage.
- [ ] Line heights are on the `4px` grid.
- [ ] Spacing follows the `4px` grid, with documented half-steps.
- [ ] Radius, elevation, and motion have a stated personality and usage.
- [ ] Responsive behavior is defined.
- [ ] Reduced motion is defined.
- [ ] The scales match `design.json`.
