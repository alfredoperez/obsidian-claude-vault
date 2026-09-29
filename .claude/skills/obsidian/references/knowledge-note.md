# Profile — Knowledge note

A TIL, a pattern, a playbook — **the user's own distilled thinking**. If the note mainly
summarizes someone else's article/video/course, it is a *source note* and belongs under
`Sources/` (same prose bar, but frontmatter is `type: article-notes|video-notes|conference`
+ `source:` + `author:`, and no `verified:` ever).

## Frontmatter

```yaml
---
tags: [angular, signals, state-management]
created: 2026-07-13
source: "[[origin note or URL]]"   # where it was learned / extracted from
lifespan: durable                  # ← reference material is kept and groomed, never aged out
verified: {by: human:alfredo, at: 2026-07-28}   # added when a human reviews it — NEVER at generation
---
```

Machine-written knowledge is a draft until a human blesses it: write the note without
`verified:` and let the review add the stamp (a human review pass is what mints these).

## Shape

**This is the profile where restraint matters most.**

A knowledge note is prose. It is the one you will actually reread, and components get in
the way of that. A `[!note]` for the key insight, a code fence for the snippet, a table if
there is genuinely tabular data. That is usually all of it.

Do not reach for cards, matrices, phases, or story maps here. If a knowledge note needs a
capability matrix, it is probably a report wearing the wrong hat.

The one thing worth more than any component: **write down why it mattered**, not just what
the thing was. `groom` flags notes with no unique information, and "what the docs
said" is the shape that gets flagged.

## Where it goes

`Knowledge/<topic>/` — the topic folder, not a date folder. Links go to
`Sources/links/<Title>.md` so they surface in the `Links.base` dashboard; article/video
notes go to `Sources/articles/` / `Sources/videos/`.

## Checklist

- [ ] `lifespan: durable`
- [ ] `source:` recorded — a knowledge note with no provenance ages badly
- [ ] Says why it mattered, not just what it was
- [ ] Prose, not decoration
- [ ] Filed by topic
