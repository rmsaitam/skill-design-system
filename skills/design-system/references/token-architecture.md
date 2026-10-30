# Token Architecture

The token model is the foundation of the design system. It must be small enough for a v1.0 team to maintain and strict enough to survive new themes, platforms, and components.

## The three layers

| Layer | Purpose | Contains | May reference | Must not contain |
| --- | --- | --- | --- | --- |
| `primitive` | Raw, theme-agnostic values | Palette steps, font families, type sizes, spacing steps, breakpoints, grid columns, gutters, margins, container widths, radii, shadows, durations, easing | Nothing | Semantic intent, component names, theme overrides |
| `semantic` | Intent and theme-aware roles | Background, foreground, border, action, feedback, typography roles, spacing, responsive layout, elevation, motion | `primitive` | Component names, raw hex values, one-off values |
| `component` | Scoped component decisions | Button background, input border, modal radius, badge foreground | `semantic` or `primitive` only through a semantic alias | Raw hex values, cross-component reuse without a semantic role |

Rules:

1. A primitive is never used directly by a component. Components consume component tokens; component tokens consume semantic tokens; semantic tokens consume primitives.
2. A semantic token answers "what is this for", not "what color is this". `color.background.danger` is semantic; `color.red.600` is primitive.
3. A component token answers "where is this used". `component.button.primary.background.hover` is component-scoped.
4. If two components need the same decision, promote it to a semantic token. Do not duplicate a component token.
5. If a component needs a one-off value, create a component token and document why it cannot use a semantic token.

## Naming convention

Use dot notation with lowercase kebab-case segments:

```text
{category}.{property}.{role}.{variant}.{state}
```

Examples:

```text
color.background.primary.default
color.foreground.muted
color.border.focus
color.action.primary.background.hover
typography.heading.2
spacing.section.md
radius.control
elevation.surface.2
motion.duration.fast
component.button.primary.background.hover
component.input.border.error
component.modal.radius
```

Naming rules:

- Use singular category names: `color`, `typography`, `spacing`, `radius`, `elevation`, `motion`.
- Use role words, not visual descriptions: `danger`, not `red`; `muted`, not `gray-light`.
- Put the state last: `default`, `hover`, `active`, `focus`, `selected`, `disabled`, `loading`, `error`, `readonly`.
- Keep variant names stable across components: `primary`, `secondary`, `ghost`, `outline`, `danger`, `link`.
- Never encode a pixel value or hex value in a semantic or component name.
- Never use a component name in a semantic token.
- Keep keys in English even when the documentation is in another language.

## JSON format

Use the W3C Design Tokens Community Group style. A token is an object with `$value` and `$type`. Groups may declare a shared `$type`. Aliases use curly braces:

```json
{
  "primitive": {
    "color": {
      "gray": {
        "$type": "color",
        "0": { "$value": "#ffffff" },
        "950": { "$value": "#0b0d12" }
      }
    }
  },
  "semantic": {
    "color": {
      "background": {
        "default": { "$type": "color", "$value": "{primitive.color.gray.0}" }
      },
      "foreground": {
        "default": { "$type": "color", "$value": "{primitive.color.gray.950}" }
      }
    }
  },
  "component": {
    "button": {
      "primary": {
        "background": {
          "default": { "$type": "color", "$value": "{semantic.color.action.primary.background.default}" }
        }
      }
    }
  }
}
```

Requirements:

- `meta` includes `name`, `version`, `baseFontSize`, `scaleRatio`, and `spacingGrid`.
- `primitive`, `semantic`, and `component` are top-level objects.
- `themes` contains `light`, `dark`, and optional `high-contrast` overrides.
- Every semantic color and component color uses an alias.
- Composite typography tokens use an object value with `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, and `letterSpacing`.
- Dimensions use a string with a unit, such as `"4px"` or `"1rem"`.
- Breakpoints use dimensions with px and rem values; grid column counts use unitless numbers.
- `primitive` includes `breakpoint` and `grid`; `semantic` includes `layout` with breakpoint, container, and grid roles.
- Shadows use a composite object with `color`, `offsetX`, `offsetY`, `blur`, and `spread`.
- Do not use comments in JSON. Do not use trailing commas.

## Color roles

Define at least these semantic color groups:

| Group | Roles |
| --- | --- |
| `color.background` | `default`, `subtle`, `muted`, `inverse`, `brand`, `danger`, `success`, `warning`, `info`, `overlay` |
| `color.foreground` | `default`, `muted`, `subtle`, `inverse`, `brand`, `danger`, `success`, `warning`, `info`, `on-brand`, `disabled` |
| `color.border` | `default`, `subtle`, `strong`, `focus`, `danger`, `success`, `warning`, `info`, `disabled` |
| `color.action` | `primary`, `secondary`, `ghost`, `danger`, `link`, each with `background`, `foreground`, and `border` states |
| `color.focus` | `ring`, `ring-offset` |
| `color.overlay` | `scrim` |

State rules:

- `default` is the resting state.
- `hover` must be distinguishable without relying on color alone.
- `active` must be darker or more compressed than hover.
- `focus` must use the focus ring token and meet 3:1 against the adjacent background.
- `disabled` must be visually distinct and must not respond to pointer or keyboard activation.
- `loading` keeps the component dimensions stable and uses a spinner or skeleton.

Palette guidance:

- Use a neutral ramp with at least 10 steps, including `0`, `50`, `100`, `200`, `300`, `400`, `500`, `600`, `700`, `800`, `900`, `950`.
- Use a brand ramp with at least 9 steps and a clear `500` or `600` primary.
- Use feedback ramps for danger, success, warning, and info.
- Verify contrast at the semantic level, not the primitive level.
- Do not assume a palette step is accessible on every background. The semantic pair is the unit of verification.

## Typography roles

Define composite tokens for:

- `typography.display.lg`, `typography.display.md`
- `typography.heading.1` through `typography.heading.4`
- `typography.body.lg`, `typography.body.md`, `typography.body.sm`
- `typography.label.lg`, `typography.label.md`, `typography.label.sm`
- `typography.caption`
- `typography.code`

Each role includes family, size, weight, line height, and letter spacing. Components consume roles, not raw sizes.

## Spacing roles

Define both a primitive scale and semantic roles:

- `spacing.inline.xs`, `sm`, `md`, `lg`
- `spacing.stack.xs`, `sm`, `md`, `lg`
- `spacing.section.sm`, `md`, `lg`
- `spacing.page.gutter`, `spacing.page.max-width`
- `spacing.control.height.sm`, `md`, `lg`

Use primitives for the numeric steps and semantic roles for layout intent. Do not hardcode `16px` in a component when `spacing.inline.md` expresses the intent.

## Layout and responsive roles

Define breakpoint, grid, and container tokens so responsive behavior is testable:

- `breakpoint.xs`, `sm`, `md`, `lg`, `xl`, `2xl` as px and rem values; `xs` is the base mobile tier at `0px`.
- `grid.columns.mobile`, `tablet`, `desktop`, `wide` as unitless numbers.
- `grid.gutter.mobile`, `tablet`, `desktop`, `wide` as dimensions.
- `grid.margin.mobile`, `tablet`, `desktop`, `wide` as dimensions.
- `grid.container.sm` through `2xl` as maximum content widths.
- Semantic `layout.breakpoint.*`, `layout.container.*`, and `layout.grid.*` alias the primitives.

Keep the breakpoint count small. Four tiers are enough for most products: mobile, tablet, desktop, and wide. Add a tier only when a layout problem cannot be solved with the existing grid.

## Radius, elevation, and motion

- Radius: `radius.none`, `xs`, `sm`, `md`, `lg`, `xl`, `full`, plus semantic `radius.control`, `radius.surface`, `radius.overlay`.
- Elevation: `elevation.surface.0` through `elevation.surface.4`, plus `elevation.overlay`. Dark themes usually need stronger shadows or visible borders.
- Motion: `motion.duration.instant`, `fast`, `normal`, `slow`; `motion.easing.standard`, `enter`, `exit`, `emphasized`. Always provide a reduced-motion fallback.

## Theme strategy

- Primitives never change between themes.
- Semantic tokens are the theme contract. A theme overrides semantic tokens only.
- Component tokens inherit from semantic tokens and normally do not change between themes.
- Define `themes.light` and `themes.dark` explicitly. Use `themes.high-contrast` when required.
- Verify every contrast pair in every theme.
- Do not create a separate component for dark mode. Theme the tokens instead.
- Provide a theme attribute or class contract: `:root`, `[data-theme="dark"]`, or the platform equivalent.
- Avoid flashing on first paint. Persist the theme choice and apply it before rendering.

## Platform mapping

| Target | Mapping |
| --- | --- |
| CSS | `--color-background-default: var(--primitive-color-gray-0);` |
| Tailwind | `colors.background.default = 'var(--semantic-color-background-default)'` |
| Tailwind screens | `screens.tablet = '768px'; screens.desktop = '1024px';` |
| Tailwind grid | `gridTemplateColumns.desktop = 'repeat(12, minmax(0, 1fr))';` |
| Swift | Generated `Color` and `CGFloat` constants grouped by layer |
| Kotlin / Compose | Generated `Color` and `Dp` constants grouped by layer |
| Figma | Variables grouped by layer, with modes for light and dark |
| JSON consumers | Flattened map with resolved values and alias metadata |

Rules:

- Generate platform outputs from `design.json`; do not hand-maintain parallel sources.
- Keep the same token names across platforms, adapted only to the language convention.
- Document which platform tokens are generated and which are handwritten.
- Version the generated package and the token source together.

## Versioning and deprecation

- Use semantic versioning for the token package.
- Adding a token or component is a minor release.
- Changing a token value without changing its meaning is a patch, unless it breaks a contrast or brand contract.
- Renaming or removing a token is a major release.
- Deprecate with an alias and a documented replacement before removal.
- Keep a migration table for every major release.
- Do not silently change a token that consumers depend on.

## Common mistakes

- Components importing primitives directly.
- Semantic tokens named after colors instead of intent.
- A separate dark-mode component instead of dark-mode tokens.
- Hardcoded hex values in component code.
- Contrast checked only on the primary button.
- Spacing values that do not follow the grid.
- Breakpoints duplicated in code instead of exported from the token source.
- Components that only work at one viewport width.
- A scale that exists in Figma but not in code.
- Tokens with no owner and no deprecation policy.
- One-off tokens created without a documented reason.
- A `design.json` that is not valid JSON.
