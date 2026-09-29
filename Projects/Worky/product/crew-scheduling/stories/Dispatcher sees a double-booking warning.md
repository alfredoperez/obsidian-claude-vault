---
type: story
project: worky
feature: crew-scheduling
story_id: STORY-004
slice: next
priority: P1
status: draft
tracker_issue:
covers_requirements: [R006]
created: 2026-09-28
lifespan: project
description: When a drop would give a crew two overlapping jobs or a long drive between them, the board warns, lets the dispatcher accept, and records that they did
inputs:
  story_map: ../Crew Scheduling Story Map.canvas
  prd: ../Crew Scheduling PRD.md
tags: [worky, crew-scheduling, story]
---

# STORY-004 — Dispatcher sees a double-booking warning

**As a** dispatcher,
**I want** the board to warn me when I give a crew two jobs that overlap or sit too far apart, without stopping me,
**so that** I catch the mistakes I would have caught on the whiteboard, and can still make the calls the board cannot.

### Why This Matters
- Overlaps are the other half of the 7am conflicts; the unavailable-crew rule catches the first half
- Warn-not-block is the trust contract with dispatch (PRD risk 4): the board advises, Marta decides

### Acceptance Criteria

#### Overlap
- Given a crew already has a job from 8 to 12, when I drop the crew on a job from 11 to 3, then the assignment is saved and the job shows a warning naming the other job and the overlap
- Given I see the warning, when I click accept, then the warning collapses to a small mark on the job that I can expand later

#### Drive time
- Given a crew's previous job is more than the drive-time threshold away, when I drop the crew on the next job, then the job shows a warning with the estimated drive time
- Given the threshold is changed in settings, when I assign again, then the new threshold applies without anyone deploying anything

#### Record of the call
- Given I accepted a warning, when anyone opens the job's history, then it shows the warning, who accepted it, and when

### Access Control
- **Audience:** Dispatchers
- **Gating:** Permission (`scheduling.assign`) — same as assigning
- **Hidden behavior:** Not applicable; warnings only appear on a write the user is allowed to make

### Dev details

#### Suggested implementation

> **Suggested implementation — not prescriptive.**

- **Approach:** Soft rules are data (design D3): a `soft_rule` table with `drive_time_max` and `overlap_tolerance`. The assignment endpoint returns `201` with a `warnings[]` array instead of refusing; accepting a warning writes an `override` row against the assignment, which is what the history reads
- **Key files:** `services/scheduling/src/rules/soft.ts` (new), `services/scheduling/src/rules/thresholds.ts` (reads `soft_rule`), `dispatch-console/src/board/JobWarning.tsx`, `dispatch-console/src/settings/SoftRules.tsx`
- **Dependencies:** STORY-003 (the assignment write this decorates)
- **Suggested split:** overlap first, drive time second if the distance lookup takes longer than expected
- **Risks / edge cases:** drive time needs a distance between two addresses; use straight-line distance at 30 mph for release 1 and say so in the warning, since real routing is out of scope

#### Notes
- Marta says the 45-minute threshold "depends on the highway". That is the argument for it being a setting, not a constant, and for not pretending to route

### Out of Scope
- Hard-rule refusals (R005) — [[Dispatcher assigns a crew to a job]]
- Real route distances or optimisation — never in this feature; straight-line is stated in the warning
- Rain-day reflow (R013) — release 2
