---
name: checkup
description: >
  One command that runs every read-only health check across the vault and reports what
  needs attention. Notes without a lifespan, wikilinks that resolve to nothing, canvases
  that do not parse, expired ephemera still in the live tree, a stale Terms.md, and how
  long since the vault was groomed. Use when the user says '/checkup', 'is everything ok',
  'check my setup', 'what needs attention', 'health check', 'anything broken', or comes
  back after time away and wants to know what rotted. Changes nothing: every fix it names
  is a separate deliberate command.
argument-hint: "[--quick]"
allowed-tools: Bash
metadata:
  author: alfredo
  source: kaiju
  tags: maintenance, health, evals, drift
---

# Checkup

**The single entry point.** Several maintenance checks exist and nobody remembers them, so this runs the read-only ones and tells you which found something. This is the vault-only cut of the kaiju checkup; the script ships in this repo at `.claude/scripts/checkup.mjs`.

## When to Use

- Coming back after time away
- Before a session that will touch a lot
- Any version of "is everything still fine"

## Run it

```bash
node .claude/scripts/checkup.mjs            # from the vault root
node .claude/scripts/checkup.mjs --json
VAULT_DIR=/path/to/vault node .claude/scripts/checkup.mjs
```

Everything is local and takes about a second; nothing hits the network.

## What it checks

| Check | Finds |
|---|---|
| Notes declare a lifespan | A note that can never be swept because nobody said how long it should live |
| Wikilinks resolve | A link that lands on nothing (any file type counts; `~`/`_` folders are real targets) |
| Canvases parse | A `.canvas` that is not valid JSON, or an edge pointing at a missing node |
| Ephemera past their expiry | `lifespan: ephemeral` notes whose `expires:` date has passed and are still in the live tree |
| Terms.md lookup | Notes written since the lookup was last generated |
| Vault grooming | How long since the last sweep, because nothing else prompts it |

## It changes nothing, on purpose

> [!danger] **A checkup that edits is not a checkup.**
> Two things are deliberately excluded because they write: `/groom vault` moves files, and
> `generate-terms-index.mjs` rewrites `Terms.md`.
>
> If this fixed what it found, you would stop reading the output, and then a fix you did not
> want would land silently. Every remedy is named in the report and run separately.

## Reading the output

Three levels, and the distinction is the point:

- **`LOOK`** — something is wrong now. The fix is on the next line.
- **`note`** — worth knowing, not urgent. Usually a count that is drifting.
- **`ok`** — checked, fine.

**A clean run means "the mechanical checks pass"**, not "everything is good." Every grader here is top-down, derived from a rule that already existed. The bottom-up half, the things only found by reading your own output, is not in here and cannot be.

## After it

Match the finding to its command:

| It said | Run |
|---|---|
| Lifespan missing | open the note and stamp it — the author decides, never a script |
| Links broken | fix the link, or restore the file it pointed at |
| Canvas invalid | open the file; check `fromNode`/`toNode` against the node ids |
| Ephemera expired | `/groom vault --dry-run` first |
| Terms.md stale | `node .claude/scripts/generate-terms-index.mjs` |
| Vault not groomed | `/groom vault --dry-run` first |

## Quality Checklist

- [ ] Report what it actually said, including the `ok` lines. A checkup that only reports problems reads as "nothing was checked" on a clean run.
- [ ] Never run a fix without being asked, even an obvious one.
- [ ] If a check errored rather than failed, say so. A check that could not run is not a check that passed.

## Tips

- Run it from the vault root, or set `VAULT_DIR`.
- Every grader here is top-down, derived from a rule in `Reference/Vault conventions.md`. A clean run means those hold, not that the notes are good.
