---
skill: create-github-issue
theme: spec-code
group: Feed other systems
maturity: stable
skill_sha: e30445479de2ca13
generated: '2026-08-23'
---

<!-- GENERATED:START -->

Create a GitHub issue from a brief description, screenshot, or rough notes.

**Theme** spec-code / Feed other systems · **Maturity** `stable` · **Invoke** `/create-github-issue`

### Triggers
- The user says 'create an issue'
- 'open a github issue'
- '/create-github-issue'
- Hands off something that should become tracked work in a repo.


### Parameters

| Parameter | Kind | Required |
|---|---|---|
| `<repo? + description or screenshot>` | argument | yes |

### Flow

```mermaid
flowchart TD
    S0["Confirm target repo."]
    S1["Draft a title — concise, imperative, under 70 ..."]
    S2["Draft a body following this structure:"]
    S3["Pick a type and a priority label from the repo..."]
    S4["Show the user the draft  for approval before c..."]
    S5["After approval, run gh issue create --title '…..."]
    S6["Return the issue URL."]
    S0 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
```

### Connections

```mermaid
graph LR
    ME["create-github-issue"]
    ME -->|delegates-to| Nlog["log"]
    Ncreatejiraticket["create-jira-ticket"] --> ME
    Nproductstories["product-stories"] --> ME
```

**Calls out to**
- `log` — delegates-to

**Called by**
- `create-jira-ticket`
- `product-stories`

### External tools

`gh`, `git`

### Source

`skills/github/create-github-issue/SKILL.md` · 101 lines · `sha e30445479de2ca13`

<!-- GENERATED:END -->

## Notes

<!-- Hand-written. Never overwritten by the generator. -->
