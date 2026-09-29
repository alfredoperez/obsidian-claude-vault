---
name: create-decision
description: >
  Escalate a decision out of chat and into a document the user can read, think about, and answer
  in their own time. Use when a choice is too big for an inline prompt: several questions
  interact, the user needs findings or evidence in front of them before choosing, the options
  need real explanation, or you are about to ask a question whose answer changes the direction
  of the work. Also use when the user says '/create-decision', "put this in a doc", "I need to think about
  this", "give me the background first", or asks to see the options written down. Writes a
  decision doc into the vault, opens it in Obsidian, then reads their answers back and asks the
  next round. Other skills call this when their own questions get too heavy for chat.
argument-hint: "<what is being decided> [--round-2] [--no-open]"
metadata:
  author: alfredo
  source: kaiju
# effort: weighs options the user will act on
effort: high
---

# Decide

A decision document is what you reach for when `AskUserQuestion` is the wrong shape. Four options
and a one-line description is fine for "which library". It is useless for "here is what eighteen
videos argued, here are the nine things you could build, which three matter."

The failure this fixes is specific. Asking a complex question in chat forces an answer before the
person has the material to answer with. They either guess, or they say "let me think" and the
thread dies. A document lets them read the findings, see every question at once, tick what they
prefer, add the "yes, but", and hand it back.

**This skill is model-invoked on purpose.** Most skills should be user-invoked, because every
model-invoked description is a permanent context cost. This one earns it: its entire value is
*you* noticing that a decision has outgrown a chat prompt. If the user has to remember to ask for
it, it will not get used at the moment it is needed.

> [!danger] **Do not add `disable-model-invocation` to this file.**
> It has been added once already, during a sweep that muted every skill reachable by name, and
> this skill is reachable by name. That is the wrong test for this one file. Muting it does not
> make it harder to reach; it removes the only thing that makes it *fire* — a model noticing that
> a chat question has outgrown chat. A user who could tell would have asked for a doc already.
>
> The symptom of getting this wrong is not an error. It is round after round of `AskUserQuestion`
> on a decision that needed a document three rounds ago.

## When to reach for it

Escalate to a doc when **any two** of these are true:

- The decision needs background the user has not read yet.
- There are more than three questions, and they interact.
- An option needs more than one line to be fair to it.
- Getting it wrong sends the work in a direction that is expensive to undo.
- The user has already said some version of "I need to think about this."

Stay in chat when it is one question, the options are self-evident, and being wrong is cheap.
**Do not produce a document for a decision that fits in a sentence.** A ceremonial doc for a
trivial choice is worse than no doc, because it teaches the user to skim them.

## Where it goes

| | |
|---|---|
| Path | `_Decisions/Decision - <Topic>.md` |
| Follow-up rounds | **the same file**, never a new one |
| Lifespan | `ephemeral`, `expires:` 21 days out |
| Cleanup | `groom` sweeps expired ephemerals; nothing to do by hand |

These are working documents, not knowledge. A decision worth keeping graduates: the *outcome*
moves into the note, spec, or skill it affects, and the doc is allowed to expire. Do not archive
them by reflex.

## Reading levels

Every part of this document has an assigned tier, and the tiers are what let one document serve
both someone who trusts the recommendations and someone who wants to audit them.

| Part | Tier |
|---|---|
| Question titles, option labels, option one-liners | **ELI5** |
| The per-question summary, the document's short version | **ELI10** |
| "Why this matters" | **ELI15** |
| The folded "Expert detail" block | **Expert** |

The ladder, in one line each: **ELI5** — a label a child could act on, no jargon; **ELI10** — one or two plain sentences that frame the choice; **ELI15** — the mechanism and the trade-off, carried by a table or diagram; **Expert** — everything else, folded so it never blocks the read.

## Frontmatter

```yaml
---
type: decision-doc
topic: <short topic name>
created: YYYY-MM-DD
expires: YYYY-MM-DD          # created + 21d
lifespan: ephemeral
status: open                 # open | partial | answered
round: 1
cssclasses:                  # REQUIRED — both of them
  - decision-doc
  - brief
sources:
  - "[[<note>]]"
---
```

`decision-doc` is what styles the questions. `brief` suppresses the duplicate filename title,
since the note carries its own H1.

## Structure

**Plain markdown. No callouts around a question.** A callout needs `> ` on every line, which makes
typing into one miserable in edit mode, and these documents exist to be written in.

```markdown
# <Topic>

## 💬 Talk to me

💬 

---

## The short version

<ELI10. Two to four sentences: what is being decided, why now, what changes after.>

> [!figure] <caption>          ← ONLY if the decision genuinely has a visual shape

## What I'm assuming

- <assumption>
- <assumption>

If one of these is wrong, say so up in the box. A wrong assumption changes the questions, not
just the answers.

---

## Q1 · <ELI5 title>

*<ELI10 summary. One or two sentences framing the choice.>*

- [ ] **<Option>** ==Recommended== — <ELI5 one-liner>
- [ ] **<Option>** — <ELI5 one-liner>

💬 

> [!info]- Why this matters
> <ELI15, carried by the right device — table, diagram, cards, stat tiles.>

> [!example]- Expert detail
> <Expert tier. Omit entirely unless it earns its place.>

---

## Decided

> [!decision] D1 · <what was chosen>
> **because** <their reason, in their words where they gave one>
> **revisit** if <the condition that would reopen it>
```

### The order is the API

There are no classes on the question parts. The CSS keys off document structure, so these are hard
rules, not style preferences:

- **Nothing may sit between the options list and the `💬` line.** Insert a table or a card row
  there and the typing slot silently loses its styling.
- **The paragraph immediately after the checkbox list is the typing slot.** Leave it as a bare
  `💬 ` with a trailing space.
- **The ELI10 summary is an italic-only paragraph** directly under the `##`. `vault.css` already
  demotes that to a muted subtitle, so it needs no markup of its own.
- **Options stay a list.** Obsidian cannot render checkboxes inside table cells. Never restructure
  options as a table, however tempting the comparison looks.
- **`==Recommended==` goes on the option**, not on a line below it. Exactly one per question.
- **Never pre-tick anything.** A ticked box always means the user decided. Pre-tick and you can no
  longer tell agreement from inattention.

### Clear answered questions out as you go

**An answered question is deleted from the document, not left ticked.** Its answer becomes a
`[!decision]` nested in the phase it belongs to, and the `## Q<n>` block goes away.

This is the single thing that keeps a decision doc usable past round three. A doc that accumulates
answered questions reaches twenty headings, of which three need the reader, and they have to check
every one to find out which. By round fourteen nobody opens it. **The document should show only
what is still open**, so its length is the size of the remaining decision and not a history of the
conversation.

The history is not lost. It moves into the phase rail, where a decision is filed under the work it
produced rather than under the order it was asked in, which is the more useful index anyway.

**Do this every time you read answers back**, before writing the next round. Not as a cleanup pass
later.

- **Numbering does not get reused.** Q9 stays Q9 in the decision record even after the block is
  gone. Renumbering breaks every reference to it in chat and in commits.
- **A question answered with a comment instead of a tick still counts as answered.** Record what
  the comment actually decided, in their words, and remove the block. If the comment changed the
  question rather than answering it, that is a new question with a new number.
- **A question that was overtaken by events gets a decision too**, marked as such. "Answered by
  events" is a real outcome and hiding it makes the doc look like it drifted.

### The phase rail

Once a doc has been answered once, it grows a `## Where we are` section directly under the comment
box. It is how the reader knows what the decisions actually bought them.

```markdown
## Where we are

> [!phase]- Phase 0 · Groundwork · <code class="done">done</code>
> **shipped** what landed.

> [!phase]+ Phase 1 · The thing in flight · <code class="now">now</code>
> **does** what it changes.
> **why now** what makes it first.

> [!phase]- Phase 2 · Follows this one · <code class="next">next</code>
> **waits on** Phase 1.
```

Five states, and **`later` is not one of them**: `done`, `now`, `next`, `queued`, `parked`.
`queued` means ready but not prioritised; `parked` means blocked on something outside the work.
"Later" hides *which* of those it is, which is the only interesting part.

**Fold everything except the `now`** — trailing `-` collapses, `+` stays open. A phase rail should
read as a column of coloured chips with one block open. Every phase body says what it **waits on**,
even when the answer is "nothing".

Exactly one phase is `now`. If two are, the plan is not a plan.

### Decisions live inside their phase

There is no standalone `## Decided` section. Once phases exist, every decision nests inside the
phase it produced, folded:

```markdown
> [!phase]+ Phase 1 · Fix what is currently wrong · <code class="now">now</code>
> **does** ...
>
> > [!decision]- D1 · What was chosen
> > **because** their reason, in their words where they gave one
> > **revisit** if the condition that would reopen it
```

This is what keeps a doc readable as it grows. A separate log puts every decision ever made between
the reader and the questions that still need them, and the reader has to scroll past their own
history to reach the ask. Nested, the whole rail collapses to a column of chips.

Number decisions `D1`, `D2` in the order they were decided, across all rounds, and **never
renumber** — a decision is referred to by number long after the doc expires.

### Put the open questions above the phase rail

The thing that needs the reader goes first. Comment box, then the open round, then the rail, then
reference material. Orientation is one folded section away; the ask is not.

### The two boxes at the top

Both are new and both matter more than they look.

**`## 💬 Talk to me`** is the only slot not scoped to a question you chose. It is where the user
says "you are asking the wrong thing" or supplies context you did not have. Read it first, before
any of the ticks.

**`## What I'm assuming`** is you exposing your premises so they can be corrected. Three to five
lines. Assume things that would change the *questions* if wrong, not trivia. When a decision doc
comes back with surprising answers, a wrong assumption is usually why.

## Making the background worth reading

Before writing any background as prose, ask which device carries it better. A wall of paragraphs is
the default failure mode of these documents.

| Device | Markdown | Reach for it when |
|---|---|---|
| Table | plain markdown table | Comparing three or more things on the same axes |
| Diagram | `> [!figure]` + themed ```mermaid | The shape is a flow, a sequence, or a lifecycle |
| Cards | `> [!cards\|3]` + nested `> > [!card]` | Parallel things with no ordering |
| Stat tiles | `> [!stats]` + `<span class="stat"><b>660</b> tokens</span>` | The argument IS a number |
| Capability matrix | table + `<span class="c-ok">` chips + `[!legend]` | Feature-by-feature comparison |
| Steps | `<span class="step">plan</span>` | A short pipeline, stated inline |
| Terminal | `> [!terminal]` + ```shell-session | A real command and its real output |
| Tree | `> [!tree]` | File or folder structure |
| Quote | `> [!quote]` | One line from a source doing the arguing |

Full syntax for all of these lives in the `obsidian` skill's `obsidian/references/components.md`.

**Visuals only where the shape is genuinely visual.** A diagram belongs when the thing being
explained *is* a flow, a sequence, or a lifecycle. Otherwise a table. The vault's own rule, stated
three times across the obsidian skill, is **do not decorate** — a decorative diagram costs you
credibility on the ones that matter.

### Three traps that will bite

- **The cards clamp.** Unless the wrapper is `|1`, every nested callout's paragraph is clamped to
  one line until hovered. **Card bodies must be lists, not paragraphs.** Lists escape the clamp.
- **Mermaid `timeline` is banned in this vault** — it ignores the theme variables and renders
  orange with no way to fix it. Use `flowchart LR` for anything time-shaped.
- **Never fabricate a schedule.** No invented dates, no speculative Gantt. A chart with a confident
  "today" line that you made up is a lie the reader will trust in three weeks.

Also inherited from the `obsidian` skill's `obsidian/references/diagrams.md`: **no transitive edges** (if `A → B → E`, do not also
draw `A → E`), and the blessed diagram types are `flowchart LR`, `sequenceDiagram`, and
`stateDiagram-v2`. The house init block is in the `obsidian` skill's `references/components.md` (*Mermaid rules*) — copy it verbatim.

## Workflow

### Step 1: Decide whether this is even a doc

Apply the test above. If it is one clean question, ask it in chat and stop.

### Step 2: Do the reading first

The doc is only worth making if it carries findings the user does not already have. Gather them
before writing: read the source notes, run the greps, check what already exists in the vault or the
repo. **A question you could have answered yourself must not appear in the document.** That is the
single fastest way to make these docs feel like homework.

### Step 3: Write it

- **Every question carries a recommendation.** No exceptions. A question with no recommended answer
  moves the whole cost of thinking onto the reader, which is what this skill exists to avoid.
- **Two to four options.** More than four means the question is not thought through yet.
- **Number them `Q1`, `Q2`, continuing across rounds.** Round two starts at Q8 if round one ended
  at Q7. Never restart the numbering, and never reuse a number.
- **Every round states its objective**, as an italic line under the `## Open questions — round N`
  heading: how many questions, roughly how long, and **what we are doing** in plain words. A reader
  returning after two days needs to know what this round is *for* before reading any of it.
- **Order by consequence.** The question that changes the most work goes first, not the easiest.
- **Say when a question is blocked.** If Q4 only matters if Q2 goes a certain way, either write that
  into Q4 or hold it for the next round.

Ask only what is on the **frontier** — decisions whose prerequisites are already settled. Everything
downstream waits. A doc with twelve questions where six depend on the other six is a doc that does
not get answered.

### Step 4: Open it in Obsidian

Unless `--no-open`:

```bash
open "obsidian://open?vault=<vault-name>&file=$(python3 -c "
import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "_Decisions/Decision - <Topic>")"
```

Then say, in one line, how many questions there are and roughly how long it will take. Stop and
wait. **Do not continue the work while it is open** — the direction is unsettled.

### Step 5: Read it back

When they say they are done, re-read the file, in this order:

1. **The `## 💬 Talk to me` box first.** It can invalidate the whole question set.
2. **`## What I'm assuming`** — did they strike one out?
3. Which options are ticked (`- [x]`).
4. Anything typed after a per-question `💬`.
5. Edits they made to the prose, which are often the most informative part.
6. Questions left blank — usually the question was wrong, not forgotten.

**Reflect their answers back in one short block before acting**, especially where a note qualified a
tick. A checked box plus "but only for kaiju" is not the same answer as a checked box.

### Step 6: Log and re-round

Move every answered question into `## Decided` as a `[!decision]`, in their words where they gave
words. Then either:

- **Done** — set `status: answered`, and say plainly what happens next.
- **Round two** — bump `round:`, replace the questions with the new frontier their answers just
  unblocked, re-open the file. Old questions stay in `## Decided`, so the file is the whole history
  of how the thinking moved.

Never silently drop a question they did not answer. Either re-ask it with better framing, or say why
it stopped mattering.

## Being called by another skill

Any skill whose questions have outgrown chat should hand off here rather than growing its own
document format. A planning skill is the obvious caller: it runs the live interrogation, and when a branch
needs real reading it exports that branch as a decision doc instead of asking blind.

A caller passes the topic, the findings it already gathered, and the questions it wants asked. This
skill owns the document, the components, and the round-trip. Callers do not write their own.

## Quality checklist

- [ ] The decision genuinely needed a document — it was not one clean question.
- [ ] Every question I could have answered myself was answered, not asked.
- [ ] Question titles and option labels pass the ELI5 test — no internal jargon.
- [ ] Every question carries exactly one `==Recommended==`, on the option itself.
- [ ] Nothing was pre-ticked.
- [ ] No question has more than four options, and options are a list, not a table.
- [ ] Nothing sits between the options and the `💬` line.
- [ ] Questions are answerable without expanding a single fold.
- [ ] Every background was checked against the device menu before being written as prose.
- [ ] Any diagram earns its place; no decoration, no fabricated schedule, no `timeline`.
- [ ] Card bodies are lists, not paragraphs.
- [ ] `cssclasses: [decision-doc, brief]` and `expires:` are in the frontmatter.
- [ ] The comment box and the assumptions block are both present.
- [ ] The file was opened in Obsidian and I stopped and waited.
- [ ] On read-back: comment box first, then assumptions, then ticks, then notes.

## Tips

- **The recommendation is the product.** A user reading a good decision doc should mostly be
  confirming, occasionally overruling. If they are doing original thinking on every question, you
  did not do enough reading in step 2.
- **Write the `💬` slots expecting them to be used.** The qualification someone adds to a tick is
  usually the constraint you did not know about.
- **A blank answer is data.** It usually means the question was badly framed or premature.
- **An overruled recommendation is the most valuable event in the document.** Ask why before moving
  on; the reason usually generalises to the next ten questions.
- **Let them expire.** These are scaffolding. The decision lives on in the thing it changed.
