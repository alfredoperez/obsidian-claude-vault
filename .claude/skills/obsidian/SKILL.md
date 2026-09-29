---
name: obsidian
description: >
  How to write in Alfredo's Obsidian vault — the structure, not the voice. Frontmatter
  schemas, `lifespan:`, the component vocabulary (cards, tickets, phases, capability
  matrices, terminals, figures, story maps), diagrams, and where a note goes. Load this
  before creating or editing ANY note in the vault: reports, PRDs, research, knowledge
  notes, backlog items. Use when the user says '/obsidian', '/brief', 'make a report',
  'a page', 'a doc', 'an explainer', 'make this visual', or when another skill is about
  to write a note into the vault. Pairs with `writing` — that one owns the voice, this
  one owns the structure. A vault note needs both.
argument-hint: "<what you are writing>"
metadata:
  author: alfredo
  source: kaiju
---

# Obsidian

The single source of truth for **how a note is built** in this vault. One invariant core,
plus one profile per note type.

This is the structural twin of `writing`. That skill owns the *voice*; this one owns the
*structure* — frontmatter, lifespan, components, diagrams, placement. Other skills
(`capture`, `product-prd`, `product-stories`, `groom`) load from here
instead of each carrying a fragment of the conventions.

**Write a note → load both.** `writing` tells you how it should sound. `obsidian` tells
you how it should be built.

## When to Use

- Creating or editing any note in the vault.
- Another skill is about to write a note and needs the conventions.
- The user asks for "a report", "a page", "a doc", "a brief", "an explainer", or wants
  something "made visual".

## Workflow

### Step 0: Find what the vault already says — grep `Terms.md`, not the vault

**Before writing a note, and before every "related notes" or "does this already exist" question,
grep `Terms.md` at the vault root.** It is a generated lookup: one line per tag, keyword, entity
and claim, naming every note that carries it.

```bash
grep -i "<concept>" Terms.md          # run from the vault root
```

**A vault-wide prose grep is fast and still wrong.** Measured on 2026-08-29: full-vault greps take
under a second, so speed was never the problem — recall was. `grep -ri "eval rubric"` returned
**zero** while six notes on the subject existed, because they say `rubric-grading`. Prose search
only matches the words you happened to guess; `Terms.md` matches the words the author chose.

- **`Terms.md`** — *which notes touch this term.* A lookup. Start here.
- **`Topics.md`** — *which concept pages exist and what sits beneath them.* A curation view. Go
  here when deciding where a note belongs, not when finding one.
- **Then grep the vault** for prose the frontmatter never captured. Terms.md covers the ~850 notes
  carrying those fields; the rest are invisible to it. It narrows the search, it does not end it.

Stale after heavy writing. Rebuild with `node .claude/scripts/generate-terms-index.mjs` from the vault root (the script is in this repo).

### Step 1: Load the core (always)

Read `references/core.md`. Frontmatter, `lifespan:`, where notes go. These are the
invariants — they apply to every note unless a profile overrides them.

**Then read the domain's `_guide.md` before writing into it** (e.g. `Work/_guide.md`).
The guide is canonical for PLACEMENT — which container, which doc type, which
`~Templates/` file shapes it. This skill is canonical for FORMAT. If a domain has no
`_guide.md` yet, fall back to core.md's placement rules. File shapes live once, in the
vault's `~Templates/` — create from the template, never improvise frontmatter a
template already defines.

### Step 2: Load exactly one profile

Pick from what you are writing, not from the topic.

| Writing | Profile |
|---|---|
| A report — design brief, decision doc, run report, research debrief, comparison | `references/report.md` |
| A PRD, spec, or design of record | `references/design-doc.md` |
| A knowledge note, TIL, captured link or video | `references/knowledge-note.md` |
| A `.base` file — live views, filters, formulas | `references/bases.md` (+ `bases-functions.md`) — vendored from kepano/obsidian-skills |
| A `.canvas` file — story-map walls, thinking boards | `references/canvas.md` (+ `canvas-examples.md`) — vendored from kepano/obsidian-skills |

### Step 3: Reach for components only when the content earns them

Read `references/components.md` when the note needs more than prose: a comparison, a set
of work items, a capability matrix, a pipeline, a story map. **Do not decorate.** A
knowledge note is usually just good prose and a couple of callouts.

For diagrams, read `references/diagrams.md`. Mermaid and Excalidraw only — never inline SVG.

### Step 4: Check

Each profile ends with its own checklist.

## Non-negotiables

**Markdown is the source of truth.** Never write a standalone `.html` file into the vault.
HTML there is dark matter: no search, no backlinks, no graph, no tags, no Bases. ~140,000
words — 11% of everything in this vault — were once locked inside HTML pages that could
not be found. If a document must leave the vault, `create-doc` renders it *out*; the
markdown stays the source.

**Every note declares a `lifespan:`.** See `references/core.md`. It is what lets the vault
be groomed on declared intent instead of guesses about folder names and file dates.

**Never hard-wrap prose.** One paragraph is one line, however long. This vault runs with
`strictLineBreaks: false`, which means Obsidian renders **every single newline as a visible
line break**. Prose wrapped at 80 or 100 columns in the source file therefore renders with
ragged breaks in the middle of sentences, and the note looks broken to the reader while
looking tidy to whoever wrote it.

Wrap is a display concern; `readableLineLength` already handles it. The rule applies inside
callouts too, where the same newline becomes a break with a `>` in front of it.

Structural lines are exempt because they are already one-per-line by nature: headings, list
items, table rows, and fenced code. Only running prose joins up.

```bash
# a paragraph broken across source lines will show breaks the reader can see
awk 'NR>1 && prev !~ /^$|^#|^[-*+|>]|^```/ && $0 !~ /^$|^#|^[-*+|>]|^```/ && length(prev)>60 \
     {print FILENAME": "NR}  {prev=$0}' <note>.md
```

**The stylesheet is required.** The components are native callouts with custom types.
Obsidian renders them, but they only *look* right with `vault.css` installed. Without it a
`[!cards]` block is a grey box labelled "Cards". Setup is in `references/core.md`.

## Migrating an old HTML page

`html2md.py` converts a legacy `.html` page to this format — design-system aware, and it
logs any component it does not recognise to a review catalog rather than flattening it
silently. It converted all 71 of the vault's HTML reports at a median 99.6% vocabulary
retention.

```bash
python3 html2md.py <page>.html <page>.md
```

Check the output against the input. A vocabulary coverage materially below 100% means a
component was **swallowed**, not that prose was trimmed. That check caught five real bugs
during the migration.
