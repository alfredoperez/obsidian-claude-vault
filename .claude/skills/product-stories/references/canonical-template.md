---
tags:
  - product
  - templates
---

## Universal AC Rules

These rules apply to **every** template below that has an Acceptance Criteria section (Feature Story, Tech Task). Bug Reports use Steps to Reproduce instead of AC.

- **Plain dashes only.** Use `-`, never `- [ ]` task-list checkboxes — JIRA doesn't render markdown checkboxes, and AC is verified by PR review / tests / QA, not by ticking boxes.
- **No technical or dev details in AC.** No file paths, class names, signal names, method/property names, or specific technical approaches. AC describes **observable outcomes** from a user or behavior perspective. Anything implementation-shaped belongs in the **Dev details** expand.
- **Plain English.** A non-developer should be able to read AC and know what "done" looks like.
- **Outcomes, not steps.** "Pinned summary rows can be configured through the table wrapper" is an outcome. "Add `pinnedTopRowData` to `TableConfig`" is an implementation step — Dev details, not AC.
- **No "How to test" section.** Anywhere, in any template. Test steps live only in the tracker's test-plan field.

---

## Feature Story Template

### Format

```markdown
## Story Title

**As a** [role],
**I want** [capability],
**so that** [outcome].

### Why This Matters
- [Business impact: client request volume, revenue impact, support ticket reduction]
- [Optional: strategic context or urgency]

### Acceptance Criteria

#### [Theme 1] · [Figma]()
- Criterion
- Criterion

#### [Theme 2] · [Figma]()
- Criterion
- Criterion

### Access Control
- **Audience:** All users | Practice users only | Role-specific
- **Gating:** Feature flag | Permission | Both | None
- **Hidden behavior:** Hidden entirely | Disabled | Upgrade prompt

### Dev details

#### Suggested implementation

> **Suggested implementation — not prescriptive.** The developer is free to choose a different approach if it better fits the problem. The bullets below are pointers to reduce discovery time, not requirements.

- **Approach:** [Suggested technical path — pattern to follow, existing utility to reuse, shape of the change]
- **Key files:** `path/to/file.ts` — role it plays
- **Proven code:** [spike branch] — [commit SHAs and what each one proves]
- **Gating wiring:** [Which service/signal wires the flag or permission, what the fallback is]
- **Dependencies:** Depends on [ticket key] — [why]
- **Suggested split:** [If it's near the sizing limit, how it would split — by PR or by ticket]
- **Risks / edge cases:** [Known pitfalls for the dev to watch for]

#### Notes
- Optional context, edge cases, or design decisions that don't fit elsewhere

### Out of Scope
- [Adjacent capability that's NOT in this story] — [where it lives instead, if known]
- [Explicit exclusion] — [why it was cut]

### References
- [Design]() | [Spike]() | [Related ticket]()
```

Visible in the open, in this order: the As a / I want / so that sentence, Why This Matters, Acceptance Criteria, Access Control, Out of Scope, References. `Dev details` is **one Jira expand block** (collapsed by default) holding everything implementation-flavoured — Suggested implementation, Notes — in that order. Omit `References` when it would be empty.

#### How the expand is written

- **In markdown** (vault notes, drafts shown for approval): the `### Dev details` heading plus everything up to the next `###` heading is the expand body. The `####` sub-headings become level-4 headings inside it.
- **In ADF** (what actually goes to Jira, `contentFormat: adf`): one top-level node in the `doc` content, where the heading was:

  ```json
  {"type": "expand", "attrs": {"title": "Dev details"}, "content": [ /* heading(4) + paragraph + bulletList nodes for Suggested implementation, Notes */ ]}
  ```

- **In a markdown-to-ADF flow** (a tool that only accepts `contentFormat: markdown`): keep the same `### Dev details` heading and sub-headings, then fold them with a follow-up description edit in ADF — a ticket never sits with an open Dev details section.

### Usage guidance

- **Story statement** — one sentence per line. The "so that" should be a real user/business outcome, not a restatement of the "I want".
- **Why This Matters** — 1-2 bullets on the business or strategic impact. The "so that" captures the user outcome; this section captures why the business cares. Acceptable impacts: client request volume, revenue impact, support ticket reduction, strategic initiative alignment. If it takes more than 2 bullets, the impact belongs on the epic.
- **Acceptance criteria** — **outcomes, not implementation**. Describe what's true when the ticket is done from a user or observable-behavior perspective. Do NOT specify file paths, class names, signal names, or a particular technical approach in AC — those go in the Dev details expand. Group under themed sub-headers (`####`) instead of a flat list. Each theme maps to a logical chunk of work a developer can pick up. Use plain dashes (`-`), not checkboxes (`- [ ]`) — JIRA doesn't render markdown checkboxes. QA verification happens through JIRA's test plan field or comments. When a theme has visual states, link the **specific Figma frame** for that theme — not the whole page. One generic link for many states defeats the purpose.
- **Sizing check** — a story should be completable in **≤1 day** including dev, code review, and manual QA. Rules of thumb:
  - **≤3 AC themes** — if you need more, split the story
  - **≤10 acceptance criteria total** — more than that usually means multiple stories bundled together
  - **If you're debating whether it fits in a day, it doesn't** — split proactively
- **Dev details** — the one expand, placed after Access Control and before Out of Scope. Holds, in order: **Suggested implementation** (technical context a dev needs BEFORE picking up the ticket — suggested approach, key files, proven code with the spike branch and commits, how gating is wired, dependencies on other tickets, a suggested split when it's near the sizing limit, and known risks; pointers, not a full design doc — if the approach is non-trivial, link to a spike or plan file instead of describing it inline; omit bullets that don't apply), and **Notes**. Everything implementation-flavoured lives here and nowhere else.
- **Out of Scope** — what's adjacent but NOT in this story. Surfacing cuts as their own section (instead of burying them in Notes) makes "what's tempting but not in this work" visible to reviewers and prevents scope creep. Reference the ticket where deferred work lives, when known. Stays in the open, after the expand.
- **INVEST Check** — quality gate run while drafting, **never written into the ticket or the story file**. Confirm Independent, Negotiable, Valuable, Estimable, Small, Testable. If any fails, split or rewrite before finalizing. Pairs with the sizing rules below — INVEST catches story-shape problems sizing doesn't.
- **Notes** — inside Dev details: anything that doesn't fit in AC, Suggested implementation, or Out of Scope — product/design decisions, migration notes, context the reader should know about.
- **References** — links to designs, spikes, related tickets, or documentation. **Never the epic** — the parent link already carries it. Omit the section when it would be empty.
- **How to test** — does not exist. Test steps go in the tracker's test-plan field after the ticket is created.

### Questions to ask before writing

1. **Epic parent** — Which existing epic should this story live under? If no epic exists yet, ask the PM to create one first or identify the closest existing epic.
2. **Audience scope** — Is this for all users or only practice users? If role-specific, which roles? This determines whether we need permission-based conditional rendering.
3. **Access control mechanism** — Will this be behind a feature flag, a permission, or both? Feature flags control rollout; permissions control long-term access. Both may be needed (flag for rollout, permission for visibility).
4. **Hidden behavior** — If gated, what should users without access see? Hidden entirely, disabled state, or an upgrade prompt?
5. **Figma links** — Are there designs for this? Get the specific frame links per AC theme, not just the top-level page.
6. **Dev details** — What technical context does a dev need up front? Suggested approach, key files, proven code (spike branch + commits), flag/permission wiring, dependencies on other tickets, suggested split, known risks. All of it goes inside the expand.
7. **References** — Any related spikes, tickets, Slack threads, or documentation that should be linked? Not the epic — and skip the section if there's nothing.

### Example

```markdown
## Bulk Export Invoices to PDF

**As a** billing manager,
**I want** to select multiple invoices and export them as a single PDF,
**so that** I can send a consolidated package to clients without downloading one at a time.

### Why This Matters
- Top 5 client feature request — 3 enterprise clients blocked on manual workaround
- Reduces export workflow from ~20 minutes (download one-by-one) to a single click

### Acceptance Criteria

#### Selection · [Figma](https://www.figma.com/file/xxx?node-id=12-34)
- User can select individual invoices via checkbox
- "Select all" toggles every invoice on the current filtered view
- Selection count badge appears in the toolbar when ≥1 invoice is selected

#### Export · [Figma](https://www.figma.com/file/xxx?node-id=12-56)
- "Export PDF" button is enabled only when ≥1 invoice is selected
- Exported PDF contains one invoice per page, ordered by invoice date ascending
- File name follows the pattern `Invoices_<YYYY-MM-DD>.pdf`

#### Limits & Feedback
- Max 50 invoices per export; show inline warning when the limit is reached
- Progress indicator appears during generation
- Toast confirms success with a download link, or shows an error message on failure

### Access Control
- **Audience:** Practice users only (billing managers)
- **Gating:** Permission (`invoices.export`)
- **Hidden behavior:** "Export PDF" button hidden entirely for users without permission

### Dev details

#### Suggested implementation

> **Suggested implementation — not prescriptive.**

- **Approach:** New `<app-bulk-export-dialog>` accepts `ids: number[]`; calls the existing `DraftInvoicesApiService.exportPdf(ids)` used by single-export — no new backend wiring needed
- **Key files:** `draft-invoices-content.component.ts` (selection state), `draft-invoices-api.service.ts` (`exportPdf`), new `bulk-export-dialog.component.ts`
- **Proven code:** `spike/bulk-export-pdf` — `a1b2c3d` (dialog + selection wiring), `e4f5a6b` (50-row limit toast)
- **Gating wiring:** `BillingPermissionsService.isBulkExportEnabled` combines `permissions.invoices.export` with the existing feature flag
- **Dependencies:** Depends on WRK-101 (bulk selection toolbar) being merged
- **Risks / edge cases:** 50-row limit enforced client-side (button disabled) and server-side (422 on oversize payload — surface a toast)

#### Notes
- PDF generation uses the existing server-side renderer — no new dependencies

### Out of Scope
- CSV export — separate story

### References
- [Figma mockup]() | [PDF renderer spike]()
```

---

## Bug Report Template

### Format

```markdown
## Bug Title

**Page:** [Where it happens]

### Expected Behavior
[What should happen — stated once, clearly]

### Steps to Reproduce
1. Step one
2. Step two
3. Step three
   → [The broken outcome]

### Notes
- Optional: frequency, workaround, affected users, screenshots

### References
- [LogRocket session]() | [Related ticket]() | [Slack thread]()
```

### Usage guidance

- **Page** — just the page or area where the bug lives. No need for a full URL, just enough for someone to navigate there (e.g., "Draft Invoices table", "Invoice Details > Adjustments tab").
- **Expected Behavior** — state what *should* happen. One or two sentences. This replaces the old "Expected vs Actual" pattern — the actual broken behavior lives at the end of the repro steps.
- **Steps to Reproduce** — numbered steps ending with an arrow (`→`) that describes the broken outcome. This does double duty: it shows the repro path AND reveals the bug in one flow. No need for a separate "Actual Behavior" section.
- **Notes** — frequency ("happens every time" vs "intermittent"), workarounds, affected user segments, browser/environment info, screenshots or recordings.
- **Dev details** — optional, the same one expand as the story template (Suggested implementation — root cause, key files, suggested fix, risks — then Notes), placed after `Notes` and before `References` whenever there's actionable engineering context.
- **References** — LogRocket sessions, related tickets, Slack threads where the issue was reported. Never the epic; omit if empty.

### Example

```markdown
## Invoice total shows $0.00 after removing a line item

**Page:** Invoice Details > Line Items

### Expected Behavior
Removing a line item recalculates the invoice total to reflect the remaining items.

### Steps to Reproduce
1. Open any draft invoice with 2+ line items
2. Click the delete icon on the first line item
3. Confirm the deletion in the dialog
   → Invoice total shows $0.00 instead of the sum of remaining items

### Notes
- Happens every time, all browsers
- Refreshing the page fixes the total
- Only affects invoices with 2+ line items; single-item invoices show correctly after deletion

### References
- [LogRocket session]() | [BILL-1234]()
```

---

## Tech Task Template

### Format

```markdown
## Task Title

### Context
[What's wrong or missing. Describe the current state and why it needs to change.]

### Why This Matters
- [Measurable impact: fewer requests, LOC removed, dependency eliminated, unblocks X]
- [Optional second bullet if there's a user-facing improvement]

### Acceptance Criteria
- Outcome-oriented criterion (what's true when this is done)
- Another outcome
- Another outcome

### Dev details

#### Suggested implementation

> **Suggested implementation — not prescriptive.** The developer is free to choose a different approach if it better fits the problem.

- **Approach:** [Suggested technical path — pattern to follow, existing utility to reuse]
- **Key files:** `path/to/file.ts` — role this file plays
- **Proven code:** [spike branch] — [commit SHAs and what each one proves]
- **Dependencies:** Depends on [ticket key] — [why]
- **Suggested split:** [If it's near the sizing limit, how it would split]
- **Risks / edge cases:** [Known pitfalls to watch for]

#### Notes
- Optional context or decisions that don't fit elsewhere

### Out of Scope
- [What this task does NOT include] — [where it lives instead, e.g. ticket key]
- [Explicit exclusion]

### References
- [Related ticket]() | [Prior discussion]()
```

Same rules as the Feature Story: `Dev details` is the one expand (after AC — there's no Access Control on a task), Out of Scope and References stay in the open, References is omitted when empty and never carries the epic, and there is no "How to test" section.

### Usage guidance

- **Context** — describe the current state and why it's a problem. This is not a user story — there's no persona or "so that". Just state the problem clearly. Include enough detail that a developer can investigate the right solution independently.
- **Why This Matters** — 1-2 bullets on the measurable impact. This answers "why should a reviewer care?" Acceptable impacts: fewer network requests, LOC deleted, dependency eliminated, unblocks another ticket. If it takes more than 2 bullets, the impact belongs on the epic, not the ticket.
- **Acceptance criteria** — describe **observable outcomes**, not implementation steps. "Tables can show pinned summary rows without touching AG-Grid directly" is an outcome. "Add `pinnedTopRowData` to `TableConfig`" is an implementation step — that belongs in the Dev details expand, not AC. Use plain dashes (`-`), not checkboxes (`- [ ]`) — these are verified by PR review and tests, not by QA ticking boxes.
- **Dev details** — the one expand: Suggested implementation (technical path, key files, proven code, dependencies, suggested split, risks — **framed as a suggestion**, devs are free to choose a different approach; pointers, not a full design; omit bullets that don't apply), then Notes. Existing `Key Files` lists move under Suggested implementation.
- **Out of Scope** — explicitly call out what's NOT included and reference the ticket where that work lives (e.g., "Out of scope: deleting state files — WRK-104"). Prevents scope creep and makes the dependency chain visible.
- **Sizing check** — same rule as feature stories: completable in **≤1 day**. If it feels bigger, split it.

### Example

```markdown
## Table wrapper doesn't support pinned summary rows

### Context
Several billing tables need to display summary/total rows pinned to the top or bottom of the grid (e.g., ApplyProgressDialog, fee allocation tables). Today there's no way to configure this through `<app-table>` — consumers would have to bypass the wrapper and use AG-Grid directly, which defeats the purpose of the abstraction.

### Why This Matters
- Unblocks 3 billing tables from migrating to `<app-table>`, reducing AG-Grid leakage
- Prevents consumers from bypassing the wrapper for a common use case

### Acceptance Criteria
- A consumer can configure pinned top and/or bottom rows through the table wrapper
- Pinned rows can be updated dynamically after initial render
- No AG-Grid imports needed in consuming components

### Dev details

#### Suggested implementation

> **Suggested implementation — not prescriptive.**

- **Approach:** Extend `TableConfig` with `pinnedRows?: { top?: T[]; bottom?: T[] }` and pass through to AG-Grid at grid-ready
- **Key files:** `table.component.ts` (wire the config through), `table.models.ts` (extend interface)
- **Dependencies:** Depends on WRK-102 — the config-passthrough refactor this builds on
- **Risks / edge cases:** Dynamic updates require calling `api.setPinnedTopRowData` after initial render; signal-based inputs should trigger this automatically

#### Notes
- Signal-based inputs already re-run on change, so no manual subscription is expected

### Out of Scope
- Styling of pinned rows — consumers handle their own row styling
- Pinned row editing — not needed by any current consumer — WRK-NNN

### References
- [Table migration plan]() | [Q2 tidy-up tickets]()
```

