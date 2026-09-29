---
type: reference
lifespan: evergreen
source: kaiju obsidian skill
description: The invariants every note follows — frontmatter, lifespan, where notes go, links, images, the stylesheet
tags: [reference, conventions, frontmatter, lifespan]
---

# Core — the invariants

Applies to every note in the vault.

## Frontmatter

```yaml
---
title: The composable workflow — master report   # only when the filename is a slug
date: 2026-06-13
type: brief                # what it IS  (article-notes, til, prd, brief, story…)
project: speckit-companion # when it belongs to one
lifespan: ephemeral        # how long it should LIVE  ← see below
cssclasses:
  - brief                  # only for reports; suppresses the duplicate filename title
---
```

**Every note gets a one-line `description:`** (source notes use `tldr:`) — Notebook Navigator
renders it as the note's preview line, so it is the note's shelf label. Write it as the
takeaway, not a restatement of the title.

`type:` and `lifespan:` answer different questions and must not be conflated. `type:` says
what a note *is*. `lifespan:` says how long it should *live*. A `prd` and a `til` are both
durable-ish; a `brief` and a `demand-radar-report` are both ephemeral. The format tells you
nothing about the lifespan.

## `lifespan:` — the one field that matters most

```yaml
lifespan: ephemeral | project | durable
expires: 2026-08-01     # optional, an explicit override
```

| Value | Means | Examples |
|---|---|---|
| `ephemeral` | Read once or twice; then only its **summary** matters | run reports, session debriefs, a doc written to send someone |
| `project` | Lives as long as the project does | specs, ADRs, PRDs, design records, backlog items |
| `durable` | Keep indefinitely, groom for quality | `Knowledge/`, `Sources/`, playbooks, patterns, reference |

**Ephemeral is not an insult.** A generated doc earns its keep once; the durable thing is
what it produced (backlog items, fixes, the one-paragraph `sub:` in its own frontmatter).
There is **no `reports.md` digest index anywhere** — the survival summary lives in the
note's own `title:` + `sub:` frontmatter, where Bases/dataview can list it. There is **no
`reports/` folder anywhere in the vault**. In `Projects/`, generated output is classified the
moment it lands (decision doc, backlog items, inbox note, knowledge) or trashed; in `Work/`,
briefs sit flat in the effort folder.

An unstamped note falls back to its folder (`Knowledge/` → durable, `Sources/` → durable,
everything else → project). With `reports/` gone there is no folder that implies
`lifespan: ephemeral` — a brief that reads once **must stamp it explicitly**, and that is the
whole point: stamping is a *declaration*, made because you know better than the folder does.

Command Center's Triage page reads this and surfaces expired ephemera for archiving. It
**proposes**; it never moves anything on its own.

### Why it is its own key

- **Not `status:`** — already carrying three unrelated pipelines and 25 drifted values
  (`listo`, `bud`, `battletested`, `raw`).
- **Not `type:`** — a format taxonomy. It says what a note is, never how long it lives.
- **Never `groom_*`** — Triage's `stripGroomKeys()` deletes every `groom*` key the moment a
  user clicks an action. A lifespan stored there would silently vanish.

## `status:` — the canonical set

`status:` is pipeline-specific but every value resolves to one phase. Grooming keys off the
**phase**, not the raw word. The authoritative, current list lives in the vault's
**`Vault-Guide.md` → "Lifecycle & Grooming Rules"** — read it before grooming; this is a mirror.

- **Terminal** (archive-ready): `published`, `shipped`, `done`, `superseded`, `cut`
- **In-flight**: articles `idea → outlined → drafting → editing`; projects `active/paused/blocked`
- **Parked**: `archived` (already under `~Archive/`)

**The archive trigger:** a note whose `status:` is Terminal and is not yet under `~Archive/` is
archive-ready. Normalize drifted values on sight: `listo→done`, `completed/implemented→done`,
`draft→drafting`, `reference`→(drop; it's `lifespan: durable`), junk (`bud/pick/5/1/3`)→clear.

## Where notes go

The vault root is the folder that holds `.obsidian/` — write there directly; don't go looking for it.

| Domain | Location |
|---|---|
| Own distilled thinking, patterns, TILs | `Knowledge/` — `lifespan: durable`; `verified: {by: human:alfredo, at}` added only on human review, never at generation |
| Notes ON other people's content | `Sources/` — `articles/`, `videos/`, `courses/`, `links/`; self-identify via `type: article-notes\|video-notes\|conference` |
| Side projects, content | `Projects/` |
| Day job | `Work/` |
| Agent communication (feedback for / critiques from Claude, Codex) | `Projects/<project>/inbox/` — `type: inbox`, `lifespan: ephemeral`, from `~Templates/Inbox Note.md` |
| Work-effort briefs | `Work/<effort>/` — flat, descriptive filename that says what it IS. No `reports/` subfolder anywhere; subfolders are for genuine bundles only (files meaningless apart, named for the bundle). Never a `reports.md` index; never a date prefix; never a numeric prefix (see *Filenames and hubs*) |
| Tasks | `/Hub.md` only. Never a per-task file. |

Utility folders are `_`-prefixed; the archive is `~Archive/`.

## Filenames and hubs — a name says what the note is

**A filename says what the note is, in words. Nothing else.** No `00-` / `NN-` ordering
prefixes, no dates, no reserved names. Prefixes were an alpha-sort hack that nothing
in the vault actually reads (Notebook Navigator sorts by modified date; no Base or
dataview query keys off them), and they made every folder open with a file called
`00-overview.md` — 22 files with the same name, so a bare `[[00-overview]]` link was
already ambiguous. If a folder's notes have a reading order, the hub lists them in order.

**A hub is a folder note, and only when the folder earns it.**

**Name the hub after its folder, in words.** `plans/workflow-builder/Workflow Builder.md`,
`Projects/toku/Toku.md`. No `00-`, no `overview`, no dashes standing in for spaces — the
same rule as every other filename, with no exception carved out for hubs. A reader
scanning a folder list should be able to tell what the hub is about without opening it,
and `00-overview.md` fails that in every folder at once.

This requires Notebook Navigator's `folderNoteNamePattern` set to `{folder}` (and
`folderNoteName` left empty). Without it the navigator will not treat the file as the
folder's note — it will not open on folder click and will not hide from the file list.
That is a settings change, not a reason to fall back to a numeric prefix.

> **Reversal, 2026-08-26.** This section previously said both things at once: the heading
> and the opening rule forbade `NN-` prefixes, and the paragraph below mandated
> `00-overview.md` for every hub. Agents followed the mandate, produced `00-overview.md`
> and `00-workflow-builder.md`, and were corrected by hand repeatedly — the contradiction
> was doing the damage, not carelessness. The `{folder}` pattern was rejected on
> 2026-08-22 for costing a settings change plus 22 renames; that trade has been taken.
> **A rule stated twice in opposite directions is worse than either rule alone.**

Create one when either is true:

- the folder holds **three or more notes** and a reader needs to know where to start, or
- the folder is a **lifecycle unit** — a workstream, an investigation round, a project —
  that carries `type:` + `status:` and the fields grooming reads (`notion:`,
  `stale_after:`, `supersedes:`, `superseded_by:`). Those live in the hub's frontmatter;
  that is the one job a hub cannot delegate.

Otherwise there is no hub: a one- or two-note folder puts `type:` + `status:` on the
note itself. A hub is a paragraph, an ordered list of the folder's notes with one line
each, and the lifecycle frontmatter — not a document. If it grows past that, the prose
was a note and belongs in its own file.

Live indexes (`Work/Workstreams.base`, `Work/Investigations.base`, `Projects/Projects.base`)
list hubs by `type:`/`status:`; do not hand-maintain `_index.md` tables.

**A hub points at lists. It never duplicates them.** When a hub needs to show work that lives
elsewhere, link to the notes that hold it rather than aggregating their contents into the hub.
An aggregating query fails in both directions and both failures look plausible: too broad and it
returns hundreds of rows nobody reads, too narrow and it returns nothing while rendering as a
perfectly healthy empty section. A hand-maintained copy is worse again, because it goes stale
silently. `Hub.md`'s task section was rewritten three times before this landed, once at 718 rows,
once at zero, and finally as a short table pointing at the four notes that actually own the lists.

## Open what you wrote

**A note the user is meant to read gets opened in Obsidian, in the same turn that wrote it.**
Not mentioned by path, not described. Opened.

```bash
open "obsidian://open?vault=<vault-name>&file=$(python3 -c "
import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "Folder/Note Name")"
```

The path is vault-relative and **without** the `.md` extension, and it must be percent-encoded,
because spaces and `&` in a note name silently truncate the URI otherwise.

When a run writes several notes, open **the one the user is meant to read first**. Open all of them
only when they are genuinely all destinations. A run that writes thirty notes opens none of them and
says so.

> [!note] Why this is a rule here and not a hook.
> A `PostToolUse` hook on `Write` would open every markdown file written, and a batch capture that
> produces three hundred notes would open three hundred tabs. Which note matters is a judgement, and
> a hook cannot make one. `create-decision` has done this correctly for months; the rule lived in
> that one skill instead of here, so every other skill that writes a note forgot it.

## Links — what actually resolves

Three constructs look broken to a naive check and are correct. Each one has already caused a tool
to report a working link as an error, so verify against this list before "fixing" anything.

- **An alias inside a table escapes its pipe: `[[Note\|Alias]]`.** The backslash stops the table
  parser eating the alias separator. This is the standard form and the vault uses it 48 times
  across 11 files. It is not a broken link and it is not an escaping mistake.
- **A wikilink resolves to any file type, not just `.md`.** `[[diagram.png]]`, `[[Links.base]]`
  and `[[board.canvas]]` are all real targets. Any index built only from markdown files will
  report every one of them as broken.
- **`~`-prefixed and `_`-prefixed folders are ordinary link targets.** `~Archive/`,
  `~Attachments/`, `~Templates/`, `_Triage/` and `_Decisions/` are hidden from the navigator by
  convention, not from resolution. A scan that skips them will flag every link into the archive.

> [!warning] These three produced over 500 false positives in one afternoon.
> A link checker that does not know them will report most of the vault as broken, and the natural
> response to a long list of errors is to start repairing links that were never broken. Narrow the
> checker before trusting its output, and when a link *looks* wrong, grep the vault for the same
> construct first: if it appears dozens of times, it is a convention, not a defect.

## Images & attachments

- **Embed with wikilinks: `![[filename.png]]`** — never a markdown `![](path)` and never an absolute path (Obsidian resolves the bare filename vault-wide).
- **Co-locate an image with the note that uses it.** A brief at `Work/<effort>/queryable-tables.md` puts its image at `Work/<effort>/queryable-tables-overview.png` — same folder, same slug prefix. General/shared attachments go in **`~Attachments/`** at the vault root.
- **A user-supplied screenshot** (e.g. one they dropped into the chat, cached under `~/.claude/image-cache/…`) is added by `cp`-ing it into the target folder with a descriptive dated name, then embedding it with `![[…]]`. Add a one-line italic caption under it saying what it shows.

## Setup — the stylesheet is required

The components are native Obsidian callouts with custom types. Obsidian renders them, but
they only *look* like a report with `vault.css` installed.

**The vault owns the stylesheet.** It lives at `<vault>/.obsidian/snippets/vault.css` and
that is the only copy. This skill deliberately does not carry its own: a skill's job is to
say *which component to use*, which the rest of this reference does. Carrying the
implementation as well means two files have to agree forever, and the copy that used to sit
here had already drifted a third of the way out of date.

On a machine that has the vault, the stylesheet is already there. On one that does not,
copy it from the vault you are syncing from, then
**Settings → Appearance → CSS snippets → turn on `vault`.**

Two traps that cost real time to find:

- **Obsidian keeps snippet and theme state in memory** and rewrites `appearance.json` from
  it. Editing that file while Obsidian is running does nothing — the toggle silently
  reverts. Quit Obsidian first, or flip the switch in the UI.
- **The stylesheet deliberately does not rely on `cssclasses`.** Everything keys off the
  callout *type*, so it works regardless of what plugins rewrite the markdown view. The one
  exception is `cssclasses: brief`, which only hides the duplicate filename title.

If prose in this vault ever looks unreadable, check the body font before blaming markdown.
It was once Geist **Mono** at 13px — every word in the vault rendered in a monospace face
sized for code.
