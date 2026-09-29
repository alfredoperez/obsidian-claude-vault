---
title: Crew Scheduling
type: prd
project: worky
feature: crew-scheduling
status: draft
created: 2026-09-28
lifespan: project
description: Replace the dispatcher's spreadsheet-and-headset process with a scheduling product across all three front-ends — 14 requirements, availability first, auto-suggest later
inputs:
  journey_map:
  mockups:
  notes: "[[Worky]]"
tags: [worky, crew-scheduling, prd]
---

# PRD — Crew Scheduling

## Problem

> [!note] The schedule lives in one dispatcher's head, and she is on vacation in three weeks.
> Worky assigns roughly 300 jobs a week to 40 crews using a shared spreadsheet, a whiteboard in the Denver office, and phone calls. The scheduling service exists but only stores the result; every constraint (who is lift-certified, who is off Thursday, which truck has the sprayer) is checked by a person. When Marta is out, the next-day schedule takes the backup dispatcher four hours instead of ninety minutes and ships with two or three conflicts that the crews discover at 7am.

Crews find out about their day the evening before, by text, and about changes by phone call. Clients get a four-hour arrival window because nobody can promise tighter. The Crew App shows yesterday's assignment until someone re-syncs it by hand.

Why now: the Denver expansion adds twelve crews in Q1, which the current process cannot absorb, and the two people who can run the whiteboard have both said so.

**Source:** the [[Worky]] brief and three shadowing sessions with dispatch (Sep 8–12). There is no journey map yet; the persona below is drawn from shadowing, not interviews, so treat the metrics as **hypothesis** until the first month of data lands.

**Persona:** Marta, senior dispatcher, Denver. Ten years in, knows every crew by truck. Her day is 6am to 3pm and the schedule is done by 9. The other persona is Diego, a crew lead, who reads the Crew App in the truck and wants to know one thing: where, with whom, and what to load.

## Goals + success metrics

| Metric | Baseline | Target | Source / how measured |
|---|---|---|---|
| Time to build next-day schedule (Denver, senior dispatcher) | ~90 min | ≤ 30 min | Dispatch Console session length, weekly median |
| Same, backup dispatcher | ~4 h | ≤ 45 min | Same, filtered by user |
| Assignment conflicts discovered after 6am | 2–3 per day | 0 per day, one per week tolerated | Conflicts flagged in Crew App or by phone, logged by dispatch |
| Crews notified of tomorrow's assignment by 5pm | ~60 % | 100 % | `scheduling` notification timestamps |
| Client arrival window | 4 h | 2 h | Portal booking record |

> Metrics inherit the confidence of their source. The baselines come from three days of shadowing, not instrumentation, so every row is `Hypothesis — validate before commit`. The first two weeks after release measure the real baseline; targets get re-set then.

## Solution overview

Scheduling becomes a product with three faces on one model. Crews declare availability in the Crew App instead of texting it. Dispatchers build the day on a board in the Dispatch Console that already knows the constraints: it will not let a two-person job go out with one painter, it warns when a crew is double-booked, and it suggests who is free and qualified. Assignments publish to the Crew App the moment they are saved, and a client sees a two-hour window in the Portal derived from the crew's actual route order. Auto-suggest ranks crews; it never assigns on its own. The dispatcher stays the decision-maker.

### Who gets what

| Capability | Client Portal | Crew App | Dispatch Console |
| --- | --- | --- | --- |
| See the schedule | <span class="c-mid">own jobs only</span> | <span class="c-mid">own crew only</span> | <span class="c-ok">everything</span> |
| Declare availability | <span class="c-no">no</span> | <span class="c-ok">yes</span> | <span class="c-ok">on behalf of a crew</span> |
| Assign a crew to a job | <span class="c-no">no</span> | <span class="c-no">no</span> | <span class="c-ok">yes</span> |
| Conflict warnings | <span class="c-no">no</span> | <span class="c-mid">read-only flag</span> | <span class="c-ok">yes, blocking for hard rules</span> |
| Auto-suggest a crew | <span class="c-no">no</span> | <span class="c-no">no</span> | <span class="c-ok">release 2</span> |
| Arrival window | <span class="c-ok">2-hour window</span> | <span class="c-ok">route order</span> | <span class="c-ok">edit</span> |
| Reschedule | <span class="c-mid">request only</span> | <span class="c-no">no</span> | <span class="c-ok">yes</span> |

> [!legend]
> <span class="c-ok chip-key"></span> have / full  <span class="c-mid chip-key"></span> partial or read-only  <span class="c-no chip-key"></span> not on this surface

The matrix is the argument for the [[One calendar or three]] decision: three front-ends, one model, three different amounts of it.

## Functional requirements

| ID | Requirement | Notes |
|---|---|---|
| R001 | A crew member can mark each day of the next four weeks as available, unavailable, or half-day in the Crew App, and the change is visible to dispatch within one minute | Replaces the Sunday-night texts |
| R002 | A crew lead can set a recurring weekly pattern (e.g. off every Thursday) that pre-fills availability and can be overridden per day | Release 2 |
| R003 | A dispatcher sees every job for a chosen day as a list ordered by start time, with each job showing scope, crew size required, and required skills | Skills come from the `jobs` record |
| R004 | A dispatcher can assign a crew to a job by dragging the crew onto the job, and the assignment is saved without a separate confirm step | Undo replaces confirm |
| R005 | System refuses an assignment that breaks a hard rule (crew unavailable, crew size below the job's minimum, missing required certification) and says which rule | Hard rules block; soft rules warn |
| R006 | System warns, without blocking, when an assignment breaks a soft rule (crew already has a job whose window overlaps, drive time between consecutive jobs exceeds 45 min) | Dispatcher can accept the warning |
| R007 | System publishes an assignment to the assigned crew's Crew App within one minute of save, including address, start window, crew members, and load list | Notification timestamp is the metric source |
| R008 | A crew member sees a changed assignment as changed — the old value struck through, the new one highlighted — until they dismiss it | Prevents the 7am surprise |
| R009 | A dispatcher can move a job to another day and the system re-runs the hard and soft rule checks for the new day | Rescheduling is assigning again |
| R010 | System derives a two-hour arrival window for each job from the crew's route order that day and shows it in the Client Portal | Window recomputes when order changes |
| R011 | A client can request a reschedule from the Portal; the request appears in the dispatcher's day view and does nothing until a dispatcher acts on it | Never auto-moves a job |
| R012 | System ranks the crews that could take an unassigned job by availability, skills, and drive time from the previous job, and shows the top three with the reason each ranked where it did | Release 2; suggests, never assigns |
| R013 | A dispatcher can mark a day as a rain day and see every exterior job on it flagged for rescheduling, with interior jobs untouched | Release 2 |
| R014 | A dispatcher can set availability on behalf of a crew member, and the crew member sees who set it and when | For crews who will not use the app |

### Non-functional requirements

| ID | Requirement | Notes |
|---|---|---|
| NFR001 | The Crew App shows the last-synced assignment when offline and labels it with the sync time | Job sites have no signal |
| NFR002 | The day board in the Dispatch Console renders 60 crews × 120 jobs without a visible pause on drag | Denver in Q1 |
| NFR003 | Every assignment change is recorded with who, when, and what it replaced, and the record is readable from the Console | The audit trail billing will eventually need |
| NFR004 | Availability data is visible only to dispatch and the crew member it belongs to | It is personal-time data |

> Every requirement is **testable** — a tester can write a pass/fail check from it.

## Scope

**In:**
- Availability from the Crew App, with a dispatcher override
- The day board: list, drag-to-assign, hard-rule blocking, soft-rule warnings
- Publish to the Crew App with change highlighting
- Two-hour client window derived from route order
- Reschedule request from the Portal, acted on by dispatch

**Out:**
- Automatic assignment — the dispatcher assigns, the system only ranks. The trust is not there yet and a wrong auto-assignment costs a whole crew-day
- Billing changes — a moved job keeps its invoice date until someone opens the billing code deliberately; see [[Worky]] for why
- Route optimisation — the crew's route order is whatever the dispatcher set; we derive windows from it, we do not compute it
- Payroll or hours tracking — availability is not a timesheet

**Future (deferred):**
- Auto-suggest ranking (R012) and rain-day reflow (R013) — release 2, once the day board has a month of real data
- Recurring availability patterns (R002) — release 2
- Client self-service rescheduling into open slots

## Technical considerations

- `scheduling` today stores `(job_id, crew_id, date)` and nothing else. Hard rules need crew skills and availability, which live in `crew`; the design doc decides whether `scheduling` reads them at check time or keeps a copy
- The Crew App is offline-first. Assignment publish is a push plus a pull-on-open, never push alone
- The Dispatch Console board is the biggest UI Worky has built. Drag performance (NFR002) rules out re-rendering the whole day on every drop
- Arrival windows (R010) leak into the Portal's existing booking record, which the Client Portal team owns. That is a contract change between two teams, not a scheduling feature
- Every rule in R005/R006 is a function of data that already exists. No new data entry is required to ship release 1 except availability itself

## Dependencies + risks

| # | Type | What | Owner | Mitigation |
|---|---|---|---|---|
| 1 | dep | `crew` must expose skills and certifications as data, not free text in a notes field | Core Services | Backfill script for the 40 current crews; new crews entered structured from day one |
| 2 | dep | Client Portal booking record gains an `arrival_window` field | Client Portal team | Ship as nullable; Portal shows the old four-hour text until it is populated |
| 3 | risk | Crews do not enter availability, so dispatch keeps texting and the board is wrong | Crew App team | R014 lets dispatch enter it; measure the share of crew-entered vs dispatch-entered weekly |
| 4 | risk | Dispatchers trust the board over their own knowledge and stop catching what the rules miss | Dispatch team | Soft rules warn, never block; the first month reviews every override with dispatch |
| 5 | risk | A moved job changes an invoice date and nobody notices until month-end | Core Services | Out of scope, explicitly; the audit record (NFR003) is what billing will reconcile against later |

> [!warning] The risk nobody wants to name
> The schedule is Marta's expertise, and the board makes that expertise legible to everyone including her manager. If the rollout reads as replacing her rather than equipping her, the best dispatcher in the company will make sure the board is wrong. The Dispatch team sits ten feet from her; the first month is theirs to get right.

## Milestones

Coarse phasing. The full slicing, with a coverage check per requirement, lives in [[Crew Scheduling Roadmap]].

- **M1 — Availability:** R001, R014 in the Crew App; dispatch can see it. Nothing else changes; the spreadsheet stays
- **M2 — The day board:** R003–R009. The spreadsheet goes away for Denver
- **M3 — Clients and suggestions:** R010, R011, then R002, R012, R013

## Open questions

- [ ] **[blocking]** Do the three front-ends share one calendar component or each build their own view over the same data? Decided in [[One calendar or three]]
- [ ] **[needs-research]** How many crews will actually enter their own availability? The 60 % notification baseline suggests engagement is low; two weeks of M1 answers this
- [ ] **[clarify-with-stakeholder]** Does a rescheduled job keep its estimate, or does moving it re-open the quote? Owner: the Core Services lead, with whoever last touched billing
- [ ] **[clarify-with-stakeholder]** Which soft rule threshold for drive time — 45 minutes is a guess from shadowing, Marta says it depends on the highway
