---
type: story
project: worky
feature: crew-scheduling
story_id: STORY-003
slice: next
priority: P0
status: Next
tracker_issue:
covers_requirements: [R003, R004, R005]
created: 2026-09-28
lifespan: project
description: The dispatcher drags a crew onto a job on the day board; the system saves it, or refuses and names the hard rule it would break
inputs:
  story_map: ../Crew Scheduling Story Map.canvas
  prd: ../Crew Scheduling PRD.md
tags: [worky, crew-scheduling, story]
---

# STORY-003 — Dispatcher assigns a crew to a job <span class="badge-later">next</span>

**As a** dispatcher,
**I want** to drag a crew onto a job on the day board and have it either stick or tell me why it cannot,
**so that** the schedule I build is one the crews can actually run.

### Why This Matters
- This is the story that retires the spreadsheet for Denver; until it ships, everything else is preparation
- Hard-rule refusals at assignment time are what take the daily 7am conflicts to zero

### Acceptance Criteria

#### The day list
- Given I pick a day, when the board loads, then I see every job for that day ordered by start time, each showing scope, minimum crew size, and required skills
- Given a job already has a crew, when I look at it, then the crew's name and members are shown on the job

#### Assigning
- Given an unassigned job and an available crew, when I drag the crew onto the job, then the assignment is saved and shown on the job without a confirm step
- Given I just assigned a crew, when I press undo, then the job returns to unassigned

#### Refusals
- Given a crew with a member marked unavailable that day, when I drop the crew on a job, then the assignment is refused and the board says which member is unavailable
- Given a job needing three painters and a crew of two, when I drop the crew on it, then the assignment is refused and the board says the crew is one short
- Given a job needing a lift-certified painter and a crew with none current, when I drop the crew on it, then the assignment is refused and the board names the missing certification

### Access Control
- **Audience:** Dispatchers
- **Gating:** Permission (`scheduling.assign`)
- **Hidden behavior:** Board is read-only without the permission; drag handles are not rendered

### Dev details

#### Suggested implementation

> **Suggested implementation — not prescriptive.**

- **Approach:** `scheduling` becomes the only writer (design D1). `POST /assignments` runs the hard-rule function from Phase 1 and returns either the saved row or `422` with `{rule, detail}`; the board renders the detail verbatim. Undo is a second assignment row with `replaced_by`, never a delete
- **Flow:** <span class="step">drop crew</span> <span class="step">POST /assignments</span> <span class="step">hard-rule check</span> <span class="step">save or 422</span>
- **Key files:** `services/scheduling/src/rules/hard.ts` (exists, untested against a real caller), `services/scheduling/src/assignments/create.ts` (new), `dispatch-console/src/board/DayBoard.tsx`, `dispatch-console/src/board/useDrop.ts`
- **Proven code:** `spike/day-board-drag` — `4f1c9a2` proves drag at 60 crews × 120 jobs stays under 16 ms per frame when only the two affected cells re-render
- **Gating wiring:** `PermissionsService.can('scheduling.assign')` gates the drag handles and the endpoint
- **Dependencies:** STORY-001 (availability data the unavailable rule reads); Phase 0 skills table
- **Suggested split:** the day list (R003) can ship alone as STORY-003a; drag + refusals as STORY-003b
- **Risks / edge cases:** two dispatchers assigning the same job in the same second — the second write refuses with a "just assigned by" message rather than silently replacing

#### Notes
- Soft-rule warnings (overlap, drive time) are R006 and a separate story so this one stays under a day
- Refusal wording is the product. Dispatch will read "crew unavailable" as "the board is wrong"; the message must say which member and which day

### Out of Scope
- Soft-rule warnings (R006) — [[Dispatcher sees a double-booking warning]]
- Publishing the assignment to the Crew App (R007) — next story in this slice
- Moving a job to another day (R009) — release 1, separate story
