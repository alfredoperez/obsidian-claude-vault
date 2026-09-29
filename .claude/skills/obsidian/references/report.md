# Profile — Report

A design brief, decision doc, run report, research debrief, execution plan, or illustrated
comparison. The thing the user means when they say "a page", "a doc", "a brief", or "make
this visual".

## Frontmatter

```yaml
---
title: The composable workflow — master report
sub: "One line on what this argues and what it asks for."
date: 2026-06-13
type: brief
project: <project-slug>
kind: "master report"        # the eyebrow badge
status: "decision · pre-spec"
lifespan: ephemeral
cssclasses:
  - brief
---
```

## Shape

**A report makes a case. It is not a dump.**

Open with the thesis in a titled `[!note]`. Close with forward momentum in a `[!tip]` —
never a summary. Use `## ① Section` for each major part with `### The real heading` under
it; H2 renders in the accent colour with a rule above it, and that is the structural spine.

Pick components from the content, not from novelty:

| Content | Component |
|---|---|
| A comparison | tinted `[!cards\|2]` + a table |
| Work items | `[!ticket]` |
| Phased plan | `[!phase]` |
| Where you stand vs. the field | the chip matrix + `[!legend]` |
| A pipeline or flow | `[!figure]` + Mermaid |
| "What it feels like" | `[!terminal]` |
| Release plan | `[!storymap]` |

## Where it goes

In the effort's folder, with a **descriptive filename that says what the note IS** — never
a bare "report", never a date prefix (the date is a frontmatter field), never a numeric
prefix. If the folder has a hub, add the note to the hub's ordered list.

**Flat, directly in the effort folder — no `reports/` subfolder.** A subfolder that ends up
holding nearly everything in the effort isn't a category, it's a second root, and it forces
a "is this a report?" judgment call on every write. Subfolder only for a genuine *bundle*:
a set of files that are meaningless apart (`WRK-103-bundle/`), named for what the bundle
is. If an existing effort still has a `reports/`, flatten it.

**No `reports.md` digest index.** The one-paragraph survival summary goes in the note's own
`sub:` frontmatter — 60–120 words carrying the *finding*, not the topic. That's what
Bases/dataview list and what outlives the ephemeral body:

> sub: "The review caught a real data-loss bug (the per-task progress log was deleted
> before its data was saved); fixed by scoping cleanup to the terminal 'completed'
> transition."


## Vocabulary — a report earns its words

A report that argues about architecture has to use the vocabulary exactly, or it stops being an
argument and becomes an impression. Adopted from mattpocock/skills, and it generalises past
architecture: **any term you use to praise or condemn something has to be one you have defined.**

**Never substitute:**

| Say | Not |
|---|---|
| module | component, service, unit |
| interface | API, signature |
| seam | boundary — overloaded with DDD's bounded context |
| — | layer, wrapper |

**Do not write "easier to maintain" or "cleaner code."** Those are not in the glossary and they do
not earn their place. They feel like findings and carry nothing — the reader cannot check them,
disagree with them, or act on them. Name the mechanism instead: *"four call sites collapse to one"*
is checkable; *"cleaner"* is not.

**Keep the wins short.** A findings bullet that states an outcome should fit in about six words.
If it needs a sentence, it is a paragraph pretending to be a bullet, and the reader will skim it.

**Honest over exhaustive.** Three real findings beat ten speculative ones, and a report that pads
to look thorough trains the reader to skim the whole thing.

## Checklist

- [ ] Thesis in a titled `[!note]` up top
- [ ] Every callout has a real title (never a bare `[!note]`)
- [ ] Cards in a compare are **tinted apart**
- [ ] Matrix uses chip spans, not emoji
- [ ] Diagrams are Mermaid/Excalidraw with the theme block; no transitive edges
- [ ] No fabricated schedule
- [ ] Ends with forward momentum, not a recap
- [ ] **`sub:` frontmatter carries the 60-120-word finding** (it outlives the body)
- [ ] Path reported
