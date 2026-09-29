---
skill: capture-youtube
theme: knowledge
group: Bring it in
maturity: stable
skill_sha: c6805941799433c6
generated: '2026-08-29'
---

<!-- GENERATED:START -->

Extract knowledge from a YouTube video into topic-based notes, harvest the links it names into link cards, archive the transcript, and optionally answer a specific question or produce an audio summary.

**Theme** knowledge / Bring it in · **Maturity** `stable` · **Invoke** `/capture-youtube`

### Triggers
- The user shares a YouTube URL and wants detailed notes
- Mentions extracting knowledge from a video
- Wants the links or resources a video mentions
- Wants a video to answer a question
- Says 'process youtube'

### Parameters

| Parameter | Kind | Required |
|---|---|---|
| `<youtube-url...>` | argument | yes |
| `--goal` | flag (takes a value) | no |
| `--audio` | flag | no |
| `--links-only` | flag | no |
| `--slides` | flag | no |
| `--report-only` | flag | no |

### Flow

```mermaid
flowchart TD
    S0["Validate Input"]
    S1["Verify dependency"]
    S2["Fetch metadata and transcript with yt-dlp"]
    S3["Harvest the links"]
    S4["Capture slides"]
    S5["Determine Destination"]
    S6["Create the Video Note"]
    S7["Find Related Notes"]
    S8["Fold into the concept layer"]
    S9["Answer the goal"]
    S10["Preserve, record, clean up"]
    S11["Audio summary"]
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
    ME["capture-youtube"]
    ME -.->|reads| Ncapture["capture"]
    ME -->|delegates-to| Ncreateaudio["create-audio"]
    ME -->|delegates-to| Ncreatenotebooklm["create-notebooklm"]
    ME ---|composes-with| Ngroom["groom"]
    ME -.->|reads| Nobsidian["obsidian"]
    ME ---|composes-with| Nplan["plan"]
    Ncapturearticle["capture-article"] --> ME
    Ncapturebookmarks["capture-bookmarks"] --> ME
    Ncreateeditorial["create-editorial"] --> ME
    Ngroomrule["groom-rule"] --> ME
    Nproductjourneymap["product-journey-map"] --> ME
```

**Calls out to**
- `capture` — reads
- `create-audio` — delegates-to
- `create-notebooklm` — delegates-to
- `groom` — composes-with
- `obsidian` — reads
- `plan` — composes-with

**Called by**
- `capture`
- `capture-article`
- `capture-bookmarks`
- `create-editorial`
- `groom-rule`
- `product-journey-map`

### External tools

`curl`, `ffmpeg`, `jq`, `notebooklm`, `uv`, `whisper-cli`, `yt-dlp`

### Vault paths touched
- `Knowledge/AI/<page>.md`
- `Personal/Health`
- `Sources/links/<Title>.md`
- `Sources/links/Links.base`
- `Sources/videos/<title>.md`
- `Sources/videos/answers/<...>.md`
- `Sources/videos/answers/<goal-slug>.md`
- `Sources/videos/answers/<slug>`
- `Sources/videos/raw/<slug>.md`
- `Sources/videos/raw/<slug>.timestamped.md`
- `_Triage/yt-capture-<slug>.md`
- `~Attachments/IMG-`

### Files
- `references/audio.md`
- `references/goal-mode.md`
- `references/link-harvest.md`
- `references/note-template.md`
- `references/slides.md`
- `scripts/extract-slides.sh`

### Source

`skills/knowledge/capture-youtube/SKILL.md` · 679 lines · `sha c6805941799433c6`

<!-- GENERATED:END -->

## Notes

<!-- Hand-written. Never overwritten by the generator. -->
