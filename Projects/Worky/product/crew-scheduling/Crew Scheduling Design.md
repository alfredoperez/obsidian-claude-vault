---
title: Crew Scheduling — design
type: spec
project: worky
feature: crew-scheduling
status: active
lifespan: project
description: How the scheduling service grows from a three-column table into the thing the PRD needs, in four phases — rules first, then the board, then the front-ends read one model
supersedes:
tags: [worky, crew-scheduling, design]
---

# Crew Scheduling — design of record

This is how [[Crew Scheduling PRD]] gets built. It decides what `scheduling` owns, where the rules run, and in what order the three front-ends get their views. It does not decide what the board looks like; that belongs to the Dispatch team and their users ten feet away.

> [!note] One model, checked in one place, read three ways.
> The rules move out of Marta's head and into `scheduling`, which becomes the only service that can write an assignment. The front-ends stop being CRUD screens over a table and become three views of a model that already knows what is allowed.

## What exists today

`scheduling` is a table: `assignment(job_id, crew_id, date)` with a REST layer that lets any front-end write a row. Nothing checks anything. `crew` holds skills as a free-text `notes` column ("lift cert exp 3/27, no spray"). `jobs` has `crew_size_min` and a `scope` enum that implies required skills but does not state them.

> [!figure] Today every front-end writes assignments; nothing checks them
>
> ```mermaid
> %%{init: {'theme':'base','themeVariables':{'primaryColor':'#eef4fd','primaryTextColor':'#1f2428','primaryBorderColor':'#3d59a1','lineColor':'#8b939c','fontFamily':'Geist, ui-sans-serif, sans-serif','fontSize':'13px','clusterBkg':'#f8fafc','clusterBorder':'#dde2e8','edgeLabelBackground':'#ffffff'}}}%%
> flowchart LR
>   DC["Dispatch Console"] -->|"write row"| T[("assignment table")]
>   CA["Crew App"] -->|"read row"| T
>   SS["spreadsheet"] -.->|"is the real schedule"| M["Marta"]
>   M -->|"types it in"| DC
> ```

## Decisions

> [!decision] D1 · `scheduling` is the only writer of assignments
> **because** a rule checked in three front-ends is three rules that drift; a rule checked where the write happens is one.
> **revisit** if a front-end needs to assign offline. The Crew App does not (crews never assign); the Console is never offline.

> [!decision] D2 · Rules read `crew` and `jobs` at check time; `scheduling` keeps no copy
> **because** availability changes minute to minute and a cached copy is a conflict waiting to be discovered at 7am. The check is a handful of indexed reads per drop, which NFR002 can afford.
> **revisit** if check latency on the board exceeds 200 ms at Denver scale. Then cache availability only, with a one-minute TTL, and say so on the board.

> [!decision] D3 · Hard rules are a closed list in code; soft rules are data
> **because** hard rules (unavailable, under-crewed, uncertified) are few and do not change; soft rules (drive time, overlap tolerance) are thresholds dispatchers argue about and should be able to change without a deploy.
> **revisit** never, probably. If a fourth hard rule appears it gets added to the list.

> [!decision] D4 · Skills become a structured table before any rule ships
> **because** every hard rule needs them, and "lift cert exp 3/27" in a notes column is not data. The backfill is 40 crews and one afternoon.
> **revisit** not applicable; this is a prerequisite, not a choice.

## The model

```
assignment    (id, job_id, crew_id, date, route_order, published_at, replaced_by)
crew_skill    (crew_member_id, skill, certified_until)
availability  (crew_member_id, date, state: available|unavailable|half, set_by, set_at)
soft_rule     (key, threshold, unit)     -- drive_time_max: 45 min; overlap_tolerance: 0 min
```

An assignment is never updated. Moving a job writes a new row and points the old one's `replaced_by` at it, which is the audit trail (NFR003) and the "what changed" the Crew App highlights (R008) in one structure.

## The check

Every write to `assignment` runs the same function, whether it came from a drag on the board (R004), a move to another day (R009), or a dispatcher acting on a client request (R011).

> [!figure] One check, three callers; hard rules block, soft rules warn
>
> ```mermaid
> %%{init: {'theme':'base','themeVariables':{'primaryColor':'#eef4fd','primaryTextColor':'#1f2428','primaryBorderColor':'#3d59a1','lineColor':'#8b939c','fontFamily':'Geist, ui-sans-serif, sans-serif','fontSize':'13px','clusterBkg':'#f8fafc','clusterBorder':'#dde2e8','edgeLabelBackground':'#ffffff'}}}%%
> flowchart LR
>   W["write request"] --> H{"hard rules"}
>   H -->|"fails"| R["refuse · name the rule"]
>   H -->|"passes"| S{"soft rules"}
>   S -->|"breaks one"| WN["save · warn · log the override"]
>   S -->|"clean"| SV["save"]
>   SV --> P["publish to Crew App"]
>   WN --> P
>   classDef anchor fill:#fde68a,stroke:#b45309;
>   class H anchor;
> ```

The pipeline is <span class="step">validate</span> <span class="step">save</span> <span class="step">publish</span> <span class="step">recompute windows</span>. Publish is a push to the Crew App plus a pull on app open, because the truck has no signal and a push alone is a lie (NFR001). Recomputing arrival windows (R010) is last and asynchronous: it changes the Portal, and the Portal can be a minute behind.

## Phases

> [!phase]- Phase 0 · Skills as data · <code class="done">done</code>
> **shipped** `crew_skill` table, the backfill of 40 crews, and the Crew App form that captures it for new hires.
> **waits on** nothing.

> [!phase]+ Phase 1 · Availability and the check · <code class="now">now</code>
> **does** `availability` table, R001 and R014 in the Crew App, the hard-rule check as a function nothing calls yet, and a read-only availability strip in the Console so dispatch stops asking.
> **why now** it is the only phase that needs no board. Two weeks of real availability data before the board exists tells us whether crews will use the app at all (risk 3 in the PRD).
> **waits on** nothing.

> [!phase]- Phase 2 · The day board · <code class="next">next</code>
> **does** R003–R009. `scheduling` becomes the only writer (D1); the Console's board calls the check on every drop; publish and the change highlight land in the Crew App.
> **waits on** Phase 1, and the Dispatch team's board prototype being through its second round with Marta.

> [!phase]- Phase 3 · Clients · <code class="queued">queued</code>
> **does** R010 arrival windows into the Portal booking record, R011 reschedule requests into the day view.
> **waits on** the Client Portal team adding `arrival_window` (dependency 2), and the [[One calendar or three]] decision, which sets whether the Portal's view is shared code or its own.

> [!phase]- Phase 4 · Suggestions and weather · <code class="parked">parked</code>
> **does** R002 recurring patterns, R012 ranked suggestions, R013 rain-day reflow.
> **waits on** a month of board data. Ranking crews by drive time needs the real route orders, and rain-day reflow needs enough moved jobs to know what dispatchers actually do with them. Parked, not queued, because the blocker is outside the work.

## What this deliberately does not solve

- **Billing.** A moved job keeps its invoice date. `replaced_by` is the record billing will reconcile against when someone owns billing again; until then, that corner of [[Worky]] stays closed.
- **Route optimisation.** `route_order` is whatever the dispatcher set by dragging. Windows derive from it; nothing computes it.
- **Automatic assignment.** R012 ranks and shows its reasons. The write still comes from a human.

> [!warning] The check is the product; the board is the demo.
> It is tempting to build the board first because it is what people will screenshot. If the board ships before the check, it is a prettier spreadsheet, and dispatch will keep the real one open in the other window. Phase 1 before Phase 2, even though Phase 1 is invisible.

> [!tip] First thing to build
> The hard-rule function with three tests: unavailable crew, under-crewed job, expired certification. Everything else in this document calls it.
