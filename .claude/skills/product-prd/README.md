---
skill: product-prd
theme: spec-code
group: Spec pipeline
maturity: stable
skill_sha: 89fba4ed94352db0
generated: '2026-08-26'
---

<!-- GENERATED:START -->

Write a Product Requirements Document (PRD) for a feature as a markdown artifact at Projects/<project>/product/<feature>/<Feature Name> PRD.md. Pulls upstream context (journey-map, mockups, notes) from the same feature folder automatically.

**Theme** spec-code / Spec pipeline · **Maturity** `stable` · **Invoke** `/product-prd`

### Triggers
- The user says '/product-prd'
- '/prd'
- Wants to spec a feature/epic/initiative for engineering handoff
- Has a journey map ready and needs the requirements document.


### Parameters

| Parameter | Kind | Required |
|---|---|---|
| `<feature-slug>` | argument | yes |

### Flow

```mermaid
flowchart TD
    S0["Interview the user"]
    S1["Resolve feature folder"]
    S2["Validate inputs"]
    S3["Compose the PRD"]
    S4["Offer diagram augmentation"]
    S5["Quality gate"]
    S6["Write the file"]
    S7["Hand-off summary"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
```

### Connections

```mermaid
graph LR
    ME["product-prd"]
    ME -.->|reads| Narticleillustrate["article-illustrate"]
    ME -->|delegates-to| Ncreatediagram["create-diagram"]
    ME ---|composes-with| Ncreateimage["create-image"]
    ME -->|delegates-to| Nlog["log"]
    ME -.->|reads| Nobsidian["obsidian"]
    ME ---|composes-with| Nplan["plan"]
    ME -->|delegates-to| Nproductjourneymap["product-journey-map"]
    ME -->|delegates-to| Nproductroadmap["product-roadmap"]
```

**Calls out to**
- `article-illustrate` — reads
- `create-diagram` — delegates-to
- `create-image` — composes-with
- `log` — delegates-to
- `obsidian` — reads
- `plan` — composes-with
- `product-journey-map` — delegates-to
- `product-roadmap` — delegates-to

**Called by**
- `obsidian`
- `product-journey-map`
- `product-roadmap`

### Vault paths touched
- `Projects/<project>/<feature>-mockups.md`
- `Projects/<project>/product/<feature>`
- `~Attachments/Projects/<project>/product/<feature>/<diagram-slug>.excalidraw`

### Files
- `references/EXAMPLE.md`
- `references/TEMPLATE.md`

### Source

`skills/product/product-prd/SKILL.md` · 184 lines · `sha 89fba4ed94352db0`

<!-- GENERATED:END -->

## Notes

<!-- Hand-written. Never overwritten by the generator. -->
