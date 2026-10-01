---
type: reference
project: worky
lifespan: durable
description: Every component in Components.md rendered live with Worky content, with its markdown folded underneath; open this first
tags: [reference, components, vault-css, worky]
---

# Component gallery

Every component the vault styles, rendered with Worky content. Each section says what it is for, shows it live, and folds the markdown underneath so you can copy it. The rules for each live in [[Components]].

## Callouts

**Use it for:** the argument up front, the one risk, the settled fact, and detail you fold away.

> [!note] One model, checked in one place, read three ways.
> The rules move into `scheduling`, which becomes the only service that can write an assignment.

> [!warning] Crews will not enter availability unless it stops the 6am phone calls.
> If fewer than 60 percent enter it in two weeks, Phase 2 waits.

> [!success] Skills are data now.
> All 40 crews are backfilled and the new-hire form writes to `crew_skill`.

> [!tip] Build the hard-rule check first
> It is the only piece every later phase calls.

> [!example]- Data and acceptance
> The `availability` table, one row per crew member per day.

> [!example]- Markdown
> ```markdown
> > [!note] One model, checked in one place, read three ways.
> > The rules move into `scheduling`, which becomes the only service that can write an assignment.
>
> > [!warning] Crews will not enter availability unless it stops the 6am phone calls.
> > If fewer than 60 percent enter it in two weeks, Phase 2 waits.
>
> > [!success] Skills are data now.
> > All 40 crews are backfilled and the new-hire form writes to `crew_skill`.
>
> > [!tip] Build the hard-rule check first
> > It is the only piece every later phase calls.
>
> > [!example]- Data and acceptance
> > The `availability` table, one row per crew member per day.
> ```

## Decision question

**Use it for:** a choice the reader answers in the file: options, the recommendation visible but never ticked, and a slot to type in.

## Q1 · Share one calendar component, or build three views?

*Whether Infra builds one calendar every front-end embeds, or each team builds its own view over the shared model.*

- [ ] **Three views over one model** ==Recommended==, each team ships on its own clock
- [ ] **One shared calendar in the Infra library**, one component to maintain, every team waits for it

💬 

> [!info]- Why this matters
> The three surfaces want different amounts of the same schedule.

> [!example]- Markdown
> ```markdown
> ## Q1 · Share one calendar component, or build three views?
>
> *Whether Infra builds one calendar every front-end embeds, or each team builds its own view over the shared model.*
>
> - [ ] **Three views over one model** ==Recommended==, each team ships on its own clock
> - [ ] **One shared calendar in the Infra library**, one component to maintain, every team waits for it
>
> 💬
>
> > [!info]- Why this matters
> > The three surfaces want different amounts of the same schedule.
> ```

## Capture slot

**Use it for:** evidence a person still has to paste in, so the hole is impossible to miss.

> [!capture] Screenshot · the Denver spreadsheet on a Monday morning

> [!example]- Markdown
> ```markdown
> > [!capture] Screenshot · the Denver spreadsheet on a Monday morning
> ```

## Feedback region

**Use it for:** a note the reader leaves for Claude mid-read; Claude acts on it and removes it.

---

<span class="badge-feedback">FEEDBACK</span> The drive-time limit in D3 should be 45 minutes, not 60.

---

> [!example]- Markdown
> ```markdown
> ---
>
> <span class="badge-feedback">FEEDBACK</span> The drive-time limit in D3 should be 45 minutes, not 60.
>
> ---
> ```

## Status badges

**Use it for:** tagging each API or decision as new, existing, later or open, inside prose or table cells.

**APIs:** <span class="badge-new">new</span> `POST /assignments` · <span class="badge-existing">existing</span> `GET /jobs` · <span class="badge-later">later</span> `GET /suggestions`

<span class="badge-open">open</span> Who owns billing when a job moves days is still unassigned.

> [!legend]
> <span class="badge-new">new</span> built for this feature  <span class="badge-existing">existing</span> already in the app  <span class="badge-later">later</span> follow-up release  <span class="badge-open">open</span> unresolved

> [!example]- Markdown
> ```markdown
> **APIs:** <span class="badge-new">new</span> `POST /assignments` · <span class="badge-existing">existing</span> `GET /jobs` · <span class="badge-later">later</span> `GET /suggestions`
>
> <span class="badge-open">open</span> Who owns billing when a job moves days is still unassigned.
>
> > [!legend]
> > <span class="badge-new">new</span> built for this feature  <span class="badge-existing">existing</span> already in the app  <span class="badge-later">later</span> follow-up release  <span class="badge-open">open</span> unresolved
> ```

## Cards

**Use it for:** a two or three way compare where the sides must read as different things at a glance.

> [!cards|2]
> > [!card|blue] After Phase 0 and 1, the MVP
> > Crews enter availability and dispatch sees it.
>
> > [!card|green] At the full vision
> > One board plans the day, warns and publishes.

> [!example]- Markdown
> ```markdown
> > [!cards|2]
> > > [!card|blue] After Phase 0 and 1, the MVP
> > > Crews enter availability and dispatch sees it.
> >
> > > [!card|green] At the full vision
> > > One board plans the day, warns and publishes.
> ```

## Tickets and phases

**Use it for:** a unit of work with its size, and for a phase rail where only the phase in flight stays open.

> [!ticket] A · Hard-rule check as a function · `small`
> **what** One function that says whether an assignment breaks a hard rule.
> **why** Every later phase calls it; nothing calls it yet.

> [!phase]- Phase 0 · Skills as data · <code class="done">done</code>
> **shipped** `crew_skill` table and the backfill of 40 crews.

> [!phase]+ Phase 1 · Availability and the check · <code class="now">now</code>
> **does** `availability` table, R001 and R014, the hard-rule check.
> **waits on** nothing.

> [!phase]- Phase 2 · The day board · <code class="next">next</code>
> **does** R003 to R009.

> [!phase]- Phase 3 · Clients · <code class="queued">queued</code>
> **does** arrival windows and reschedule requests.

> [!phase]- Phase 4 · Suggestions and weather · <code class="parked">parked</code>
> **does** ranked suggestions and rain-day reflow.

> [!example]- Markdown
> ```markdown
> > [!ticket] A · Hard-rule check as a function · `small`
> > **what** One function that says whether an assignment breaks a hard rule.
> > **why** Every later phase calls it; nothing calls it yet.
>
> > [!phase]- Phase 0 · Skills as data · <code class="done">done</code>
> > **shipped** `crew_skill` table and the backfill of 40 crews.
>
> > [!phase]+ Phase 1 · Availability and the check · <code class="now">now</code>
> > **does** `availability` table, R001 and R014, the hard-rule check.
> > **waits on** nothing.
>
> > [!phase]- Phase 2 · The day board · <code class="next">next</code>
> > **does** R003 to R009.
>
> > [!phase]- Phase 3 · Clients · <code class="queued">queued</code>
> > **does** arrival windows and reschedule requests.
>
> > [!phase]- Phase 4 · Suggestions and weather · <code class="parked">parked</code>
> > **does** ranked suggestions and rain-day reflow.
> ```

## Capability matrix

**Use it for:** who gets what across surfaces, with colored cells and a legend built from the same classes.

| Capability | Client Portal | Crew App | Dispatch Console |
| --- | --- | --- | --- |
| See the schedule | <span class="c-mid">own jobs only</span> | <span class="c-mid">own crew only</span> | <span class="c-ok">everything</span> |
| Declare availability | <span class="c-no">no</span> | <span class="c-ok">yes</span> | <span class="c-ok">on behalf of a crew</span> |
| Assign a crew to a job | <span class="c-no">no</span> | <span class="c-no">no</span> | <span class="c-ok">yes</span> |

> [!legend]
> <span class="c-ok chip-key"></span> have  <span class="c-mid chip-key"></span> partial  <span class="c-no chip-key"></span> not on this surface

> [!example]- Markdown
> ```markdown
> | Capability | Client Portal | Crew App | Dispatch Console |
> | --- | --- | --- | --- |
> | See the schedule | <span class="c-mid">own jobs only</span> | <span class="c-mid">own crew only</span> | <span class="c-ok">everything</span> |
> | Declare availability | <span class="c-no">no</span> | <span class="c-ok">yes</span> | <span class="c-ok">on behalf of a crew</span> |
> | Assign a crew to a job | <span class="c-no">no</span> | <span class="c-no">no</span> | <span class="c-ok">yes</span> |
>
> > [!legend]
> > <span class="c-ok chip-key"></span> have  <span class="c-mid chip-key"></span> partial  <span class="c-no chip-key"></span> not on this surface
> ```

## Story map

**Use it for:** a small map: activities across the top, releases down the side, stories as sticky notes.

> [!storymap] Crew scheduling by release
> | | Set availability | Build the day | Notify the crew |
> | --- | --- | --- | --- |
> | **Today** | <span class="story-cut">phone calls</span> | <span class="story-cut">spreadsheet</span> | <span class="story-cut">texts at 6am</span> |
> | **Release 1** | <span class="story-done">weekly availability</span> | <span class="story">drag crew onto job</span> | <span class="story">publish to Crew App</span> |

> [!example]- Markdown
> ```markdown
> > [!storymap] Crew scheduling by release
> > | | Set availability | Build the day | Notify the crew |
> > | --- | --- | --- | --- |
> > | **Today** | <span class="story-cut">phone calls</span> | <span class="story-cut">spreadsheet</span> | <span class="story-cut">texts at 6am</span> |
> > | **Release 1** | <span class="story-done">weekly availability</span> | <span class="story">drag crew onto job</span> | <span class="story">publish to Crew App</span> |
> ```

## Tree

**Use it for:** showing where things live in a folder, annotated line by line.

> [!tree] Projects/Worky/
> - Worky.md · *the hub: what Worky is, the teams*
> - **decisions/** · *open questions for the reader*
> - **product/crew-scheduling/** · *PRD, design, roadmap, story map*
>     - **stories/** · *one note per story*
> - **updates/** · *weekly updates*

> [!example]- Markdown
> ```markdown
> > [!tree] Projects/Worky/
> > - Worky.md · *the hub: what Worky is, the teams*
> > - **decisions/** · *open questions for the reader*
> > - **product/crew-scheduling/** · *PRD, design, roadmap, story map*
> >     - **stories/** · *one note per story*
> > - **updates/** · *weekly updates*
> ```

## Stats

**Use it for:** two to five numbers that are the finding.

> [!stats]
> <span class="stat"><b>90 min</b> to build tomorrow today</span> <span class="stat"><b>30 min</b> target</span> <span class="stat"><b>2 to 3</b> conflicts after 6am, daily</span>

> [!example]- Markdown
> ```markdown
> > [!stats]
> > <span class="stat"><b>90 min</b> to build tomorrow today</span> <span class="stat"><b>30 min</b> target</span> <span class="stat"><b>2 to 3</b> conflicts after 6am, daily</span>
> ```

## Lead

**Use it for:** one framing paragraph directly under a note's title, at most once per note.

> [!lead]
> Crew scheduling replaces a spreadsheet and a headset with one model the three front-ends read. Availability lands first because every rule reads it.

> [!example]- Markdown
> ```markdown
> > [!lead]
> > Crew scheduling replaces a spreadsheet and a headset with one model the three front-ends read. Availability lands first because every rule reads it.
> ```

## Chip

**Use it for:** a neutral tag in prose; it labels, it never judges.

Tagged: <span class="chip">availability</span> <span class="chip">Denver</span> <span class="chip">Phase 1</span>

> [!example]- Markdown
> ```markdown
> Tagged: <span class="chip">availability</span> <span class="chip">Denver</span> <span class="chip">Phase 1</span>
> ```

## Steps

**Use it for:** a short pipeline where the order is the point; the arrows draw themselves.

<span class="step">drop crew</span> <span class="step">check hard rules</span> <span class="step">save</span> <span class="step">publish</span>

> [!example]- Markdown
> ```markdown
> <span class="step">drop crew</span> <span class="step">check hard rules</span> <span class="step">save</span> <span class="step">publish</span>
> ```

## Kbd

**Use it for:** keyboard shortcuts in a how-to.

Undo the last assignment with <kbd>Cmd</kbd><kbd>Z</kbd>.

> [!example]- Markdown
> ```markdown
> Undo the last assignment with <kbd>Cmd</kbd><kbd>Z</kbd>.
> ```

## Pull quote

**Use it for:** the one line worth lifting out of an article or a retro.

> [!quote]
> The schedule lives in one dispatcher's head, and she is on vacation in three weeks.

> [!example]- Markdown
> ```markdown
> > [!quote]
> > The schedule lives in one dispatcher's head, and she is on vacation in three weeks.
> ```

## Terminal

**Use it for:** command output that is already captured, so it reads as a terminal and not a code listing.

> [!terminal] migrate the scheduling database
> ```bash
> $ npm run migrate -- --service scheduling
> applied 0007_availability.sql (12 ms)
> applied 0008_assignment_replaced_by.sql (9 ms)
> 2 migrations, 0 pending
> ```

> [!example]- Markdown
> ````markdown
> > [!terminal] migrate the scheduling database
> > ```bash
> > $ npm run migrate -- --service scheduling
> > applied 0007_availability.sql (12 ms)
> > applied 0008_assignment_replaced_by.sql (9 ms)
> > 2 migrations, 0 pending
> > ```
> ````

## Figure

**Use it for:** a Mermaid diagram with a caption that states the takeaway.

> [!figure] One check, three callers; hard rules block, soft rules warn
>
> ```mermaid
> %%{init: {'theme':'base','themeVariables':{'primaryColor':'#eef4fd','primaryTextColor':'#1f2428','primaryBorderColor':'#3d59a1','lineColor':'#8b939c','fontFamily':'Geist, ui-sans-serif, sans-serif','fontSize':'13px','clusterBkg':'#f8fafc','clusterBorder':'#dde2e8','edgeLabelBackground':'#ffffff'}}}%%
> flowchart LR
>   B["Dispatch board"] --> K["hard-rule check"]
>   A["Crew App"] --> K
>   P["Client Portal"] --> K
>   K --> S["save or refuse"]
> ```

> [!example]- Markdown
> ````markdown
> > [!figure] One check, three callers; hard rules block, soft rules warn
> >
> > ```mermaid
> > %%{init: {'theme':'base','themeVariables':{'primaryColor':'#eef4fd','primaryTextColor':'#1f2428','primaryBorderColor':'#3d59a1','lineColor':'#8b939c','fontFamily':'Geist, ui-sans-serif, sans-serif','fontSize':'13px','clusterBkg':'#f8fafc','clusterBorder':'#dde2e8','edgeLabelBackground':'#ffffff'}}}%%
> > flowchart LR
> >   B["Dispatch board"] --> K["hard-rule check"]
> >   A["Crew App"] --> K
> >   P["Client Portal"] --> K
> >   K --> S["save or refuse"]
> > ```
> ````
