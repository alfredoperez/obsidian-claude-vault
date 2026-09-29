---
skill: writing
theme: output-style
group: House style
maturity: stable
skill_sha: 4ae6bee1a837d216
generated: '2026-08-26'
---

<!-- GENERATED:START -->

Alfredo's writing voice, structure, and house rules. Load this before drafting, editing, or polishing ANY prose a human will read: blog and Medium articles, LinkedIn or X posts, CFP abstracts, vault notes, READMEs, release notes, video scripts, summaries, and persuasive copy (landing pages, ads, launch copy, product descriptions, sales emails, promo scripts) via the Ogilvy persuasion profile. Use this skill whenever the user says '/writing', asks to write, draft, edit, rewrite, or polish something, asks whether something "sounds like me", wants copy that sells rather than copy that wins awards, or when another skill needs voice calibration. Make sure to use it even when the user does not explicitly mention voice or tone.

**Theme** output-style / House style · **Maturity** `stable` · **Invoke** `/writing`

### Flow

```mermaid
flowchart TD
    S0["Load the core voice"]
    S1["Load exactly one surface profile"]
    S2["Write, then run the checks"]
    S0 --> S1
    S1 --> S2
```

### Connections

```mermaid
graph LR
    ME["writing"]
    ME -.->|reads| Narticledraft["article-draft"]
    ME -.->|reads| Narticleedit["article-edit"]
    ME -.->|reads| Narticleplan["article-plan"]
    ME -.->|reads| Narticlesocial["article-social"]
    ME -.->|reads| Ncfpdraft["cfp-draft"]
    ME -.->|reads| Ncreateaudio["create-audio"]
    ME -.->|reads| Ncreatecarousel["create-carousel"]
    ME -.->|reads| Ncreatesocialmediapost["create-social-media-post"]
    ME -.->|reads| Nlog["log"]
    ME -.->|reads| Nobsidian["obsidian"]
    Ncreateeditorial["create-editorial"] --> ME
    Nreadinglevel["reading-level"] --> ME
```

**Calls out to**
- `article-draft` — reads
- `article-edit` — reads
- `article-plan` — reads
- `article-social` — reads
- `cfp-draft` — reads
- `create-audio` — reads
- `create-carousel` — reads
- `create-social-media-post` — reads
- `log` — reads
- `obsidian` — reads
- `plan` — reads

**Called by**
- `article-draft`
- `article-edit`
- `article-plan`
- `article-social`
- `cfp-draft`
- `create-audio`
- `create-carousel`
- `create-editorial`
- `create-social-media-post`
- `reading-level`
- `groom-rule`
- `obsidian`
- `presentation-storyboard`
- `quarterly-reflection`
- `report-style`

### Files
- `references/article.md`
- `references/cfp.md`
- `references/core-voice.md`
- `references/explainer.md`
- `references/general.md`
- `references/ogilvy-principles.md`
- `references/persuasion.md`
- `references/social.md`
- `references/structure.md`
- `references/vault-note.md`

### Source

`skills/content/writing/SKILL.md` · 80 lines · `sha 4ae6bee1a837d216`

<!-- GENERATED:END -->

## Notes

<!-- Hand-written. Never overwritten by the generator. -->
