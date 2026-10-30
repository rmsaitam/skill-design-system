# Accessibility Baseline

Target WCAG 2.1 Level AA unless the user explicitly requires AAA or a local regulation. Accessibility is a design-system gate, not a component-by-component afterthought. Every token, component, and documentation example must pass this baseline.

## WCAG 2.1 AA matrix

| ID | Criterion | Requirement | Design system rule | Verification |
| --- | --- | --- | --- | --- |
| A11Y-001 | 1.4.3 Contrast (Minimum) | Normal text has at least 4.5:1; large text has at least 3:1 | Verify every semantic foreground/background pair in every theme | Automated contrast script and manual review |
| A11Y-002 | 1.4.11 Non-text Contrast | UI components, graphical objects, and focus indicators have at least 3:1 against adjacent colors | Control borders, icons, checkmarks, and focus rings use tokens that pass 3:1 | Contrast script and visual review |
| A11Y-003 | 2.1.1 Keyboard | All functionality is operable through a keyboard | Every interactive component supports Tab, Shift+Tab, Enter, Space, Escape, and arrow keys where applicable | Keyboard-only test |
| A11Y-004 | 2.1.2 No Keyboard Trap | Focus can move away from every component | Modals trap focus intentionally and release it on close; no other component traps focus | Keyboard-only test |
| A11Y-005 | 2.4.3 Focus Order | Focus order preserves meaning and operability | DOM order matches visual order; do not use positive `tabindex` | Keyboard and screen-reader test |
| A11Y-006 | 2.4.7 Focus Visible | Every keyboard-operable element has a visible focus indicator | Use a 2px focus ring with a 2px offset; never remove the outline without a replacement | Visual and keyboard test |
| A11Y-007 | 2.4.11 Focus Not Obscured (Minimum) | Focused elements are not entirely hidden by sticky headers, footers, or overlays | Account for sticky regions when scrolling focus into view | Keyboard test with sticky UI |
| A11Y-008 | 2.5.8 Target Size (Minimum) | Pointer targets are at least 24x24 CSS px, or have equivalent spacing | Prefer 44x44 CSS px; never go below 24x24 without spacing | Measurement and touch test |
| A11Y-009 | 1.4.4 Resize Text | Text can be resized to 200% without loss of content or functionality | Use relative units; test at 200% zoom | Browser zoom test |
| A11Y-010 | 1.4.10 Reflow | Content reflows at 320 CSS px without two-dimensional scrolling | Design mobile-first; allow horizontal scroll only for data tables | Viewport test at 320px and 400% zoom |
| A11Y-011 | 1.4.1 Use of Color | Color is not the only visual means of conveying information | Pair color with text, icon, shape, or pattern | Grayscale and color-blind simulation |
| A11Y-012 | 1.4.12 Text Spacing | Content remains usable when line height, paragraph spacing, letter spacing, and word spacing are increased | Avoid fixed-height text containers | Text-spacing bookmarklet |
| A11Y-013 | 2.3.1 Three Flashes or Below | No content flashes more than three times per second | Cap motion and flashing in the motion tokens | Motion review |
| A11Y-014 | 2.3.3 Animation from Interactions | Motion triggered by interaction can be disabled | Respect `prefers-reduced-motion: reduce` | OS reduced-motion test |
| A11Y-015 | 3.3.1 Error Identification | Errors are identified in text | Every error has a text message, not only a red border | Form review |
| A11Y-016 | 3.3.2 Labels or Instructions | Inputs have labels or instructions | Every input has a visible label; placeholders are not labels | Form review |
| A11Y-017 | 3.3.3 Error Suggestion | Error messages suggest a correction when known | Error copy explains how to fix the problem | Content review |
| A11Y-018 | 4.1.2 Name, Role, Value | Every UI component exposes name, role, value, and state | Use native HTML first; add ARIA only when native semantics are insufficient | Accessibility tree inspection |
| A11Y-019 | 4.1.3 Status Messages | Status messages are announced without moving focus | Use `role="status"` or `aria-live="polite"` for toasts and async feedback | Screen-reader test |
| A11Y-020 | 2.5.7 Dragging Movements | Dragging has a single-pointer alternative | Provide buttons or keyboard controls for drag interactions | Pointer and keyboard test |

## Contrast thresholds

| Content | Minimum ratio | Notes |
| --- | --- | --- |
| Normal text below 24px, or below 18.66px bold | 4.5:1 | Body, labels, links, placeholder text, error text |
| Large text at least 24px, or at least 18.66px bold | 3:1 | Headings and display text |
| UI component boundaries and states | 3:1 | Input borders, checkbox borders, toggle tracks, selected states |
| Graphical objects required to understand content | 3:1 | Icons, chart lines, meaningful illustrations |
| Focus indicator | 3:1 | Against adjacent colors; use a 2px ring with a 2px offset |
| Disabled controls | Exempt | Still aim for 3:1 readability; never rely on low contrast alone to signal disabled |
| Decorative content | Exempt | Mark as decorative and hide from assistive technology |

Rules:

- Verify the actual token pair, not a screenshot or an approximation.
- Verify every theme separately.
- A border that is the only visual boundary of an input must meet 3:1.
- Placeholder text is text and must meet 4.5:1.
- Error, success, and warning states must not rely on hue alone.
- Link text inside body copy must meet 4.5:1 and be distinguishable from surrounding text by more than color, or have a persistent underline.

## Contrast pair matrix

Record one row per pair in `DESIGN-SYSTEM.md`:

| ID | Foreground token | Background token | Usage | Required | Measured | Result |
| --- | --- | --- | --- | --- | --- | --- |
| A11Y-C01 | `color.foreground.default` | `color.background.default` | Body text | 4.5:1 | 19.45:1 | Pass |
| A11Y-C02 | `color.foreground.muted` | `color.background.default` | Secondary text | 4.5:1 | 4.84:1 | Pass |
| A11Y-C03 | `color.foreground.brand` | `color.background.default` | Links and brand text | 4.5:1 | 6.71:1 | Pass |
| A11Y-C04 | `color.action.primary.foreground.default` | `color.action.primary.background.default` | Primary button label | 4.5:1 | 5.18:1 | Pass |
| A11Y-C05 | `color.foreground.danger` | `color.background.default` | Error text | 4.5:1 | 4.84:1 | Pass |
| A11Y-C06 | `color.border.default` | `color.background.default` | Input and control border | 3:1 | 4.84:1 | Pass |
| A11Y-C07 | `color.focus.ring` | `color.background.default` | Focus indicator | 3:1 | 3.68:1 | Pass |
| A11Y-C08 | `color.foreground.inverse` | `color.background.inverse` | Inverse text | 4.5:1 | 19.45:1 | Pass |

The measured values above are examples from the starter tokens. Replace them with the measured values from the project's `design.json`. The validator recomputes the key pairs and fails when a ratio is below the threshold.

## Keyboard and focus

### Global rules

- All interactive elements are reachable with `Tab` in a logical order.
- `Shift+Tab` reverses the order.
- `Enter` activates buttons, links, and submit actions.
- `Space` activates buttons, checkboxes, switches, and toggles.
- `Escape` closes menus, popovers, dialogs, and drawers.
- Arrow keys move within composite widgets: radio groups, tabs, menus, listboxes, and sliders.
- Do not use positive `tabindex` values.
- Do not remove the focus outline unless a visible replacement is provided.
- Focus must not be obscured by sticky headers, footers, or cookie banners.
- Provide a skip link to the main content.
- After closing an overlay, return focus to the element that opened it.
- When content is removed, move focus to a logical next element, not to the top of the page.

### Component patterns

| Component | Keyboard behavior |
| --- | --- |
| Button | `Enter` and `Space` activate; focus ring visible; loading keeps focus and exposes `aria-busy` |
| Icon Button | Same as Button; requires an accessible name via visible text or `aria-label` |
| Input | `Tab` moves in and out; text selection and editing use native behavior; error text is linked with `aria-describedby` |
| Select | `Enter`, `Space`, or `ArrowDown` opens; arrows move; `Enter` selects; `Escape` closes; type-ahead is recommended |
| Checkbox | `Space` toggles; label is clickable; indeterminate state is exposed with `aria-checked="mixed"` |
| Radio Group | Arrow keys move and select within the group; `Tab` moves into and out of the group |
| Switch | `Space` or `Enter` toggles; exposes `role="switch"` and `aria-checked` |
| Badge | Non-interactive by default; if interactive, use a button or link, not a badge |
| Card | If interactive, the whole card is a link or button with one accessible name; avoid nested interactive elements |
| Modal | Focus moves into the dialog; focus is trapped; `Escape` closes; focus returns to the trigger; background is inert |
| Toast | Announced with `role="status"` or `aria-live="polite"`; critical errors use `role="alert"`; pause on hover and focus |
| Tabs | Arrow keys move between tabs; `Home` and `End` jump to first and last; `Tab` moves into the panel |

## Focus indicator specification

```css
:focus-visible {
  outline: 2px solid var(--semantic-color-focus-ring);
  outline-offset: 2px;
  border-radius: var(--semantic-radius-control);
}
```

Rules:

- Use `:focus-visible` for pointer users and keyboard users; do not hide focus for keyboard users.
- The ring must meet 3:1 against the adjacent background and the component.
- If the component sits on a colored background, use a two-color ring or an offset ring.
- Do not animate the ring in a way that reduces its visibility.
- Ensure the ring is not clipped by `overflow: hidden` on the parent.

## Forms

- Every input has a visible label associated with `for` and `id`.
- Placeholders are examples or hints, never labels.
- Required fields are marked in text and with the `required` attribute.
- Helper text is linked with `aria-describedby`.
- Error text is specific, in text, and linked with `aria-describedby`.
- Invalid fields expose `aria-invalid="true"`.
- Error summaries link to the fields they describe.
- Do not validate on every keystroke in a way that interrupts typing; validate on blur or submit.
- Group related controls with `fieldset` and `legend`.
- Preserve user input when validation fails.
- Announce async validation results with a live region.
- Support autofill with the correct `autocomplete` values.
- Use `inputmode` for numeric and telephone inputs.

## Touch and pointer

- Prefer a 44x44 CSS px target for all interactive controls.
- The WCAG 2.1 AA minimum is 24x24 CSS px, or equivalent spacing.
- Keep at least 8px between adjacent targets.
- Do not place destructive actions next to primary actions without separation.
- Support both pointer and keyboard interaction.
- Provide a single-pointer alternative for drag interactions.
- Ensure hover-only information is also available on focus and touch.

## Color independence

- Pair error, success, and warning colors with an icon and text.
- Do not use color as the only way to indicate selection, status, or required fields.
- Use patterns, labels, or shapes in charts.
- Test the UI in grayscale and with common color-vision deficiencies.
- Ensure links in body text are distinguishable without color alone.

## Motion and animation

- Respect `prefers-reduced-motion: reduce`.
- Remove parallax, large transforms, and autoplay animations in reduced-motion mode.
- Keep essential motion short and avoid motion that could trigger vestibular symptoms.
- Do not flash more than three times per second.
- Pause, stop, or hide moving content that lasts more than five seconds.
- Do not use motion as the only feedback for an action.

## Content and reflow

- Body text is at least 16px on web.
- Line height is at least 1.5 for body text.
- Paragraph spacing is at least 2 times the font size.
- Letter spacing is at least 0.12 times the font size.
- Word spacing is at least 0.16 times the font size.
- Content reflows at 320 CSS px without horizontal scrolling.
- Text can resize to 200% without loss of content or functionality.
- Do not use fixed-height containers for text.
- Support RTL layouts when required, including icons with direction.

## Screen readers and semantics

- Prefer native HTML elements over ARIA.
- Use landmarks: `header`, `nav`, `main`, `aside`, `footer`.
- Use one `h1` per page and a logical heading order.
- Give every image an appropriate `alt`; use `alt=""` for decorative images.
- Give every icon-only control an accessible name.
- Expose state with `aria-expanded`, `aria-selected`, `aria-checked`, `aria-pressed`, `aria-current`, and `aria-busy`.
- Do not use `aria-hidden="true"` on focusable elements.
- Hide decorative icons from assistive technology.
- Ensure the accessibility tree matches the visual structure.
- Test with at least one screen reader: NVDA or JAWS on Windows, VoiceOver on macOS or iOS, TalkBack on Android.

## Testing

### Automated

- Contrast checks on every semantic pair and theme.
- Lint rules for alt text, labels, and ARIA usage.
- Unit tests for keyboard behavior and focus management.
- Axe or equivalent checks in component tests and Storybook.
- Visual regression tests for focus, error, disabled, and loading states.

### Manual

- Keyboard-only walkthrough of every component and page.
- Screen-reader walkthrough of the primary journey.
- 200% zoom and 320px reflow test.
- Reduced-motion test.
- Grayscale and color-blind simulation.
- Touch-target measurement on mobile.
- RTL review when applicable.

### Release gate

Do not release a component that:

- fails a contrast pair;
- has no visible focus state;
- cannot be operated by keyboard;
- has no accessible name;
- relies on color alone;
- traps focus outside a modal;
- hides content at 200% zoom;
- ignores reduced motion.

## Severity for accessibility findings

| Severity | Definition | Examples |
| --- | --- | --- |
| High | Blocks a core task for assistive-technology users or creates a legal risk | Keyboard trap, missing accessible name, contrast below 3:1 on essential UI, modal without focus management |
| Medium | Causes confusion or significant friction, but a workaround exists | Missing focus style, color-only error, inconsistent target size, missing live region |
| Low | Best-practice gap with limited direct impact | Inconsistent focus offset, missing documentation, minor order issue |

Record evidence, affected component or token, user impact, remediation, and verification for every finding.
