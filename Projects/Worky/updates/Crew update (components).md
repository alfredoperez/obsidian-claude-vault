---
date: 2026-09-28
type: update
project: worky
feature: crew-scheduling
lifespan: ephemeral
description: Week of 28 September for crew scheduling, built from vault components; the same facts as the plain version, for comparison
tags: [worky, crew-scheduling, update, components]
---

# Crew scheduling update, week of 28 September

> [!note] Availability is the only thing that has to land this month.
> Everything in Phase 2 reads it, so the board waits until crews are actually entering it.

## This week

> [!stats]
> <span class="stat"><b>40</b> crews backfilled</span> <span class="stat"><b>22 / 38</b> Denver members entered</span> <span class="stat"><b>58%</b> of the 60% target</span>

- The `availability` table is merged and backfilled for all 40 crews.
- The Crew App availability screen is in beta with Crew Denver-1.
- The Console shows each crew as available, unavailable or half-day, read-only.

## Where the MVP ends

> [!cards|2]
> > [!card|blue] After Phase 0 and 1, the MVP
> > Crews enter availability and dispatch sees it.
>
> > [!card|green] At the full vision
> > One board plans the day, warns and publishes.

## Phases

> [!phase]- Phase 0 · Skills as data · <code class="done">done</code>
> **shipped** `crew_skill` table, the backfill of 40 crews, the new-hire form.

> [!phase]+ Phase 1 · Availability and the check · <code class="now">now</code>
> **does** `availability` table, R001 and R014, the hard-rule check, a read-only strip in the Console.
> **waits on** nothing.

> [!phase]- Phase 2 · The day board · <code class="next">next</code>
> **does** R003 to R009: assign, warn, publish, show changes.

> [!phase]- Phase 3 · Clients · <code class="queued">queued</code>
> **does** arrival windows in the Portal, reschedule requests.

> [!phase]- Phase 4 · Suggestions and weather · <code class="parked">parked</code>
> **does** ranked suggestions and rain-day reflow, after a month of board data.

## Who gets what after Phase 1

| Capability | Client Portal | Crew App | Dispatch Console |
| --- | --- | --- | --- |
| See the schedule | <span class="c-mid">own jobs only</span> | <span class="c-mid">own crew only</span> | <span class="c-ok">everything</span> |
| Declare availability | <span class="c-no">no</span> | <span class="c-ok">yes</span> | <span class="c-ok">on behalf of a crew</span> |
| Assign a crew to a job | <span class="c-no">no</span> | <span class="c-no">no</span> | <span class="c-mid">from Phase 2</span> |

> [!legend]
> <span class="c-ok chip-key"></span> have  <span class="c-mid chip-key"></span> partial or later  <span class="c-no chip-key"></span> not on this surface

## Risk

> [!warning] If fewer than 60 percent of active crew members have entered availability by 9 October, Phase 2 waits.
> The board would be checking against data nobody trusts.

## Asks

- Decide [[One calendar or three]] by Friday; Phase 3 is blocked on it.
- Dispatch: keep calling Denver-1 crews who have not entered availability.
