> **Not bundled.** Both routes below delegate to skills that live in kaiju, not in this vault (`create-notebooklm`, `create-audio`). Install them if you want `--audio`; otherwise this reference is documentation of what the flag would do.

# Audio summaries — `--audio`

Two routes, asked fresh each run. Neither is the default; the choice depends on whether the
user wants quality (NotebookLM, capped) or unlimited local generation (Voicebox).

Only offer this when `--audio` was passed. Do not generate audio unprompted.

---

## The menu

Ask with `AskUserQuestion` after the note is written and before cleanup:

| Option | Route | Cost |
|---|---|---|
| **NotebookLM deep-dive** | two AI hosts, conversational, ~8-15 min | free tier: 3 audio overviews/day |
| **NotebookLM brief** | same voices, short-form summary | same cap |
| **`/create-audio`** | local Voicebox render in the user's own voice | free, unlimited, plays aloud |
| **Skip** | no audio | — |

Recommend NotebookLM deep-dive for a talk worth revisiting; `/create-audio` when the daily cap is
spent, the user wants it immediately, or they want it in their own voice.

---

## Route A — NotebookLM

CLI is installed (`create-notebooklm`, pipx package `notebooklm-py`). See the `create-notebooklm` skill for
the full command surface; this is the subset for one video.

### Preflight

```bash
notebooklm auth check --test --json
```

Good only if `status == "ok"` **and** `checks.token_fetch == true`. The exit code is unreliable —
parse the JSON.

**Never call `create-notebooklm login` from a tool call.** It blocks on a browser plus ENTER and will
hang the run. On auth failure, tell the user to run it themselves and offer the Voicebox route
instead.

### Generate

```bash
notebooklm create "<Video Title>"            # append " — YYYY-MM-DD" on title collision
notebooklm use <id-prefix>                   # 6-8 chars is enough

notebooklm source add "<abs path to Sources/videos/raw/<slug>.md>" \
  --type file --title "<slug> transcript"
notebooklm source add "<abs path to Sources/videos/<Video Title>.md>" \
  --type file --title "<slug> notes"
# in goal mode, add the answer note too:
notebooklm source add "<abs path to the answer note>" --type file --title "<goal-slug> answer"

notebooklm source list --json                # poll until every status == ready (3s sleep, 3 min cap)

notebooklm generate audio "<focus line>" --format deep-dive --no-wait --json
# brief variant: --format brief --length short

notebooklm artifact wait <artifact-id> --timeout 600 --interval 5
notebooklm download audio "<vault>/~Attachments/create-notebooklm/<slug>/audio.mp3" --latest --force
```

The `<focus line>` steers the hosts. In goal mode, pass the user's question so the episode
answers it. Otherwise pass the note's abstract.

### Known limits

- ~50 sources per notebook; not a concern for one video.
- `create-notebooklm create` does not dedupe titles.
- `generate audio` can be hourly-rate-limited — add `--retry 3` or wait ~10 minutes.
- On `artifact wait` timeout, fall back to `create-notebooklm artifact poll <task-id>` and tell the
  user it is still cooking rather than failing the run.
- Any mid-flow `Authentication expired or invalid. Redirected to: https://accounts.google.com/...`
  is an auth failure — stop the audio step, keep everything else.

---

## Route B — `/create-audio` (local, your own voices)

**Delegate to the `create-audio` skill.** It owns Voicebox: profile selection, the `type: audio-script`
note convention, the write-for-the-ear rules, per-turn rendering, and the ffmpeg stitch. Do not
re-implement any of it here.

```
/create-audio "<abs path to Sources/videos/<Video Title>.md>" --out Sources/videos/audio/
```

Pass the video note as the source — it is the distilled version, and it reads far better aloud than
a raw transcript. In goal mode, narrate the **answer note** instead; it is short, it leads with the
conclusion, and it is usually the thing worth listening to.

**One voice is the default and is usually right here.** A video summary is a straight read with no
framing/delivering split, so do not pass `--voices two` unless the user asks for it.

`create-audio` handles its own preflight — if the Voicebox MCP server is not registered or the app is
not running, it says so and offers `--script-only`. If it comes back unavailable, offer Route A.

## Landing it in the note

Both routes end the same way. Add to the video note:

```markdown
## Audio Summary
![[<slug>-summary.wav]]
*Spoken summary, <route>, YYYY-MM-DD. Script: [[<slug>-summary]]*
```

And stamp the frontmatter:

```yaml
audio: "Sources/videos/audio/<slug>-summary.wav"     # or the notebooklm path
audio_source: notebooklm-deep-dive | notebooklm-brief | narrate
```

Where each route's files land:

| Route | Audio | Companion |
|---|---|---|
| `/create-audio` | `Sources/videos/audio/<slug>-summary.wav` | the `type: audio-script` note beside it |
| NotebookLM | `~Attachments/create-notebooklm/<slug>/audio.mp3` | save the episode transcript as `<slug>-transcript.txt` alongside |

**Save the NotebookLM transcript too.** The existing `notebooklm-exports/` folder in the
Architecture for Flow talk keeps a `transcripts/` directory next to `media/` for exactly this
reason: the audio is unsearchable, the transcript is greppable, and the phrasing the hosts land on
is often worth stealing. Pull it with `create-notebooklm download report` or the episode's transcript
artifact if one is offered.

Record the artifact path, the size, and the route in the capture manifest, so a failed or skipped
audio run is visible rather than silently absent.
