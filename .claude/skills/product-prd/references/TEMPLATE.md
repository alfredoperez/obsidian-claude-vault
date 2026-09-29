---
type: prd
project: <project-slug>
feature: <feature-slug>
status: draft
created: YYYY-MM-DD
inputs:
  journey_map: <Feature Name> Journey Map.md, or empty
  mockups: <relative-path-or-empty>
  notes: <relative-path-or-empty>
---

# PRD — <Feature display name>

## Problem

<2–4 sentences. What's broken or missing today, who's affected, why now.
Link to the journey map's pain points / moments of truth for evidence.>

**Source:** `<Feature Name> Journey Map.md` (top pain: <pain X>; moment of truth: <MoT Y>) — or the brief, when there is no journey map

## Goals + success metrics

| Metric | Baseline | Target | Source / how measured |
|---|---|---|---|
| <Specific outcome — e.g. "Time from outline to draft-ready"> | <current> | <goal> | <signal: observation / instrumentation / survey> |
| | | | |

> Metrics inherit the confidence level of their source. If journey map is `hypothesis`, mark metrics derived from it as `Hypothesis — validate before commit`.

## Solution overview

<3–6 sentences. User-facing functionality and the key capabilities the feature enables.
Avoid implementation. The "what users can do", not "how the code works".>

## Functional requirements

| ID | Requirement | Notes |
|---|---|---|
| R001 | <User-perspective, testable. "User can …" or "System displays …"> | |
| R002 | | |
| R003 | | |
| … | | |

### Non-functional requirements

| ID | Requirement | Notes |
|---|---|---|
| NFR001 | <Performance / accessibility / availability / privacy / security claim> | |
| NFR002 | | |

> Every requirement is **testable** — a tester can write a pass/fail check from it.

## Scope

**In:**
- <Capability 1>
- <Capability 2>

**Out:**
- <Explicit exclusion — and why>
- <Explicit exclusion>

**Future (deferred):**
- <Capability that's likely next but not now>
- <Capability>

## Technical considerations

- <Constraint or integration: "Reads from Projects/<project>/...", "Depends on X being available", "Existing pattern Y should be reused">
- <Architectural note engineering needs to know, but not a design>
- <Anything that affects deployment, data, or compliance>

## Dependencies + risks

| # | Type | What | Owner | Mitigation |
|---|---|---|---|---|
| 1 | dep | <external system / team / library> | <name> | <plan> |
| 2 | risk | <what could go wrong> | <name> | <plan> |

## Milestones *(optional)*

<Coarse phasing. The real slicing lives in the story map's release slices (`/product-story-map`).>

- **M1:** <theme>
- **M2:** <theme>
- **M3:** <theme>

## Open questions

- [ ] **[blocking]** <Question — what decision is gated on this?>
- [ ] **[needs-research]** <Question — what evidence would close it?>
- [ ] **[clarify-with-stakeholder]** <Question — who needs to answer?>
