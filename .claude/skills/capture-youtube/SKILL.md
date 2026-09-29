---
name: capture-youtube
description: "Extract knowledge from a YouTube video into topic-based notes, harvest the links it names into link cards, archive the transcript, and optionally answer a specific question or produce an audio summary. Use when the user shares a YouTube URL and wants detailed notes, mentions extracting knowledge from a video, wants the links or resources a video mentions, wants a video to answer a question, or says 'process youtube'. Pass --slides for slide screenshots, --goal to answer a question, --audio for a spoken summary, --links-only for a cheap link harvest, --report-only when running as a subagent."
argument-hint: "<youtube-url...> [--goal \"question\"] [--audio] [--links-only] [--slides] [--report-only]"
---

# Process YouTube

Extract knowledge from a YouTube video into structured topic-based notes, and keep everything
around it that would otherwise die with the video: the links it names, the description, the
transcript. Optionally answer a question you brought to it, and read the result back to you.

## When to Use

- User says `/capture-youtube <url>`
- User shares a YouTube URL and wants notes from it
- User wants to extract knowledge from a video
- User wants the resources / links a video mentions ("what did they link?", `--links-only`)
- User has a **question** a video might answer (`--goal "..."`)
- User wants to listen rather than read (`--audio`)

## Inputs

- **YouTube URL** (required) — one or more valid YouTube video URLs
- **`--slides`** (optional, alias `--screenshots`) — also capture the video's slides as
  screenshots and embed them in the note. Off by default (text-only). Best for conference talks.
- **`--goal "<question>"`** (optional) — a question you brought to the video. Runs the full
  normal pipeline *and* writes a focused answer note with timestamped citations. See
  `references/goal-mode.md`.
- **`--audio`** (optional) — offer a spoken summary at the end (NotebookLM two-host podcast, or
  a local render). Both routes need skills that are not bundled with this vault (`create-notebooklm`, `create-audio` from kaiju); without them, skip the flag. See `references/audio.md`.
- **`--links-only`** (optional) — harvest the description + spoken links into link cards and
  write the capture manifest, then stop. No note, no slides, no concept merge. Cheap.

- **`--report-only`** (optional) — **for subagent / batch runs.** Does everything that touches
  only this video's own files, and *returns* the link and concept-merge decisions instead of
  writing them. Nothing shared gets written, so many videos can run in parallel without
  colliding. See "Report-only mode" below.

Flags compose: `--goal` and `--audio` can run together, with or without `--slides`.
`--links-only` overrides the others. `--report-only` can combine with any of them except
`--audio`, which it disables.

## Reference files

| Topic | File |
|---|---|
| URL regexes, normalisation, classification table, link-card schema | `references/link-harvest.md` |
| Answer-note template, verdict vocabulary, citation + deep-link rules | `references/goal-mode.md` |
| The two audio routes: `create-notebooklm` and `create-audio` | `references/audio.md` |
| Slide capture: frame diff, dedupe, captioning, embed rules | `references/slides.md` |
| The video note's exact shape: frontmatter, sections, per-block rules | `references/note-template.md` |
| Slide-candidate extraction | `scripts/extract-slides.sh` |

## Report-only mode

For **subagent and batch runs**, where nothing can ask the user a question and many videos run at
once. The rule is simple: **write only what belongs to this video; return everything shared.**

| Step | Normal | `--report-only` |
|---|---|---|
| Video note, both transcripts, slides, manifest | written | **written** (paths are unique per video, so no collision) |
| Goal answer note | written | **written** (unique per video + goal) |
| Link cards → `Sources/links/` | confirmed, then written | **not written** — the classified list is returned |
| Concept merges → `Personal/`, `Knowledge/` | proposed, approved, written | **not written** — proposals are returned |
| Audio (Step 8) | menu | **skipped** |

Shared vault state is exactly where parallel runs collide: several videos in a batch will name the
same repo, and several will want the same concept page. Deciding those once, centrally, beats
racing on them.

> [!danger] **Every scratch file you create must carry the video ID in its name.**
> The vault paths in the table above are already unique per video. Your *temporary* files are not,
> and that is where parallel runs actually corrupt each other. Sibling agents share one scratchpad
> directory. A helper written to `clean.py`, `clean.txt`, or `ts.txt` will be silently overwritten
> by another video mid-run, and you will ship someone else's transcript under your video's title
> without any error being raised.
>
> Namespace everything: `yt-<video_id>.en.vtt`, `clean-<video_id>.txt`, or your own subdirectory
> `<scratchpad>/<video_id>/`. Never a bare generic name.
>
> **Then verify before reporting success.** Every deep link in the timestamped transcript you wrote
> must carry your own video ID:
>
> ```bash
> grep -oE 'v=[A-Za-z0-9_-]{11}' <timestamped file> | sort -u
> ```
>
> One ID, and it is yours. More than one means either a legitimate cross-link in the transcript
> body or a collision — open the file and look. This check costs a second and is the only thing
> standing between a clobbered temp file and a permanently wrong archive.
>
> *Written after a real incident: in a 66-video parallel batch, one agent's generic `clean.txt` was
> overwritten by another's, and the victim's transcript shipped with 46 lines of a different video
> and 2 of its own. The note read correctly, because it had been written before the clobber. Only
> the provenance layer was wrong, which is the failure mode nobody checks.*

**Return this structure** so a parent can merge across videos:

```yaml
video: "<title>"
url: <URL>
note: Sources/videos/<title>.md
transcripts: [Sources/videos/raw/<slug>.md, Sources/videos/raw/<slug>.timestamped.md]
manifest: _Triage/yt-capture-<slug>.md
answer: Sources/videos/answers/<...>.md    # goal mode only
slides: 0
summary: |
  5 lines on what the video actually argues.
links:
  - url: https://github.com/foo/bar
    verdict: substantive          # or noise
    reason: repo                  # drop reason when noise
    timestamp: "04:12"            # omit if description-only
    why: one line on why it matters
merges:
  - page: Knowledge/AI/<page>.md
    substance: what would move
    contradiction: what it conflicts with, or null
```

Say plainly in the return when a section is empty — an absent `links:` key and "no substantive
links" are different facts to whoever is merging.

## Workflow

### Step 1: Validate Input

1. If no URL provided, ask: "What's the YouTube video URL?"
2. Validate it's a YouTube URL (youtube.com or youtu.be).
3. Parse the flags:
   - `--slides` (alias `--screenshots`) → **slides mode** on; otherwise the run is text-only and
     you skip every slide step below.
   - `--goal "<question>"` → **goal mode** on. Capture the question verbatim; you will need it
     word-for-word in the answer note's frontmatter.
   - `--audio` → offer the audio menu at Step 8.
   - `--links-only` → run Steps 1, 2, 3, 3.5 and 7's manifest only, then stop. Say clearly in the
     report that no video note was written.
   - `--report-only` → **report mode** on. Turn `--audio` off if it was also passed (the audio
     menu needs a human). See "Report-only mode" below for exactly what changes.
4. **Check whether this video is already in the vault** before spending anything on it. Extract the
   video ID and grep the source layer for it:

   ```bash
   grep -rl "<video_id>" Sources/ 2>/dev/null     # from the vault root
   ```

   If a note comes back, **stop and tell the user** which note already covers it and when it was
   created. Do not silently reprocess. Continue only if they explicitly want it refreshed — and if
   they do, edit the existing note in place rather than creating a second one.

   When several URLs are passed at once, run this check for **each** of them up front and report
   the skips together, so the user sees the whole picture before any downloads start.

### Step 2: Verify dependency

Check that `yt-dlp` is available:

```bash
command -v yt-dlp
```

If missing, stop and tell the user:

> `yt-dlp` is required to fetch transcripts. Install it with `brew install yt-dlp` (or `pipx install yt-dlp`).

WebFetch alone cannot extract YouTube transcripts — the page is JS-rendered and only the bare HTML shell comes back. `yt-dlp` is the reliable path.

**If slides mode is on**, also check `ffmpeg`:

```bash
command -v ffmpeg
```

If `ffmpeg` is missing, don't fail the run — turn slides mode **off**, continue text-only, and note
in the final report that slides were skipped (suggest `brew install ffmpeg`).

> **yt-dlp freshness matters for slide resolution.** A stale yt-dlp can't solve YouTube's
> n-challenge, so only a low-res (360p) format downloads and slide text comes out blurry.
>
> Homebrew's `yt-dlp` formula often lags upstream by weeks, and `yt-dlp -U` **does not work on a
> Homebrew install** (it self-updates only standalone binaries). If yt-dlp is behind, the working
> remedy is a pipx/uv install carrying the impersonation extra:
>
> ```bash
> uv tool install --force "yt-dlp[default,curl-cffi]"
> ```
>
> Check impersonation with `yt-dlp --list-impersonate-targets` — if every target says
> `(unavailable)`, `curl_cffi` is missing and downloads will be slower and more timeout-prone.
> Don't auto-update their tools from the skill; tell the user.

### Step 3: Fetch metadata and transcript with yt-dlp

Run two `yt-dlp` invocations.

**Metadata (title, channel, date, duration, description, chapters):**

```bash
yt-dlp --skip-download --dump-json "<URL>" > /tmp/yt-<video_id>.json
jq -r '.title, .channel, .upload_date, .duration_string' /tmp/yt-<video_id>.json
```

Read `.title`, `.channel`, `.upload_date`, `.duration_string`, `.description`, `.chapters[]`
and `.tags[]` from that JSON.

> **Use `--dump-json`, never a pipe-delimited `--print`.** Descriptions routinely contain `|`
> characters and newlines, which silently corrupt a delimiter-split parse — the field that breaks
> first is the description, which is exactly the field Step 3.5 needs. Keep the JSON on disk until
> cleanup; Step 3.5 and Step 7 both read it.

**Auto-generated English captions:**

```bash
yt-dlp --write-auto-sub --skip-download \
  --sub-lang en --sub-format vtt \
  -o "/tmp/yt-%(id)s.%(ext)s" "<URL>"
```

This writes `/tmp/yt-<video_id>.en.vtt`.

**Clean the VTT into plain text** (strip `<00:00:00.000>` timing tags, drop the WEBVTT header, dedupe rolling-caption lines):

```python
import re, html
with open('/tmp/yt-<video_id>.en.vtt') as f:
    raw = f.read()
out, seen = [], set()
for line in raw.split('\n'):
    line = line.strip()
    if not line or line.startswith(('WEBVTT', 'Kind:', 'Language:')) or '-->' in line:
        continue
    line = html.unescape(re.sub(r'<[^>]+>', '', line)).replace('\xa0', ' ').strip()
    line = re.sub(r'\s+', ' ', line)
    if line and line.lower() != '[music]' and line not in seen:
        seen.add(line)
        out.append(line)
print(' '.join(out))
```

`html.unescape` matters — raw auto-captions are full of `&gt;&gt;`, `&nbsp;`, `&#39;` that
otherwise leak into the note and make it look broken.

**Also build a timestamped version.** The clean text above is what you read and what NotebookLM
ingests; the timestamped version is what makes citations and `--goal` deep links possible. Same
cleaning, but grouped into ~45-second blocks keyed by the cue time:

```python
import re, html
BLOCK = 45  # seconds per block
cues, t = [], None
for line in open('/tmp/yt-<video_id>.en.vtt'):
    m = re.match(r'(\d+):(\d+):([\d.]+)\s*-->', line)
    if m:
        h, mm, ss = m.groups(); t = int(h)*3600 + int(mm)*60 + float(ss)
    elif t is not None and line.strip() and '-->' not in line \
            and not line.strip().isdigit() \
            and not line.startswith(('WEBVTT','Kind:','Language:')):
        txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', line)).replace('\xa0',' ')).strip()
        if txt and txt.lower() != '[music]':
            cues.append((t, txt))
blocks, seen = {}, set()
for sec, txt in cues:
    if txt in seen: continue          # rolling-caption dedupe
    seen.add(txt)
    blocks.setdefault(int(sec // BLOCK) * BLOCK, []).append(txt)
for start in sorted(blocks):
    mmss = f"{start//60:02d}:{start%60:02d}"
    print(f"**[{mmss}](https://www.youtube.com/watch?v=<video_id>&t={start}s)** " + ' '.join(blocks[start]) + "\n")
```

Hold both in memory; Step 7 writes them to disk.

**Read the full cleaned transcript before writing anything.** Do not skim or work from the
first few lines — the depth and accuracy of the note depend on understanding the whole talk
(its arc, the examples, the payoff). An 18-minute talk is ~3-4k words; read all of it.

If the captions file is missing (no auto-subs available for this video — common for
Looms, small channels, raw files), **fall back to local whisper transcription** instead
of degrading to the description:

```bash
command -v whisper-cli || echo "whisper-cli missing — brew install whisper-cpp"
yt-dlp -q -f "ba/b" -x --audio-format wav --postprocessor-args "-ar 16000 -ac 1" \
  -o "/tmp/yt-%(id)s-audio.%(ext)s" "<URL>"
whisper-cli -m <model> -l auto -np -otxt -of "/tmp/yt-<video_id>-whisper" \
  "/tmp/yt-<video_id>-audio.wav"
```

Model resolution: use an existing `ggml-*.bin` if one is on disk (check
`~/dev/GitHub/whisper.cpp/models/` and `$(brew --prefix)/share/whisper-cpp/`); otherwise
download `ggml-small.bin` once from https://huggingface.co/ggerganov/whisper.cpp/tree/main
into `~/dev/GitHub/whisper.cpp/models/` (ask before the ~466MB download). Long videos take
minutes of CPU — tell the user before transcribing anything over ~30 minutes. The output
`.txt` replaces the cleaned-captions text; note in the final report that the transcript
came from whisper. Only if BOTH captions and whisper are unavailable, fall back to the
description and warn that the note will be thinner than usual.

> **Keep the raw `/tmp/yt-<video_id>.en.vtt` on disk** until cleanup (Step 7). Slide captioning
> (Step 3.6) re-parses it for timestamps. The plain-text version above is only for the note body.

### Step 3.5: Harvest the links

Creators put their real resources in the description or say them out loud, and both vanish when
the video does. This step captures every URL the video offers, keeps the substantive ones as link
cards in `Sources/links/`, and records the rest in the manifest.

Full procedure — regexes, normalisation, the classification table, and the card schema — lives in
**`references/link-harvest.md`**. Read it before running this step. The shape:

1. **Scan the description** (`.description` from the Step 3 JSON) for URLs and bare domains.
2. **Scan the timestamped transcript** for spoken URLs ("github dot com slash…"), named
   repos/papers/tools, and "link's in the description" moments. Each hit carries its `[mm:ss]`.
3. **Normalise** — expand `youtu.be`, resolve shorteners, strip `utm_*`/`si`/`ref`/`fbclid`
   tracking params, dedupe.
4. **Classify** each as `substantive` or `noise`, with a one-word drop reason
   (`sponsor`, `affiliate`, `social`, `merch`, `membership`, `newsletter`, `own-video`,
   `chapter-link`, `subscribe`, `self-promo`).
5. **Check for existing cards** — `grep -rl "<url>" Sources/links/` —
   and report matches as "already carded" instead of duplicating.
6. **Show the shortlist and ask.** Never write cards unprompted. Print the substantive list with
   its `[mm:ss]` and a one-line why, plus a summary count of what was dropped and why. Accept
   `all`, a subset, or `none`.
7. **Write the approved cards** to `Sources/links/<Title>.md` using the `capture` skill's existing
   schema plus `from_video: "[[<Video Title>]]"` and, when spoken, `timestamp: "mm:ss"`. Those two
   fields are what the "From videos" view in `Sources/links/Links.base` filters on.

Everything found — kept, declined, and dropped — goes into the capture manifest at Step 7,
so nothing is lost even when the user says `none`.

> **`--links-only` stops here.** Write the manifest, report what was carded, and skip the rest of
> the workflow. Say explicitly that no video note was created.

> **In `--report-only`, stop after step 4.** Do the scan, normalisation, and classification, then
> return the list. Do not check for existing cards, do not ask, do not write to `Sources/links/`.
> The parent merges across every video and cards them once.

### Step 3.6: Capture slides (only when slides mode is on)

Off by default. When slides mode is on, follow **`references/slides.md`** — the frame-diff capture,
dedupe, caption, and embed rules live there in full. Two rules that must not be forgotten if you
skip the read: always write the explicit `.png` extension (`![[IMG-<SLUG>-slide-NN.png]]`), and in
a text-only run omit the `## Slides` section and every inline embed.

### Step 4: Determine Destination

Video notes are **processed input**, not knowledge — they live under `Sources/videos/`
(never `Knowledge/`). Default is the flat folder; use a topic subfolder only when the
video belongs to an already-tracked series:

```bash
ls Sources/videos/      # from the vault root
```

(at time of writing the only series subfolder is `sdd/`). If unsure whether a video starts
a new series, **ask the user** before creating a subfolder.

### Step 5: Create the Video Note

Write the note to the destination from Step 4 using the exact shape in
**`references/note-template.md`** — frontmatter, section order, and the rule for each block.
Do not improvise the structure; `Links.base` and the concept layer both key off it.

### Step 6: Find Related Notes

1. Actually search the vault (grep/glob over `Sources/` and `Knowledge/`) for notes on the
   same topics — don't invent links. Only add `[[wikilinks]]` to notes that exist.
2. Add them under `## Related Notes`.
3. Suggest (don't auto-add) backlinks from those notes to this one.

### Step 6.5: Fold into the concept layer

This is the step that makes the vault compound instead of accumulate. A video note is *processed
input*; the knowledge only becomes retrievable when it reaches a **concept page** — a durable,
topic-scoped note that synthesizes every source covering that topic.

The vault already works this way in places. `Personal/Health/` is the reference implementation:
~20 concept pages (`VO2 Max.md`, `Mobility & Movement.md`, `Daily Mobility Routine.md`), each
ending in a `## Sources` section with a per-source block of key points and a link. Read one before
merging so you match the existing shape.

**1. Find the candidate pages.** `Terms.md` first, prose grep second:

```bash
grep -i "<topic>" Terms.md          # the author's own words for it (from the vault root)
grep -ril "<topic>" Knowledge/ Projects/
```

**Run both.** The prose grep alone misses pages whose wording differs from the video's:
`grep -ri "eval rubric"` finds nothing while six notes say `rubric-grading`. `Terms.md` catches
those. It only covers notes carrying `tags`/`keywords`/`entities`/`claims`, so the prose grep is
still what reaches the rest.

The video note's own `## Related Notes` is usually the best starting list.

**2. Decide what actually merges.** Not everything does:

- **Merges:** substance the concept page doesn't already have — a protocol, a study with numbers,
  a mechanism, a boundary condition ("this works, except when…").
- **Sources entry only:** the video restates what the page already says, or is thin. Add it to
  `## Sources` so it is findable and not orphaned, but do not pad the prose.
- **Nothing at all:** clickbait with no substance. Say so in the report rather than merging noise.

**3. Apply the page-creation threshold before inventing a new page.** A topic earns its own concept
page when it recurs across **≥2 sources** or is linked from **≥2 places**. Below that bar it belongs
inside an existing page. When a video clearly has no home and clears the bar, propose the new page —
don't create it silently.

**4. Flag conflicts, never silently resolve them.** If the video contradicts what a concept page
already asserts, add a callout on the page citing both sources and let the reader judge:

```markdown
> **Tension:** La Rosa argues recomposition suits nearly everyone; Tomic argues a lean bulk wins
> once you are already lean post-cut. They agree on the mechanism and differ on who should do what.
> — [[Recomposición CORPORAL]] vs [[Why Fixing Skinny Fat Takes SO Long]]
```

A refinement is not a contradiction — if the new source adds nuance to an existing prescription
(a beginner scaffold, a frequency floor), integrate it as nuance and say so.

> **In `--report-only`, do the analysis and return the proposals.** Steps 1-4 below still run —
> you are the one who read the talk, so you are best placed to judge what merges. Write nothing to
> `Personal/` or `Knowledge/`, and skip step 5's ask; there is no user to ask.

**5. Always ask before writing.** Show the user the merge plan — which video, into which page, what
substance moves — and get a yes. These pages are usually hand-built and carry the user's voice;
never bulk-rewrite them. Default to additive: extend prose where it genuinely belongs, and always
append the `## Sources` entry.

**6. Update `## Sources` on every page you touch**, following the page's existing format:

```markdown
### <Video Title> — <Channel> (<upload_date>)
- <key point this video contributed>
- <key point>
- [Watch](<URL>)
```

If the domain folder has an index note, add the new/updated pages to it.

### Step 6.6: Answer the goal (only in goal mode)

Skip entirely when no `--goal` was passed.

Goal mode is **additive** — everything above has already run in full. Now write the answer as its
own note. Template, verdict vocabulary, and citation rules live in **`references/goal-mode.md`**.

Path: `Sources/videos/answers/<slug> — <goal-slug>.md`, where `<goal-slug>` is the question
kebab-cased and truncated to ~40 characters (so one video can hold several answers).

```yaml
---
created: YYYY-MM-DD
type: video-answer
goal: "<the question, verbatim as the user asked it>"
video: "[[<Video Title>]]"
source: <YouTube URL>
verdict: answered | partial | not-answered
---
```

Body order is fixed, because the value is in the ordering:

1. **The answer**, 2-4 sentences, first thing on the page. No "in this video the speaker
   discusses…" — state the conclusion.
2. **`## Evidence`** — bullets, each with `**[mm:ss]**`, what was said, and a
   `[Watch](https://www.youtube.com/watch?v=<id>&t=<seconds>s)` deep link. Timestamps come from
   the timestamped transcript built in Step 3, never guessed.
3. **`## What this video does not answer`** — the honest gap. Write it even when the verdict is
   `answered`; it is what stops the user over-trusting a partial source.
4. **`## Where to look next`** — only when there is a genuine lead. Omit otherwise.

`verdict: not-answered` is a **successful run**, not a failure. A note recording "this talk does
not cover X" saves rewatching it later. Never stretch a `partial` into an `answered`.

**Several URLs with one `--goal`** → each video still gets its own full processing, and the answer
is a single synthesis note at `Sources/videos/answers/<goal-slug>.md` with a `videos:` list,
evidence grouped by video, and a `## Where they disagree` section when the sources genuinely
conflict. Present both sides and cite both; do not resolve it.

Add the answer note to the source video note's `## Related Notes`.

### Step 7: Preserve, record, clean up

**1. Write both transcripts.** They are the provenance layer: a few KB that make every later
citation possible. Two files, same slug as the note:

```bash
mkdir -p Sources/videos/raw      # from the vault root
```

| File | `type:` | What it holds |
|---|---|---|
| `Sources/videos/raw/<slug>.md` | `raw-transcript` | the clean, readable prose from Step 3 — the good NotebookLM ingest source |
| `Sources/videos/raw/<slug>.timestamped.md` | `raw-transcript-timestamped` | the `[mm:ss]`-prefixed blocks, each a deep link — what `--goal` and slide captions cite |

Both get the same minimal frontmatter, so they are identifiable and never hand-edited:

```yaml
---
type: raw-transcript          # or raw-transcript-timestamped
immutable: true
source: <YouTube URL>
video_id: <video_id>
note: "[[<Video Title>]]"
---
```

**Append the description verbatim** to `Sources/videos/raw/<slug>.md` under a `## Description`
heading. It is where the links came from and it is the part that dies with the video — keep it
even when it is mostly sponsor boilerplate. Include the chapter list from `.chapters[]` if present.

**2. Write the capture manifest** — a disposable receipt of the whole run, so the user can see
everything that was captured before deciding what to keep:

`_Triage/yt-capture-<slug>.md`

```yaml
---
type: capture-manifest
lifespan: ephemeral
expires: <today + 14 days>
source: <YouTube URL>
video: "[[<Video Title>]]"
---
```

It records, in this order:

- **Files written** — every path, including the note, both transcripts, each link card, each
  slide image, the answer note, and any audio artifact.
- **Links** — every URL found, each marked carded / declined / dropped with its reason. This is
  the full list, including the noise, so nothing is silently discarded.
- **Description** — verbatim, plus the chapter list.
- **Slides** — candidates extracted, kept, and rejected (with why), when slides mode ran.
- **Concept merges** — pages touched and what moved, plus pages considered and declined with the
  reason.
- **Goal** — the question and the verdict, when goal mode ran.
- **Skipped** — anything that did not happen and why (ffmpeg missing, auth expired, user declined).

No cleanup machinery is needed: `groom` already treats `lifespan: ephemeral` past its
`expires:` as a strong stale signal and proposes archiving it.

**3. Delete the temp files.** The downloaded video and candidate thumbnails are large and
disposable. Keep only the selected `~Attachments/IMG-*-slide-*.png`:

```bash
rm -f /tmp/yt-<video_id>.en.vtt /tmp/yt-<video_id>.json
rm -rf /tmp/yt-slides-<video_id> /tmp/yt-audio-<video_id>
```

### Step 8: Audio summary (only when `--audio` was passed)

Skip entirely otherwise — never generate audio unprompted. Also skipped in `--report-only`:
the menu needs a human, so audio is a parent-session decision.

Ask which route with `AskUserQuestion`. Both routes and their exact commands live in
**`references/audio.md`**; read it before running this step.

| Option | Route | Cost |
|---|---|---|
| NotebookLM deep-dive | two AI hosts, conversational | free tier: 3/day |
| NotebookLM brief | same voices, short form | same cap |
| `/create-audio` | local Voicebox render, the user's own voice | free, unlimited, **plays aloud** |
| Skip | — | — |

Two things to surface rather than discover mid-run:

- **NotebookLM** — preflight with `create-notebooklm auth check --test --json` and parse the JSON
  (the exit code is unreliable). **Never call `create-notebooklm login` from a tool call** — it blocks on
  a browser. On auth failure, offer `/create-audio` instead.
- **`/create-audio`** — delegate the local route entirely; that skill owns Voicebox, the
  `type: audio-script` convention, and the write-for-the-ear rules. Pass the video note as the
  source (or, in goal mode, the answer note — it is shorter and leads with the conclusion). One
  voice is the default and is right for a summary. `create-audio` runs its own preflight and warns that
  rendering plays out loud; if it reports Voicebox unavailable, fall back to NotebookLM.

Either route ends by embedding the result in the video note under `## Audio Summary` and stamping
`audio:` + `audio_source:` in its frontmatter. Save the NotebookLM episode transcript alongside
its mp3 — the audio is unsearchable, the transcript is not. Record the artifact path, its size,
or the reason audio was skipped, in the manifest.

### Step 9: Report

> Created video notes at `Sources/videos/<title>.md`
> - X main ideas extracted
> - Y related notes found
> - Z slides captured  ← only when slides mode ran (say "slides skipped: ffmpeg missing" if that was the reason)
> - N links carded, M dropped (`Sources/links/`)
> - Transcripts preserved at `Sources/videos/raw/<slug>.md` (+ `.timestamped.md`)
> - Goal: "<question>" → **<verdict>** — `Sources/videos/answers/<...>.md`  ← goal mode only
> - Audio: `<path>` via <route>  ← audio mode only, or the reason it was skipped
> - Folded into: `<concept page>` (what moved) — or "no concept merge: <reason>"
> - Capture manifest: `_Triage/yt-capture-<slug>.md` (expires <date>)

For `--links-only` runs, report only the link and manifest lines, and say explicitly that no
video note was created.

## Examples

```
/capture-youtube https://youtu.be/abc123
```
Full note, links harvested and confirmed, both transcripts archived, concept merge proposed.

```
/capture-youtube https://youtu.be/abc123 --slides
```
Same, plus a `## Slides` gallery of the talk's content-bearing frames.

```
/capture-youtube https://youtu.be/abc123 --links-only
```
Just the links: classify, confirm, card, write the manifest. No note. Cheap and fast.

```
/capture-youtube https://youtu.be/abc123 --goal "does this actually work without a GPU?"
```
Everything above, plus `Sources/videos/answers/<slug> — does-this-actually-work-without-a-gpu.md`
leading with the answer and citing timestamps.

```
/capture-youtube <url-a> <url-b> <url-c> --goal "which of these handles auth best?"
```
Three full video notes, one synthesis answer note citing across all three, with a
`## Where they disagree` section.

```
/capture-youtube https://youtu.be/abc123 --slides --goal "..." --audio
```
The works. Asks which audio route at the end.

```
/capture-youtube https://youtu.be/abc123 --report-only --goal "..."
```
Subagent/batch mode. Writes this video's own note, transcripts, manifest and answer note; returns
the link and merge decisions for the parent to dedupe across the whole batch.

## Quality Checklist

> [!danger] **Grade these one at a time, not all at once.**
> Handing a model an eleven-item checklist and asking it to grade the lot in one pass produces a
> general impression dressed up as eleven judgements. It washes out and goes lazy, and every item
> comes back "fine". Fan out: one sub-agent, or one pass, per criterion.
>
> Source: Hamel Husain and Shreya Shankar, who named this exact failure. This checklist has been
> graded in a single pass since it was written.

- [ ] Dedupe check ran **before** any download, and reported skips up front for multi-URL runs.
- [ ] Metadata came from `--dump-json`, not a pipe-delimited `--print`.
- [ ] The **whole** transcript was read before writing — not the first few lines.
- [ ] Both transcripts written; the description is archived verbatim.
- [ ] Every link was classified, the shortlist was **confirmed** before any card was written, and
      the dropped ones are in the manifest with reasons.
- [ ] Every `[[wikilink]]` in `## Related Notes` points at a note that actually exists.
- [ ] Concept-layer merges were **proposed and approved**, never written silently.
- [ ] In goal mode: the answer leads the note, every claim traces to a timestamp, and the
      "does not answer" section is present.
- [ ] Slide captions describe what is **on** the slide, not the transcript fragment at that moment.
- [ ] Temp files deleted; only selected slide PNGs remain in `~Attachments/`.
- [ ] The manifest lists every file written and every URL considered.
- [ ] In `--report-only`: nothing was written to `Sources/links/`, `Personal/`, or `Knowledge/`,
      and the return carries the structured `links:` / `merges:` blocks.

## Tips

- **The dedupe check is the cheapest step and saves the most.** Always run it first.
- **A thin note is worse than no note.** If captions and whisper both fail, say the note will be
  description-only and ask whether to continue.
- **Prefer over-including a link to over-dropping one.** An extra line in a shortlist costs
  nothing; a silently dropped repo is gone.
- **`not-answered` is a real result.** Recording that a talk does not cover something is worth
  the note.
- **Slides mode is for talks.** A talking-head video produces mostly presenter frames and burns
  a video download for nothing.
- **Fanning out over a batch? Use `--report-only` and skip `--slides`.** Parallel video downloads
  are the expensive part, and shared writes are where parallel runs collide. Let the parent do
  the cards and merges once, then re-run `--slides` on the few videos that earn it.
