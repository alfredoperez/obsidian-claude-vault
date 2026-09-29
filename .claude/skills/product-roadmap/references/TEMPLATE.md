---
type: roadmap
project: <project-slug>
feature: <feature-slug>
status: planning
created: YYYY-MM-DD
inputs:
  prd: ./prd.md
slices: [now, next, later]
---

# Roadmap — <Feature display name>

## Summary

<3–4 sentences. What's shipping, in what order, and the bet behind the slicing.>

## Slice: Now

**Outcome:** <One sentence the user can feel. "Users can …">

**Requirements covered:** R001, R002, R003

**Depends on:** —

**Deferred from this slice:** <if any — requirements that are scope-adjacent but not in Now>

**Definition of done:**
- <Observable signal 1>
- <Observable signal 2>

---

## Slice: Next

**Outcome:** <One sentence.>

**Requirements covered:** R004, R005, R006

**Depends on:** Now landed

**Deferred from this slice:**

**Definition of done:**
-

---

## Slice: Later

**Outcome:** <One sentence — or "deferred until X validates">

**Requirements covered:** R007, R008, R009, R010

**Depends on:** Next landed

**Deferred from this slice:**

**Definition of done:**
-

---

## Coverage check

| Requirement | Title (short) | Slice | Notes |
|---|---|---|---|
| R001 | <short title> | Now | |
| R002 | <short title> | Now | |
| R003 | <short title> | Now | |
| R004 | <short title> | Next | |
| R005 | <short title> | Next | |
| R006 | <short title> | Next | |
| R007 | <short title> | Later | |
| R008 | <short title> | Later | |
| R009 | <short title> | Later | |
| R010 | <short title> | Later | |

> Every PRD requirement appears in this table. Any requirement labeled "deferred" must also appear with `Slice: Future`.

## Mermaid Gantt *(optional)*

```mermaid
gantt
    title <Feature> delivery
    dateFormat YYYY-MM-DD
    section Now
    <theme> :now1, 2026-MM-DD, Xd
    section Next
    <theme> :next1, after now1, Xd
    section Later
    <theme> :later1, after next1, Xd
```

## Open decisions

- <Provisional slicing choice that could flip — and what would flip it>
- <Dependency on infra/other team work that's not in the PRD>
