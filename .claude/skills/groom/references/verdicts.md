# Verdicts: the shared judgment pass

This is the single judgment engine for **both** `groom vault` and `groom knowledge`. It replaces the
older, weaker per-folder heuristics that `groom` used to carry — the two modes now judge a
note identically; only the scope and the extra outputs differ.

Everything here is **propose-only**. A verdict never moves, merges, archives, or deletes a note.

## Assigning a verdict

Read each note's full content. Assign **at most one** verdict, only when confident — default to
leaving a note unflagged:

- **misfiled** — content's true domain doesn't match its folder. → `groom_suggest: relocate`, `groom_target: <folder>`. Before emitting, read 2–3 sibling notes in the current folder AND the proposed target to confirm the boundary empirically; if the vault has no clear folder convention, emit NO misfiled verdicts and say so. For work/project → `Knowledge/*` moves the test is REUSABILITY, not topic overlap: anything tied to a specific employer, codebase, ticket system (e.g. WRK-####), or internal tool stays put; relocate only employer-agnostic reference.
- **duplicate** — substance already covered, more fully, elsewhere. Identify the canonical note. → `groom_suggest: merge`, `groom_target: [[canonical]]`.
- **low-value / single-use** — short, no unique information, 0–1 inbound links, never revisited. → `groom_suggest: archive` (or `keep` if borderline).
- **stale** — superseded, or references tools/facts that no longer apply. → `groom_suggest: archive` or `merge`.

## `lifespan:` beats every heuristic

**Read `lifespan:` before judging** — it is a declaration of intended life:

- `durable` → **exempt from low-value**; the author already said it stays.
- `ephemeral` past its window (or explicit `expires:`) → strong `stale` signal → archive.
- `project` → tie its fate to the project, not the calendar: stale only once the project reaches a terminal `status:` (`published`, `shipped`, `done`, `superseded`, `cut` — see the `obsidian` skill's `references/core.md`). A note whose own `status:` is terminal and not under `~Archive/` is itself archive-ready.
- unstamped → folder default: `Knowledge/` durable, `Sources/` durable (processed-input archive — never a low-value candidate for being "just notes on someone else's content"; that's its job), everything else project-scoped. No folder implies `ephemeral` any more — an unstamped read-once brief reads as `project` until someone stamps it.

## Boundary and clock checks

- **Misfile check at the Knowledge/Sources boundary:** a note under `Knowledge/` with `type: article-notes`, `video-notes`, or `conference` is processed input → `groom_suggest: relocate`, `groom_target: Sources/<articles|videos|courses>/`. The reverse (own-POV distillation sitting in `Sources/`) → relocate to `Knowledge/<topic>/`.
- **Inbox notes** (`inbox/` folders under `Projects/<x>/`): the folder is the signal — files there are agent-communication material (`type: inbox`) even when created bare by hand. Unstamped → propose stamping the `~Templates/Inbox Note.md` frontmatter (`type: inbox`, `status: open`, `lifespan: ephemeral`). `status: consumed`, or `open` with no edits in 30+ days → `stale` → `groom_suggest: archive`. Their durable residue is the backlog items / fixes they produced, never the note itself.
- **Content pipeline clocks** (`Projects/Content/Writing/`): `status: idea` files are not allowed — propose folding to a line in `Ideas Backlog.md` + archive the outline. In-flight (`outlined|drafting|editing`) untouched **45+ days** → propose `cut` (archive, or fold back to a backlog line). `status: published` or `cut` still in the live tree → archive-ready immediately (mirrored `~Archive/Projects/Content/` path) — there is no settle window; the publishing flow archives at publish and this check is the fallback.
- **`reports/` is dead everywhere:** a `reports/` folder or `reports.md` anywhere outside `~Archive/`, `_Triage/`, and frozen projects is legacy → flag it. Under `Projects/<x>/`, generated output classifies immediately into a real doc type (decision doc, backlog items, inbox note, knowledge) or trash. Under `Work/<effort>/`, the briefs flatten into the effort folder; propose `groom_suggest: relocate` with `groom_target:` the parent. A subfolder survives only when it is a genuine bundle — files meaningless apart, named for what the bundle is.

## The low-value bar (and its exemptions)

Combine signals before flagging low-value — few backlinks alone is normal; require short body AND
thin content AND low inbound links.

- EXEMPT deliberate collections: a hub/index/MOC/library/prompt-catalog (a `## section` list, or those words in the title) is "a stub that should grow," even at 0 backlinks.
- EXEMPT short-but-complete reference docs: a runbook/setup guide with concrete external links or numbered repeatable steps is reference value regardless of length — word count measures verbosity, not usefulness.
- CONVERSELY, verbatim AI/chat output (✅ status lines, "What Was Accomplished" headings, truncated mid-sentence) is a session artifact → single-use regardless of word count.
- Tiebreaker: pasted blocks that are *inputs authored for reuse* (test prompts, templates, command catalogs) → fixture, keep; *outputs captured from a past run* (terminal dumps, tool logs) → single-use, even when long.

## The `groom_*` stamp

Add/refresh ONLY these fields (never touch existing frontmatter values or the body):

```yaml
groom: review
groom_verdict: duplicate        # duplicate | misfiled | low-value | single-use | stale
groom_reason: "2-line stub; fully covered in [[Layered Context]]."
groom_suggest: merge            # merge | relocate | archive | keep
groom_target: "[[Layered Context]]"
groom_at: <today ISO date>
```

If a note has NO frontmatter, create a fresh `---` block; if malformed, do NOT stamp — list it under
"could not stamp". Never produce two `---` blocks.

**Idempotent per scope.** Re-runs replace the whole `groom_*` block; if a note no longer crosses the
bar, REMOVE its block.

## The digest

`_Triage/groom-<date>-<slug>.md` (`<slug>` = slugified scope, `full` for full-vault — never a bare
date, so same-day multi-scope runs don't clobber). Contents: frontmatter (`type: groom-digest`,
`generated_by: groom`, `generated_at`, `scope`), one section per verdict (`[[wikilink]]` + reason +
suggested action), and "Worth attention".
