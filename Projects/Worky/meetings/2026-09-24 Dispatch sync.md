---
date: 2026-09-24
type: meeting
project: worky
feature: crew-scheduling
lifespan: ephemeral
description: Dispatch walked through how Monday's schedule gets built today; the spreadsheet is the thing Phase 2 has to replace, and it has rules nobody wrote down
tags: [worky, crew-scheduling, meeting]
---

# Dispatch sync, 24 September

**With** Marta (senior dispatcher), the Dispatch team, Core Services.

Marta built Tuesday's schedule live while we watched. It took 84 minutes, close to the 90 in the [[Crew Scheduling PRD]] baseline.

> [!capture] Screenshot · the Denver spreadsheet on a Monday morning

## What we saw

- Availability comes in by phone and text between 6 and 8am and gets typed into a column called "notes".
- The spreadsheet has a hidden tab of crews who "do not work together". Nobody outside dispatch knew it existed.
- Lift certifications are checked from memory; Marta keeps the expiry dates on a sticky note.

> [!warning] The "do not work together" tab is a hard rule nobody wrote down.
> If the day board ships without it, the first conflict it misses will be one Marta would have caught, and dispatch will stop trusting the board.

## Actions

- Core Services: add the pairing rule to the hard-rule list in [[Crew Scheduling Design]].
- Dispatch: send a copy of the spreadsheet, names removed.
- Update [[Worky]] once the rule is in the design.
