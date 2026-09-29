---
type: story
project: worky
feature: crew-scheduling
story_id: STORY-001
slice: now
priority: P0
status: draft
tracker_issue:
covers_requirements: [R001]
created: 2026-09-28
lifespan: project
description: A painter marks each of the next four weeks' days as available, unavailable or half-day from the Crew App, and dispatch sees it within a minute
inputs:
  story_map: ../Crew Scheduling Story Map.canvas
  prd: ../Crew Scheduling PRD.md
tags: [worky, crew-scheduling, story]
---

# STORY-001 — Crew member sets weekly availability

**As a** crew member,
**I want** to mark each day of the coming four weeks as available, unavailable, or half-day from my phone,
**so that** dispatch schedules me around my real week instead of texting me on Sunday night.

### Why This Matters
- Sunday-night availability texts are the single biggest source of the 2–3 conflicts a day dispatch finds at 7am
- Nothing on the day board is trustworthy until availability is data; this is the first story for that reason

### Acceptance Criteria

#### Marking a day
- Given I open Availability in the Crew App, when the screen loads, then I see today and the next 27 days as a grid, each day showing its current state or "not set"
- Given a day is "not set", when I tap it once, then it becomes available; a second tap makes it unavailable; a third makes it half-day; a fourth returns it to available
- Given I change a day, when I leave the screen, then the change is kept without a save button

#### Dispatch sees it
- Given I mark Thursday unavailable, when a dispatcher looks at my row in the Console within one minute, then Thursday shows as unavailable
- Given a dispatcher set a day on my behalf, when I look at that day, then I see who set it and when, and I can still change it

#### Offline
- Given I have no signal, when I change a day, then the change is queued and the day shows a "pending sync" mark until it lands
- Given the app comes back online, when the queued change lands, then the pending mark clears without me doing anything

### Access Control
- **Audience:** Crew members, for their own availability only
- **Gating:** None
- **Hidden behavior:** Not applicable

### Dev details

#### Suggested implementation

> **Suggested implementation — not prescriptive.** Pointers to reduce discovery time, not requirements.

- **Approach:** New `availability` table per the design doc (`crew_member_id, date, state, set_by, set_at`); upsert on `(crew_member_id, date)`. The Crew App writes through the existing offline queue used for job photos, so the pending-sync mark comes for free
- **Key files:** `crew-app/src/screens/Availability.tsx` (new), `crew-app/src/sync/queue.ts` (reuse), `services/crew/src/availability/` (new module, exposes `GET /crew/:id/availability?from&to` and `PUT`)
- **Gating wiring:** none; the screen is visible to every crew member
- **Dependencies:** none. Phase 0 (skills as data) is shipped and unrelated
- **Suggested split:** if the offline theme pushes past a day, ship marking + dispatch visibility first and the offline queue as STORY-001b
- **Risks / edge cases:** a day marked by dispatch and by the crew member within the same minute — last write wins, and `set_by` says whose it was

#### Notes
- Four weeks, not "forever": the PRD scopes availability to 28 days so the grid fits one screen without scrolling. Recurring patterns are R002, release 2

### Out of Scope
- Recurring weekly patterns (R002) — release 2
- Dispatcher entering availability on a crew member's behalf (R014) — [[Dispatcher sets availability for a crew member]]
- Hours or timesheet capture — availability is not a timesheet
