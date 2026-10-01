---
type: project
project: worky
status: active
lifespan: project
description: A fictional field-service company that schedules painter crews — the subject every PRD, story map, story and decision doc in this vault is about
tags: [worky, project, fictional]
---

# Worky

Worky schedules painter crews. A client books a job through a portal, a dispatcher builds the day, a crew of two to four painters shows up with the right ladders, and someone bills for it afterwards. Roughly 40 crews across three metro areas, about 300 jobs a week in season, half that in winter. Everything in this folder is fictional; it exists so the documents in `product/` have a real subject to argue about instead of lorem ipsum.

> [!note] Why a painting company
> Crew scheduling has every shape a product doc needs: a calendar, a constraint solver nobody wants to write, three audiences who each think the schedule is theirs, and weather. It is small enough to hold in your head and messy enough that the trade-offs are real.

## The architecture

Three front-ends, three core services, and billing in a corner.

> [!figure] Three front-ends over three services; billing reads from all of them and writes to none
>
> ```mermaid
> %%{init: {'theme':'base','themeVariables':{'primaryColor':'#eef4fd','primaryTextColor':'#1f2428','primaryBorderColor':'#3d59a1','lineColor':'#8b939c','fontFamily':'Geist, ui-sans-serif, sans-serif','fontSize':'13px','clusterBkg':'#f8fafc','clusterBorder':'#dde2e8','edgeLabelBackground':'#ffffff'}}}%%
> flowchart LR
>   subgraph fe["Front-ends"]
>     CP["Client Portal"]
>     CA["Crew App"]
>     DC["Dispatch Console"]
>   end
>   subgraph core["Core services"]
>     J["jobs"]
>     C["crew"]
>     S["scheduling"]
>   end
>   B["billing"]
>   CP --> J
>   CA --> C
>   DC --> S
>   S --> J
>   S --> C
>   J --> B
>   classDef corner fill:#f4f4f5,stroke:#a1a1aa,stroke-dasharray: 4 3;
>   class B corner;
> ```

| Piece | What it is | Owner |
|---|---|---|
| **Client Portal** | Where a homeowner or property manager books a job, sees the estimate, and watches for the crew | Client Portal team |
| **Crew App** | The phone app a painter opens at 6:40am: today's jobs, the address, who else is on the crew, what to load | Crew App team |
| **Dispatch Console** | The desktop board a dispatcher lives in all day: every job, every crew, drag one onto the other | Dispatch team |
| **jobs** | The job record: address, scope, estimate, status from *quoted* to *closed* | Core Services |
| **crew** | People, skills (spray, lift-certified, lead-safe), availability, the truck they drive | Core Services |
| **scheduling** | The assignment of crews to jobs on days. Today a thin CRUD layer over a table; the constraint logic lives in dispatchers' heads | Core Services |
| **billing** | Invoices from closed jobs. Works, untouched since 2024, nobody currently owns it | — |

## The teams

| Team | Owns | Size | Note |
|---|---|---|---|
| Client Portal | the portal front-end | 4 | Next.js, ships weekly |
| Crew App | the crew front-end | 3 | React Native; offline-first because job sites have no signal |
| Dispatch | the console front-end | 4 | The heaviest UI in the company; the users sit ten feet from the team |
| Core Services | jobs, crew, scheduling | 5 | Owns the data model every front-end reads |
| Infra | CI, deploys, the on-call rota, the shared component library | 3 | Also the de-facto owner of anything nobody claims |

A sixth team, **Billing**, built the billing service in 2023 and was disbanded in the 2024 reorg. The service still runs. Its README is accurate, its tests pass, and every change to it is made by whichever Core Services engineer drew the short straw. That corner of the diagram is the one every scheduling decision has to route around: a job that moves days moves its invoice date, and nobody wants to open that code.

## The folder

> [!tree] Projects/Worky/
> - Worky.md · *this hub: what Worky is, the teams, the current work*
> - Worky Dashboard.md · *live Dataview tables*
> - **decisions/** · *questions the reader answers in the file*
>     - One calendar or three.md · *the open decision*
> - **meetings/** · *one note per meeting*
> - **product/crew-scheduling/** · *the live feature*
>     - Crew Scheduling PRD.md · *requirements, R001 onward*
>     - Crew Scheduling Roadmap.md · *three slices tied to IDs*
>     - Crew Scheduling Design.md · *the design of record, in phases*
>     - Crew Scheduling Story Map.canvas · *the wall*
>     - Crew Board.base · *stories as a Kanban board and a table*
>     - **stories/** · *four stories, ready to file*
> - **updates/** · *weekly updates*

## Current work

The live feature is **crew scheduling**: replacing the table-and-headset process with an actual scheduling product across all three front-ends.

- [[Crew Scheduling PRD]] — the requirements, R001 onward, and which front-end gets what
- [[Crew Scheduling Story Map.canvas|Crew Scheduling Story Map]] — the wall: five activities across the top, two release slices below
- [[Worky Dashboard]] — live tables: stories by status, open decisions, latest updates, what changed this week
- [[Crew Scheduling Design]] — how the scheduling service grows to carry it, in phases
- `product/crew-scheduling/stories/` — the first four stories, ready to file
- [[One calendar or three]] — the open decision: do the three front-ends share one calendar view
- [[Crew update (components)]] and [[Crew update (plain)]] · this week's update, the same facts in two shapes
- [[2026-09-24 Dispatch sync]] · the last dispatch sync, with the spreadsheet still to capture
- [[2026-09-28]] · the daily note for the week's work
- [[Team Topologies notes]] · the reading behind the team split

## What is out of scope for the fiction

No real company, no real people, no real numbers. The metrics in the PRD are plausible for a business this size and were chosen to make the trade-offs bite, not measured anywhere.
