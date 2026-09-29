---
skill: checkup
theme: kaiju
group: Keep it honest
maturity: stable
skill_sha: f00d5fb309c477fe
generated: '2026-08-23'
---

<!-- GENERATED:START -->

One command that runs every read-only health check across the skills and the vault and reports what needs attention. Rules on published output, the graders themselves, skills that never fire, vault-versus-blog drift, upstream drift, repeated friction, and how long since the vault was groomed.

**Theme** kaiju / Keep it honest · **Maturity** `stable` · **Invoke** `/checkup`

### Triggers
- The user says '/checkup'
- 'is everything ok'
- 'check my setup'
- 'what needs attention'
- 'health check'
- 'anything broken'
- Comes back after time away and wants to know what rotted

### Parameters

| Parameter | Kind | Required |
|---|---|---|
| `--quick` | flag | no |

### Flow

```mermaid
flowchart TD
    S0["Run it"]
    S1["What it checks"]
    S2["It changes nothing, on purpose"]
    S3["Reading the output"]
    S4["After it"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
```

### Connections

```mermaid
graph LR
    ME["checkup"]
    ME ---|composes-with| Ngroom["groom"]
    ME ---|composes-with| Ngroomrule["groom-rule"]
    ME ---|composes-with| Nlog["log"]
```

**Calls out to**
- `groom` — composes-with
- `groom-rule` — composes-with
- `log` — composes-with

### Source

`skills/projects/checkup/SKILL.md` · 91 lines · `sha f00d5fb309c477fe`

<!-- GENERATED:END -->

## Notes

<!-- Hand-written. Never overwritten by the generator. -->
