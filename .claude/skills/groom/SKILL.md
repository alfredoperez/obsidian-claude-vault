---
name: groom
description: "One grooming skill, scope as an argument. `groom vault [subfolder]` — cross-vault pass: auto-removes orphaned images to _Triage/Trash/ with a restorable grace window (mechanical + reversible), and FLAGS — never executes — misfiled / duplicate / low-value / stale notes via `groom: review` frontmatter + a dated digest (judgment + propose-only). `groom knowledge <topic>` — the same audit over one Knowledge/<topic>/ folder, plus stubs, near-duplicates, broken links, missing frontmatter, and a regenerable index.md. `groom project <name>` — a DIFFERENT operation: moves finished items into Done/ by terminal frontmatter `status`. Use when the user says '/groom', '/groom vault', '/groom knowledge', '/groom project', wants to clean up / tidy / audit / reorganize the vault or a folder, remove orphaned or unreferenced images, flag misfiled / duplicate / low-value notes, find duplicates or stubs in a knowledge area, ask for an index of a knowledge topic, or says completed work is cluttering an active project view."
argument-hint: "vault [<subfolder>] | knowledge <topic> | project <name> [--dry-run] [--no-images]"
---

# Groom

Three scopes, one entry point. **They are not the same operation** — read the guarantee table before
running anything, because the promise the skill makes to the user changes per scope.

| Scope | What it does | Writes | Guarantee |
|---|---|---|---|
| `groom vault [subfolder]` | Cross-folder pass: orphaned-image sweep + note verdicts | Tier 1: image moves to `_Triage/Trash/`. Tier 2 (on confirm): `groom: review` stamps + a dated digest | **Notes are propose-only.** Images are moved, never deleted, and stay restorable from the manifest |
| `groom knowledge <topic>` | Same verdict pass over ONE `Knowledge/<topic>/` folder, plus stubs / clusters / broken links / frontmatter gaps | On confirm: `index.md`, frontmatter backfill, `Hub.md` tasks, `groom: review` stamps | **Never deletes, never merges, never edits bodies** |
| `groom project <name>` | **Moves finished files into `Done/`** by terminal frontmatter `status` | File moves inside the project folder | **Move only, confirm-first, no judgment, no flags, no deletes** |

Vault and knowledge *audit and flag*. Project *moves files*. The first two share one judgment engine
(`references/verdicts.md`) — knowledge mode is that engine scoped to a folder plus the folder-level
outputs a vault-wide sweep can't produce. Project mode is deliberately kept in its own section below
with its own guarantees; do not blend its behaviour into the other two.

## When to Use

- `/groom vault`, `/groom vault Projects/sdd`, or the legacy `/groom` — vault cleanup, orphaned/unreferenced images, flagging misfiled / duplicate / low-value notes.
- `/groom knowledge Knowledge/AI`, or the legacy `/groom` — a topic folder has accumulated cruft, duplicates, or stale notes; the user wants an `index.md`, or asks to "audit" / "consolidate" / "find duplicates" in a knowledge area.
- `/groom project Projects/speckit companion`, or the legacy `/groom` — completed work is cluttering an active project view; the user wants to "clean up" / "tidy" / "organize" a `Projects/<name>/` folder.
- Bare `/groom` — ask which scope, then which target. Never pick unilaterally.

## References

| File | Load when |
|------|-----------|
| `references/verdicts.md` | Judging notes in `vault` or `knowledge` mode — full verdict definitions, `lifespan:` rules, boundary/clock checks, the low-value bar and its exemptions, the `groom_*` stamp, the digest format. |
| `references/image-sweep.md` | Running the image sweep or the evict pass, or writing the trash manifest — full algorithms, guards, and the canonical manifest schema. |
| `references/knowledge-audit.md` | Running `knowledge` mode — scan rules, per-file capture, clustering, report block, write menu, `index.md` format. |

## Inputs

- **Scope** (first argument): `vault` | `knowledge` | `project`. Missing → ask.
- **Target** (second argument): a path relative to the vault root. Optional for `vault` (a subfolder, e.g. `Projects/sdd`); required for `knowledge` and `project` — with none, list the immediate directory children of `Knowledge/` or `Projects/` and ask which to groom.
- **Vault root**: the folder holding `.obsidian/` (the current working directory when run from the vault), unless the user names another.
- **Flags** (vault mode): `--dry-run` (report everything, move/write nothing); `--no-images` (skip the image sweep).

Confirm the resolved folder exists; bail clearly if not.

---

## Scope: `vault` — audit + flag (propose-only for notes)

Two tiers. **Tier 1 — mechanical & reversible:** orphaned images are a deterministic call, so they
are ACTIONED automatically — moved to `_Triage/Trash/` with a restorable grace window, never
hard-deleted. **Tier 2 — judgment & propose-only:** misfiled / duplicate / low-value note verdicts
are only *proposed* — a `groom: review` frontmatter stamp plus a dated digest in `_Triage/` — for the
user or the Command Center Triage page to apply. The line: **mechanical + reversible → auto;
judgment → propose.**

With no subfolder argument, ask the user to pick a top-level area (`Projects`, `Work`, `Personal`,
`Knowledge`) or confirm a full-vault pass.

### Step 1: Enumerate candidate notes

1. Recursively list `.md` files in scope. **Skip entirely**: `.obsidian/`, `.git/`, `.serena/`, `.specify/`, `_claude/`, `node_modules/`, `_Templates/`, `~Templates/`, `_Attachments/`, `~Attachments/`, `~Archive/`, `_Triage/`, and every `index.md` (that's `groom knowledge`'s output).
2. Build the vault-wide inbound-link map in a SINGLE pass — never grep per note (see the performance note in `references/image-sweep.md`). Inbound links = wikilinks in any form (aliases, `#heading`, `#^block`, `![[embeds]]`) AND markdown links that resolve to the note; tags are NOT links.
3. If no notes remain, skip Steps 3–5 but STILL run the image sweep, then stop.

### Step 1.5: Rebuild `Terms.md` (auto, mechanical)

```bash
node .claude/scripts/generate-terms-index.mjs     # from the vault root
```

`Terms.md` is the vault-root lookup that turns "where did I write about X" into one grep. It is
generated from `tags`/`keywords`/`entities`/`claims` frontmatter, so **it goes stale every time a
note is written** — and a stale lookup is worse than none, because it answers confidently with an
old picture. `groom` is the only routine that runs after a batch of writing, which makes this its
job.

Report the counts it prints. A drop in indexed notes since last run means frontmatter is being
dropped somewhere, which is worth a line in the audit report.

### Step 2: Sweep orphaned images (Tier 1 — auto, reversible)

Load `references/image-sweep.md` and follow it exactly (skip if `--no-images`). It covers the
vault-wide referenced-image scan, orphan detection, the conservative guards, the scale guard, and the
manifest. Two constraints from it are non-negotiable, earned by real data loss:

- **NEVER sweep a generated asset bundle.** A folder with a `carousel.pdf`, named `create-carousel/`, or under `~Attachments/Carousels/` is a *unit* — deleted deliberately, as a folder, or not at all. An individual slide is never an orphan.
- **Use these exact keys** in the manifest: `{originalPath, trashedPath, reason, deletedAt, size}`. Command Center's Restore/Sweep depend on them; the old forked shape left 209 images neither restorable nor sweepable.

Report the outcome at the top of the Step-4 block.

### Step 2.5: Flag non-note ballast (evict — propose only)

Nested git clones, code/render projects, and loose non-note files are **evict** candidates — they
leave the vault entirely and are never auto-moved. Detection heuristics and report format are in
`references/image-sweep.md`.

### Step 2.7: House style (mechanical, propose-only)

Three checks that need no judgement and are therefore worth running every time. All three are
**reported, never fixed silently** — a bulk rewrite of someone's notes is not a grooming action.

If the vault ships a house-rules linter with a baseline, run it first so only new breakage is reported. This vault ships none, so go straight to the checks below:

**Em dashes in headings.** House style is a colon when the dash separates a label from its
explanation, and a middot when it separates a title from its source.

```bash
grep -rn '^#\{1,6\} .*—' --include='*.md' <scope> | grep -v '/~Archive/\|/_Triage/\|/raw/'
```

Skip anything with `generated-by:` in its frontmatter. Those regenerate and a fix there is
overwritten on the next build.

**Filenames.** The vault's conventions, and each one is a real retrieval failure when broken:

| Rule | Why |
|---|---|
| Folder notes are named after their folder (`Projects/Worky/Worky.md`), never `00-overview.md` | Twenty-two files with the same name make every bare `[[00-overview]]` link ambiguous |
| No `/` or `:` in filenames | They become escapes and break links silently |
| A date in the name is `YYYY-MM-DD` | Any other order sorts wrong forever |
| Utility folders are `_`-prefixed, archive and attachments `~`-prefixed | The navigator hides them by prefix |

**Frontmatter.** Every note declares `lifespan:`, and that is what lets the vault be groomed on
declared intent rather than guesses about folder names and file dates. A note without one cannot
be swept, so it accumulates forever. Report which notes lack it; do not invent a value.

> [!note] Why these are reported and not fixed
> An em dash in a heading is cosmetic. A filename change breaks every link to it. Frontmatter is a
> claim about intent that only the author can make. None of the three is a call this skill gets to
> make on its own, and a grooming pass that quietly rewrote 781 headings would be a grooming pass
> nobody runs twice.

### Step 3: Read and judge each note (the AI pass)

Load `references/verdicts.md` and apply it. Read each note's full content; assign **at most one**
verdict (`misfiled` | `duplicate` | `low-value / single-use` | `stale`), only when confident. Default
to leaving a note unflagged.

### Step 4: Show the audit report (before writing anything)

Print one block: header `Grooming: <scope> (<N> notes read, <M> flagged)` plus the image-sweep
outcome line, then a section per verdict (omit empty ones), each item
`<path> → <suggested action> — <one-line reason>` (low-value adds `[<W> words, <K> backlinks]`; word
counts are whole-file `wc -w`, approximate). Close with `Worth attention` (NOT a verdict): broken
links, malformed frontmatter → hand to `groom knowledge <folder>`.

### Step 5: Ask what to write

Numbered menu (nothing written yet): **1** stamp `groom: review` frontmatter on flagged notes ·
**2** write the digest · **3** both · **4** none — exit, print "No changes made."

Both the stamp shape and the digest path/format are in `references/verdicts.md`.

Then report one line:
`Flagged 12 notes, wrote _Triage/groom-2026-06-13-full.md (4 misfiled, 5 duplicate, 3 low-value)`.

### Clean scope

Report `Nothing to groom in <scope> — <N> notes all look well-placed.` and exit without writing.

---

## Scope: `knowledge` — audit one topic folder + index (propose-only)

Same verdict engine as `vault` mode, scoped to ONE `Knowledge/<topic>/` folder (non-recursive), plus
the folder-level outputs: stub detection, missing-frontmatter detection, broken wiki links, keyword
clustering for near-duplicates, and a regenerable `index.md`.

1. **Resolve the folder.** With no path, list the immediate directory children of `Knowledge/` and ask which to groom. Confirm it exists; bail clearly if not.
2. **Scan and capture** per `references/knowledge-audit.md` (skip `index.md`, `Done/`, `~Archive/`, `_*`, `~*`; empty folder → "Nothing to groom — folder is empty" and stop).
3. **Judge** each note with `references/verdicts.md` — the same verdicts vault mode assigns.
4. **Cluster** by shared keywords for merge candidates.
5. **Show the report block**, then **ask what to execute** from the numbered menu. Both are specified in `references/knowledge-audit.md`.

**One folder per invocation.** No `--all`, no recursion. Run separately per topic.

---

## Scope: `project` — MOVE finished items into `Done/`

> **Different operation, different guarantees.** This scope does not audit, does not read note
> content, and does not flag anything. It reads one frontmatter field and **moves files**. It is
> mechanical and confirm-first: it prints the full plan and waits for an explicit `y` before any file
> moves. It never deletes and never edits file contents (except the opt-in Step 4 frontmatter
> prepend, which only adds).

### Step 1: Resolve the target folder

With no path, list the immediate directory children of `Projects/` and ask which to groom. Confirm it
exists.

### Step 2: Scan for completed files

1. List all `.md` files in the target folder (**non-recursive** — do not descend into subfolders).
2. **Skip these subfolders entirely**: `Done/`, `~Archive/`, anything starting with `_` or `~`.
3. For each `.md` file, read the YAML frontmatter and look for a `status:` field.
4. Categorize:
   - **Done** (terminal) — `status` ∈ `published`, `shipped`, `done`, `superseded`, `cut` (also legacy `completed`/`closed` → treat as done and normalize to `done`)
   - **Active** — `status` exists but is not terminal (e.g. `active`, `in-progress`, `drafting`, `idea`, `blocked`, or any unrecognized value)
   - **No status** — no frontmatter, or no `status:` field

`archived` means already parked in `~Archive/` — skip it, don't move it to `Done/`.

The canonical set is the vault's `Vault-Guide.md` → "Lifecycle & Grooming Rules" (mirrored in the
`obsidian` skill's `obsidian/references/core.md`). If the vocabulary needs to change, edit `Vault-Guide.md`
(the source), then mirror here.

### Step 3: Show the plan, then move

```
Grooming: <target folder>

Will move to Done/ (N files):
  - <filename> [status: <value>]

Will keep as active (M files):
  - <filename> [status: <value>]

No status field (K files — consider adding one):
  - <filename>
```

Then ask: **"Proceed with the move? (y/n)"** If the user says no, stop. Do not modify anything.

On confirm:

1. Create `<target folder>/Done/` if it does not already exist.
2. For each Done file, `mv "<target>/<filename>" "<target>/Done/<filename>"`.
3. Use git-aware moves if the vault is a git repo (`git mv` instead of `mv`); otherwise plain `mv`.
4. Report the number of files moved, plus a one-line list of the K files without a status field.

### Step 4: Follow-up offer (only if any files lacked status)

> "Found K files without a `status` field. Want me to add `status: open` to each so they show up as
> active in future runs? (y/n)"

If yes, prepend a minimal frontmatter block to each of those files (or insert a `status` field into
existing frontmatter). If no, leave them alone. **Never auto-create `status:` fields without asking.**

### Nothing to do

`Nothing to groom. All N files are active.` — and still surface any files that lack a status field.

---

## Constraints

Grouped by the scope they bind. Losing one of these is worse than a missed finding.

**vault + knowledge (audit scopes):**

- **Notes are propose-only.** Never move, merge, archive, or delete a NOTE — flag and digest only. Orphaned IMAGES are the sole auto-action, and even they go to trash, never deleted; `groom` never empties the trash (the 14-day grace sweep is the Command Center Triage page's job).
- **Never edit note bodies.** Frontmatter writes only add/refresh `groom_*` fields, or fill blank fields during knowledge-mode backfill — never modify an existing value.
- **Conservative by default.** Unflagged when unsure — a false "misfiled" is worse than a miss.
- **Idempotent per scope.** Re-runs replace the whole `groom_*` block; if a note no longer crosses the bar, REMOVE its block.
- **Never auto-merge files.** Surface candidates only; the user does merges and deletions manually from the report.
- **`index.md` is an output, not an input.** Skip it on scan, treat the existing one as overwritable, and state its regenerability in its frontmatter.

**project (move scope):**

- **Move only.** Never delete. Never edit file contents beyond the opt-in `status:` prepend.
- **Confirm before moving.** The plan block and an explicit `y` are mandatory — there is no `--yes`.
- **One folder per invocation.** Don't recurse, don't groom multiple projects at once. Keeps the blast radius small.
- **Don't touch `Done/`, `~Archive/`, `_*`, or `~*`.**

## Examples

| Input | What happens |
|---|---|
| `/groom vault` | Asks which top-level area (or full vault), then sweeps images + flags notes. |
| `/groom vault Projects/sdd --dry-run` | Full report for that subtree; moves nothing, writes nothing. |
| `/groom knowledge Knowledge/AI` | Audits `Knowledge/AI/`, clusters near-duplicates, proposes `index.md`, shows the menu. |
| `/groom knowledge` | Lists the directories under `Knowledge/` and asks which to groom. |
| `/groom project Projects/speckit companion` | Lists done vs active vs no-status, asks once, moves done files into `Done/`. |
| `/groom` | Asks which scope first. Never picks unilaterally. |

## Quality Checklist

- [ ] Scope was resolved explicitly — never guessed when the user gave none.
- [ ] `vault`/`knowledge`: no note was moved, merged, archived, or deleted.
- [ ] `vault`: every swept image is in `_Triage/Trash/<date>/` AND has a manifest entry with the exact keys `{originalPath, trashedPath, reason, deletedAt, size}`.
- [ ] `vault`: no generated asset bundle (carousel slides etc.) was swept.
- [ ] `vault`: the scale guard fired and was confirmed if candidates exceeded 50 or 10% of vault images.
- [ ] `--dry-run` wrote nothing at all.
- [ ] The report block was printed BEFORE any write, and the user chose from the menu.
- [ ] `project`: the plan block was shown and confirmed before any `mv`.

## Tips

- The Command Center **Triage page** is the downstream consumer of vault mode: "Needs review" reads `groom: review` notes; orphan Restore reads `_Triage/Trash/manifest.json`. Keep both schemas stable.
- First sweep on a real vault: `--dry-run` and eyeball the orphan candidates — this is the one place a bug deletes referenced files.
- Vault mode's "Worth attention" list (broken links, malformed frontmatter) is the handoff into `groom knowledge <folder>`, which is the mode that actually fixes them.
- If someone asks to "groom" a project expecting an audit, say what project mode really does — it is a status-driven file move, not a content review. Run `groom vault Projects/<name>` for the audit.
