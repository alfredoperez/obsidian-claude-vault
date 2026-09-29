---
name: product-prd
description: >
  Write a Product Requirements Document (PRD) for a feature as a markdown artifact at
  Projects/<project>/product/<feature>/<Feature Name> PRD.md. Pulls upstream context (journey-map,
  mockups, notes) from the same feature folder automatically. Use when the user says
  '/product-prd', '/prd', wants to spec a feature/epic/initiative for engineering
  handoff, or has a journey map ready and needs the requirements document.
argument-hint: "<feature-slug> [project]"
metadata:
  phase: deliver
  category: product
  inspired_by: product-on-purpose/pm-skills (deliver-prd, Apache 2.0)
---

# Product — PRD

Produce a Product Requirements Document that bridges problem understanding and engineering implementation. Section structure adapted from product-on-purpose's `deliver-prd`. Requirement numbering uses `R001, R002, …` to match the SDD spec habit.

## When to Use

- User says `/product-prd` or `/prd`
- User has a journey map and wants the next phase
- User wants to spec a feature, epic, or initiative for engineering handoff
- Stakeholders need to approve scope before investment

## Inputs

**Required:**
- **Feature slug** (kebab-case). Resolves to `Projects/<project>/product/<feature>/`. Inferred if invoked from inside that folder.
- Project — inferred from cwd. Ask if ambiguous.

**Auto-composed (read from the feature folder, no args needed):**
- `<Feature Name> Journey Map.md` (if it exists) — pulls persona, pain points, opportunities
- Any sibling files referenced in upstream frontmatter `inputs:` (e.g. mockups, captured research)

**Optional explicit inputs:**
- Path to mockups (e.g. `Projects/<project>/<feature>-mockups.md`) if it lives outside the feature folder
- Brief / problem statement when no journey map exists
- Existing PRD to revise or extend

## Workflow

### Step 0: Interview the user (default mode)

When invoked, the skill **defaults to interview mode** — gather problem statement, goals, success metrics, scope decisions, and known constraints from the user via `AskUserQuestion` in 2–4 structured rounds. Compose the PRD from their answers.

**Do not auto-compose from conversation context, even if a complete brief is provided in the invocation.** The conversation may be wrong or partial; the user is the source of truth. Treat any in-conversation brief (or the sibling `<Feature Name> Journey Map.md`) as **default-option suggestions** inside the AskUserQuestion options (with "Other" as free-text override), never as the final answer.

**Suggested rounds for a PRD:**

- **Round 1 (problem + value):** Restate the problem the journey map surfaced / why-now / who-it's-for. Confirm or amend.
- **Round 2 (goals + metrics):** Top 2–3 success metrics with baselines and targets.
- **Round 3 (scope):** What's In / Out / Future. Force explicit Out — surface what's tempting but cut.
- **Round 4 (only if needed):** Technical constraints, dependencies, blocking open questions.

**Skip interview only when** the user explicitly says "use the brief I gave you" / "skip the interview" / "no interview". Then validate the brief against the refusal protocols (Step 2) and proceed.

### Step 1: Resolve feature folder

Feature folder inference:
1. Inside `Projects/<project>/product/<feature>/` → both inferred
2. Inside `Projects/<project>/` + feature arg → project inferred
3. `<project>/<feature>` explicit → use as given
4. Else → ask "Which project?"

Ensure the feature folder exists; create if missing.

### Step 2: Validate inputs (refuse if insufficient)

1. **No problem statement AND no journey map** → refuse: "I need either a journey map (persona, pain points, opportunities — write one as `<Feature Name> Journey Map.md` in the feature folder) or a problem statement. Which do you want?"
2. **No persona** → refuse: "Who is this for? Provide a persona — name + 1-line summary."
3. **Brief is two sentences with no metrics, no scope, no users** → refuse: "This is too thin. Either write a journey map first, or expand the brief to cover: problem, who, success looks like, what's in/out."

### Step 3: Compose the PRD

Follow `references/TEMPLATE.md`. Section order (all required unless marked):

1. **Frontmatter** — `type: prd`, `project`, `feature`, `status: draft|review|approved`, `created`, `inputs: { journey_map, mockups, notes }`
2. **Problem** — recap of what's being solved. Link to journey map. Ensure readers understand *why* before *what*.
3. **Goals + success metrics** — specific, measurable. Each metric has a baseline + target. Connects directly to the problem.
4. **Solution overview** — high-level. User-facing functionality and key capabilities. Enough detail for stakeholders to evaluate; not enough to design the system.
5. **Functional requirements** — numbered `R001, R002, …`. Each requirement is **testable** (someone can verify pass/fail). Use plain English with a user-perspective verb. NFRs as `NFR001, NFR002, …`.
6. **Scope** — explicit `In / Out / Future`. The Out + Future sections are critical — they prevent scope creep.
7. **Technical considerations** — constraints, integration requirements, architectural notes engineering needs to know. Don't design the system; surface considerations.
8. **Dependencies + risks** — external dependencies, assumptions, risks. Include owners and mitigation where applicable.
9. **Milestones** *(optional)* — phase outline, not specific dates. (Real phasing lives in the roadmap.)
10. **Open questions** — explicit list. Each question has a tag: `[blocking]`, `[needs-research]`, `[clarify-with-stakeholder]`.

### Step 3.5: Offer diagram augmentation (optional, never forced)

After composing the PRD body but before writing the file, scan for patterns where a visual would argue something text can't:

**Detection heuristics for a PRD:**
- **Layered/hierarchical model** that requirements depend on (e.g. a 4-layer context model, a tier system) → layered diagram (concentric or stacked)
- **Multiple system components needing integration** (e.g. frontend + backend + external API + storage) → component-relationship diagram
- **Side-by-side current vs target user-visible behavior** → contrast diagram (often a re-use of the journey-map's visual)
- **Decision tree** in scope choices (e.g. "if X, do A; else B") → diamond + branch diagram

**If one or more patterns appear, ask the user via `AskUserQuestion`:**
- Question: "Would a diagram help here?"
- Options: `{ "Skip", "<type-1> (1-line argument)", "<type-2> (...)", ... }`

**Never auto-generate.** Only draw one if the user picks a generate option.

**If user picks generate:**
1. Draw it as an Excalidraw file (the `create-diagram` skill if installed; otherwise write the `.excalidraw` JSON by hand) from a focused prompt — the *argument* the diagram should make (not just what to display), the layout, the style preference (default: `neo-brutalist`)
2. Save to `~Attachments/Projects/<project>/product/<feature>/<diagram-slug>.excalidraw`
3. Render the PNG next to it
4. Embed in the PRD body under a `## Visual: <name>` section using `![[<diagram-slug>.excalidraw]]`
5. Add the diagram path to the artifact's `inputs.diagrams: [...]` frontmatter (new field)

### Step 4: Quality gate (refuse to finalize until all pass)

- [ ] Problem + "why now" clearly stated
- [ ] Success metrics specific and measurable (baseline + target)
- [ ] Scope explicit (In + Out + Future)
- [ ] Every requirement testable and numbered (`R001`, `R002`, …)
- [ ] Technical considerations surface constraints without over-specifying
- [ ] Dependencies + risks documented
- [ ] Readable in under 15 min

### Step 5: Write the file

Write to `Projects/<project>/product/<feature>/<Feature Name> PRD.md`. If the file exists, ask before overwriting (offer "extend existing" vs "replace").

### Step 6: Hand-off summary

Print to the user:
- Path to the artifact
- Requirement count + scope split (In / Out / Future)
- Top 2 open questions
- Suggested next: `/product-story-map <feature>` to lay the requirements out as a wall with release slices, then `/product-stories <feature>`

## Composition

- **Feeds into:** `product-story-map <feature>` and `product-stories <feature>` — both read `<Feature Name> PRD.md` from the same feature folder
- **Reads from:** sibling `<Feature Name> Journey Map.md` (if present), upstream mockups / notes declared in `inputs:`
- **Context boundary:** the feature folder. One feature, one PRD.

## Examples

See `references/EXAMPLE.md` for a worked example using the **command-center article-mgmt** use case.


## Vault conventions

Load the **`obsidian`** skill before writing the note. It owns the structure — frontmatter,
`lifespan:`, components, diagrams, and where a note goes — so this skill does not carry its
own copy of the conventions.

A PRD is a design of record: `lifespan: project`. Read `obsidian/references/design-doc.md`.

## Quality Checklist

- [ ] Frontmatter complete (project, feature, status, created, inputs)
- [ ] All 10 sections present (open questions can be empty but must exist)
- [ ] Requirements numbered `R001+`; testable + plain English
- [ ] Scope split clean (no "TBD" in Out / Future)
- [ ] Refusal protocols applied where applicable
- [ ] File written to `Projects/<project>/product/<feature>/<Feature Name> PRD.md`

## Tips

- "Improve the dashboard" is not a requirement. "R005: Editor displays the article's current status as a chip in the breadcrumb row" is.
- Out-of-scope is just as important as In-scope. If you don't know what's out, you don't know what's in.
- Pull metrics from the journey map's Opportunities section when possible — keeps the chain coherent.
- If the journey map has `confidence: hypothesis`, every PRD metric tied to it inherits the same caveat. Note this in the metrics section.

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
