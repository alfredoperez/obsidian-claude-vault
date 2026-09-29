---
name: product-roadmap
description: >
  Slice a PRD into a phased roadmap (now / next / later, or M1 / M2 / M3) and write
  it to Projects/<project>/product/<feature>/<Feature Name> Roadmap.md. Each slice references PRD
  requirement IDs (R001…) so drift between roadmap and PRD is detectable later. Use
  when the user says '/product-roadmap', '/roadmap', has a PRD ready and wants to
  phase the work, or wants to communicate delivery sequence to stakeholders.
argument-hint: "<feature-slug> [project]"
metadata:
  phase: deliver
  category: product
  inspired_by: product-on-purpose/pm-skills + deanpeters/Product-Manager-Skills (roadmap-planning)
---

# Product — Roadmap

Slice a PRD into a phased delivery plan. The output is a lean, scannable artifact — not a Gantt chart. Each slice carries a user-visible outcome and a list of the PRD requirement IDs it covers, so anyone can trace a slice back to the spec.

## When to Use

- User says `/product-roadmap` or `/roadmap`
- User has a PRD ready (`Projects/<project>/product/<feature>/<Feature Name> PRD.md` exists) and wants to phase it
- User needs to communicate delivery sequence to stakeholders
- A PRD has 10+ requirements and needs prioritization

## Inputs

**Required:**
- **Feature slug** — resolves to `Projects/<project>/product/<feature>/`. Inferred if invoked inside the folder.
- A PRD file (sibling `<Feature Name> PRD.md` in the feature folder)

**Optional:**
- Time horizon — e.g. "M1 = this week", "M2 = this month", "M3 = this quarter". Defaults to relative buckets `now / next / later`.
- Slice theme override — if the user wants to group differently from the PRD's `## Milestones` section

## Workflow

### Step 0: Interview the user (default mode)

When invoked, the skill **defaults to interview mode** — gather slicing strategy, time horizon, dependencies, and prioritization signals from the user via `AskUserQuestion` in 1–3 structured rounds. Compose the roadmap from their answers.

**Do not auto-compose from conversation context, even if a complete brief is provided in the invocation.** Treat any in-conversation brief (or the sibling `<Feature Name> PRD.md`) as **default-option suggestions** in AskUserQuestion options (with "Other" as free-text override), never as the final answer.

**Suggested rounds for a roadmap:**

- **Round 1 (slicing strategy):** now/next/later vs M1/M2/M3 / how many slices / what defines "Now" (one-week ship? one-month? user-visible delivery?)
- **Round 2 (priorities + dependencies):** Which requirements are P0 vs P1 vs deferred / known cross-slice dependencies / blocking infra work
- **Round 3 (only if needed):** clarify slice-by-slice rationale before composing.

**Skip interview only when** the user explicitly says "use the brief I gave you" / "skip the interview". Then validate against refusal protocols (Step 2) and proceed.

### Step 1: Resolve feature folder

Same inference rules as other product/ skills.

### Step 2: Refuse if PRD is missing or thin

1. **No `<Feature Name> PRD.md` in feature folder** → refuse: "Need a PRD first. Run `/product-prd <feature>` or point me at one."
2. **PRD has zero requirements (`R001+`)** → refuse: "PRD has no requirements. Add requirements before I can slice them."
3. **PRD `status: draft` AND open questions tagged `[blocking]`** → warn (don't refuse): "PRD has blocking open questions. The roadmap will reflect current scope, but expect rework after blockers resolve."

### Step 3: Slice the PRD

Default slicing strategy:
- **Now** — smallest deliverable that produces user-visible value. Usually one milestone or one tight set of requirements.
- **Next** — the obvious follow-up; depends on Now landing.
- **Later** — known-but-deferred capabilities.

If the PRD already has a `## Milestones` section (M1, M2, M3...), use that mapping by default. Re-slice only if the user asks or if the milestones don't deliver standalone value.

Each slice must:
- Have a 1-line **user-visible outcome** ("Users can chat with Claude about the active article")
- List the **PRD requirement IDs** it covers (`R001, R002, R003`)
- Note **dependencies** on prior slices (none for Now)
- Note **deferred items** explicitly (what's NOT in this slice from the PRD's In-scope list)

### Step 4: Compose the roadmap

Follow `references/TEMPLATE.md`. Section order:

1. **Frontmatter** — `type: roadmap`, `project`, `feature`, `status: planning|active|done`, `created`, `inputs: { prd: ./<Feature Name> PRD.md }`, `slices: [now, next, later]`
2. **Summary** — 3–4 sentences: what's shipping, in what order, the bet behind the slicing
3. **Slice: Now** — outcome, requirements covered, dependencies, what's deferred
4. **Slice: Next** — same
5. **Slice: Later** — same
6. **Coverage check** — table showing every PRD requirement and the slice it lives in. Surfaces gaps (requirements with no slice) and double-counts.
7. **Mermaid Gantt** *(optional)* — only if the user explicitly asked for visual phasing
8. **Open decisions** — what about the slicing is provisional and what would change it

### Step 4.5: Offer diagram augmentation (optional, never forced)

After composing the roadmap body but before writing the file, scan for patterns where a visual would argue something the text and tables can't:

**Detection heuristics for a roadmap:**
- **Phased delivery with cross-slice dependencies** (e.g. Next depends on Now; Later depends on Next + an external thing) → dependency graph
- **Convergence of slices toward a single shipped state** (multiple parallel tracks merging) → convergence diagram
- **Time-bounded milestones across weeks/months** with clear date anchors → Gantt
- **Risk-weighted slices** (one slice is the high-bet spike, others depend on it landing) → risk-flagged stage flow

**If one or more patterns appear, ask the user via `AskUserQuestion`:**
- Question: "Would a diagram help here?"
- Options: `{ "Skip", "<type-1> (1-line argument)", "<type-2> (...)", ... }`

**Never auto-generate.** Only invoke `/create-diagram` if the user picks a generate option.

**If user picks generate:**
1. Invoke `/create-diagram` with a focused prompt — the *argument* the diagram should make
2. Save to `~Attachments/Projects/<project>/product/<feature>/<diagram-slug>.excalidraw`
3. Render the PNG next to it
4. Embed in the roadmap body under a `## Visual: <name>` section using `![[<diagram-slug>.excalidraw]]`
5. Add the diagram path to the artifact's `inputs.diagrams: [...]` frontmatter

### Step 5: Quality gate (refuse to finalize until all pass)

- [ ] Every slice has a user-visible outcome (not just a technical theme)
- [ ] Every requirement in PRD `Scope: In` is assigned to exactly one slice (or explicitly marked "deferred to Future")
- [ ] Slices respect dependencies (Now doesn't depend on Next)
- [ ] No slice is purely scaffolding / refactoring — every slice delivers user value
- [ ] Coverage check shows no orphaned requirements

### Step 6: Write the file

Write to `Projects/<project>/product/<feature>/<Feature Name> Roadmap.md`. If the file exists, ask before overwriting.

### Step 7: Hand-off summary

Print to the user:
- Path to the artifact
- Slice count + requirements per slice
- Suggested next: `/product-stories <feature>` to decompose a slice into user stories. Optionally `--slice now` to start with the first slice.

## Composition

- **Feeds into:** `product-stories <feature>` — reads `<Feature Name> Roadmap.md` from the same feature folder; user picks which slice to decompose
- **Reads from:** sibling `<Feature Name> PRD.md`
- **Context boundary:** the feature folder. One feature, one roadmap.

## Examples

See `references/EXAMPLE.md` for a worked example using the **command-center article-mgmt** use case.

## Quality Checklist

- [ ] Frontmatter complete (project, feature, status, created, inputs, slices)
- [ ] All slices have user-visible outcomes + requirement-ID coverage + deferred notes
- [ ] Coverage check table covers every PRD requirement
- [ ] No orphan requirements
- [ ] File written to `Projects/<project>/product/<feature>/<Feature Name> Roadmap.md`

## Tips

- "Build the backend" is not a slice. "Users can save and reload their chat history" is.
- If a slice depends on a thing that's not in the PRD (e.g. infra work), surface it in `Open decisions` rather than hiding it.
- Don't over-slice. Three slices is usually right. Five is the upper bound before the roadmap becomes a backlog with extra steps.
- If the PRD's `## Milestones` already match the user-value test, just use them — don't re-slice for the sake of re-slicing.

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
