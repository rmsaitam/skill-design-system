# Responsive layout and grid

Responsive behavior is a system decision, not a per-screen patch. Define the breakpoints, the column grid, and the component adaptation rules once, then reuse them.

For an existing product, start with [layout-audit.md](layout-audit.md) to inventory the current layouts, classify debt, and sequence the migration.

## Build a new layout

Author every new template from the layout contract, not from a screenshot. Use this sequence:

1. **Pick the template pattern** from the pattern map below. One pattern per route; do not mix an app shell and a centered auth flow on the same screen.
2. **Define the shell**: header, primary navigation, secondary navigation, main, optional aside, and footer. State which regions are persistent, collapsible, or off-canvas at each tier.
3. **Place regions on the grid**: assign each region a column span at mobile, tablet, desktop, and wide. Use `minmax(0, 1fr)` for every fluid track so long content can shrink instead of overflowing.
4. **Size the container**: use the semantic layout tokens for max content width, side margins, and gutters. Center the container; do not center individual paragraphs.
5. **Set the content measure**: keep body copy between `45ch` and `75ch`; widen the container rather than the paragraph.
6. **Define the reflow rule per region**: stack, collapse to off-canvas, move to a sheet, become a card list, or scroll. Never hide required content.
7. **Define the overflow strategy** before writing CSS: wrap, scroll region, truncate with an accessible full label, or reflow. `overflow-x: hidden` is not a strategy.
8. **Cover the states**: default, loading, empty, error, dense data, longest label, translated string, and `200%` zoom.
9. **Verify** with the testing checklist at the end of this document.

Layout regions consume `semantic.layout.*` tokens. A route must not introduce a new breakpoint, container width, gutter, or hardcoded page margin.

### Layout pattern map

| Template | Mobile | Tablet | Desktop / wide | Key rules |
| --- | --- | --- | --- | --- |
| App shell | Top bar + off-canvas navigation | Collapsible sidebar | Persistent sidebar + top bar | Keep location and active state when the nav changes shape |
| Dashboard | 1 column, stacked summaries | 2 columns | 3–4 columns with a 12-column grid | Use `minmax(0, 1fr)`; cap chart height; avoid fixed card heights |
| List + detail | List, then detail as a full screen | List with detail panel | List and detail side by side | Preserve selection and back behavior; do not lose scroll position |
| Table + filters | Card/list fallback; filters in a sheet | Scrollable table or hidden low-priority columns | Full table with sticky header | Keep the same data and actions in the fallback |
| Form | Single column, labels above, full-width actions | 1–2 columns | 2 columns with a grouped summary | Keep errors next to fields; never place labels beside inputs on mobile |
| Settings | Stacked sections with full-row controls | Stacked or 2 columns | Sidebar sections + content | Keep the save action reachable on every tier |
| Authentication | Single column, centered, no app shell | Single column | Centered card with a max width | Never require horizontal scrolling; support password managers |
| Empty and error | Full-width message + primary action | Same | Same, within the content measure | Use the same shell; do not drop navigation |

## Breakpoints

Use mobile-first `min-width` queries. The values are starting points; keep them consistent across the product.

| Tier | Min width | Typical device | Columns | Side margin | Gutter | Max content |
| --- | --- | --- | --- | --- | --- | --- |
| Mobile | 0 | Phone | 4 | 16px | 16px | 100% |
| Tablet | 768px / 48rem | Tablet, small laptop | 8 | 24px | 24px | 768px |
| Desktop | 1024px / 64rem | Laptop, desktop | 12 | 32px | 24px | 1280px |
| Wide | 1280px / 80rem | Large desktop | 12 | 40px | 32px | 1536px |

Optional upper breakpoint: `1536px / 96rem` for very wide canvases. Do not add a breakpoint without a layout problem that needs it.

Rules:

- Design at `320px` first, then enhance at `768px`, `1024px`, and `1280px`.
- No horizontal scrolling at `320px`, except an intentionally scrollable data table.
- Keep body text between `45ch` and `75ch`; widen the container, not the paragraph.
- Use fluid spacing and type with `clamp()` only when it preserves the token scale at the tested widths.
- Respect safe areas on mobile: `env(safe-area-inset-*)` for fixed bars, sheets, and toasts.
- Test at `200%` zoom and in portrait and landscape.

## Grid formula

For a centered container:

```text
content = min(maxContent, viewport - 2 * sideMargin)
column  = (content - (columns - 1) * gutter) / columns
```

Example at `1280px`: `content = 1280 - 80 = 1200px`; with 12 columns and 32px gutters, `column = (1200 - 352) / 12 = 70.67px`.

Rules:

- Use the grid for page-level layout; components use their own internal spacing tokens.
- Align cards, forms, and content blocks to column boundaries; avoid arbitrary pixel offsets.
- Use `minmax(0, 1fr)` for grid tracks so long content can shrink without overflow.
- Collapse from 12 to 8 to 4 columns; do not invent a 6-column tier unless the product needs it.
- Prefer CSS Grid for two-dimensional layout and Flexbox for one-dimensional alignment.

## Container queries

Use container queries when a component’s available width differs from the viewport, such as a card in a sidebar or a table in a split pane.

- Name containers explicitly: `container-type: inline-size; container-name: card;`.
- Set component breakpoints from the component’s content needs, not the page breakpoints.
- Provide a viewport-query fallback for older browsers.
- Do not use container queries to hide required content; reflow it.

## Component adaptation matrix

| Component | Mobile | Tablet | Desktop / wide | Rules |
| --- | --- | --- | --- | --- |
| Button | Auto width; full-width in forms and narrow panels | Auto width | Auto width | Keep the 44px target; stack button groups; never truncate the label |
| Icon Button | 44×44px minimum | 44×44px | 40–44px | Icon-only needs an accessible name and tooltip; do not shrink below the minimum target |
| Input | Full-width; label above; help/error below | Full-width or 2-column form | 1–2 columns | Use at least 16px text on mobile to avoid browser zoom; never place labels beside fields on narrow screens |
| Select | Full-width; native picker where possible | Full-width | Fixed or fluid width | Cap menu height and keep the selected value visible; searchable on desktop |
| Checkbox | Full-row tap target | Full-row tap target | Compact row | Keep the 44px row target; the label is part of the target |
| Radio Group | Vertical stack | Vertical or 2 columns | Horizontal if labels are short | Wrap rather than clip; show all options without scrolling |
| Switch | Full-row label | Full-row label | Compact row | Use for immediate on/off settings, not destructive confirmations; keep the 44px target |
| Badge | Inline; wrap with text | Inline | Inline | Never rely on color alone; truncate with an accessible full label |
| Card | 1 column | 2 columns | 3–4 columns | Full-width action on mobile; keep media aspect ratio; avoid hover-only actions |
| Modal | Full-screen sheet | Centered dialog | Centered dialog | Sticky header/footer; 44px close target; trap focus; lock background scroll |
| Toast | Top center below the safe area | Top center | Bottom right | Stack with a limit; errors persist until dismissed; use `aria-live` |
| Tabs | Horizontal scroll with edge fade | Fit or scroll | Fit | Never wrap into multiple rows; keep the active tab visible; 44px height |

### Data Table fallback

Data tables are not one of the 12 core components, but they need an explicit rule.

- Desktop and wide: show the full table with a sticky header and aligned numeric columns.
- Tablet: hide low-priority columns or allow horizontal scroll with a sticky first column.
- Mobile: prefer a card/list fallback using a definition list. If the table must remain, allow horizontal scroll, freeze the first column, and never squeeze columns below readable width.
- Always expose the same data and actions in the fallback; do not hide required fields.
- Put row actions in an overflow menu on mobile; keep the primary action visible.
- Announce sort and filter changes; keep the table caption and headers associated.

## Testing checklist

- [ ] Layout reflows at `320px`, `768px`, `1024px`, and `1280px`.
- [ ] No horizontal scrolling except an intentional table region.
- [ ] Buttons become full-width in mobile forms and narrow panels.
- [ ] Data tables have a card fallback or a usable scroll strategy.
- [ ] Touch targets are at least 44px where practical and never below 24px.
- [ ] Text remains readable at `200%` zoom.
- [ ] Modals become sheets on mobile and remain keyboard operable.
- [ ] Tabs scroll on mobile and keep the active tab visible.
- [ ] Toasts respect safe areas and do not cover primary actions.
- [ ] Container-query components reflow correctly inside sidebars and split panes.
