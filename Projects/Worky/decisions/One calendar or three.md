---
type: decision-doc
topic: One calendar or three
project: worky
feature: crew-scheduling
created: 2026-09-28
expires: 2026-10-19
lifespan: ephemeral
status: open
round: 1
cssclasses:
  - decision-doc
  - brief
sources:
  - "[[Crew Scheduling PRD]]"
  - "[[Crew Scheduling Design]]"
  - "[[Worky]]"
description: Whether the Client Portal, Crew App and Dispatch Console share one calendar view or each build their own over the same scheduling model — three questions, about ten minutes
tags: [worky, crew-scheduling, decision]
---

# One calendar or three

## 💬 Talk to me

💬 

---

## The short version

Three front-ends will each show the schedule, and the [[Crew Scheduling PRD]] gives each a different slice of it. The question is whether they share one calendar component from Infra's library or each build their own view over the same `scheduling` model. It looks like a code-reuse question; it is actually a question about who can ship without waiting for whom. Phase 3 of the [[Crew Scheduling Design]] is blocked on this, so it needs an answer before the day board is done, not after.

## What I'm assuming

- The three front-ends stay on three stacks (Next.js, React Native, the Console's React app). Nobody is proposing to merge them.
- `scheduling` is the only writer of assignments (design D1), so "one model" is settled. This is only about the view.
- The Infra team can own a shared component, but a shared component is a fourth team's roadmap item, not a free one.
- The Crew App must work offline; whatever it renders has to render from a local copy.

If one of these is wrong, say so up in the box. A wrong assumption changes the questions, not just the answers.

---

## What I found

The three surfaces want different amounts of the same thing.

| | Client Portal | Crew App | Dispatch Console |
|---|---|---|---|
| Shows | one client's jobs, a two-hour window each | one crew's day, in route order | every crew, every job, a whole day |
| Time span | weeks | today and tomorrow | one day at a time, 60 rows |
| Interaction | read; request a reschedule | read; dismiss a change | drag, drop, undo, warn |
| Density | 2–5 items | 3–6 items | ~120 items |
| Offline | no | yes, required | no |
| Team | Client Portal (4) | Crew App (3) | Dispatch (4) |

> [!stats]
> <span class="stat"><b>3</b> stacks</span> <span class="stat"><b>~120</b> items on the busiest view</span> <span class="stat"><b>2–5</b> on the lightest</span> <span class="stat"><b>1</b> surface that must work offline</span>

Two of the three views are lists with dates on them. Only the Console is a calendar in any real sense, and it is the one with the drag performance requirement (NFR002) and the one team that sits next to its users. A shared component would be designed for the Console's needs and then carried by the other two.

The one thing that is genuinely shared is the model and the vocabulary: what an assignment is, what "changed" means, what a window is, how a warning is named. That already lives in `scheduling` and in the design doc.

---

## Q1 · Share one calendar component, or build three views?

*Whether Infra builds one calendar every front-end embeds, or each team builds its own view over the shared model.*

- [ ] **Three views over one model** ==Recommended== — each team ships on its own clock; the shared thing is the API and the vocabulary, not the pixels
- [ ] **One shared calendar in the Infra library** — one component to maintain, and every team waits for it
- [ ] **Shared for Portal and Console, custom for Crew App** — the two web surfaces share; the offline app goes its own way

💬 

> [!info]- Why this matters
> A shared calendar component means Phase 3 waits on Infra to build it, and the Crew App team has to make it render offline from a local copy, which nothing in the library does today. It also means the Console's drag performance work becomes a constraint on a component the Portal shows five items in.
>
> Three views over one model means three teams write three date grids. The duplicated code is small (the Portal and Crew App views are lists), and the thing that must not diverge, the model, cannot diverge because `scheduling` owns it.
>
> | | One shared component | Three views |
> |---|---|---|
> | Ships when | Infra finishes it, then each team integrates | each team is ready |
> | Drift risk | none in the UI; the model is shared either way | cosmetic only |
> | Offline | has to be designed in from day one | Crew App team solves it once, for itself |
> | Owner | Infra (3 people, also on-call) | each team |

> [!example]- Expert detail
> The Crew App is React Native; the Portal and Console are React DOM. A "shared" component is either two implementations behind one API or a web view inside the native app, and the second is what the Crew App team removed in 2025 because it did not work offline. The honest version of option two is therefore option three.

---

## Q2 · Where does the shared vocabulary live?

*If the views are separate, something still has to keep "changed", "window" and "warning" meaning the same thing on every screen.*

- [ ] **A typed client package published from `scheduling`** ==Recommended== — the API types, the warning names and the change diff in one package every front-end imports
- [ ] **In the design doc only** — the words are written down; each team reads them
- [ ] **In the shared component** — only makes sense if Q1 picked the shared calendar

💬 

> [!info]- Why this matters
> The failure this prevents is the Crew App calling something "updated" that the Console calls "moved" and the Portal calls "rescheduled". The model is shared, so the data agrees; the words on screen are what drift. A typed package makes the warning names and the change shape a compile error to get wrong, at the cost of one more thing Core Services publishes.

---

## Q3 · Which surface goes first in Phase 3?

*Phase 3 is the Portal window and the reschedule request. It could start on either end.*

- [ ] **Portal first: arrival windows (R010)** ==Recommended== — the client-facing win, and it only needs a read of route order
- [ ] **Console first: reschedule requests (R011)** — completes the dispatcher's loop before touching the Portal
- [ ] **Both at once** — two teams, two stories, one contract change

💬 

> [!info]- Why this matters
> R010 needs the Client Portal team to add `arrival_window` to the booking record (PRD dependency 2). That is a contract change between two teams and it takes calendar time regardless of who codes first, so starting it first is starting the slow thing first. R011 is entirely inside the Console and can follow in the same phase.
>
> This question only matters if Q1 picks three views. With a shared component both wait on Infra and the order is moot.

---
