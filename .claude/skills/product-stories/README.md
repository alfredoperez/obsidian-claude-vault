---
skill: product-stories
theme: spec-code
group: Spec pipeline
maturity: stable
skill_sha: 9f475aa51e6d6cb2
generated: '2026-08-26'
---

<!-- GENERATED:START -->

Decompose a roadmap slice into user stories with Given/When/Then acceptance criteria and INVEST validation. Writes one file per story to Projects/<project>/product/<feature>/stories/<Story Name>.md. Markdown only — does NOT push to GitHub or Jira (that's `/create-github-issue` or `/create-jira-ticket`).

**Theme** spec-code / Spec pipeline · **Maturity** `stable` · **Invoke** `/product-stories`

### Triggers
- The user says '/product-stories'
- '/stories'
- Wants to break a slice into trackable work items
- Has an approved roadmap ready.


### Parameters

| Parameter | Kind | Required |
|---|---|---|
| `<feature-slug>` | argument | yes |
| `--slice` | flag | no |

### Flow

```mermaid
flowchart TD
    S0["Interview the user"]
    S1["Resolve feature folder + slice"]
    S2["Refuse if upstream is missing or thin"]
    S3["Pick persona"]
    S4["Load the canonical template"]
    S5["Decompose"]
    S6["Number + name"]
    S7["Offer diagram augmentation"]
    S8["Quality gate per story"]
    S9["Write the files"]
    S10["Hand-off summary"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> S8
    S8 --> S9
    S9 --> S10
```

### Connections

```mermaid
graph LR
    ME["product-stories"]
    ME ---|composes-with| Narticledraft["article-draft"]
    ME ---|composes-with| Narticleedit["article-edit"]
    ME ---|composes-with| Narticleexport["article-export"]
    ME ---|composes-with| Narticleillustrate["article-illustrate"]
    ME -->|delegates-to| Ncreatediagram["create-diagram"]
    ME -.->|reads| Ncreategithubissue["create-github-issue"]
    ME -.->|reads| Ncreatejiraticket["create-jira-ticket"]
    ME -.->|reads| Nobsidian["obsidian"]
    ME -.->|alternative-to| Nplan["plan"]
    ME ---|composes-with| Nproductroadmap["product-roadmap"]
```

**Calls out to**
- `article-draft` — composes-with
- `article-edit` — composes-with
- `article-export` — composes-with
- `article-illustrate` — composes-with
- `create-diagram` — delegates-to
- `create-github-issue` — reads
- `create-jira-ticket` — reads
- `obsidian` — reads
- `plan` — alternative-to
- `product-roadmap` — composes-with

**Called by**
- `create-jira-ticket`
- `obsidian`
- `product-roadmap`

### Vault paths touched
- `Projects/<project>/product/<feature>/stories`
- `~Attachments/Projects/<project>/product/<feature>/stories/<story-slug>-diagram.excalidraw`

### Files
- `references/EXAMPLE.md`
- `references/TEMPLATE.md`
- `references/canonical-template.md`

### Source

`skills/product/product-stories/SKILL.md` · 195 lines · `sha 9f475aa51e6d6cb2`

<!-- GENERATED:END -->

## Notes

<!-- Hand-written. Never overwritten by the generator. -->
