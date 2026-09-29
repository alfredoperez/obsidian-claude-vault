---
title: Crew Scheduling Roadmap
type: roadmap
project: worky
feature: crew-scheduling
status: planning
created: 2026-09-28
lifespan: project
description: Crew Scheduling sliced into Now, Next and Later, each slice tied to the PRD requirement IDs it covers, so any drift between the plan and the PRD shows in the coverage table.
inputs:
  prd: "[[Crew Scheduling PRD]]"
slices: [now, next, later]
tags: [worky, crew-scheduling, roadmap]
---

# Roadmap — Crew Scheduling

## Summary

Crew Scheduling ships in three slices, each of which changes something a dispatcher or a crew can feel. Now gets availability into the Crew App and onto the dispatcher's screen, and changes nothing else, so the spreadsheet stays. Next is the day board: assign, warn, publish, and show changes, which is what lets Denver retire the spreadsheet. Later adds the client's arrival window, reschedule requests and the smarter suggestions. The bet behind the slicing is that crews will only enter their own availability if the first thing it does is stop the 6 a.m. phone calls, so that has to land, and be measured, before any dispatcher tooling depends on it.

> [!note] The order is a dependency chain, not a priority list
> Availability is the input to every rule check. Nothing in Next can be trusted until Now has real data in it.

## Slice: Now

**Outcome:** A crew member can tell Worky which days they can work, and a dispatcher can see it before calling anyone.

**Requirements covered:** R001, R014

**Depends on:** —

**Deferred from this slice:** R002 (recurring weekly patterns). It is a convenience on top of R001 and only earns its build once we know crews enter availability at all.

**Definition of done:**
- Crew Denver-1 enters four weeks of availability in the Crew App without help.
- The dispatcher's day view shows each crew as available, unavailable or half-day, and who set it.
- After two weeks, at least 60 percent of active crew members have entered availability, or the slice's open question is answered with a number.

---

## Slice: Next

**Outcome:** A dispatcher plans a whole day in one screen, and each crew sees its assignment change as it changes.

**Requirements covered:** R003, R004, R005, R006, R007, R008, R009

**Depends on:** Now landed

**Deferred from this slice:** The arrival window for clients (R010) waits for route order to be trustworthy, which needs a few weeks of real assignments.

**Definition of done:**
- Denver dispatch plans a full week without opening the spreadsheet.
- A hard-rule violation (crew unavailable, crew too small, missing certification) is refused with the reason shown.
- An assignment reaches the crew's phone within one minute, and a moved job shows the old value struck through.

---

## Slice: Later

**Outcome:** Clients know when the crew will arrive, and dispatchers get help choosing which crew.

**Requirements covered:** R010, R011, R002, R012, R013

**Depends on:** Next landed

**Deferred from this slice:** Multi-region rules and automatic rescheduling are not in this PRD at all; see its Out of scope list.

**Definition of done:**
- A client sees a two-hour arrival window in the Portal and can request a reschedule that does nothing until a dispatcher accepts it.
- A rain day flags every exterior job on it and leaves interior jobs alone.
- Suggested crews are ranked by availability, skills and drive time, and the dispatcher can still override.

---

## Coverage check

| Requirement | Title (short) | Slice | Notes |
|---|---|---|---|
| R001 | Crew enters four weeks of availability | Now | |
| R002 | Recurring weekly availability pattern | Later | Deferred from Now on purpose |
| R003 | Day view of all jobs by start time | Next | |
| R004 | Drag a crew onto a job | Next | |
| R005 | Refuse hard-rule violations | Next | |
| R006 | Warn on soft-rule violations | Next | |
| R007 | Publish assignments to the Crew App | Next | |
| R008 | Show changed assignments as changed | Next | |
| R009 | Move a job to another day | Next | |
| R010 | Client arrival window | Later | Needs real route data from Next |
| R011 | Client reschedule request | Later | |
| R012 | Ranked crew suggestions | Later | |
| R013 | Rain-day flagging | Later | |
| R014 | Dispatcher sets availability for a crew member | Now | For crews who will not use the app yet |

> Every PRD requirement appears in this table. The four non-functional requirements (NFR001–004) apply to every slice and are checked in each slice's definition of done, not sliced.

## Open decisions

- **Recurring patterns (R002) might belong in Now.** If crew leads say weekly patterns are the reason they would enter anything, moving R002 earlier is cheap. What would flip it: the first week of Now showing crews entering days one at a time and stopping.
- **Whether Next needs the calendar decision resolved first.** [[One calendar or three]] decides whether the three front-ends share one component. Next builds the day view, so it should land before Next starts.
- **Infra work not in the PRD:** push delivery inside one minute (R007) needs a change in the notifications service, owned by a team that is not on this roadmap yet.
