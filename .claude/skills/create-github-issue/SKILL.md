---
name: create-github-issue
description: >
  Create a GitHub issue from a brief description, screenshot, or rough notes.
  Use when the user says 'create an issue', 'open a github issue', '/create-github-issue',
  or hands off something that should become tracked work in a repo.
argument-hint: "<repo? + description or screenshot>"
# effort: fills a template from a description
effort: low
---

# Create Issue

Stub. Wraps `gh issue create` with light structure.

## When to Use

- User says `/create-github-issue` or "open an issue for X"
- User shares a bug report, feature request, or screenshot that should become a tracked issue
- User wants to convert a piece of conversation into actionable work

## Inputs

- **Required**: a description (text) or a screenshot
- **Required**: a **type** label and a **priority** label — every issue created by this skill gets both (see [Labels](#labels-mandatory))
- **Optional**: target repo (default: current working directory's git remote)
- **Optional**: milestone, assignee, extra labels

## Workflow

1. Confirm target repo. If not given, use `gh repo view --json nameWithOwner` from the cwd. Then read the repo's label vocabulary with `gh label list --limit 100` — never guess label names; pass only labels that exist (`gh issue create` errors on an unknown label).
2. Draft a title — concise, imperative, under 70 chars.
3. Draft a body following this structure:
   - **Context**: what triggered this (1–2 sentences)
   - **Expected** vs **Actual** for bugs; **Goal** for features
   - **Reproduction steps** if applicable
   - **Acceptance criteria** — see AC rules below
   - **Technical details** (bugs only): wrap in a collapsible `<details><summary>Technical details</summary>...</details>` block at the bottom. This is where file paths, line numbers, root-cause analysis, code identifiers, and suggested fixes live — keeps the top of the issue PM-readable.
4. **Pick a type and a priority label** from the repo's actual vocabulary — see [Labels](#labels-mandatory). Surface both in the draft so the user can correct them.
5. Show the user the draft (title + body + **the chosen type & priority labels**) for approval before creating.

### AC rules (mandatory)

- **Plain bullets only** (`- ...`). No `[ ]` task-list checkboxes.
- **Plain English.** No code identifiers, no file paths, no class/method/property names, no technical jargon. Describe what the user observes, not what the code does. Code references belong in the Technical Details section.
- Each bullet is a verifiable outcome stated from the user's perspective.
- 3+ criteria preferred; include a "no regression for existing X" bullet when the change touches a shared surface.

### Labels (mandatory)

**Every issue gets a type label AND a priority label.** Resolve both against the repo's real vocabulary (`gh label list`) — schemes differ per repo.

- **Type** — infer from the issue (bug report → `bug`; new capability → `enhancement`/`feature`; docs-only → `documentation`). Match the repo's actual name (e.g. `enhancement` vs `feature`).
- **Priority** — priority is a judgment call: infer a sensible default and **state it in the draft for the user to confirm or override** (don't silently pick). Match the repo's scheme — e.g. `tier:P0`/`tier:P1`/`tier:P2`/`tier:P3`, or `priority:high`/`med`/`low`, or `P0`/`P1`. Rough guide: P0 = broken-for-all / data loss, P1 = broken common path or no workaround, P2 = important but has a workaround, P3 = nice-to-have / polish.
- **If the repo has no type or priority label set**, say so and ask whether to create the labels (`gh label create`) or proceed without — don't pass a non-existent label (the create call fails).

6. After approval, run `gh issue create --title "…" --body "…" --label "<type>" --label "<priority>"` (use a heredoc for the body; add any extra labels/milestone/assignee the user gave).
7. Return the issue URL.

## Examples

**Input:** "create an issue: add-retro skill keeps duplicating entries when run twice in a row"

**Output draft:**
```
Title: add-retro deduplicates entries when invoked twice

Body:
**Context**: Running /log back-to-back creates a duplicate row in Retros.md.

**Expected**: Second invocation appends or merges with the first.
**Actual**: Two identical rows.

**Reproduction**:
1. /log "test note"
2. /log "test note"
3. Open Retros.md — two entries

**Acceptance criteria**:
- Running the command twice in quick succession does not produce duplicate entries.
- The user is notified or the entry is merged when a duplicate is detected.
- Any duplicates already in the file can be cleaned up in one action.

Labels: bug · tier:P2  (priority inferred — has a workaround; confirm?)
```

## Quality Checklist

- [ ] Title is concise and actionable
- [ ] Body has context + acceptance criteria
- [ ] **A type label AND a priority label are applied** — both resolved against the repo's real `gh label list`
- [ ] Priority was surfaced in the draft for the user to confirm (not silently chosen)
- [ ] Repo target is correct (not accidentally pointing at the wrong repo)
- [ ] User approved the draft before issue was created
- [ ] Issue URL returned to user

## Tips

- For screenshots: use `gh issue create --body-file -` and pipe the body in.
- If the user describes something fuzzy, ask one clarifying question rather than creating a vague issue.
- If the repo is not under `gh auth status`'s known orgs, escalate.
