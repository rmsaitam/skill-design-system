# Components Catalog

This is the v1.0 component set. Each specification is a contract: anatomy, variants, states, usage, accessibility, tokens, content, and do/don't guidance. Keep the component count at 12 unless the user records a swap.

Swap candidates for product-specific needs:

- Replace `Tabs` with `Data Table` for data-heavy B2B products.
- Replace `Select` with `Bottom Sheet` for mobile-first products.
- Replace `Card` with `List Item` for dense mobile lists.
- Replace `Toast` with `Banner` for persistent inline messaging.

## Responsive defaults

All components use the breakpoints, columns, margins, and gutters in [responsive-layout.md](responsive-layout.md). At minimum:

- Buttons become full-width in mobile forms and narrow panels.
- Cards stack to one column on mobile, two on tablet, and three or four on desktop.
- Modals become full-screen sheets on mobile.
- Tabs scroll horizontally on mobile and keep the active tab visible.
- Toasts move to the top center on mobile and respect safe areas.
- Data tables use a card/list fallback or a scrollable region with a sticky first column.

Document the component-specific behavior in the artifact's component section.

## CMP-001: Button

**Purpose:** Trigger an action or submit a form. The primary action primitive.

**Anatomy:**

- `root` (`<button>`)
- `label` (required)
- `leading icon` (optional)
- `trailing icon` (optional)
- `spinner` (loading only)
- `focus ring`

**Variants:**

- `primary`: the main action on a surface. Use once per view or section.
- `secondary`: a supporting action next to a primary action.
- `ghost`: a low-emphasis action in toolbars, cards, and tables.
- `danger`: a destructive action. Always pair with confirmation when irreversible.
- `link`: an action styled as a link; use for navigation-like actions inside text.
- Sizes: `sm` (32px), `md` (40px), `lg` (48px). Use `md` by default.
- Full width: only on mobile forms and narrow panels.

**States:**

| State | Behavior |
| --- | --- |
| Default | Resting state |
| Hover | Background or border changes; no layout shift |
| Active | Slightly darker or compressed |
| Focus | 2px focus ring, 2px offset, 3:1 minimum |
| Disabled | Non-interactive, `disabled` or `aria-disabled` with explanation |
| Loading | Spinner replaces or precedes the label; width stays stable; `aria-busy="true"` |
| Error | N/A; use a form-level error or inline message |

**Usage:**

- Use for actions that change state or submit data.
- Use one `primary` per view or section.
- Use `danger` only for destructive actions with a clear label.
- Do not use a Button for navigation to another page; use a link.
- Do not use a Button for a toggle; use Switch, Checkbox, or a segmented control.
- Do not put a Button inside a link or a link inside a Button.
- Do not use icon-only buttons without an accessible name; use Icon Button.

**Accessibility:**

- Render a native `<button>` with an explicit `type`.
- Keep the label visible; do not rely on an icon alone.
- Expose loading with `aria-busy="true"` and keep focus on the button.
- For disabled buttons that need an explanation, use `aria-disabled="true"` and keep the button focusable, or place the explanation next to the button.
- Minimum target: 44x44 CSS px; for `sm`, add spacing.
- The focus ring must be visible on all backgrounds.
- Do not remove the outline without a replacement.

**Tokens:**

- `component.button.{variant}.background.{state}`
- `component.button.{variant}.foreground.{state}`
- `component.button.{variant}.border.{state}`
- `component.button.radius`
- `component.button.height.{size}`
- `component.button.padding.{size}`
- `semantic.color.focus.ring`
- `semantic.motion.duration.fast`

**Content:**

- Use sentence case: "Save changes", not "SAVE CHANGES".
- Start with a verb: "Create account", "Delete project".
- Keep labels short: 1 to 3 words.
- For destructive actions, name the object: "Delete project", not "Yes".
- Loading label: keep the original label or use "Saving..." with `aria-busy`.

**Do / Don't:**

- Do: "Save changes" as the primary action.
- Don't: two primary buttons side by side.
- Do: "Delete project" in a danger button with a confirmation dialog.
- Don't: "OK" for a destructive action.

## CMP-002: Icon Button

**Purpose:** A compact action represented by an icon, used in toolbars, headers, tables, and cards.

**Anatomy:**

- `root` (`<button>`)
- `icon` (required)
- `accessible name` (required, via visible label or `aria-label`)
- `tooltip` (recommended for unfamiliar icons)
- `focus ring`

**Variants:**

- `ghost`: default for toolbars and dense surfaces.
- `solid`: high-emphasis compact action.
- `outline`: bordered action on busy backgrounds.
- `danger`: destructive compact action.
- Sizes: `sm` (32px), `md` (40px), `lg` (48px). Use `md` by default.

**States:**

| State | Behavior |
| --- | --- |
| Default | Resting state |
| Hover | Background or border changes; tooltip may appear |
| Active | Slightly darker or compressed |
| Focus | 2px focus ring, 2px offset |
| Disabled | Non-interactive, accessible name preserved |
| Loading | Spinner replaces the icon; width stays stable; `aria-busy="true"` |
| Error | N/A |

**Usage:**

- Use for a single, well-understood action in a compact space.
- Use when the icon is conventional: close, search, menu, edit, delete, more.
- Use a visible text label when the action is not obvious.
- Do not use for the primary action of a page.
- Do not use two icon buttons for actions that users often confuse.
- Do not use an icon-only button for a destructive action without a confirmation.

**Accessibility:**

- Always provide an accessible name with `aria-label` or visually hidden text.
- Use `aria-pressed` for toggle buttons.
- Use `aria-expanded` for buttons that open menus.
- Provide a tooltip for unfamiliar icons, but do not rely on the tooltip as the only name.
- Minimum target: 44x44 CSS px.
- Keep the focus ring visible.

**Tokens:**

- `component.icon-button.{variant}.background.{state}`
- `component.icon-button.{variant}.foreground.{state}`
- `component.icon-button.size.{size}`
- `component.icon-button.radius`
- `semantic.color.focus.ring`

**Content:**

- Accessible name is a verb phrase: "Close dialog", "Search", "Open menu".
- Do not use the icon name as the accessible name: "X" is not a name.
- Tooltip text matches the accessible name or adds context.

**Do / Don't:**

- Do: a search icon button with `aria-label="Search"`.
- Don't: a trash icon button with no label.
- Do: a "More actions" button with `aria-haspopup="menu"`.
- Don't: a primary "Create" action as an icon-only button.

## CMP-003: Input

**Purpose:** Collect a single line of text or a single value from the user.

**Anatomy:**

- `field` wrapper
- `label` (required, visible)
- `input` (`<input>`)
- `prefix` (optional)
- `suffix` (optional)
- `helper text` (optional)
- `error text` (conditional)
- `character counter` (optional)
- `required indicator` (conditional)
- `focus ring`

**Variants:**

- Text, email, password, number, search, telephone, URL.
- With prefix or suffix (currency, unit, domain).
- With clear button (search).
- Sizes: `sm` (32px), `md` (40px), `lg` (48px).
- Inline and full width.

**States:**

| State | Behavior |
| --- | --- |
| Default | Resting state |
| Hover | Border or background change |
| Focus | Focus ring; label remains visible |
| Filled | Value present; clear button may appear |
| Disabled | Non-interactive; value remains readable |
| Readonly | Focusable and copyable, not editable |
| Loading | N/A for the input itself; show async validation separately |
| Error | Error border, icon, and text; `aria-invalid="true"` |

**Usage:**

- Use for free-form, single-line input.
- Use a Select for a bounded list, a Checkbox for a boolean, and a Radio Group for mutually exclusive options.
- Use a Textarea for multi-line text.
- Do not use a placeholder as the label.
- Do not use an Input for a date if a date picker or structured input is available.
- Do not validate on every keystroke in a way that interrupts typing.

**Accessibility:**

- Associate the label with `for` and `id`.
- Link helper and error text with `aria-describedby`.
- Set `aria-invalid="true"` when invalid.
- Use the correct `type`, `inputmode`, and `autocomplete`.
- Mark required fields with the `required` attribute and a visible indicator.
- Do not use color alone for errors; add an icon and text.
- Preserve input on validation failure.
- Announce async validation with a live region.
- Minimum target: 44px height for touch.

**Tokens:**

- `component.input.background.{state}`
- `component.input.foreground.{state}`
- `component.input.placeholder`
- `component.input.border.{state}`
- `component.input.radius`
- `component.input.height.{size}`
- `component.input.padding.{size}`
- `semantic.color.focus.ring`
- `semantic.color.foreground.danger`

**Content:**

- Labels are nouns or short noun phrases: "Email address", "Company name".
- Helper text explains format or constraints before the error occurs.
- Error text explains what is wrong and how to fix it: "Enter an email in the format name@example.com".
- Do not use "Invalid input" without a reason.
- Placeholder examples are short and do not repeat the label.

**Do / Don't:**

- Do: a visible "Email address" label with `autocomplete="email"`.
- Don't: a placeholder-only field.
- Do: "Enter a date in the past" for a birth date error.
- Don't: "Error" as the only message.

## CMP-004: Select / Dropdown

**Purpose:** Choose one or more options from a bounded list without leaving the page.

**Anatomy:**

- `field` wrapper
- `label` (required)
- `trigger` (`<button>` or native `<select>`)
- `value` or placeholder
- `chevron` icon
- `popover` / listbox
- `option` items
- `search` field (optional, for long lists)
- `helper text` and `error text`
- `focus ring`

**Variants:**

- Native select (recommended for simple forms).
- Custom single-select listbox.
- Multi-select with tags.
- Searchable combobox.
- Sizes: `sm`, `md`, `lg`.

**States:**

| State | Behavior |
| --- | --- |
| Default | Placeholder or selected value |
| Hover | Trigger background or border change |
| Focus | Focus ring on the trigger |
| Open | Popover visible; trigger exposes `aria-expanded="true"` |
| Selected | Option shows a check or selected style |
| Disabled | Non-interactive |
| Loading | Show a loading row in the popover; keep the trigger stable |
| Error | Error border and text; `aria-invalid="true"` |

**Usage:**

- Use when the list is bounded and the user does not need to see all options at once.
- Use a Radio Group when there are fewer than about five options and visibility matters.
- Use a Combobox when the list is long or searchable.
- Do not use a Select for navigation; use a menu or links.
- Do not use a custom Select when a native select meets the need.
- Do not hide the label inside the trigger.

**Accessibility:**

- Prefer a native `<select>` for simple cases.
- For a custom listbox, implement the WAI-ARIA listbox pattern: `role="listbox"`, `role="option"`, `aria-selected`, `aria-activedescendant`.
- `Enter`, `Space`, or `ArrowDown` opens; arrows move; `Enter` selects; `Escape` closes.
- Support type-ahead.
- Return focus to the trigger on close.
- Expose `aria-expanded` and `aria-controls`.
- Do not use a div as a button without keyboard support.
- Minimum target: 44px height.

**Tokens:**

- `component.select.trigger.background.{state}`
- `component.select.trigger.foreground.{state}`
- `component.select.trigger.border.{state}`
- `component.select.menu.background`
- `component.select.option.background.{state}`
- `component.select.option.foreground.{state}`
- `component.select.radius`
- `semantic.elevation.surface.2`
- `semantic.color.focus.ring`

**Content:**

- Label describes the choice: "Country", "Plan".
- The placeholder is an instruction, not a value: "Select a country".
- Option labels are short and parallel: "Starter", "Growth", "Enterprise".
- Do not use "All" unless the list supports an all-options state.

**Do / Don't:**

- Do: a native select for a country list with a visible label.
- Don't: a custom dropdown with no keyboard support.
- Do: a searchable combobox for a list of 100+ items.
- Don't: a Select for two options; use a Radio Group or Switch.

## CMP-005: Checkbox

**Purpose:** Select one or more independent options, or acknowledge a statement.

**Anatomy:**

- `root` label wrapper
- `box` (control)
- `check` or `dash` (indeterminate)
- `label` (required)
- `helper text` (optional)
- `error text` (conditional)
- `focus ring`

**Variants:**

- Single checkbox.
- Checkbox group with `fieldset` and `legend`.
- Indeterminate parent for partial selection.
- Sizes: `sm`, `md`.

**States:**

| State | Behavior |
| --- | --- |
| Default | Unchecked |
| Hover | Border or background change |
| Focus | Focus ring on the control |
| Checked | Checkmark visible |
| Indeterminate | Dash visible; `aria-checked="mixed"` |
| Disabled | Non-interactive; state remains visible |
| Loading | N/A; disable the group while saving |
| Error | Error text; group-level message; `aria-invalid` on the group |

**Usage:**

- Use for independent choices where more than one can be selected.
- Use a single checkbox for acknowledgment: "I agree to the terms".
- Use a Switch for an immediate on/off setting.
- Use a Radio Group for mutually exclusive choices.
- Do not use a Checkbox for an action that takes effect immediately.
- Do not use a Checkbox to trigger navigation.

**Accessibility:**

- Use a native `<input type="checkbox">`.
- The label is clickable and associated with the input.
- Group related checkboxes with `fieldset` and `legend`.
- Expose indeterminate with `aria-checked="mixed"` and a visible dash.
- Do not use color alone to show selection.
- Minimum target: 44x44 CSS px; the label can provide the target area.
- Error messages are linked to the group.

**Tokens:**

- `component.checkbox.background.{state}`
- `component.checkbox.border.{state}`
- `component.checkbox.check`
- `component.checkbox.radius`
- `component.checkbox.size.{size}`
- `semantic.color.focus.ring`

**Content:**

- Labels are statements or nouns: "Send me product updates".
- Avoid double negatives.
- Keep labels short and parallel in a group.
- Error text explains the group requirement: "Select at least one notification".

**Do / Don't:**

- Do: "I agree to the terms of service" as a single checkbox.
- Don't: a checkbox that immediately saves a setting; use a Switch.
- Do: a parent checkbox with an indeterminate state for partial selection.
- Don't: a checkbox group without a legend.

## CMP-006: Radio Group

**Purpose:** Choose exactly one option from a small, visible set.

**Anatomy:**

- `fieldset`
- `legend` (required)
- `radio` items
- `control` and `label` per item
- `helper text` (optional)
- `error text` (conditional)
- `focus ring`

**Variants:**

- Vertical (default).
- Horizontal for short labels.
- Card radio for rich options with descriptions.
- Sizes: `sm`, `md`.

**States:**

| State | Behavior |
| --- | --- |
| Default | Unselected |
| Hover | Border or background change |
| Focus | Focus ring on the selected or first radio |
| Selected | Filled dot and selected style |
| Disabled | Non-interactive; selected state remains visible |
| Loading | N/A; disable the group while saving |
| Error | Error text; group-level message |

**Usage:**

- Use for mutually exclusive choices with about two to five options.
- Use a Select when the list is long or space is constrained.
- Use a Checkbox for independent choices.
- Do not use a Radio Group for a binary on/off setting; use a Switch or a single Checkbox.
- Do not pre-select an option unless there is a safe, obvious default.

**Accessibility:**

- Use native `<input type="radio">` with the same `name`.
- Group with `fieldset` and `legend`.
- Arrow keys move and select within the group; `Tab` moves into and out of the group.
- The label is clickable.
- Do not use color alone to show selection.
- Error messages are linked to the group.
- Minimum target: 44x44 CSS px.

**Tokens:**

- `component.radio.background.{state}`
- `component.radio.border.{state}`
- `component.radio.dot`
- `component.radio.size.{size}`
- `semantic.color.focus.ring`

**Content:**

- Legend describes the choice: "Billing period".
- Options are short and parallel: "Monthly", "Yearly".
- Include the trade-off in helper text when needed: "Save 20% with yearly billing".
- Do not use "Option 1" or "Yes/No" when a clearer label exists.

**Do / Don't:**

- Do: "Monthly" and "Yearly" under the legend "Billing period".
- Don't: a Radio Group with 20 options; use a Select.
- Do: a safe default when the user must choose now.
- Don't: a pre-selected destructive or paid option without consent.

## CMP-007: Switch

**Purpose:** Toggle a setting that takes effect immediately.

**Anatomy:**

- `root` label wrapper
- `track`
- `thumb`
- `label` (required)
- `helper text` (optional)
- `focus ring`

**Variants:**

- Default.
- With label on the left or right.
- Sizes: `sm`, `md`.
- Loading state while saving.

**States:**

| State | Behavior |
| --- | --- |
| Default | Off |
| Hover | Track or thumb change |
| Focus | Focus ring on the control |
| On | Track and thumb in the on position |
| Disabled | Non-interactive; state remains visible |
| Loading | Thumb shows a spinner or the control is disabled with `aria-busy` |
| Error | N/A; show a form-level message if saving fails |

**Usage:**

- Use for an immediate on/off setting, such as "Enable notifications".
- Use a Checkbox when the change requires a form submission.
- Use a Radio Group for more than two mutually exclusive options.
- Do not use a Switch for a destructive action.
- Do not use a Switch without a clear label and current state.
- Do not rely on the position alone; expose the state to assistive technology.

**Accessibility:**

- Use `role="switch"` with `aria-checked`, or a native checkbox with switch semantics.
- `Space` or `Enter` toggles.
- The label is clickable.
- The state is announced as "on" or "off".
- Do not use color alone; the thumb position and state text must also change.
- Minimum target: 44x44 CSS px.
- Announce async save failures with a live region.

**Tokens:**

- `component.switch.track.off`
- `component.switch.track.on`
- `component.switch.thumb`
- `component.switch.track.disabled`
- `component.switch.radius`
- `semantic.color.focus.ring`

**Content:**

- Labels are settings: "Email notifications", "Public profile".
- Helper text explains the consequence: "You will receive weekly summaries".
- Avoid "Enable/Disable" in the label; the switch already conveys the state.

**Do / Don't:**

- Do: "Public profile" with a helper that explains visibility.
- Don't: a Switch that deletes data immediately.
- Do: show a saving state while the setting persists.
- Don't: use a Switch for a multi-step form choice.

## CMP-008: Badge

**Purpose:** Display a compact status, count, or category.

**Anatomy:**

- `root`
- `label` (optional)
- `dot` (optional)
- `icon` (optional)
- `count` (optional)

**Variants:**

- `neutral`, `brand`, `success`, `warning`, `danger`, `info`.
- `solid`, `subtle`, `outline`.
- With dot, icon, or count.
- Sizes: `sm`, `md`.

**States:**

| State | Behavior |
| --- | --- |
| Default | Static label |
| Hover | N/A; badges are not interactive |
| Focus | N/A; badges are not focusable |
| Disabled | N/A |
| Loading | N/A |
| Error | N/A |

**Usage:**

- Use for status, counts, and categories.
- Use an inline Alert for feedback that requires reading.
- Use a Tag with a remove action for user-editable labels.
- Do not use a Badge as a button; use a Button or Tag.
- Do not use a Badge for long text.
- Do not rely on color alone; include a label or icon.

**Accessibility:**

- Badges are text, not controls.
- Ensure text contrast meets 4.5:1 for normal text and 3:1 for large text.
- If the badge conveys status, include a text label; do not use a colored dot alone.
- Hide decorative dots from assistive technology.
- If the badge is inside a link or button, ensure the accessible name remains clear.
- Do not make the badge focusable unless it is interactive.

**Tokens:**

- `component.badge.{variant}.background`
- `component.badge.{variant}.foreground`
- `component.badge.{variant}.border`
- `component.badge.radius`
- `component.badge.padding`
- `component.badge.font`

**Content:**

- Keep labels to 1 to 3 words: "Active", "Pending", "3 items".
- Use consistent casing: sentence case or uppercase, not both.
- Counts over 99 can use "99+".
- Do not use ambiguous labels: "New" can mean unread or recently created.

**Do / Don't:**

- Do: a green "Active" badge with a check icon.
- Don't: a green dot with no label.
- Do: "3 items" for a count.
- Don't: a badge that looks like a button.

## CMP-009: Card

**Purpose:** Group related content and actions into a single surface.

**Anatomy:**

- `root` container
- `media` (optional)
- `header` (optional)
- `title` (recommended)
- `description` (optional)
- `body`
- `footer` (optional)
- `actions` (optional)
- `focus ring` when interactive

**Variants:**

- `elevated`: shadow and no border.
- `outlined`: border and no shadow.
- `filled`: subtle background.
- `interactive`: whole card is a link or button.
- Sizes: `sm`, `md`, `lg`.

**States:**

| State | Behavior |
| --- | --- |
| Default | Resting state |
| Hover | Only for interactive cards; elevation or border change |
| Focus | Only for interactive cards; focus ring around the card |
| Selected | Only for selectable cards; check or border change |
| Disabled | Non-interactive; reduced emphasis |
| Loading | Skeleton blocks that match the final layout |
| Error | N/A; show an inline Alert inside the card |

**Usage:**

- Use to group related content that can stand alone.
- Use a List Item for dense, repeating rows.
- Use a Modal for focused tasks that interrupt the flow.
- Do not use a Card for page layout or as a generic container.
- Do not nest interactive elements inside an interactive card.
- Do not use a Card when a simple section with a heading is enough.

**Accessibility:**

- Use a semantic heading for the card title.
- If the whole card is interactive, use one link or button with one accessible name; do not make every element interactive.
- If the card contains multiple actions, keep the card non-interactive and make each action focusable.
- Ensure the focus ring is visible around the whole card.
- Do not use hover as the only way to reveal actions.
- Loading skeletons are hidden from assistive technology; announce loading with text.

**Tokens:**

- `component.card.background`
- `component.card.border`
- `component.card.radius`
- `component.card.padding.{size}`
- `component.card.shadow`
- `component.card.title.typography`
- `semantic.elevation.surface.1`

**Content:**

- Titles are short and specific: "Monthly revenue", not "Information".
- Descriptions add context, not repetition.
- Actions use clear verbs.
- Empty cards need an empty state with a next step.

**Do / Don't:**

- Do: a card with a heading, a short description, and one primary action.
- Don't: a card with five competing actions.
- Do: a non-interactive card with a "View details" link.
- Don't: nested links and buttons inside a fully clickable card.

## CMP-010: Modal / Dialog

**Purpose:** Focus the user on a task or decision that requires attention before continuing.

**Anatomy:**

- `overlay` / scrim
- `container` / dialog
- `header`
- `title` (required)
- `description` (optional)
- `close` button
- `body`
- `footer`
- `actions`
- `focus trap`

**Variants:**

- `dialog`: general focused task.
- `alertdialog`: confirmation or destructive action.
- `drawer`: side panel for filters or details.
- `fullscreen`: mobile or immersive task.
- Sizes: `sm` (400px), `md` (560px), `lg` (720px), `full`.

**States:**

| State | Behavior |
| --- | --- |
| Closed | Not rendered or hidden |
| Opening | Overlay fades in; dialog enters |
| Open | Focus inside; background inert |
| Loading | Actions show loading; content may show skeleton |
| Error | Inline Alert or field errors inside the dialog |
| Closing | Exit animation; focus returns to trigger |

Default, Hover, Focus, and Disabled are `N/A` for the dialog container itself; they apply to the controls inside it.

**Usage:**

- Use for a focused task, a confirmation, or content that must be seen before continuing.
- Use an Alert Dialog for destructive confirmations.
- Use a Toast for transient feedback.
- Use a Drawer for secondary content that can stay in context.
- Do not use a Modal for long, complex workflows; use a page.
- Do not stack modals.
- Do not use a Modal for information that can be inline.

**Accessibility:**

- Use `role="dialog"` and `aria-modal="true"`.
- Label the dialog with `aria-labelledby` pointing to the title.
- Describe it with `aria-describedby` when a description exists.
- Move focus to the first meaningful element or the dialog itself.
- Trap focus inside the dialog.
- `Escape` closes the dialog unless the action is irreversible and requires an explicit choice.
- Return focus to the trigger on close.
- Make the background inert with `inert` or `aria-hidden`.
- Prevent background scroll.
- The close button has an accessible name.
- For destructive actions, name the action and the object.
- Do not autofocus a destructive action.

**Tokens:**

- `component.modal.overlay`
- `component.modal.background`
- `component.modal.border`
- `component.modal.radius`
- `component.modal.shadow`
- `component.modal.max-width.{size}`
- `semantic.elevation.overlay`
- `semantic.motion.duration.slow`

**Content:**

- Titles are short and specific: "Delete project?".
- Descriptions explain the consequence: "This action cannot be undone."
- Actions are explicit: "Delete project" and "Cancel".
- Do not use "OK" and "Cancel" for a destructive action.
- Keep the primary action on the right in left-to-right layouts.

**Do / Don't:**

- Do: "Delete project?" with "Delete project" and "Cancel".
- Don't: "Are you sure?" with "Yes" and "No".
- Do: return focus to the "Delete" button after cancel.
- Don't: open a modal from inside a modal.

## CMP-011: Toast / Alert

**Purpose:** Communicate transient feedback or an inline status message.

**Anatomy:**

- `root`
- `icon` (recommended)
- `title` (optional)
- `description`
- `action` (optional)
- `close` button (optional)
- `progress` (optional, for auto-dismiss)

**Variants:**

- `toast`: transient, floating feedback.
- `inline alert`: persistent message inside the page.
- `info`, `success`, `warning`, `danger`.
- With action: "Undo", "Retry", "View".
- Sizes: `sm`, `md`.

**States:**

| State | Behavior |
| --- | --- |
| Entering | Slide or fade in |
| Visible | Readable; timer running for toast |
| Paused | Timer paused on hover or focus |
| Exiting | Fade or slide out |
| Action | Action executes and the toast dismisses |
| Error | Danger variant; may persist until dismissed |

Default is the visible resting state. Hover and Focus pause the timer. Disabled and Loading are `N/A` for the toast container.

**Usage:**

- Use a Toast for non-blocking, transient feedback: "Changes saved".
- Use an inline Alert for persistent status that belongs to the page.
- Use a Modal for a decision that blocks progress.
- Do not use a Toast for critical errors that require action; use an Alert or Dialog.
- Do not auto-dismiss an error that the user must read.
- Do not stack more than three toasts.

**Accessibility:**

- Use `role="status"` or `aria-live="polite"` for non-critical messages.
- Use `role="alert"` or `aria-live="assertive"` for critical errors, sparingly.
- Do not move focus to a toast.
- Pause the timer on hover and focus.
- Provide a close button for persistent messages.
- Ensure the message is readable for at least five seconds or until dismissed.
- Do not rely on color alone; include an icon and text.
- The action is keyboard accessible.

**Tokens:**

- `component.toast.{variant}.background`
- `component.toast.{variant}.foreground`
- `component.toast.{variant}.border`
- `component.toast.{variant}.icon`
- `component.toast.radius`
- `component.toast.shadow`
- `semantic.elevation.surface.3`
- `semantic.motion.duration.normal`

**Content:**

- Lead with the outcome: "Changes saved", "Could not save changes".
- Errors explain the cause and the next step: "Check your connection and try again".
- Actions are short: "Undo", "Retry".
- Do not use "Success!" alone; say what succeeded.
- Keep the message under two lines when possible.

**Do / Don't:**

- Do: "Changes saved" with an "Undo" action.
- Don't: "Error" with no explanation.
- Do: an inline Alert for a failed payment that needs attention.
- Don't: a toast that disappears before it can be read.

## CMP-012: Tabs

**Purpose:** Switch between related views in the same context without leaving the page.

**Anatomy:**

- `tablist`
- `tab` items
- `indicator`
- `tabpanel`
- `focus ring`

**Variants:**

- `underline`: default for page-level sections.
- `pill`: compact segmented control.
- `segmented`: mutually exclusive view switch.
- Sizes: `sm`, `md`.

**States:**

| State | Behavior |
| --- | --- |
| Default | Inactive tab |
| Hover | Text or background change |
| Focus | Focus ring on the active tab |
| Active | Selected tab and visible panel |
| Disabled | Non-interactive; remains visible |
| Loading | Show a skeleton in the panel; keep the tab stable |
| Error | N/A; show an inline Alert in the panel |

**Usage:**

- Use to switch between related views at the same level.
- Use a Select or a menu for navigation between pages.
- Use a segmented control for a compact binary or ternary switch.
- Do not use Tabs for sequential steps; use a Stepper.
- Do not use Tabs when the content is short enough to show together.
- Do not hide critical content behind a tab that users may miss.

**Accessibility:**

- Use `role="tablist"`, `role="tab"`, and `role="tabpanel"`.
- Each tab has `aria-selected`, `aria-controls`, and an `id`.
- Each panel has `aria-labelledby` pointing to its tab.
- Arrow keys move between tabs; `Home` and `End` jump to the first and last.
- `Tab` moves into the active panel.
- Only the active tab is in the tab order; use roving `tabindex`.
- Keep the panel in the DOM or restore focus correctly when it changes.
- Do not use Tabs as a navigation menu.
- Ensure the selected state is not conveyed by color alone; use an indicator and weight.

**Tokens:**

- `component.tabs.tab.foreground.{state}`
- `component.tabs.tab.background.{state}`
- `component.tabs.indicator`
- `component.tabs.panel.background`
- `component.tabs.radius`
- `semantic.color.border.default`
- `semantic.color.focus.ring`

**Content:**

- Tab labels are short nouns: "Overview", "Activity", "Settings".
- Use sentence case.
- Keep labels parallel.
- Do not use more than about seven tabs; use a menu or a Select for more.
- Do not use icons without labels unless the meaning is universally clear.

**Do / Don't:**

- Do: "Overview", "Activity", and "Settings" tabs for one project.
- Don't: tabs that navigate to different pages.
- Do: arrow-key navigation between tabs.
- Don't: a tab that is selected only by color.

## Component quality gate

Every component must pass:

- [ ] Anatomy and slots are documented.
- [ ] Variants and sizes are documented.
- [ ] Default, Hover, Focus, Disabled, Loading, and Error states are documented, with `N/A` where applicable.
- [ ] Usage includes when to use and when not to use.
- [ ] Accessibility covers role, name, keyboard, focus, ARIA, contrast, and target size.
- [ ] Tokens are listed and exist in `design.json`.
- [ ] Content rules are documented.
- [ ] Do/Don't examples are included.
- [ ] The component works in every theme.
- [ ] The component passes the accessibility release gate.
