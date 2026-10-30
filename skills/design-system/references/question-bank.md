# Question Bank

Use this bank to run the design system interview. Ask at most five questions per round. Prefer structured multiple-choice questions when the host supports them. Otherwise ask numbered questions and wait for the answers.

Do not read the entire bank to the user. Select the next questions that reduce the most design and delivery uncertainty. Cover every category before writing `design.json` or `DESIGN-SYSTEM.md`. When a category does not apply, record why in the artifact instead of skipping it silently.

## Round 1: Product, users, and brand

### Product and context

- What is the product name and type: mobile finance app, B2B SaaS dashboard, e-commerce, internal tool, or something else?
- Describe the product in one sentence.
- Who are the primary users, secondary users, and operators?
- What are the top three user journeys?
- Which surfaces are most important: onboarding, daily task, checkout, reporting, administration?
- What is explicitly out of scope for v1.0?

### Platforms and team

- Which platforms are in scope: web, iOS, Android, desktop, email, embedded?
- Which frameworks and versions are already in use: React, Vue, Angular, Tailwind, native, Flutter, other?
- How many designers and developers will build and maintain the system?
- Who owns design, frontend, mobile, documentation, and accessibility?
- Is there a design tool library, and who maintains it?
- What is the release cadence and the first deadline?

### Brand and personality

- Which three to five adjectives describe the brand: minimal, corporate, friendly, technical, bold, calm, premium, playful?
- Which brands or products are the visual reference, and which are anti-references?
- Are there existing brand colors, fonts, logos, illustrations, or photography guidelines?
- Which brand assets are mandatory, and which can the design system ignore?
- What must the UI never look like?

## Round 2: Tokens and theming

### Current state

- Are there existing tokens, CSS variables, Tailwind theme values, or design-tool styles?
- Where is the source of truth today: Figma, code, a spreadsheet, or tribal knowledge?
- Which naming conventions already exist, and which must be preserved?
- Are there known inconsistencies, duplicate tokens, or hardcoded values?
- Is there an existing token pipeline or build step?

### Color and themes

- What are the brand primary, secondary, and accent colors?
- Which neutral palette is preferred: warm, cool, or pure gray?
- Are success, warning, danger, and info colors already defined?
- Which themes are required: light, dark, high contrast, brand, seasonal, white-label?
- Does the product need per-tenant theming or runtime theme switching?
- Which color pairs are business-critical and must be verified first?
- Are there legal or brand rules that restrict color use?

### Platform outputs

- Which output formats are required: CSS custom properties, Tailwind, SCSS, Swift, Kotlin, Compose, Figma variables, JSON?
- Is there a design-tool and code synchronization workflow?
- Which token naming style is preferred: dot notation, kebab-case, camelCase, or platform-specific?
- Is there a package registry or monorepo for distributing the tokens?

## Round 3: Typography, spacing, and density

### Typography

- Which brand fonts are licensed for web and mobile?
- Which fallback stacks are acceptable?
- What is the base body size: 16px, 15px, 14px?
- Which scale ratio fits the product: 1.125, 1.200, 1.250, or 1.333?
- Which languages and scripts must the fonts support?
- Does the product need fluid typography, or a fixed scale?
- What are the line-height, paragraph spacing, and maximum line-length rules?
- Are there performance or bundle-size constraints for web fonts?

### Spacing and layout

- Which spacing grid is preferred: 4px, 8px, or another base?
- How dense is the UI: comfortable, compact, or dense data tables?
- What are the standard page gutters, container widths, and breakpoints?
- How many columns at mobile, tablet, desktop, and wide?
- What are the side margins and gutters at each breakpoint?
- Which components change layout on mobile: full-width buttons, stacked cards, table-to-card, bottom sheet?
- Which breakpoints are mandatory, and which are optional?
- Does the product need container queries for sidebars, split panes, or reusable cards?
- Does the product need responsive spacing tokens?
- Are there platform-specific density requirements?

### Radius, elevation, and motion

- What is the radius personality: sharp, soft, pill, or mixed?
- Which surfaces need elevation, and which use borders instead?
- Does dark mode use shadows, borders, or both?
- What motion style fits the brand: none, subtle, standard, expressive?
- Are there performance, vestibular, or reduced-motion requirements?

## Round 4: Accessibility and content

### Accessibility

- Which target applies: WCAG 2.1 AA, AAA, or a local regulation?
- Are there known accessibility issues or complaints?
- Which assistive technologies must be supported: screen readers, switch access, voice control, magnification?
- Which browsers, OS versions, and devices are supported?
- What are the minimum touch target and focus indicator requirements?
- Is there an accessibility testing process, vendor, or audit cadence?
- Are there legal, procurement, or public-sector requirements?

### Content and localization

- Which languages and writing directions must be supported, including RTL?
- Who writes UI copy, and is there a content style guide?
- How are dates, numbers, currencies, names, and addresses formatted?
- Which tone applies to errors, empty states, and destructive actions?
- Are there content-length constraints for buttons, labels, and navigation?

## Round 5: Components and patterns

### Component priorities

- Which components does the product use today?
- Which components cause the most bugs, inconsistency, or design debt?
- Which three components must exist for the first pilot screen?
- Which components are platform-specific?
- Which components are compositions of others?
- Which components can wait for v1.1?

### States and behavior

- Which states are required: default, hover, focus, disabled, loading, error, selected, readonly, empty?
- Which components need async loading, optimistic updates, or error recovery?
- Which components need keyboard shortcuts or complex focus management?
- Which components need analytics events or privacy review?
- Which components render user-generated or rich content?

## Round 6: Governance and adoption

### Ownership and process

- Who approves token and component changes?
- How are contributions proposed, reviewed, and released?
- Which versioning and deprecation policy applies?
- Is there a design review, accessibility review, or code review gate?
- How are exceptions handled?

### Documentation and adoption

- Where will documentation live: Storybook, a docs site, the repository, Figma?
- Which examples and code snippets are required?
- How will teams migrate from existing UI?
- Which pilot screen or product area will adopt the system first?
- Which metrics prove adoption: component coverage, token usage, accessibility defects, duplicate components?
- How will feedback be collected?

## Round 7: Audit mode

Use this round only when auditing an existing design system.

- What is the scope of the audit: tokens, components, accessibility, documentation, governance, layouts, or all?
- Which version and platforms are in scope?
- Which known issues and user complaints exist, including overflow, clipping, zoom, and unusable mobile screens?
- Which evidence is available: code, screenshots, Figma, analytics, accessibility reports, support tickets?
- Which severity model and report audience apply?
- Which findings are already accepted as known exceptions?
- Which security concerns apply: unsafe HTML rendering, third-party scripts, dependency risk, or data exposure in components?

### Layout audit

- Which representative templates and highest-traffic routes should be inventoried first?
- Which breakpoints, media queries, container widths, and grid rules exist today, and where are they defined?
- Where do fixed widths, `min-width`, `max-width`, `overflow-x`, `100vh`, and absolute positioning appear?
- Do you have viewport analytics, device data, or top-journey data to prioritize templates?
- Do support tickets, crash reports, or accessibility reports mention horizontal scrolling, clipped content, zoom, or unusable mobile screens?
- Which screens must be preserved as-is, and which may be restructured?
- What are the content extremes: longest labels, translations, empty, loading, error, many rows, long file names, missing media?
- Is RTL in scope, and where do directional margins, icons, and navigation break?
- Which screen is the pilot for the migration, and what is the rollback plan?
- Which acceptance criteria and viewport evidence prove a template is migrated?

## Decision rules

- Prefer measurable answers over adjectives. Replace "accessible" with a WCAG target and a contrast ratio. Replace "modern" with a scale, a radius, and a motion style. Replace "small team" with a headcount and an ownership model.
- When the user does not know, propose two or three concrete options with trade-offs and ask the user to choose.
- When the user delegates the decision, record it as an assumption and ask for approval at Gate 3.
- Do not ask about hex codes before the product, platforms, brand, and accessibility constraints are clear.
- Do not ask more than five questions at once. Group related questions.
- Do not repeat a question that the repository or a previous answer already answers.
- Do not infer a requirement from silence. Mark it as an assumption or an open decision.
- Stop when the remaining questions would not change the token model, the component list, the accessibility matrix, or the definition of done.

## Minimum coverage before writing the artifacts

Record an answer or an explicit non-applicability note for:

- product type, users, top journeys, and out-of-scope scope;
- platforms, frameworks, team size, owners, and deadline;
- brand personality, references, anti-references, and mandatory assets;
- existing tokens, source of truth, naming, and known inconsistencies;
- brand colors, neutrals, feedback colors, and required themes;
- platform output formats and token distribution;
- fonts, licensing, fallbacks, base size, scale ratio, and density;
- spacing grid, breakpoints, columns, margins, gutters, component adaptation, radius, elevation, and motion;
- WCAG target, known issues, supported assistive technologies, and testing process;
- localization, RTL, content style, and formatting;
- component priorities, required states, and pilot screen;
- governance, versioning, deprecation, contribution, documentation, and adoption metrics;
- audit scope, evidence, severity model, and accepted exceptions when auditing.
