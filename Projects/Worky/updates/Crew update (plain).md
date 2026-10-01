---
date: 2026-09-28
type: update
project: worky
feature: crew-scheduling
lifespan: ephemeral
description: Week of 28 September for crew scheduling, written as plain markdown; the same facts as the components version, for comparison
tags: [worky, crew-scheduling, update]
---

# Crew scheduling update, week of 28 September

Availability is the only thing that has to land this month. Everything in Phase 2 reads it, so the board waits until crews are actually entering it.

## This week

- The `availability` table is merged and backfilled for all 40 crews.
- The Crew App availability screen is in beta with Crew Denver-1.
- 22 of 38 Denver crew members have entered four weeks of availability (58 percent).
- The Console shows each crew as available, unavailable or half-day, read-only.

## Where the MVP ends

- **After Phase 0 and 1, the MVP:** crews enter availability and dispatch sees it.
- **At the full vision:** one board plans the day, warns and publishes.

## Phases

| Phase | Status | What it does |
|---|---|---|
| Phase 0 · Skills as data | done | `crew_skill` table, the backfill of 40 crews, the new-hire form |
| Phase 1 · Availability and the check | now | `availability` table, R001 and R014, the hard-rule check, a read-only strip in the Console |
| Phase 2 · The day board | next | R003 to R009: assign, warn, publish, show changes |
| Phase 3 · Clients | queued | arrival windows in the Portal, reschedule requests |
| Phase 4 · Suggestions and weather | parked | ranked suggestions and rain-day reflow, after a month of board data |

## Who gets what after Phase 1

- Client Portal: sees own jobs only; cannot declare availability; cannot assign.
- Crew App: sees own crew only; declares availability; cannot assign.
- Dispatch Console: sees everything; declares availability on behalf of a crew; assigns from Phase 2.

## Risk

If fewer than 60 percent of active crew members have entered availability by 9 October, Phase 2 waits. The board would be checking against data nobody trusts.

## Asks

- Decide [[One calendar or three]] by Friday; Phase 3 is blocked on it.
- Dispatch: keep calling Denver-1 crews who have not entered availability.
