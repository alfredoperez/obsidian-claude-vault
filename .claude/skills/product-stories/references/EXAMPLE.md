# Example output — `now` slice of command-center article-mgmt

Running `/product-stories article-mgmt --slice now` produces three story files in `Projects/command-center/product/article-mgmt/stories/`:

---

## File 1: `STORY-001-persistent-claude-sidebar.md`

```markdown
---
type: story
project: command-center
feature: article-mgmt
story_id: STORY-001
slice: now
priority: P0
status: draft
tracker_issue:
covers_requirements: [R001, R002]
created: 2026-06-04
inputs:
  roadmap: ../roadmap.md
  prd: ../prd.md
---

# STORY-001 — Persistent Claude sidebar with article context

## Story

As Alfredo writing build logs
I want a persistent Claude chat sidebar that knows the active article and SDD series
So that I can iterate on refinements without leaving the editor or losing conversation state

## Acceptance Criteria

- Given I open an article in the editor, when the page loads, then a chat sidebar appears on the right side of the editor with a "CLAUDE — CONTEXT: <article title>" eyebrow label.
- Given I send a message in the sidebar, when Claude responds, then the response streams into the panel and remains visible after I scroll or save the article.
- Given I reload the page, when the editor returns, then my prior chat thread for this article is restored from local storage.
- Given I open a different article, when the editor loads it, then the sidebar shows a fresh thread for that article (no cross-contamination).
- Given the sidebar is open, when I look at the eyebrow region, then the article's series, status, and word count are visible in the system context.

## Dev details

### Suggested implementation

- Replaces `terminal-panel.tsx` in `article-editor.tsx`
- Persistence via SQLite (Prisma) — new `chat_threads` table keyed by article path
- Streaming via Claude API; enable prompt caching from day 1 (PRD risk #5)

## Out of Scope

- Cross-article chat that spans the whole series
- Voice input or audio output
- Sharing chat history with another user
```

---

## File 2: `STORY-002-phase-action-buttons.md`

```markdown
---
type: story
project: command-center
feature: article-mgmt
story_id: STORY-002
slice: now
priority: P1
status: draft
tracker_issue:
covers_requirements: [R003]
created: 2026-06-04
inputs:
  roadmap: ../roadmap.md
  prd: ../prd.md
---

# STORY-002 — Phase-action buttons in the chat sidebar

## Story

As Alfredo writing build logs
I want phase-action buttons (DRAFT, EDIT, ILLUSTRATE, EXPORT) directly in the chat sidebar
So that I can trigger the right pipeline skill on the active article without typing a command

## Acceptance Criteria

- Given the chat sidebar is open, when I look at the action toolbar, then four buttons labeled DRAFT, EDIT, ILLUSTRATE, EXPORT are visible.
- Given I click DRAFT, when the action runs, then the existing draft skill is invoked with the active article path as input.
- Given I click EDIT, when the action runs, then the existing edit skill is invoked with the active article path.
- Given I click ILLUSTRATE, when the action runs, then the existing illustrate skill is invoked with the active article path.
- Given I click EXPORT, when the action runs, then the existing export skill is invoked with the active article path.
- Given a phase action is running, when the chat panel renders, then the chat shows a streaming status message and disables the action toolbar until it completes.

## Dev details

### Suggested implementation

- Buttons map 1:1 to existing kaiju skills: `/article-draft`, `/article-edit`, `/article-illustrate`, `/article-export`
- Skills run via the same dispatcher as the existing terminal panel

## Out of Scope

- Custom phase actions configurable by the user
- Confirmation dialogs before running an action
```

---

## File 3: `STORY-003-sidebar-context-auto-injection.md`

```markdown
---
type: story
project: command-center
feature: article-mgmt
story_id: STORY-003
slice: now
priority: P1
status: draft
tracker_issue:
covers_requirements: [R002]
created: 2026-06-04
inputs:
  roadmap: ../roadmap.md
  prd: ../prd.md
---

# STORY-003 — Sidebar auto-injects article + series context

## Story

As Alfredo writing build logs
I want Claude in the sidebar to already know the article body, frontmatter, and SDD series outline
So that I don't have to re-explain the context every refinement turn

## Acceptance Criteria

- Given I open the sidebar on an article, when I send my first message, then Claude's system prompt includes the article's markdown body and frontmatter (series, status, word count).
- Given the active article belongs to a series, when Claude responds, then the system prompt also includes a pointer to the series outline file so cross-article references work.
- Given the article changes (I save edits), when I send my next message, then the updated article content is what Claude sees — no stale snapshot.
- Given the system prompt would exceed a reasonable token budget, when I send a message, then the prompt is truncated to the article body and last 5 chat turns and Claude is told what was elided.

## Dev details

### Suggested implementation

- System prompt assembled server-side from article path + frontmatter parse
- Series outline resolved by walking up `Projects/Content/Writing/<series>/00 - Series Outline.md`
- Token budget: target ≤ 8k tokens for the system prompt; use prompt caching to amortize cost

## Out of Scope

- Including prior published articles in the system prompt
- Pulling Knowledge/ notes related to the article topic (future enhancement)
```

---

## Hand-off summary printed to the user

```
✓ Wrote 3 stories to Projects/command-center/product/article-mgmt/stories/
  - STORY-001 Persistent Claude sidebar with article context (P0, covers R001, R002)
  - STORY-002 Phase-action buttons in the chat sidebar (P1, covers R003)
  - STORY-003 Sidebar auto-injects article + series context (P1, covers R002)

Coverage for `now` slice: R001, R002, R003 + NFR001, NFR003, NFR004
  All `now` requirements covered.

Next: /product-sync-tracker article-mgmt
```
