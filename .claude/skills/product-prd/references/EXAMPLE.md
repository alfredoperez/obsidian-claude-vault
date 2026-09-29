---
type: prd
project: command-center
feature: article-mgmt
status: draft
created: 2026-06-04
inputs:
  journey_map: ./journey-map.md
  mockups: ../../article-mgmt-mockups.md
  notes:
---

<!-- Lives at: Projects/command-center/product/article-mgmt/prd.md -->
<!-- Sibling artifacts: journey-map.md (above), roadmap.md (next), stories/, config.yml -->
<!-- Invoke next phase with: /product-roadmap article-mgmt -->

# PRD — Article Management Extension (command-center)

## Problem

Writing build-log articles in command-center today requires leaving the editor for every refinement (one-shot Claude terminal panel can't iterate), every image (Higgsfield in a side terminal), and every self-note ("come back to this" lives in Slack DMs). The journey map's top friction stage is **Refines** — the moment-of-truth is the first refinement turn, and the current stateless flow turns that into a multi-day pause. Articles sit half-edited; the build-log cadence drifts.

**Source:** `./journey-map.md` (top pain: context-switch for Claude rewrites, severity 4; MoT: first refinement turn quality, severity 5)

## Goals + success metrics

| Metric | Baseline | Target | Source / how measured |
|---|---|---|---|
| Median time from "Drafting" → "Editing" kanban transition | ~3 days | ≤ 1 day | command-center kanban-status timestamps |
| Tool switches per article (editor exits to terminal / browser) | ~6 per article | ≤ 2 | Self-logged for the next 3 articles |
| Refinement-callout resolution time (first-touch to resolved) | not tracked | ≤ 30 min | New telemetry on `ad-refine` block state changes |
| Articles shipped per week (current cadence) | 0.5 | 1.0 | Blog repo commit history |

> Metrics 1, 2, 4 inherit `confidence: medium` from the journey map. Metric 3 requires new instrumentation (NFR002 covers it).

## Solution overview

Extend the existing command-center articles app with: (1) a persistent Claude chat sidebar that knows the active article and the SDD series context, (2) inline comments on paragraphs with a sidebar roll-up, (3) inline Higgsfield image generation triggered from chat or directly, and (4) richer kanban cards with hover-expanded detail. The article-mgmt-mockups doc has visual references for all four views. Users continue using the existing editor — these are additive panels and enhancements, not a rewrite.

## Functional requirements

| ID | Requirement | Notes |
|---|---|---|
| R001 | User can open a persistent Claude chat sidebar from the article editor that retains conversation history for the article session | Replaces the stateless one-shot terminal panel |
| R002 | The chat sidebar's system context auto-includes the article markdown, frontmatter (series, status, word count), and a pointer to sibling notes in the same series | "Context: Build Log 1" eyebrow label per mockup |
| R003 | User can trigger phase actions (DRAFT, EDIT, ILLUSTRATE, EXPORT) from buttons in the chat sidebar that invoke the existing skill of the same name | One-click skill invocation; no terminal switch |
| R004 | User can attach an inline comment to any paragraph of the article via a `Cmd+Shift+M` keystroke or a hover gutter icon | Comments persist across saves |
| R005 | Comments appear in a sidebar roll-up filtered by `ALL / OPEN / RESOLVED`, with each card showing a "JUMP TO LINE" link | Mirrors refinement-list pattern |
| R006 | Comments can be marked Resolved; resolved comments collapse out of the active gutter but remain accessible in the sidebar with strikethrough | |
| R007 | User can trigger Higgsfield image generation from the chat sidebar; results appear as a 2×2 thumbnail grid with INSERT actions | Reuses `/create-image` skill semantics |
| R008 | Generated images can be inserted into the active article as a wikilink (`![[IMG-…]]`) at the cursor position | Matches existing image-paste pattern |
| R009 | Generated images are saved to `~Attachments/<project>/<feature>/<article-slug>/` on insert | Folder convention matches article-illustrate |
| R010 | Hovering a kanban card expands it to show the full description, last-edited timestamp, and inline actions (OPEN, PREVIEW, MOVE →) | Other cards fade by 10% on hover focus |

### Non-functional requirements

| ID | Requirement | Notes |
|---|---|---|
| NFR001 | Chat sidebar streaming response time ≤ 1s for the first token | UX feel; not a hard SLA |
| NFR002 | Refinement-callout state changes emit telemetry to a local jsonl log for metric 3 | New file: `~/.command-center/refine-events.jsonl` |
| NFR003 | Comments and chat history persist locally (SQLite or JSON in command-center data dir); no external service | Single-user app; no sync need |
| NFR004 | All new panels honor the existing brutalism-dark theme tokens (no new palettes) | Matches the mockups |

## Scope

**In:**
- Persistent Claude chat sidebar with article + series context
- Inline comments with sidebar roll-up
- Inline Higgsfield image generation
- Kanban hover-expanded card

**Out:**
- Multi-user collaboration (no real-time presence, no shared cursors)
- Cloud sync of chat history or comments
- Chat across multiple articles in one session (each article = fresh thread)
- Voice input or audio responses
- Mobile / responsive layout (desktop only, matches existing app)

**Future (deferred):**
- Per-section AI suggestions (auto-flag weak hooks, suggest titles)
- Comment threads with replies
- Higgsfield video generation inline (current scope: images only)
- Cross-article chat that knows the whole series at once

## Technical considerations

- Reuses existing `~/dev/GitHub/command-center/src/app/(dashboard)/articles/[slug]/article-editor.tsx` — sidebar replaces `terminal-panel.tsx`, doesn't fork the editor
- Claude chat uses Claude API directly from a Next.js server action; needs `ANTHROPIC_API_KEY` in the local env (existing `.env.local` pattern)
- Higgsfield integration calls `higgsfield generate create` via a server-side child process (CLI already auth'd locally), polls status, downloads result to the attachments folder
- Comment storage: SQLite via Prisma (already in command-center for kanban state) — add `comments` table keyed by article path + line range
- Brutalism-dark theme tokens already exist; no new design tokens

## Dependencies + risks

| # | Type | What | Owner | Mitigation |
|---|---|---|---|---|
| 1 | dep | `higgsfield` CLI authenticated locally | Alfredo | Already auth'd as of 2026-06-04; document re-auth in README |
| 2 | dep | Claude API key in command-center `.env.local` | Alfredo | Document in README; reuse existing pattern |
| 3 | risk | Higgsfield CLI session expiry mid-generation | Alfredo | Surface CLI auth errors in chat; deep-link to re-auth instructions |
| 4 | risk | Comment storage schema changes during iteration | Alfredo | SQLite migration scripts via Prisma; keep schema in sync with the spec |
| 5 | risk | Claude API cost on long chat threads | Alfredo | Enable prompt caching from day 1 (matches kaiju `claude-api` skill guidance) |

## Milestones

- **M1:** Persistent Claude chat sidebar (R001, R002, R003) — replaces `terminal-panel.tsx`
- **M2:** Inline Higgsfield image generation (R007, R008, R009)
- **M3:** Comments inline + sidebar (R004, R005, R006)
- **M4:** Kanban hover-expanded card (R010)

> Real phasing lives in `roadmap.md` next.

## Open questions

- [ ] **[blocking]** Should the chat sidebar's system prompt include the SDD series outline by default, or only when explicitly referenced? Affects token cost.
- [ ] **[needs-research]** What's the actual baseline for "tool switches per article"? Metric 2 needs a 1-week self-log before we can target it credibly.
- [ ] **[clarify-with-stakeholder]** N/A — single-user feature, no stakeholders beyond the author.
