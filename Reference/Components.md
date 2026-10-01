---
type: reference
lifespan: evergreen
source: kaiju obsidian skill
description: The component vocabulary — every custom callout vault.css styles, with the markdown to copy
tags: [reference, components, vault-css]
---

# Components

Native Obsidian markdown, styled by `vault.css`. Reach for one only when the content earns
it — most notes are prose and a callout or two. **Do not decorate.**

### Callouts

| Component | Markdown | Use for |
|---|---|---|
| Thesis | `> [!note] The claim, in one line.` | the argument, stated up front |
| Caution | `> [!warning] The one hard part.` | risk, gotcha, the thing that bites |
| Confirmed | `> [!success] The shape.` | something settled or verified |
| Band / CTA | `> [!tip] The one thing to build first` | the closing call to action |
| Detail | `> [!example]- data & acceptance` | collapsible supporting detail |
| Capture | `> [!capture] Screenshot — the drift report` | an evidence slot **still to be filled** |

**Always give a callout a title.** A bare `> [!note]` renders a dead bar that
says "Note". Promote the lead sentence into the title instead.

### Decision docs — questions the reader answers in the file

Written by the `create-decision` skill. Opt in with `cssclasses: [decision-doc, brief]`. Everything else is
**plain markdown on purpose**: a callout needs `> ` on every line, which makes typing into one
miserable in edit mode, and these documents exist to be written in.

```markdown
## Q1 · Where should decision docs live?

*One italic line framing the choice. The global heading rules demote it to a muted subtitle.*

- [ ] **Per project** ==Recommended== — next to the work it belongs to
- [ ] **One inbox** — easy to sweep on a schedule

💬 

> [!info]- Why this matters
> The background, carried by a table or a diagram rather than prose.
```

**The order is the API.** There are no classes on the question parts; the CSS keys off document
structure. So:

- **Nothing between the options list and the `💬` line.** A table or card row inserted there
  silently kills the typing slot's styling.
- The paragraph immediately after the checkbox list **is** the typing slot.
- The italic-only paragraph under the `##` **is** the summary. No markup needed.
- **Options stay a list** — Obsidian cannot render checkboxes inside table cells.
- `==Recommended==` goes **on** the option, exactly once per question. `mark` rather than inline
  code, because options legitimately contain code spans and a blanket code rule would pill those too.
- **Never pre-tick.** A ticked box must always mean the reader decided.

Two blocks belong at the top of every one of these, above the questions: a `## 💬 Talk to me` box
(the only slot not scoped to a question the author chose) and a `## What I'm assuming` list (the
author's premises, exposed so they can be corrected). A wrong assumption changes the questions, not
just the answers.

Reading levels are `create-decision`'s own vocabulary — see that skill.

### Capture — a slot waiting for evidence

A runbook is mostly holes: paste the output here, drop the screenshot there. An
HTML comment (`<!-- paste here -->`) renders as *nothing*, so an unfilled slot is
invisible at exactly the moment you're scanning for what's left to do.
`[!capture]` is a dashed frame you can't miss; once the evidence lands inside, the
frame stops being a prompt and becomes its caption.

```markdown
> [!capture] Screenshot — the viewer showing loaded and folded content
```

**An empty slot must look empty.** Never pre-fill it with a placeholder — a `{}`
or a `[paste output]` reads like real evidence at a glance, and a runbook whose
holes look filled is worse than one with no slots at all. Leave the body blank;
the callout says "empty" on its own. Use it for the slots a human fills by hand
(screenshots, pasted terminal output). For evidence that is *already* captured,
use `[!terminal]`, or collapse it into `[!example]-` so a completed runbook stays
scannable instead of becoming 3,000 lines of pasted JSON.

### Feedback region — the reader's notes to Claude, left in the file

The one component **Claude never writes**. The reader drops it mid-read (a hotkey, or a
top-level item in the right-click menu, kept out of any submenu because two menu levels is
exactly the friction that stops a note from being left) and Claude collects them later. It is a pair of dividers with a badge on the first line; everything
between them is plain markdown, so it wraps and formats like prose with no `>` to fight:

```markdown
---

<span class="badge-feedback">FEEDBACK</span> The dates in the second table are all off by one week.

---
```

The selection at insert time becomes the first line. `vault.css` paints the badge and the
opening divider purple so a region is visible at a scroll.

**Sweeping.** On "sweep the catalog feedback", "sweep the feedback in <note>", or the same in
other words, find every region (`grep -rn badge-feedback`, scoped to the note or folder named),
then for each one:

1. Read the feedback and the surrounding section.
2. Do what it asks: fix the note, or answer in one line right below the region when it is a
   question rather than an instruction.
3. Remove the whole region, both dividers included, once acted on. A swept region left in place
   reads as unfinished work the next time the note is opened.

Report one line per region: where it was, what it said, what changed. Never rewrite a region's
wording, and never insert one as a way of asking a question: that channel is the reader's.

### Status badges — inline NEW / existing / later / open

A spec tags each API, control, or decision with a status word. As bare `**NEW**` or
`` `existing` `` those read as noise; as inline pills the eye scans the *pattern* of
what's net-new versus already there. Use them in prose and inside table cells.

```markdown
**APIs:** pools list with counts — <span class="badge-new">new</span> `GET work-pool/list`

<span class="badge-open">open</span> Stage-row cascade rule still unspecified — owner: dispatch lead
```

| Class | Means | Tint |
|---|---|---|
| `badge-new` | built for this feature | green |
| `badge-existing` | already in the app today | grey |
| `badge-later` | follow-up release, not this scope | blue |
| `badge-open` | unresolved question or assumption | amber |

The word stays inside the span, so it is still searchable text. Define them once near
the top with a `[!legend]` whose swatches use the SAME badge classes:

```markdown
> [!legend]
> <span class="badge-new">new</span> built for this feature  <span class="badge-existing">existing</span> already in the app  <span class="badge-later">later</span> follow-up release  <span class="badge-open">open</span> unresolved
```

`badge-open` is the inline twin of a bottom **Open Questions** roll-up: tag the gap
*where it lives* in the section, and still list it in the register at the end. Don't
wrap each open item in its own callout — that fragments the read; inline keeps flow.

#### Option chips — a slot's pickable alternatives

A third axis. A badge judges *content* ("is this API new?"), a review chip tracks a
*section's state*; an option chip is one **choice a slot offers**, with a leading dot
carrying its readiness. Built for catalogs where the reader picks between variants —
one table row per slot, one chip per choice:

```markdown
| Draft the spec | <span class="opt-ok opt-default">User stories</span> <span class="opt-todo">EARS requirements</span> <span class="opt-later">Lens menu</span> |
```

| Class | Dot | Means |
|---|---|---|
| `opt-ok` | green | the body already exists — offering it is wiring, not writing |
| `opt-todo` | amber | to author, but the shape is fully specified |
| `opt-later` | grey | blocked on engine work |
| + `opt-default` | ring | the choice that ships as the default — exactly one per row |

The word stays inside the span, so the cell is searchable. Define them once with a
`[!legend]` built from the SAME classes. Don't mix axes in one cell: a badge is a
verdict, a `chip` span is a tag, an option chip is a choice.

#### Review-state chips — a section walk

A **different axis** from the badges above. Those tag *content* ("is this API new?");
these tag a whole section's *review state* as you walk a draft. Hand-set the word next
to the heading; a plain span, no plugin, survives a Notion round-trip.

```markdown
## 3 · Create / edit dialog  <span class="review-questions">questions</span>
```

| Class | Means | Tint |
|---|---|---|
| `review-todo` | not yet reviewed | grey outline |
| `review-questions` | reviewed, has open items | amber outline |
| `review-ready` | reviewed, signed off | green outline |

They are **outline**, not filled — so a grey `review-todo` never reads as the grey
*filled* `badge-existing` sitting beside it. A section carrying a `badge-open` can't be
`review-ready`; start it at `review-questions`. Obsidian has no native multi-state click
toggle without a plugin (Meta Bind) — this is the plugin-free, sync-safe substitute.

### Cards — a 2/3-up compare

```markdown
> [!cards|2]
> > [!card|blue] after Phase 0–1 — the MVP
> > What you get at the MVP.
>
> > [!card|green] at the full vision
> > What you get at the end.
```

Tints are `blue`, `green`, `amber`. **Tint them apart** — a two-up compare is
two different things, and matched grey boxes make the reader work to tell them
apart. `|3`, `|4`, and `|5` widen the grid; all of them collapse to one column
under 900px. **`|1` is a lone card at full width** — a finalist, a single
proposal, a picked winner. (Don't reach for `|1` to shrink a card; it's the
opposite — it spans the whole content column.)

### Tickets and phases

```markdown
> [!ticket] A · Teach the pipeline when it's finished · `small`
> **what** Read the pipeline as an ordered list of steps.
> **why** There is no "finished" event, so the tail has nowhere to attach.
>
> > [!example]- data & acceptance
> > The schema and the acceptance criteria.

> [!phase] Phase 0 · Node engine — the pipeline becomes data · `MVP`
> **adds** What this phase changes.
> ```yaml
> workflow: standard
> ```
```

The trailing `` `chip` `` renders as a pill (size, MVP, priority).


**Status chips on a phase.** A plain `` `chip` `` in the title takes the callout's own colour —
right for a size (`small`, `MVP`), wrong for a **state**, because every phase then reads
identically. States get a class:

```markdown
> [!phase]- Phase 0 · Groundwork · <code class="done">done</code>
> [!phase]+ Phase 1 · The thing in flight · <code class="now">now</code>
> [!phase]- Phase 2 · Follows this one · <code class="next">next</code>
> [!phase]- Phase 3 · Ready, not prioritised · <code class="queued">queued</code>
> [!phase]- Phase 4 · Blocked outside the work · <code class="parked">parked</code>
```

Five states. **`later` is deliberately not one of them** — it says nothing `queued` and `parked`
do not say better, and it hides *why* a thing is not next. Trailing `-` folds, `+` stays open:
fold everything except the `now`, so a phase rail reads as a column of chips with one open block.

### Capability matrix

Use **colored cells, never emoji.** Emoji are loud, unevenly sized, and pull
the eye to the icon instead of the shape of the data.

```markdown
| Capability | Companion | spec-kit |
| --- | --- | --- |
| In-editor GUI | <span class="c-ok">yes</span> | <span class="c-no">no</span> |
| Auto-mode | <span class="c-no">no</span> | <span class="c-mid">partial</span> |

> [!legend]
> <span class="c-ok chip-key"></span> have / strong  <span class="c-mid chip-key"></span> partial  <span class="c-no chip-key"></span> missing
```

`c-ok` green, `c-mid` amber, `c-no` red. The word stays inside the span, so the
cell is still searchable text.

### Story map

A story map is a **grid**, so it is a table. The backbone (the user's activities)
runs across the top; releases stack downward; stories are sticky notes.

```markdown
> [!storymap] By release
> | | Author a spec | Build it | Ship it |
> | --- | --- | --- | --- |
> | **Skeleton** | <span class="story-done">specify · plan</span> | <span class="story-done">implement</span> | <span class="story-cut">manual PR</span> |
> | **MVP** | <span class="story">A · knows it's finished</span> | <span class="story">B · history</span> | <span class="story">D · open PR</span> |
```

`story` amber (planned), `story-done` green (shipped), `story-cut` struck-through
(the gap today). A column that is empty in the skeleton row and full in the MVP
row **is the argument** — the map should make the gap visible without prose.

**Beyond ~4 activities × 3 releases, build the map as a canvas** and embed it
(`![[x-story-map.canvas]]`) — spatial walls are what canvas is for; the table stays
for maps small enough to read as one grid.

**The legend must use the SAME classes as the cells.** Using the matrix chips
(`c-ok`/`c-mid`/`c-no`) to explain a story map's sticky notes produces a key that
shows colours which appear nowhere in the map. The key then lies.

### Tree — folder/file trees

Two variants. **`[!tree]` callout is the default for guides and reports** — it gets
folder icons, level guides, and per-part color from plain markdown: title = root path,
**bold** = folder, plain = file, *italic* = annotation, `backticks` = variable segment:

```markdown
> [!tree] Projects/`<project>`/
> - `<project>`.md — *the hub: status, repo, what it is*
> - **inbox/** — *agent communication*
> - **plans/`<subject>`/** — *one folder per sub-effort*
>     - plan.md — *the decision doc*
```

The ```` ```tree ```` fence is the quick variant for verbatim dumps (`tree` output,
deep listings) — labeled card, no per-part color. Never use a bare fence. The stylesheet
gives it a labeled card ("FOLDER TREE"), an accent edge, and tall line-height —
trees are scanned line-by-line hunting for one entry, so they get air. Annotate
entries with `← what lives here`; the no-wrap rule keeps annotations on their line.

````markdown
```tree
Projects/<project>/
  <project>.md          ← the hub: status, repo, what it is
  inbox/                ← agent communication
  plans/<subject>/      ← one folder per sub-effort
```
````

### Stats, lead, chip, steps, kbd, pull quote

The HTML-brief survivors, all native + `vault.css`:

```markdown
> [!stats]
> <span class="stat"><b>21.3m</b> median wall time</span> <span class="stat"><b>9/9</b> cells correct</span>

> [!lead]
> One paragraph that frames the whole note — first thing after the title. No box, one size up.

prose tags: <span class="chip">drift</span>            ← neutral label, carries NO verdict (badges do)
pipeline:  <span class="step">specify</span> <span class="step">plan</span>   ← arrows draw themselves
keycaps:   <kbd>Cmd</kbd><kbd>K</kbd>

> [!quote]
> The lifted line — article drafts, retros. Renders as an editorial pull quote, not a box.
```

Rules: `[!lead]` at most once per note, directly under the title. `[!stats]` for 2–5
numbers that ARE the finding — more than that is a table. `chip` vs badge: a chip tags,
a badge judges. `[!quote]` replaces the old blockquote habit in articles only; in
reports a plain `>` quote stays a quote.

### Terminal and figure

````markdown
> [!terminal] what the dev sees
> ```text
> implement ✓ → review 2 findings → PR #214 → status completed
> ```

> [!figure] born in `specs/` → distilled at the tail → lives next to the code
>
> ```mermaid
> flowchart LR
>   A["author"] --> B["implement → review"] --> C["living spec"]
> ```
````

Diagrams are **Mermaid or Excalidraw** — both render natively. Never inline SVG.

#### Mermaid rules

**Theme it in the block.** Mermaid writes `fill`/`stroke` as inline attributes on
the SVG, so a CSS variable cannot override them. Without this you get lavender
nodes in a canary-yellow cluster:

```
%%{init: {'theme':'base','themeVariables':{
  'primaryColor':'#eef4fd','primaryTextColor':'#1f2428','primaryBorderColor':'#3d59a1',
  'lineColor':'#8b939c','fontFamily':'Geist, ui-sans-serif, sans-serif','fontSize':'13px',
  'clusterBkg':'#f8fafc','clusterBorder':'#dde2e8','edgeLabelBackground':'#ffffff'
}}}%%
```

**Draw the constraints, not every true relationship.** If `A → B → E`, do NOT also
draw `A → E`. It is true, it is transitive, and it turns the graph into spaghetti
that hides the actual shape. A dependency diagram earns its keep by showing the
*chains*; every redundant edge costs you one.

**Give roles a `classDef`.** The anchor (the thing that blocks the most) should
look like the anchor. Free work with no dependencies should look pickup-able.

### Schedules — do not fabricate them

A Gantt chart renders with a confident "today" line and looks like a plan. If you
invent the dates and durations, you have produced an authoritative-looking lie
that the user will trust in three weeks when they've forgotten you made it up.

If there are no real estimates, **either omit the schedule or derive it from data
that exists and say so on the page** — t-shirt sizes on the tickets, for example
(`small` = 2d, `medium` = 4d, `larger` = 8d), laid out against the real dependency
order. State the mapping in a `[!warning]` above the chart and tell the reader to
read the shape, not the dates.

## The rules that were learned the hard way

**Always title a callout.** A bare `> [!note]` renders a dead bar that just says "Note".
Promote the lead sentence into the title.

**Tint a compare apart.** Two matched grey boxes make the reader work out which is which.
That is the entire point of the layout.

**Never emoji in a matrix.** Emoji are loud, unevenly sized, and pull the eye to the icon
instead of the shape of the data. Use the chip spans — the word stays inside, so the cell
is still searchable text.

**A legend must use the SAME classes as the cells it explains.** Using the matrix chips to
explain a story map's sticky notes produces a key showing colours that appear nowhere in
the map. The key then lies.
