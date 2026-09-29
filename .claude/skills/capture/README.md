---
skill: capture
theme: knowledge
group: Bring it in
maturity: stable
skill_sha: e25db7b9994d472c
generated: '2026-08-23'
---

<!-- GENERATED:START -->

Smart capture for ideas, tasks, URLs, YouTube videos, and quotes. Auto-detects input type and routes to the right location in the vault.

**Theme** knowledge / Bring it in · **Maturity** `stable` · **Invoke** `/capture`

### Triggers
- The user says '/capture'
- Wants to save something quickly
- Shares a YouTube URL
- Mentions adding a task
- Link
- Note

### Flow

```mermaid
flowchart TD
    S0["Fetch metadata with WebFetch:"]
    S1["Derive filename from the title — readable casi..."]
    S2["Detect category :"]
    S3["Infer 3-5 tags from content (e.g."]
    S4["Create the note using this template — leave wh..."]
    S5["Confirm path to user:"]
    S6["Check if Sources/links/Phrases.md exists"]
    S7["If topic-specific quote, search for relevant n..."]
    S8["Append to appropriate file with attribution"]
    S9["Analyze title for category and tags"]
    S10["Search Knowledge/ for related notes"]
    S11["Ask for content or if user wants to paste/dict..."]
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
    S10 --> S11
```

### Connections

```mermaid
graph LR
    ME["capture"]
    ME -->|delegates-to| Ncapturebookmarks["capture-bookmarks"]
    ME -->|delegates-to| Ncaptureyoutube["capture-youtube"]
    ME -.->|reads| Nobsidian["obsidian"]
    Ncapturearticle["capture-article"] --> ME
    Ncreatevideo["create-video"] --> ME
    Ngroomrule["groom-rule"] --> ME
    Nproductjourneymap["product-journey-map"] --> ME
```

**Calls out to**
- `capture-bookmarks` — delegates-to
- `capture-youtube` — delegates-to
- `obsidian` — reads

**Called by**
- `capture-article`
- `capture-bookmarks`
- `capture-youtube`
- `create-video`
- `groom-rule`
- `obsidian`
- `product-journey-map`

### External tools

`yt-dlp`

### Vault paths touched
- `Knowledge/<category>/<title>.md`
- `Knowledge/Angular`
- `Knowledge/Sources`
- `Personal/Health`
- `Sources/links/<Name>.md`
- `Sources/links/<Title>.md`
- `Sources/links/Impeccable.md`
- `Sources/links/Links.base`
- `Sources/links/Phrases.md`
- `Sources/videos`

### Source

`skills/knowledge/capture/SKILL.md` · 198 lines · `sha e25db7b9994d472c`

<!-- GENERATED:END -->

## Notes

<!-- Hand-written. Never overwritten by the generator. -->
