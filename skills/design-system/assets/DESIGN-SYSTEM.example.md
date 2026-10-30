<!-- design-system:artifact type=design-system version=1 -->
# Design System: Northstar

- Status: Draft
- Date: 2026-01-01
- Owner: Design Systems team
- Artifact language: English
- Version: 1.0.0
- Mode: Create
- Platforms: Web (React + Tailwind), iOS, Android
- Product: B2B SaaS analytics dashboard
- Team: 2 designers and 4 developers

<!-- design-system:counts components=12 a11y=8 questions=6 -->

<!-- design-system:section id=context -->
## 1. Context

Northstar is a B2B analytics dashboard used by operations teams to monitor revenue, retention, and account health. The current UI has inconsistent spacing, three button implementations, and no shared accessibility baseline. The team is small and needs a v1.0 that is pragmatic, documented, and easy to adopt.

Scope for v1.0: foundations, light and dark themes, web components, and a pilot migration of the account overview screen. Out of scope: white-label theming, email templates, and a native mobile component library beyond token parity.

<!-- design-system:section id=principles -->
## 2. Principles

| ID | Principle | What it means in practice |
| --- | --- | --- |
| PRIN-001 | Clarity over decoration | Every visual choice must improve comprehension or task completion. |
| PRIN-002 | Accessible by default | Components ship with keyboard, focus, contrast, and screen-reader behavior. |
| PRIN-003 | Tokens are the contract | Components consume semantic and component tokens, never raw values. |
| PRIN-004 | Predictable over clever | The same action looks and behaves the same way everywhere. |
| PRIN-005 | Small and maintainable | Prefer a smaller set of well-documented components over a large unfinished library. |

<!-- design-system:section id=tokens -->
## 3. Design Tokens

The token model has exactly three layers:

- **Primitive**: raw values such as `primitive.color.gray.0`, `primitive.font.size.md`, `primitive.space.4`, and `primitive.breakpoint.md`.
- **Semantic**: intent and theme-aware roles such as `color.background.default`, `color.foreground.muted`, `color.action.primary.background.hover`, `spacing.section.md`, and `layout.grid.columns.desktop`.
- **Component**: scoped decisions such as `component.button.primary.background.hover` and `component.input.border.error`.

Naming convention: `{category}.{property}.{role}.{variant}.{state}`. Example: `color.background.primary.default`.

Alias rule: component tokens reference semantic tokens; semantic tokens reference primitive tokens. A component must never reference a primitive directly.

The machine-readable source of truth is `design.json`. It includes `meta`, `primitive`, `semantic`, `component`, and `themes`. Light is the base theme; dark overrides semantic tokens only.

<!-- design-system:section id=typography -->
## 4. Typography

- Base size: `16px` / `1rem`.
- Product ratio: `1.200` (minor third). Marketing surfaces may use `1.250`.
- Formula: `size(n) = 16 * 1.200^n`.
- Rounding: nearest even pixel; line heights snap to the `4px` grid.

| Token | Raw | Rounded | rem | Line height | Usage |
| --- | --- | --- | --- | --- | --- |
| `font.size.xs` | 11.111px | 12px | 0.75rem | 16px | Caption and helper text |
| `font.size.sm` | 13.333px | 14px | 0.875rem | 20px | Dense body and labels |
| `font.size.md` | 16px | 16px | 1rem | 24px | Default body |
| `font.size.lg` | 19.2px | 20px | 1.25rem | 28px | Lead paragraph |
| `font.size.xl` | 23.04px | 24px | 1.5rem | 32px | Heading 4 |
| `font.size.2xl` | 27.648px | 28px | 1.75rem | 36px | Heading 3 |
| `font.size.3xl` | 33.178px | 32px | 2rem | 40px | Heading 2 |
| `font.size.4xl` | 39.813px | 40px | 2.5rem | 48px | Heading 1 |

Families: `Inter` for UI, `Source Serif 4` for editorial content, and `JetBrains Mono` for code. Weights: 400, 500, 600, 700.

<!-- design-system:section id=spacing -->
## 5. Spacing

- Base grid: `4px`. Layout rhythm: `8px`.
- Formula: `space(n) = 4px * n`.

| Token | Value | rem | Usage |
| --- | --- | --- | --- |
| `space.1` | 4px | 0.25rem | Tight inline gap |
| `space.2` | 8px | 0.5rem | Default inline gap |
| `space.3` | 12px | 0.75rem | Control padding |
| `space.4` | 16px | 1rem | Default stack |
| `space.6` | 24px | 1.5rem | Section padding |
| `space.8` | 32px | 2rem | Large section gap |
| `space.12` | 48px | 3rem | Page block gap |
| `space.16` | 64px | 4rem | Hero spacing |

Semantic roles: `spacing.inline.sm`, `spacing.stack.md`, `spacing.section.lg`, `spacing.page.gutter`, and `spacing.control.height.md`.

Responsive layout and grid:

| Tier | Min width | Columns | Side margin | Gutter | Max content |
| --- | --- | --- | --- | --- | --- |
| Mobile | 0 | 4 | 16px | 16px | 100% |
| Tablet | 768px / 48rem | 8 | 24px | 24px | 768px |
| Desktop | 1024px / 64rem | 12 | 32px | 24px | 1280px |
| Wide | 1280px / 80rem | 12 | 40px | 32px | 1536px |

Grid formula: `content = min(maxContent, viewport - 2 * margin)` and `column = (content - (columns - 1) * gutter) / columns`. Use mobile-first breakpoints and test at `320px`, `768px`, `1024px`, and `1280px`.

Component adaptation matrix:

| Component | Mobile | Tablet and up | Rule |
| --- | --- | --- | --- |
| Button | Full-width in forms and narrow panels | Auto width | Keep the 44px target; stack button groups |
| Icon Button | 44×44px | 40–44px | Icon-only needs an accessible name |
| Input | Full-width, label above | 1–2 columns | Use at least 16px text on mobile |
| Select | Full-width, native picker | Fixed or fluid | Cap menu height; keep the value visible |
| Checkbox | Full-row target | Compact row | The label is part of the target |
| Radio Group | Vertical stack | 2 columns or horizontal | Wrap rather than clip |
| Switch | Full-row label | Compact row | Not for destructive confirmations |
| Badge | Inline, wraps with text | Inline | Never rely on color alone |
| Card | 1 column | 2–4 columns | Full-width action on mobile |
| Modal | Full-screen sheet | Centered dialog | Focus trap; 44px close target |
| Toast | Top center, below safe area | Bottom right | Stack with a limit; use `aria-live` |
| Tabs | Horizontal scroll | Fit | Keep the active tab visible |

Data Table fallback: switch to a card/list view or a scrollable region with a sticky first column. Keep the same data and actions; never squeeze columns below readable width. The full matrix lives in `references/responsive-layout.md`.

<!-- design-system:section id=radius -->
## 6. Radius

| Token | Value | Usage |
| --- | --- | --- |
| `radius.xs` | 2px | Badges and chips |
| `radius.sm` | 4px | Checkboxes and small controls |
| `radius.md` | 8px | Buttons and inputs |
| `radius.lg` | 12px | Cards and panels |
| `radius.xl` | 16px | Modals and large surfaces |
| `radius.full` | 9999px | Pills, avatars, switches |

Semantic aliases: `radius.control = radius.md`, `radius.surface = radius.lg`, `radius.overlay = radius.xl`.

<!-- design-system:section id=elevation -->
## 7. Elevation

| Token | Usage |
| --- | --- |
| `elevation.surface.0` | Flat surfaces and tables |
| `elevation.surface.1` | Cards and inputs on subtle backgrounds |
| `elevation.surface.2` | Dropdowns and popovers |
| `elevation.surface.3` | Modals and sticky headers |
| `elevation.overlay` | Dialog overlays and high-emphasis surfaces |

Dark mode increases shadow opacity and adds a visible border where needed. Elevation is never the only signal of interactivity.

<!-- design-system:section id=motion -->
## 8. Motion

| Token | Value | Usage |
| --- | --- | --- |
| `motion.duration.fast` | 100ms | Hover, focus, small toggles |
| `motion.duration.normal` | 200ms | Default transitions |
| `motion.duration.slow` | 300ms | Modals, drawers |
| `motion.easing.standard` | cubic-bezier(0.2, 0, 0, 1) | Default |

Rules: animate `transform` and `opacity`; respect `prefers-reduced-motion: reduce`; never flash more than three times per second; keep hover and focus feedback at or below 100ms.

<!-- design-system:section id=accessibility -->
## 9. Accessibility

Target: WCAG 2.1 Level AA. Normal text must meet 4.5:1; large text, UI components, graphical objects, and focus indicators must meet 3:1. Every interactive element must be keyboard operable, have a visible focus indicator, and expose an accessible name, role, and state. Touch targets should be 44x44 CSS px, with 24x24 as the absolute minimum. Text must resize to 200% and reflow at 320px. Motion must respect `prefers-reduced-motion`.

| ID | Rule | Verification |
| --- | --- | --- |
| A11Y-001 | Normal text meets 4.5:1 in every theme | Contrast script and manual review |
| A11Y-002 | UI components, borders, and focus rings meet 3:1 | Contrast script and visual review |
| A11Y-003 | Every interactive component is keyboard operable | Keyboard-only test |
| A11Y-004 | Focus is visible, not obscured, and returns after overlays close | Keyboard test with sticky UI |
| A11Y-005 | Every icon-only control has an accessible name | Accessibility tree inspection |
| A11Y-006 | Forms have visible labels, linked errors, and `aria-invalid` | Form review and screen reader |
| A11Y-007 | Color is never the only signal of status or error | Grayscale and color-blind simulation |
| A11Y-008 | Motion respects reduced motion and never flashes more than three times per second | OS reduced-motion test |

Contrast pairs:

| ID | Foreground | Background | Usage | Required | Measured | Result |
| --- | --- | --- | --- | --- | --- | --- |
| A11Y-C01 | `color.foreground.default` | `color.background.default` | Body text | 4.5:1 | 19.45:1 | Pass |
| A11Y-C02 | `color.foreground.muted` | `color.background.default` | Secondary text | 4.5:1 | 4.84:1 | Pass |
| A11Y-C03 | `color.foreground.brand` | `color.background.default` | Links | 4.5:1 | 6.71:1 | Pass |
| A11Y-C04 | `color.action.primary.foreground.default` | `color.action.primary.background.default` | Primary button | 4.5:1 | 5.18:1 | Pass |
| A11Y-C05 | `color.foreground.danger` | `color.background.default` | Error text | 4.5:1 | 4.84:1 | Pass |
| A11Y-C06 | `color.border.default` | `color.background.default` | Input border | 3:1 | 4.84:1 | Pass |
| A11Y-C07 | `color.focus.ring` | `color.background.default` | Focus ring | 3:1 | 3.68:1 | Pass |
| A11Y-C08 | `color.foreground.inverse` | `color.background.inverse` | Inverse text | 4.5:1 | 19.45:1 | Pass |

<!-- design-system:section id=components -->
## 10. Components

<!-- design-system:component id=CMP-001 name=Button status=stable layer=action -->
### CMP-001: Button

**Anatomy:** root button, label, optional leading icon, optional trailing icon, loading spinner, focus ring.
**Variants:** primary, secondary, ghost, danger, link; sizes sm, md, lg.
**States:** Default, Hover, Active, Focus, Disabled, Loading; Error: N/A (use form-level error).
**Usage:** Use for actions that change state or submit data. One primary per view. Do not use for navigation; use a link. Do not use for toggles; use Switch or Checkbox.
**Accessibility:** Native `<button>` with explicit `type`; visible focus ring; 44px target; `aria-busy` when loading; loading keeps width stable.
**Tokens:** `component.button.{variant}.background.{state}`, `component.button.{variant}.foreground.{state}`, `component.button.radius`, `semantic.color.focus.ring`.

<!-- design-system:component id=CMP-002 name=Icon Button status=stable layer=action -->
### CMP-002: Icon Button

**Anatomy:** root button, icon, accessible name, optional tooltip, focus ring.
**Variants:** ghost, solid, outline, danger; sizes sm, md, lg.
**States:** Default, Hover, Active, Focus, Disabled, Loading; Error: N/A.
**Usage:** Use for a single, well-understood action in a compact space. Do not use for the primary page action. Do not use without an accessible name.
**Accessibility:** `aria-label` or visually hidden text; `aria-pressed` for toggles; `aria-expanded` for menus; 44px target; visible focus ring.
**Tokens:** `component.icon-button.{variant}.background.{state}`, `component.icon-button.size.{size}`, `component.icon-button.radius`, `semantic.color.focus.ring`.

<!-- design-system:component id=CMP-003 name=Input status=stable layer=form -->
### CMP-003: Input

**Anatomy:** field wrapper, visible label, input, optional prefix, optional suffix, helper text, error text, optional counter, focus ring.
**Variants:** text, email, password, number, search, telephone, URL; sizes sm, md, lg.
**States:** Default, Hover, Focus, Filled, Disabled, Readonly, Error; Loading: N/A (show async validation separately).
**Usage:** Use for single-line free-form input. Do not use a placeholder as a label. Do not validate on every keystroke in a way that interrupts typing.
**Accessibility:** `for`/`id` label association; `aria-describedby` for helper and error text; `aria-invalid`; correct `type`, `inputmode`, and `autocomplete`; 44px height.
**Tokens:** `component.input.background.{state}`, `component.input.foreground.{state}`, `component.input.border.{state}`, `component.input.radius`, `component.input.height.{size}`, `semantic.color.focus.ring`.

<!-- design-system:component id=CMP-004 name=Select status=stable layer=form -->
### CMP-004: Select / Dropdown

**Anatomy:** field wrapper, label, trigger, value or placeholder, chevron, popover listbox, options, optional search, helper and error text, focus ring.
**Variants:** native select, custom single-select, multi-select with tags, searchable combobox; sizes sm, md, lg.
**States:** Default, Hover, Focus, Open, Selected, Disabled, Loading, Error.
**Usage:** Use for a bounded list when all options do not need to be visible. Use a Radio Group for fewer than about five options. Do not use for navigation. Do not hide the label inside the trigger.
**Accessibility:** Prefer native `<select>`; custom listbox follows the WAI-ARIA listbox pattern with `aria-expanded`, `aria-selected`, and `aria-activedescendant`; arrow keys, Enter, Escape, and type-ahead; 44px target.
**Tokens:** `component.select.trigger.background.{state}`, `component.select.trigger.border.{state}`, `component.select.menu.background`, `component.select.option.background.{state}`, `component.select.radius`, `semantic.elevation.surface.2`.

<!-- design-system:component id=CMP-005 name=Checkbox status=stable layer=form -->
### CMP-005: Checkbox

**Anatomy:** label wrapper, box, check or indeterminate dash, label, optional helper text, error text, focus ring.
**Variants:** single checkbox, checkbox group, indeterminate parent; sizes sm, md.
**States:** Default, Hover, Focus, Checked, Indeterminate, Disabled, Error; Loading: N/A.
**Usage:** Use for independent choices and acknowledgments. Use a Switch for an immediate setting. Do not use a Checkbox for navigation or for an action that saves immediately.
**Accessibility:** Native `<input type="checkbox">`; clickable label; `fieldset` and `legend` for groups; `aria-checked="mixed"` for indeterminate; 44px target; error linked to the group.
**Tokens:** `component.checkbox.background.{state}`, `component.checkbox.border.{state}`, `component.checkbox.check`, `component.checkbox.radius`, `semantic.color.focus.ring`.

<!-- design-system:component id=CMP-006 name=Radio Group status=stable layer=form -->
### CMP-006: Radio Group

**Anatomy:** fieldset, legend, radio items, control and label per item, optional helper text, error text, focus ring.
**Variants:** vertical, horizontal, card radio; sizes sm, md.
**States:** Default, Hover, Focus, Selected, Disabled, Error; Loading: N/A.
**Usage:** Use for mutually exclusive choices with about two to five options. Use a Select for long lists. Do not use for binary on/off settings; use a Switch or single Checkbox.
**Accessibility:** Native radios with the same `name`; `fieldset` and `legend`; arrow keys move and select; `Tab` enters and leaves the group; 44px target.
**Tokens:** `component.radio.background.{state}`, `component.radio.border.{state}`, `component.radio.dot`, `component.radio.size.{size}`, `semantic.color.focus.ring`.

<!-- design-system:component id=CMP-007 name=Switch status=stable layer=form -->
### CMP-007: Switch

**Anatomy:** label wrapper, track, thumb, label, optional helper text, focus ring.
**Variants:** default, label left or right; sizes sm, md.
**States:** Default, Hover, Focus, On, Disabled, Loading; Error: N/A (show form-level message).
**Usage:** Use for an immediate on/off setting. Use a Checkbox when the change requires form submission. Do not use for destructive actions or multi-step choices.
**Accessibility:** `role="switch"` with `aria-checked`, or a native checkbox with switch semantics; `Space` or `Enter` toggles; state announced as on/off; 44px target; async failures announced with a live region.
**Tokens:** `component.switch.track.off`, `component.switch.track.on`, `component.switch.thumb`, `component.switch.radius`, `semantic.color.focus.ring`.

<!-- design-system:component id=CMP-008 name=Badge status=stable layer=display -->
### CMP-008: Badge

**Anatomy:** root, optional dot, optional icon, label or count.
**Variants:** neutral, brand, success, warning, danger, info; solid, subtle, outline; sizes sm, md.
**States:** Default; Hover: N/A; Focus: N/A; Disabled: N/A; Loading: N/A; Error: N/A.
**Usage:** Use for compact status, counts, and categories. Use an inline Alert for feedback that requires reading. Do not use as a button; use a Button or Tag.
**Accessibility:** Badges are text, not controls; text meets 4.5:1; status includes a text label, not a colored dot alone; decorative dots are hidden from assistive technology; the visible label supplies the accessible name.
**Tokens:** `component.badge.{variant}.background`, `component.badge.{variant}.foreground`, `component.badge.{variant}.border`, `component.badge.radius`, `component.badge.padding`, `semantic.color.background.muted`.

<!-- design-system:component id=CMP-009 name=Card status=stable layer=surface -->
### CMP-009: Card

**Anatomy:** container, optional media, optional header, title, optional description, body, optional footer, optional actions, focus ring when interactive.
**Variants:** elevated, outlined, filled, interactive; sizes sm, md, lg.
**States:** Default, Hover, Focus, Selected, Disabled, Loading; Error: N/A (use an inline Alert inside the card).
**Usage:** Use to group related content that can stand alone. Use a List Item for dense repeating rows. Do not use for page layout. Do not nest interactive elements inside an interactive card.
**Accessibility:** Semantic heading for the title; one link or button for an interactive card; focus ring around the card; hover is not the only way to reveal actions; skeletons are hidden from assistive technology.
**Tokens:** `component.card.background`, `component.card.border`, `component.card.radius`, `component.card.padding.{size}`, `component.card.shadow`, `semantic.elevation.surface.1`.

<!-- design-system:component id=CMP-010 name=Modal status=stable layer=overlay -->
### CMP-010: Modal / Dialog

**Anatomy:** overlay, dialog container, header, title, optional description, close button, body, footer, actions, focus trap.
**Variants:** dialog, alertdialog, drawer, fullscreen; sizes sm, md, lg, full.
**States:** Closed, Opening, Open, Loading, Error, Closing; Default, Hover, Focus, Disabled: N/A (the dialog container is not a pointer target).
**Usage:** Use for a focused task, confirmation, or content that must be seen before continuing. Use a Toast for transient feedback. Do not use for long workflows, do not stack modals, and do not use for content that can be inline.
**Accessibility:** `role="dialog"` and `aria-modal="true"`; `aria-labelledby` and `aria-describedby`; focus moves inside and is trapped; `Escape` closes; focus returns to the trigger; background is inert; do not autofocus a destructive action.
**Tokens:** `component.modal.overlay`, `component.modal.background`, `component.modal.radius`, `component.modal.shadow`, `component.modal.max-width.{size}`, `semantic.elevation.overlay`.

<!-- design-system:component id=CMP-011 name=Toast status=stable layer=feedback -->
### CMP-011: Toast / Alert

**Anatomy:** root, icon, optional title, description, optional action, optional close button, optional progress.
**Variants:** toast, inline alert; info, success, warning, danger; sizes sm, md.
**States:** Default, Hover (pause), Focus (pause), Disabled: N/A, Loading: N/A, Error (danger variant persists until dismissed), Entering, Visible, Paused, Exiting, Action.
**Usage:** Use a Toast for non-blocking transient feedback. Use an inline Alert for persistent page status. Use a Modal for a blocking decision. Do not use auto-dismiss for errors that the user must read. Do not stack more than three toasts.
**Accessibility:** `role="status"` or `aria-live="polite"` for non-critical messages; `role="alert"` sparingly for critical errors; do not move focus; pause the timer on hover and focus; include an icon and text, not color alone; the action is keyboard accessible.
**Tokens:** `component.toast.{variant}.background`, `component.toast.{variant}.foreground`, `component.toast.{variant}.border`, `component.toast.radius`, `component.toast.shadow`, `semantic.elevation.surface.3`.

<!-- design-system:component id=CMP-012 name=Tabs status=stable layer=navigation -->
### CMP-012: Tabs

**Anatomy:** tablist, tab items, indicator, tabpanel, focus ring.
**Variants:** underline, pill, segmented; sizes sm, md.
**States:** Default, Hover, Focus, Active, Disabled, Loading; Error: N/A (use an inline Alert in the panel).
**Usage:** Use to switch between related views at the same level. Use a Select or menu for page navigation. Do not use for sequential steps; use a Stepper. Do not hide critical content behind a tab.
**Accessibility:** `role="tablist"`, `role="tab"`, and `role="tabpanel"`; `aria-selected`, `aria-controls`, and `aria-labelledby`; arrow keys move, `Home` and `End` jump; roving `tabindex`; selected state uses an indicator and weight, not color alone.
**Tokens:** `component.tabs.tab.foreground.{state}`, `component.tabs.tab.background.{state}`, `component.tabs.indicator`, `component.tabs.radius`, `semantic.color.focus.ring`.

<!-- design-system:section id=governance -->
## 11. Governance

| ID | Rule | Owner | Cadence |
| --- | --- | --- | --- |
| GOV-001 | Semantic versioning for the package and tokens; breaking changes require a major release and migration guide | Design Systems lead | Every release |
| GOV-002 | Deprecate with an alias and replacement; keep for at least one minor cycle | Design Systems lead | Every deprecation |
| GOV-003 | Contributions require design review, accessibility review, tests, and documentation | Design and frontend leads | Every contribution |
| GOV-004 | Release gate includes lint, type check, unit tests, visual regression, and contrast checks | Frontend lead | Every release |
| GOV-005 | Exceptions are recorded with an owner and an expiry date | Design Systems lead | Quarterly review |

<!-- design-system:section id=adoption -->
## 12. Adoption

- Pilot: migrate the account overview screen first.
- Migration guide: map legacy buttons, inputs, and cards to the new components; list removed tokens and replacements.
- Documentation: Storybook with live examples, props, anatomy, states, accessibility notes, and token references.
- Office hours: weekly 30-minute session for the first two months.
- Metrics: component coverage on pilot screens, percentage of hardcoded colors removed, accessibility defects per release, duplicate component count, and token adoption by platform.
- Feedback: a shared intake form reviewed in the weekly design systems meeting.

<!-- design-system:section id=audit -->
## 13. Layout Audit

Scope: the shared app shell and the account overview pilot. Baseline evidence was captured before migration at `320px`, `768px`, `1024px`, `1280px`, and `200%` zoom.

Target pattern map:

| Legacy pattern | Target pattern | Tiers |
| --- | --- | --- |
| Fixed 360px filter sidebar | Off-canvas filters on mobile; persistent sidebar on desktop | Mobile, tablet, desktop |
| Three-column card grid at every width | 1 column mobile; 2 columns tablet; 3 columns desktop | All |
| Multi-column form at every width | Stacked fields with labels above on mobile | Mobile |

| ID | Route or template | Viewport | Evidence | Severity | Remediation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AUDIT-001 | `/account` | 320px | Fixed sidebar causes 48px horizontal overflow | High | Off-canvas filters; `minmax(0, 1fr)` content | Frontend | In progress |
| AUDIT-002 | `/account` | 200% | Two-column form clips error text | Medium | Stack fields; label above; keep errors next to fields | Frontend | Open |

Migration sequence: global shell, then the account overview pilot, then forms and tables, then overlays, then the long tail. Acceptance: no horizontal scrolling at `320px` or `200%` zoom, every action reachable, and visual regression passes at every target viewport. Rollback: keep the legacy screen behind a feature flag until the pilot passes.

<!-- design-system:section id=qa -->
## 14. Design Answers

### Q-001

- Question: What product and platforms are in scope?
- Answer: A B2B SaaS analytics dashboard for web (React + Tailwind), with iOS and Android token parity.

### Q-002

- Question: What is the brand personality?
- Answer: Calm, precise, and trustworthy, with a technical edge.

### Q-003

- Question: Which accessibility target applies?
- Answer: WCAG 2.1 Level AA, verified in light and dark themes.

### Q-004

- Question: Which scale and grid are approved?
- Answer: Base 16px, product ratio 1.200, 4px spacing grid with an 8px layout rhythm.

### Q-005

- Question: Which themes are required?
- Answer: Light and dark at launch; high contrast is planned for v1.1.

### Q-006

- Question: Who owns and approves changes?
- Answer: The Design Systems lead owns tokens; design and frontend leads review contributions; releases follow the quality gate.

<!-- design-system:section id=traceability -->
## 15. Traceability

| Component | Tokens | Accessibility rules | Platforms |
| --- | --- | --- | --- |
| CMP-001 Button | `component.button.*`, `semantic.color.action.*` | A11Y-001, A11Y-002, A11Y-003, A11Y-004 | Web, iOS, Android |
| CMP-002 Icon Button | `component.icon-button.*` | A11Y-002, A11Y-003, A11Y-005 | Web, iOS, Android |
| CMP-003 Input | `component.input.*`, `semantic.color.focus.ring` | A11Y-001, A11Y-004, A11Y-006 | Web, iOS, Android |
| CMP-004 Select | `component.select.*`, `semantic.elevation.surface.2` | A11Y-002, A11Y-003, A11Y-006 | Web, iOS, Android |
| CMP-005 Checkbox | `component.checkbox.*` | A11Y-002, A11Y-003, A11Y-006, A11Y-007 | Web, iOS, Android |
| CMP-006 Radio Group | `component.radio.*` | A11Y-002, A11Y-003, A11Y-006, A11Y-007 | Web, iOS, Android |
| CMP-007 Switch | `component.switch.*` | A11Y-002, A11Y-003, A11Y-007 | Web, iOS, Android |
| CMP-008 Badge | `component.badge.*` | A11Y-001, A11Y-002, A11Y-007 | Web, iOS, Android |
| CMP-009 Card | `component.card.*`, `semantic.elevation.surface.1` | A11Y-003, A11Y-004 | Web, iOS, Android |
| CMP-010 Modal | `component.modal.*`, `semantic.elevation.overlay` | A11Y-003, A11Y-004, A11Y-005 | Web, iOS, Android |
| CMP-011 Toast | `component.toast.*`, `semantic.elevation.surface.3` | A11Y-003, A11Y-007, A11Y-008 | Web, iOS, Android |
| CMP-012 Tabs | `component.tabs.*`, `semantic.color.focus.ring` | A11Y-003, A11Y-004, A11Y-007 | Web, iOS, Android |

<!-- design-system:section id=dod -->
## 16. Definition of Done

- [ ] `design.json` is valid JSON and contains the three token layers.
- [ ] Every semantic and component value aliases a lower layer.
- [ ] Typography, spacing, radius, elevation, and motion scales include formulas and rationale.
- [ ] Breakpoints, per-tier grid columns, margins, gutters, and component adaptation rules are defined and tested at `320px`, `768px`, `1024px`, and `1280px`.
- [ ] Light and dark themes are defined and verified.
- [ ] Every contrast pair meets WCAG 2.1 AA.
- [ ] Keyboard, focus, target size, text resize, reduced motion, and screen-reader rules are documented.
- [ ] All 12 components have anatomy, variants, states, usage, accessibility, tokens, content rules, and do/don't guidance.
- [ ] Every component traces to tokens, accessibility rules, and platforms.
- [ ] Existing-product layouts have `AUDIT-###` evidence, a target pattern map, and a migration sequence.
- [ ] Governance, versioning, deprecation, contribution, and adoption are defined.
- [ ] The validator passes with no errors.
