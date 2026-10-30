# Layout audit and restructuring

Use this playbook when the product already exists and its layouts must be analyzed, prioritized, and migrated to the design system's responsive grid. For greenfield work, use [responsive-layout.md](responsive-layout.md) directly.

The goal is not a visual rewrite. The goal is a measurable, incremental migration from ad hoc layouts to one responsive layout contract.

## Outcomes

A completed layout audit produces:

- an inventory of screens, templates, breakpoints, containers, and layout patterns;
- baseline evidence at the target viewports, zoom levels, and content extremes;
- findings with severity, evidence, and remediation;
- a target layout contract mapped to the existing templates;
- a sequenced migration plan with acceptance criteria;
- a summary recorded in `DESIGN-SYSTEM.md` using `AUDIT-###` findings.

## 1. Scope and evidence

Start with representative templates, not every route. Group screens by layout pattern: app shell, dashboard, list, table, detail, form, settings, authentication, empty state, and error state.

Collect:

- route and screen inventory, including the highest-traffic screens;
- existing breakpoints, media queries, container widths, grid CSS, and framework utilities;
- component inventory and layout-related variants;
- screenshots or recordings at the baseline viewports;
- analytics for viewport widths, devices, and top journeys;
- support tickets and accessibility reports about overflow, clipping, zoom, or unusable mobile screens;
- design files, legacy specs, and known exceptions;
- constraints: browser support, CMS, design tooling, release cadence, and team capacity.

Do not audit every screen at the same depth. Audit one representative screen per template first, then sample the long tail.

## 2. Inventory

Create one row per screen or template. Use `AUDIT-###` for findings; do not invent a new ID family.

| ID | Screen or route | Template | Current breakpoints | Current grid or container | Key components | Layout debt | Severity | Target tier | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AUDIT-001 | `/orders` | Table + filters | 760px, 1024px | Fixed 360px sidebar; fluid table | Table, Input, Select, Button | Horizontal overflow at 320px; filters do not collapse | High | Mobile, tablet, desktop | Off-canvas filters; table card fallback |
| AUDIT-002 | `/account` | Detail + form | 900px | 2-column form at all widths | Input, Select, Button, Card | Labels beside fields on mobile | Medium | Mobile | Stack fields; label above |

Also record:

- every distinct breakpoint value and where it is defined;
- every fixed width, `min-width`, `max-width`, and `overflow-x` rule;
- every use of `100vh`, `position: fixed`, absolute positioning, and sticky headers or footers;
- every component that changes layout by screen;
- every layout exception that must be preserved.

## 3. Baseline matrix

Capture the current state before changing code. Test at minimum:

| Viewport | Zoom | Orientation | Required evidence |
| --- | --- | --- | --- |
| 320px | 100% | Portrait | No horizontal scroll; all content reachable |
| 375px | 100% | Portrait | Forms, tables, modals, and navigation usable |
| 768px | 100% | Portrait and landscape | Tablet grid and navigation behavior |
| 1024px | 100% | Landscape | Desktop shell and content width |
| 1280px | 100% | Landscape | Wide layout and line length |
| 1536px | 100% | Landscape | Maximum container and whitespace |
| 320px | 200% | Portrait | Reflow without two-dimensional scrolling |
| Any target | 200% | Any | Text resize and focus visibility |
| RTL locale | 100% | Any | Logical properties and mirrored navigation |

Also test content extremes: longest labels, translated strings, empty state, loading state, error state, many rows, large numbers, long file names, and missing images.

## 4. Layout debt catalog

Use this catalog to classify findings consistently. Map each finding to the existing High, Medium, or Low severity model.

| Finding | Detection | Why it matters | Default severity |
| --- | --- | --- | --- |
| Horizontal overflow at 320px or 200% zoom | Scroll width exceeds viewport; content clipped | Breaks WCAG reflow and hides content | High |
| Fixed width or `min-width` larger than the viewport | Search for `width: ...px` and `min-width` | Causes overflow and blocks mobile use | High |
| Data table with no fallback | Table overflows; columns are squeezed or hidden | Data becomes unreadable or unreachable | High |
| Modal not adapted to mobile | Dialog is wider than the viewport; close action is off-screen | Blocks the task and focus management | High |
| Sidebar or navigation not collapsible | Content is obscured or pushed off-screen | Blocks navigation on mobile | High |
| Content hidden instead of reflowed | `display: none` on required content at small widths | Removes information and actions | High |
| Form uses multiple columns on mobile | Fields sit side by side below 768px | Labels and errors become hard to associate | Medium |
| Input text below 16px on mobile | Computed font size is under 16px | Triggers browser zoom and layout instability | Medium |
| Tabs wrap or clip | Tabs break into rows or overflow without scroll | Hides views and breaks the tab pattern | Medium |
| Toast covers primary action or safe area | Fixed position overlaps controls | Blocks tasks and ignores device insets | Medium |
| Sticky header or footer overlaps content | Content is hidden behind fixed bars | Users cannot reach the end of the page | Medium |
| `100vh` used on mobile | Content jumps when browser chrome appears | Creates overflow and unstable layout | Medium |
| Absolute positioning used for page layout | Many `position: absolute` rules | Prevents reflow and creates fragile layouts | Medium |
| Hardcoded spacing or widths | Values not backed by spacing or layout tokens | Causes drift and blocks theme changes | Medium |
| Duplicate or near-duplicate breakpoints | 760px, 768px, 800px used for the same intent | Creates inconsistent behavior | Medium |
| Container too wide or line length outside 45–75ch | Measured text width | Reduces readability | Low |
| Media not fluid | Fixed image or video dimensions | Causes overflow and distortion | Medium |
| RTL layout mirrors incorrectly | Directional margins, icons, and navigation | Breaks RTL locales | High when RTL is in scope |
| Hover-only action | Action has no focus or touch equivalent | Makes actions inaccessible on touch and keyboard | High |
| Layout shift after load | CLS or visible jump | Causes mis-taps and reading disruption | Medium |
| z-index escalation | Large or conflicting z-index values | Causes overlays to cover the wrong content | Medium |

## 5. Target layout contract

Adopt the breakpoints, columns, margins, gutters, containers, and component adaptation rules from [responsive-layout.md](responsive-layout.md). Do not create a second grid for the migration.

Map every legacy pattern to a target pattern:

| Legacy pattern | Target pattern | Target tiers | Notes |
| --- | --- | --- | --- |
| Fixed sidebar + content | Off-canvas navigation on mobile; persistent sidebar on desktop | Mobile, tablet, desktop | Preserve current location and active state |
| Desktop dashboard grid | 1 column mobile; 2 columns tablet; 3–4 columns desktop | All | Use `minmax(0, 1fr)` |
| Wide data table | Table on desktop; card/list or scrollable table on mobile | All | Keep the same data and actions |
| Multi-column form | Single column mobile; 2 columns tablet and up | Mobile, tablet, desktop | Labels above fields on mobile |
| Centered modal | Full-screen sheet mobile; centered dialog tablet and up | All | Focus trap and 44px close target |
| Fixed toast | Top center mobile; bottom right desktop | All | Respect safe areas |
| Wrapped tabs | Horizontal scroll mobile; fit desktop | All | Keep the active tab visible |
| Fixed-height hero | Fluid height with min/max and aspect ratio | All | Avoid `100vh` on mobile |

Document exceptions explicitly: route, reason, owner, expiry, and compensating control. An exception without an expiry is layout debt.

## 6. Prioritize and sequence

Use the existing severity model:

- **High**: reflow blockers, inaccessible content, broken navigation, data loss, or a task that cannot be completed on mobile.
- **Medium**: inconsistent layouts, maintainability cost, or a degraded but usable experience.
- **Low**: visual polish, naming, or a minor inconsistency.

Sequence the work:

1. **Global shell**: navigation, page container, grid, header, footer, and safe areas.
2. **Highest-traffic templates**: the screens with the most users and the most layout debt.
3. **Forms and data-heavy screens**: inputs, validation, tables, filters, and bulk actions.
4. **Overlays and feedback**: modals, sheets, toasts, and popovers.
5. **Long tail**: low-traffic screens, edge cases, and visual polish.

Do not attempt a big-bang rewrite. Migrate by template, keep the old path behind a feature flag when needed, and define a rollback plan.

## 7. Implement the target layout

- Use CSS Grid for two-dimensional layout and Flexbox for one-dimensional alignment.
- Replace fixed widths with `width: 100%`, `max-width`, and `minmax(0, 1fr)`.
- Use the layout tokens for breakpoints, containers, gutters, and margins; do not add screen-specific breakpoints.
- Use logical properties such as `margin-inline` and `padding-inline` for RTL.
- Prefer `dvh` or `svh` over `100vh` when mobile browser chrome is a risk.
- Use container queries for reusable cards, sidebars, and split panes.
- Reflow content; do not hide required content on small screens.
- Keep touch targets at least 44px where practical and never below 24px.
- Preserve focus order, keyboard behavior, and screen-reader associations.
- Replace hardcoded spacing and widths with semantic tokens as each template is migrated.

## 8. Verify

Every migrated template must pass:

- [ ] No horizontal scrolling at `320px` or `200%` zoom, except an intentional table region.
- [ ] Content is reachable and readable at `320px`, `768px`, `1024px`, `1280px`, and `1536px`.
- [ ] Buttons become full-width in mobile forms and narrow panels.
- [ ] Data tables have a card/list fallback or a usable scroll strategy.
- [ ] Modals become full-screen sheets on mobile and remain keyboard operable.
- [ ] Tabs scroll on mobile and keep the active tab visible.
- [ ] Toasts respect safe areas and do not cover primary actions.
- [ ] Forms stack on mobile, keep labels above fields, and use at least 16px input text.
- [ ] Navigation is usable with touch, keyboard, and screen readers.
- [ ] Focus is visible and not obscured by sticky bars or overlays.
- [ ] RTL layouts mirror correctly when RTL is in scope.
- [ ] Long labels, empty states, loading states, errors, and many rows do not break the layout.
- [ ] Visual regression screenshots pass at every target viewport.
- [ ] No new hardcoded breakpoint, width, or spacing value was introduced.

## 9. Record in DESIGN-SYSTEM.md

Set `Mode: Audit` in the artifact header and record the findings in the `audit` section:

```html
<!-- design-system:section id=audit -->
```

Use `AUDIT-###` findings in that section. If an artifact predates the audit section, summarize the findings in adoption or QA and link the standalone file.

| ID | Route or template | Viewport | Evidence | Severity | Remediation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AUDIT-001 | `/orders` | 320px | 48px horizontal overflow from fixed sidebar | High | Off-canvas filters; `minmax(0, 1fr)` content | Frontend | Open |
| AUDIT-002 | `/account` | 320px | Two-column form clips error text | Medium | Stack fields; label above | Frontend | Open |

Also record:

- the target pattern map;
- the migration sequence and pilot screens;
- exceptions with owner and expiry;
- metrics: migrated templates, remaining overflow defects, distinct breakpoint count, hardcoded width count, and reflow accessibility defects.

Run `python3 skills/design-system/scripts/validate_design_system.py DESIGN-SYSTEM.md --tokens design.json --require-audit --min-audit 1` (or set `Mode: Audit`). The validator checks the `AUDIT-###` table, severity, target viewports, target pattern map, and migration sequence. It cannot inspect rendered layouts, so keep the screenshots and viewport evidence in the audit record.

For a large audit, keep a standalone `LAYOUT-AUDIT.md` and summarize the findings in `DESIGN-SYSTEM.md`.

## 10. Anti-patterns

- Redesigning every screen before fixing the shell.
- Copying the desktop layout into a narrower viewport.
- Hiding content on mobile instead of reflowing it.
- Adding a new breakpoint for each screen.
- Masking overflow with `overflow-x: hidden`.
- Fixing visuals without keyboard, focus, zoom, or screen-reader checks.
- Keeping the legacy grid and the new grid in parallel indefinitely.
- Declaring the migration complete without viewport evidence.
