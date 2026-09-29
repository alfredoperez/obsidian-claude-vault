---
type: story
project: worky
feature: crew-scheduling
story_id: STORY-002
slice: now
priority: P1
status: draft
tracker_issue:
covers_requirements: [R014]
created: 2026-09-28
lifespan: project
description: A dispatcher records a crew member's availability from the Console when the crew member phones it in, and the crew member sees who set it
inputs:
  story_map: ../Crew Scheduling Story Map.canvas
  prd: ../Crew Scheduling PRD.md
tags: [worky, crew-scheduling, story]
---

# STORY-002 — Dispatcher sets availability for a crew member

**As a** dispatcher,
**I want** to record a crew member's availability myself when they phone it in,
**so that** the board is complete even for the crews who will not open the app.

### Why This Matters
- Risk 3 in the PRD: if the crews who do not use the app have no availability on the board, dispatch goes back to the spreadsheet for everyone
- Lets us measure crew-entered versus dispatch-entered availability, which decides how hard to push app adoption

### Acceptance Criteria

#### Setting it
- Given I open a crew member's row in the Console availability strip, when I click a day, then I can set it to available, unavailable, or half-day
- Given I set a day, when the crew member opens their Availability screen, then that day shows the state I set, with my name and the time

#### Not overriding silently
- Given the crew member already set that day, when I change it, then the Console asks me to confirm and shows what they had set
- Given I confirm, when the crew member next opens the app, then the day shows as changed by me, not as their own entry

### Access Control
- **Audience:** Dispatchers
- **Gating:** Permission (`scheduling.availability.write`)
- **Hidden behavior:** Days are read-only for users without the permission; no edit affordance is shown

### Dev details

#### Suggested implementation

> **Suggested implementation — not prescriptive.**

- **Approach:** Same `PUT /crew/:id/availability` endpoint as STORY-001 with `set_by` taken from the caller's identity; the Console availability strip already exists read-only from Phase 1, so this adds the click handler and the confirm dialog
- **Key files:** `dispatch-console/src/board/AvailabilityStrip.tsx`, `services/crew/src/availability/write.ts` (add the "already set by owner" flag in the response so the client can prompt)
- **Gating wiring:** `PermissionsService.can('scheduling.availability.write')`; falls back to read-only rendering
- **Dependencies:** STORY-001 (the table and endpoint)
- **Risks / edge cases:** a dispatcher setting a day the crew member is editing offline at the same time; the crew member's queued write lands later and wins, which is acceptable and visible via `set_by`

#### Notes
- No bulk entry in this story. Dispatch asked for "mark the whole week"; that is a follow-up once we see how often it happens

### Out of Scope
- Bulk or range entry — follow-up story if dispatch-entered share stays above 30 % after two weeks
- Recurring patterns (R002) — release 2
