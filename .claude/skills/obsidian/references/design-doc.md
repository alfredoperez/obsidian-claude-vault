# Profile — Design doc

A PRD, spec, ADR, roadmap, or design of record. Something the project **depends on**.

## Frontmatter

```yaml
---
title: <feature>
type: prd            # prd | spec | adr | roadmap
project: <slug>
feature: <slug>
status: active       # active | superseded | shipped | archived
lifespan: project    # ← the important one
---
```

**`lifespan: project`, always.** A design of record must never be swept on age. It dies with
its project, not on the calendar. This is the exact case the field exists for: before it,
the only expiry rule guessed from folder names, so a PRD sitting in the wrong folder could
be surfaced for archiving purely because it was old.

If it is superseded, say so explicitly rather than leaving it to rot:

```yaml
status: superseded
superseded-by: "[[11-feature-audit]]"
```

## Shape

Prose first, components second. A PRD is read by people deciding whether to build something
— it must be *legible*, not decorated. Reach for:

- `[!note]` for the problem statement
- `[!decision]` for locked calls
- a table for requirements (`R001`…) so a roadmap can reference the IDs later
- `[!warning]` for the risk nobody wants to name

Skip cards, matrices, and story maps unless the content genuinely is a comparison or a
release plan.

## Where it goes

`Projects/<project>/product/<feature>/` alongside the journey map, mockups, and stories.
Keep the feature folder together — that colocation is what lets the downstream skills
(`product-story-map`, `product-stories`) find their upstream context.

## Checklist

- [ ] `lifespan: project` — never `ephemeral`
- [ ] Requirements carry stable IDs a roadmap can reference
- [ ] Superseded docs say so, with a forward link
- [ ] Prose is legible on its own; components support it rather than carry it
