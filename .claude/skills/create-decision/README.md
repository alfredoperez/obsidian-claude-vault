---
skill: create-decision
theme: output-style
group: How Claude responds
maturity: beta
skill_sha: 5f6d4c823a742a17
generated: '2026-08-29'
---

<!-- GENERATED:START -->

Escalate a decision out of chat and into a document the user can read, think about, and answer in their own time.

**Theme** output-style / How Claude responds · **Maturity** `beta` · **Invoke** `/create-decision`

### Triggers
- A choice is too big for an inline prompt: several questions interact
- The user needs findings or evidence in front of them before choosing
- The options need real explanation
- You are about to ask a question whose answer changes the direction of the work

### Parameters

| Parameter | Kind | Required |
|---|---|---|
| `<what is being decided>` | argument | yes |
| `--round-2` | flag | no |
| `--no-open` | flag | no |

### Flow

```mermaid
flowchart TD
    S0["Decide whether this is even a doc"]
    S1["Do the reading first"]
    S2["Write it"]
    S3["Open it in Obsidian"]
    S4["Read it back"]
    S5["Log and re-round"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
```

### Connections

```mermaid
graph LR
    ME["create-decision"]
    ME -.->|reads| Ngroom["groom"]
    ME ---|composes-with| Nlog["log"]
    ME ---|composes-with| Nobsidian["obsidian"]
    ME -->|delegates-to| Nplan["plan"]
    ME -.->|reads| Nreadinglevel["reading-level"]
    Ncreateeditorial["create-editorial"] --> ME
    Nreportstyle["report-style"] --> ME
```

**Calls out to**
- `groom` — reads
- `log` — composes-with
- `obsidian` — composes-with
- `plan` — delegates-to
- `reading-level` — reads

**Called by**
- `create-editorial`
- `obsidian`
- `plan`
- `reading-level`
- `report-style`

### Source

`skills/knowledge/create-decision/SKILL.md` · 416 lines · `sha 5f6d4c823a742a17`

<!-- GENERATED:END -->

## Notes

<!-- Hand-written. Never overwritten by the generator. -->
