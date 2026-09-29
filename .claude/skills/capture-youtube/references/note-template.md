# The video note

The exact shape of the note this skill writes: frontmatter, section order, and the rules for
each block. Read it before writing the note, not after.

Write a **deep, readable note** — not a list of fragments. The bar is the user's own
gold-standard note at `Sources/videos/Self-Evolving Claude Code Memory.md`: read it once to
calibrate depth, structure, and voice. A good note teaches the talk to someone who didn't
watch it.

Create the note at `Sources/videos/<Video Title>.md` (strip characters illegal in
filenames — use `-` for `:` / `/`).

```markdown
---
created: YYYY-MM-DD
type: video-notes
source: <YouTube URL>
channel: <Channel Name>
upload_date: YYYY-MM-DD
duration: MM:SS
tags:
  - <4-7 specific tags: topic, tools/products named, domain>
---

# <Video Title>

**Channel:** <Channel Name>
**Source:** <YouTube URL>
**Speaker:** <name + role, if stated>
<!-- add **Repo:** / other links the talk names, if any -->

<Opening abstract: 2-3 sentences. What does the talk argue, and why does it matter?
This is the part the user reads first — make it land.>

## Main Ideas

- **Bold lead-in.** Then a few sentences of real explanation in prose — the *why* and
  *how*, not a headline. Weave in a verbatim quote where one lands.
- **Bold lead-in.** ... (aim for the talk's actual structure; ~5-9 developed points.)

## Key Takeaways
- Actionable, specific conclusions a reader can apply.

## Notable Quotes
> "Verbatim line worth keeping." — speaker

## Reference Snapshot
- Tools, products, repos, papers, and links the talk names — captured so they survive
  even if the video disappears.

## Links
- **[04:12]** [[Card Title]] — why this one matters to the talk
- [[Card Title]] — description-only link, no timestamp
- `example.com/thing` — found but not carded (plain text so the note stays complete)

## Related Notes
- [[Real backlink found by searching the vault]]
```

**`## Links`** — populated from Step 3.5. Cards the user approved appear as `[[wikilinks]]`;
links they declined or that were dropped appear as plain text, so the note records what the video
offered regardless of what got carded. Omit the section entirely when the video named nothing.

**In goal mode**, let the question bias depth without distorting the note: develop the
goal-relevant Main Ideas further and order `## Reference Snapshot` with the goal-relevant entries
first. Do **not** truncate the rest or turn the note into a goal document — someone reading it a
year from now with no memory of the question should still get a fair account of the talk. The
answer itself lives in its own note (Step 6.6).

**Adaptive sections** — include a section only when the talk has the material:
- Add `## Architecture` and/or `## Code Examples` (with real code blocks) for **technical**
  talks that show systems or code. Skip them for non-technical talks — never leave an empty
  or padded section.
- Add `## Open Questions / Follow-Ups` when the talk leaves genuine threads open.
- `## Notable Quotes` / `## Reference Snapshot` — include when there's something worth
  keeping; omit if truly nothing.

**Style:**
- Developed prose with **bold lead-ins**, not telegraphic fragments. Preserve quotes verbatim.
- Substantive over fleeting — the goal is a note you'd return to, not a highlight reel.
- No HTML entities, no `[music]`/filler — the cleaned transcript already handles this.

**Slides (only in slides mode) — both, sparing inline:**
- **Gallery** — a `## Slides` section (place it after `## Reference Snapshot`, before
  `## Related Notes`) lists **every** kept slide chronologically with its `[mm:ss]` and caption.
- **Inline — sparingly** — embed a slide next to a Main Idea **only** when it directly
  illustrates that point. A handful at most; most slides live only in the gallery. Reading
  flow beats decoration.
- Always use the explicit `.png` extension: `![[IMG-<SLUG>-slide-NN.png]]`.
- In text-only runs, omit the `## Slides` section and all inline embeds.

```markdown
## Slides
- **[mm:ss]** One-line caption describing what's on the slide
  ![[IMG-<SLUG>-slide-01.png]]
```

