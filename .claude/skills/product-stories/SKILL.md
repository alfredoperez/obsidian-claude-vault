---
name: product-stories
description: >
  Decompose a roadmap slice into user stories with Given/When/Then acceptance
  criteria and INVEST validation. Writes one file per story to
  Projects/<project>/product/<feature>/stories/<Story Name>.md. Markdown only —
  does NOT push to a tracker (that's `/create-github-issue`). Use when the
  user says '/product-stories', '/stories', wants to break a slice into trackable
  work items, or has an approved roadmap ready.
argument-hint: "<feature-slug> [--slice now|next|later]"
metadata:
  phase: deliver
  category: product
  inspired_by: product-on-purpose/pm-skills (deliver-user-stories, Apache 2.0)
  related: kaiju github/create-github-issue (the one-off equivalent)
---

# Product — User Stories

Decompose a roadmap slice into deliverable user stories. Each story is a markdown file in `Projects/<project>/product/<feature>/stories/` with frontmatter declaring its slice, priority, and tracker placeholder. INVEST validation runs before each story is finalized. **This skill does not push to a tracker** — `/create-github-issue` does that.

## When to Use

- User says `/product-stories` or `/stories`
- User has a roadmap and wants to break a slice into stories
- User wants stories as markdown artifacts that can later be synced to a tracker
- Sprint planning, ticket writing, or backlog grooming for a feature

## Inputs

**Required:**
- **Feature slug** — resolves to `Projects/<project>/product/<feature>/`. Inferred from cwd.
- A slicing of the PRD's requirements into releases: a sibling `<Feature Name> Roadmap.md` if one exists, otherwise the release rows of `<Feature Name> Story Map.canvas` or the PRD's Milestones section

**Optional:**
- `--slice now|next|later` — which slice to decompose. Defaults to `now`. Run again per slice as work progresses.
- Persona override — defaults to the persona from `<Feature Name> Journey Map.md` if present, else asks
- Specific requirement IDs to focus on — e.g. `--reqs R001,R002,R003`

## Workflow

### Step 0: Interview the user (default mode)

When invoked, the skill **defaults to interview mode** — confirm the slice, persona, and any non-obvious AC details from the user via `AskUserQuestion` in 1–2 structured rounds before decomposing.

**Do not auto-compose from conversation context, even if the roadmap is explicit.** Treat any in-conversation brief as **default-option suggestions** in AskUserQuestion options (with "Other" as free-text override), never as the final answer.

**Suggested rounds for stories:**

- **Round 1 (slice + persona):** Which slice (now/next/later) / persona override if needed / max story count target
- **Round 2 (only if the slice's requirements look ambiguous):** Clarify which requirements collapse into one story vs split into peers

**Skip interview only when** the user explicitly says "use the brief I gave you" / "skip the interview". Then validate against refusal protocols (Step 2) and proceed.

### Step 1: Resolve feature folder + slice

Same inference rules as other product/ skills. If no `--slice`, default to `now` and confirm with the user before proceeding.

### Step 2: Refuse if upstream is missing or thin

1. **No roadmap, no story map and no Milestones in the PRD** → refuse: "Need the requirements sliced into releases first — a story map (`/product-story-map <feature>`) or a Milestones section in the PRD."
2. **Slice has zero requirements** → refuse: "Slice `<name>` is empty. Either re-slice or pick a different slice."
3. **PRD requirement text is missing or has only a placeholder** → refuse: "Requirement R00X has no clear text in the PRD. Fix the PRD first or stories will be guesses."

### Step 3: Pick persona

- If `<Feature Name> Journey Map.md` exists in the feature folder, default to its persona
- If multiple personas were defined, ask which applies to this slice
- If no persona is set anywhere, ask once and write back to the journey map (or PRD) for future runs

### Step 3.5: Load the canonical template

Before decomposing, **read `references/canonical-template.md`** — the embedded copy of the user's authoritative Feature Story / Tech Task templates (the canonical copy ships inside this skill). Every story this skill produces must match the canonical's:

- **Story statement** — bold `**As a** … **I want** … **so that** …` with line breaks
- **Themed AC sub-headers** (`#### [Theme] · [Figma]()` if a Figma link exists, else just the theme name) — flat AC lists are not allowed
- **Section order:** Story + Why This Matters + Acceptance Criteria + Access Control + **Dev details** + Out of Scope + References. `Dev details` is ONE block (rendered in Jira as one expand titled "Dev details") holding, in order: Suggested implementation pointers and Notes. The INVEST result is never written into the story. Nothing implementation-flavoured sits outside it.
- **No "How to test" section** — test steps belong in the tracker's test-plan field, never in the story body
- **References** never carries the epic link (the parent link already does); omit the section when it would be empty
- **AC rules** (canonical's "Universal AC Rules"): plain dashes only, no `- [ ]` checkboxes, no technical jargon / file paths / method names in AC — those go in Dev details
- **Sizing:** ≤1 day, ≤3 AC themes, ≤10 ACs total. If debating whether it fits, split.

The canonical template is the source of truth. Do not invent shape; conform.

### Step 4: Decompose

For each requirement (or coherent group of requirements) in the slice:

1. **Identify the user goal** — what a complete, valuable capability looks like
2. **Write the story statement** in canonical form:
   ```
   As a <persona>
   I want <action>
   So that <benefit>
   ```
   The benefit clause is critical — it explains why and helps prioritize later.
3. **Write Given/When/Then acceptance criteria** — each criterion is testable. Plain English, user perspective. **AC formatting matches the canonical user story template** — plain bullets, no `[ ]` checkboxes, no code identifiers, no file paths. Technical references go in the `Dev details` block.
4. **Apply INVEST validation** (refuse to finalize the story if it fails):
   - **I**ndependent — can be built without strict ordering against peer stories in the slice
   - **N**egotiable — implementation detail is open
   - **V**aluable — benefit clause is concrete user value, not "improves performance"
   - **E**stimable — engineering can size it (≈ 1–5 days; no T-shirt sizes here, that's another skill)
   - **S**mall — fits in one slice; if too big, split
   - **T**estable — every AC is verifiable

If a story fails INVEST, split or rewrite. Do not finalize.

5. **Write the Dev details block** — `### Dev details` with `#### Suggested implementation` (approach, key files, proven code / spike branch and commits, gating wiring, dependencies, suggested split, risks — omit bullets that don't apply), `#### Notes`. Step 4's INVEST result stays out of the file — it is a gate, not content. When the story is pushed to a tracker, this heading and its body become the one collapsed `Dev details` block.
6. **List Out of scope** — what's adjacent but explicitly NOT in this story

### Step 5: Number + name

- Numbering: per-project sequential. Scan `Projects/<project>/product/<feature>/stories/` for existing `STORY-NNN-*.md` files and continue from the highest. Stories from other features in the same project share the counter? **No — per-feature counter is simpler.** Scan only the current feature folder.
- Slug: kebab-case capability — e.g. `STORY-001-persistent-claude-sidebar.md`, `STORY-002-phase-action-buttons.md`

### Step 5.5: Offer diagram augmentation (optional, never forced, story-by-story)

Stories rarely benefit from diagrams (they describe user value, not system structure). **Default: skip.** Only offer when a specific story shows one of these patterns:

**Detection heuristics for a single story:**
- **Complex state machine in ACs** (>3 distinct states the user moves through) → state diagram
- **Sequence with branches** (>3 distinct interactions with conditional paths) → sequence diagram
- **Side-by-side current vs target behavior** explicit in the story → contrast diagram

**If a story shows one of these patterns, ask the user via `AskUserQuestion`:**
- Question: "Story STORY-NNN has a complex flow. Would a diagram help?"
- Options: `{ "Skip", "Sequence diagram", "State diagram", "Contrast diagram" }`

**Never auto-generate.** Only draw one if the user picks a generate option.

**If user picks generate:**
1. Draw it as an Excalidraw file (the `create-diagram` skill if installed; otherwise write the `.excalidraw` JSON by hand) from a focused prompt scoped to that one story
2. Save to `~Attachments/Projects/<project>/product/<feature>/stories/<story-slug>-diagram.excalidraw`
3. Render the PNG next to it
4. Embed in the story body under a `## Visual` section using `![[<story-slug>-diagram.excalidraw]]`
5. Add the diagram path to the story's `inputs.diagrams: [...]` frontmatter

### Step 6: Quality gate per story (refuse to finalize until all pass)

- [ ] Story statement uses canonical As-a / I-want / So-that
- [ ] At least 2 acceptance criteria, every one plain-English + verifiable
- [ ] INVEST passes (rewrite if not)
- [ ] Out of scope section present (can be "none" if genuinely none)
- [ ] Linked back to PRD requirement IDs in frontmatter

### Step 7: Write the files

One file per story. Path: `Projects/<project>/product/<feature>/stories/<Story Name>.md`. Create `stories/` if missing.

### Step 8: Hand-off summary

Print to the user:
- N stories written, list of titles
- Total requirement coverage for the slice (e.g. "R001, R002, R003 covered; R004 deferred to next slice")
- Suggested next: `/create-github-issue` to push a story to its tracker

## Composition

- **Feeds into:** `/create-github-issue` — one story file becomes one issue
- **Reads from:** sibling `<Feature Name> PRD.md` (+ `<Feature Name> Story Map.canvas` or `Roadmap.md` for the slices), plus `<Feature Name> Journey Map.md` if present (for persona)
- **Related:** `github/create-github-issue` for one-off stories outside a feature pipeline. **Do not duplicate logic.** If a one-off story is needed without a PRD/roadmap, the user should use `/create-github-issue` directly.
- **Context boundary:** the feature folder. One feature, many stories — all share frontmatter `project` and `feature`.

## Examples

See `references/EXAMPLE.md` for a worked example using the **command-center article-mgmt** `now` slice.

## Quality Checklist

- [ ] One file per story; filename `<Story Name>.md`
- [ ] Per-feature sequential numbering (continued from existing files)
- [ ] Every story passes INVEST
- [ ] AC format matches kaiju conventions (plain bullets, plain English)
- [ ] Frontmatter has `tracker_issue:` empty (sync skill fills it in)
- [ ] Coverage of the slice's requirements is complete or explicitly deferred
- [ ] Dev details folded; no How to test; no epic line in References

## Tips

- A story for "build the API" is not a story. It's an implementation note. The user-facing capability is the story.
- If you can't write a Given/When/Then for a criterion, the criterion isn't testable — rewrite.
- Don't pre-create stories for Next / Later slices. Stories age fast. Decompose a slice when you're about to work on it.
- If two stories must ship together to deliver value, that's a signal to merge them. Independence is the I in INVEST.

## Filenames

**A filename says what the note is, on its own.** `Workflow Builder PRD.md`, not `prd.md`;
`Workflow Builder Roadmap.md`, not `roadmap.md`. A reader scanning a folder — or a search
result, or a link — should know what a file is without reconstructing it from the path.

No numeric prefixes, no dashes standing in for spaces, no reserved type-names as filenames.
This is the vault-wide rule in the `obsidian` skill; these skills used to carve an exception
for themselves and it produced `prd.md` and `STORY-001-some-slug.md`, which is what the rule
exists to prevent.

The **feature folder** is title-case words too — `product/Workflow Builder/`. Composition
between these skills resolves by feature name, not by a fixed filename: a downstream skill
looks for the sibling ending in ` PRD.md`, ` Roadmap.md`, or ` Journey Map.md`.
