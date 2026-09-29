---
name: product-story-map
description: >
  Generate an Obsidian .canvas story map for a feature or workstream — swimlane
  groups per surface, short named cards on a fixed grid, and arrows showing what
  depends on what. Built for a PM scanning names and dependencies, not reading
  scope. Use when the user says '/product-story-map', 'make the story map',
  'story map canvas', 'dependency wall', or has an execution map / ticket list /
  roadmap slice ready to lay out visually. Produces the canvas only — stories and
  tickets come from /product-stories or /create-github-issue.
argument-hint: "<feature-or-workstream> [--source <note>]"
metadata:
  phase: deliver
  category: product
  related: product-stories (markdown stories), obsidian (canvas conventions)
---

# Product — Story Map Canvas

Lay a feature's work out as a wall: one swimlane per surface, one short card per story, and arrows for the real dependencies. The output is a single `.canvas` file the user pans in Obsidian during planning and sprint conversations.

**The audience is a PM.** They want to see what the pieces are called and what blocks what. They do not want to read scope on a canvas — that is what the ticket is for. A wall of prose is the single most common way this artifact fails.

## When to Use

- User says `/product-story-map`, "make the story map", "story map canvas", "dependency wall"
- An execution map, ticket list, or roadmap slice exists and needs the visual wall
- A workstream kickoff needs the "what runs in parallel, what waits" picture

Not for: markdown user stories (`/product-stories`), free-form thinking boards (plain canvas), diagrams inside a note (`obsidian` skill, mermaid).

## Inputs

- **Required**: the feature or workstream name.
- **Source of cards** (find in this order): an execution map / plan note with tickets, a tracker epic's ticket list the user pastes or names, a roadmap slice, or the conversation. Each card needs only a short name, an optional ticket id, and a status.
- **Lanes**: derive from surfaces (a shared library, a page, the backend, release). Confirm the lane list with the user when it is not obvious.

## The layout contract

Fixed grid — every canvas this skill writes uses these numbers, so maps stay comparable:

| Element | Geometry |
|---|---|
| Card (`type: text`) | 320 × 90, x pitch 360 (columns at 0, 360, 720, 1080, 1440), first row at lane y + 50 |
| Lane (`type: group`) | x −40, width 1880 (5 columns), height 170 per card row, y pitch = height + 20 |
| Legend card | (0, 0), 760 × 100 |
| First lane | y 200 |

**Card text — two lines, and that is the ceiling:**

```
## <short name>
<TICKET-ID> <status glyph>
```

Three or four words in the title. **No scope line, no description, no wave markers.** A card that needs explaining is a card whose detail belongs in its ticket.

Status glyphs, one per card, nothing more elaborate: `✅` landed · `🚧` built but not landed · `⬜` not built.

**Colors** (Obsidian canvas palette): default for a normal card; `"5"` cyan for a lane of shared foundation consumed by the others; `"3"` yellow for a lane or card that is a hard blocker. Nothing else — colour is a signal, not decoration.

**Edges carry the dependencies, and they are half of what the map is for.** Order lanes so work flows downward (shared foundation at the top, release at the bottom), then draw an arrow for each real "needs this first". Keep to the load-bearing ones, roughly eight to twelve — an arrow a reader can infer from lane order is noise. Use `bottom → top` between lanes, `right → left` within one.

## Workflow

1. **Gather the cards.** Read the source note(s). One card per story, named in three or four words. Anything without a ticket id renders without one — the map is honest about what is not filed yet.
2. **Derive the lanes**, ordered so dependencies flow downward: shared foundation first, the shipping surface next, release last. 3 to 6 lanes is the healthy range.
3. **Confirm the shape** with the user in one short round when the lanes are not obvious. Skip if the source note already implies them.
4. **Compute the grid.** Apply the geometry table exactly; do not hand-tune positions.
5. **Draw the edges** for the dependencies that are not already obvious from lane order.
6. **Write the file.** `Work/Workstreams/<ws>/Story Map.canvas` for work, `Projects/<project>/product/<feature>/<Feature> Story Map.canvas` for products.
7. **Validate the JSON** — parse it and check every edge's `fromNode`/`toNode` resolves to a node id. A dangling edge fails silently in Obsidian.
8. **Open it in Obsidian** (`obsidian://open?vault=<vault-name>&file=<url-encoded path>`, including the `.canvas` extension).

## Examples

**Input:** `/product-story-map saved-views --source "Execution Map"`

**Output:** `Work/Workstreams/saved-views/Story Map.canvas` — lanes for Table library (cyan) / Saved views / Backend / Projects page / Release, each card a three-word name plus its ticket and status, and ten arrows showing the critical path from the wrapper through the chip row to the migration and out to the ramp.

## Quality Checklist

- [ ] Every card is two lines: a short name and a ticket + status
- [ ] No card carries a scope or description line
- [ ] Geometry matches the table — no hand-tuned positions
- [ ] Lanes flow downward in dependency order
- [ ] Edges cover the load-bearing dependencies and nothing inferable
- [ ] JSON parses and no edge points at a missing node
- [ ] File opened in Obsidian after writing

## Tips

- If a card's name needs a qualifier to make sense, the lane label is probably wrong.
- When a lane exceeds 5 cards, give it a second row (height 340) before widening the canvas.
- On a re-run, refresh the status glyphs in place and never reflow positions unless cards were added — stable positions are what make diffs readable.
- Work owned by another team gets one pointer card, not a lane of their tickets.
