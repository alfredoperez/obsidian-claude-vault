---
type: story
project: <project-slug>
feature: <feature-slug>
story_id: STORY-NNN
slice: now | next | later
priority: P0 | P1 | P2 | P3
status: draft
tracker_issue:
covers_requirements: [R001, R002]
created: YYYY-MM-DD
inputs:
  story_map: ../<Feature Name> Story Map.canvas
  prd: ../<Feature Name> PRD.md
---

# STORY-NNN — <Short capability title>

## Story

As a <persona>
I want <action>
So that <benefit>

## Acceptance Criteria

- Given <starting condition>, when <action>, then <observable outcome>.
- Given <starting condition>, when <action>, then <observable outcome>.
- Given <starting condition>, when <action>, then <observable outcome>.

> Plain bullets only. Plain English. No code identifiers, file paths, or technical jargon in this section.

## Dev details

> One block, rendered in Jira as a single expand titled "Dev details". Everything under this heading up to Out of Scope is folded. No "How to test" — test steps go in the tracker's test-plan field.

### Suggested implementation *(omit bullets that don't apply)*

- **Approach:** <pattern to follow, existing utility to reuse>
- **Key files:** <file / module / API engineering should know about>
- **Proven code:** <spike branch — commit SHAs and what each proves>
- **Gating wiring:** <flag / permission wiring and fallback>
- **Dependencies:** <ticket key — why>
- **Suggested split:** <if near the sizing limit, how it would split>
- **Risks / edge cases:** <known pitfalls>

### Notes

- <Decisions or context that don't fit elsewhere>

## Out of Scope

- <Adjacent capability that's NOT in this story>
- <Explicit exclusion>

## References *(omit if empty — never the epic; the parent link carries it)*

- <Design / spike / related ticket>
