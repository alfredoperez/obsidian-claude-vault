# Capturing slides

The full slide-extraction pipeline. Loaded only when slides mode is on — it is inert for the
text-only runs that are the default.

Skip this entire step in text-only runs. The goal: end up with a handful of **slide** screenshots,
not the moments the camera cut to the presenter or audience.

1. Choose a workdir and a slug:
   - `WORKDIR=/tmp/yt-slides-<video_id>`
   - `SLUG` = kebab-case of the title (lowercase; non-alphanumerics → single hyphens; trimmed).
     Fallback to `<video_id>` if the title makes a poor slug.

2. **Extract candidates** with the helper script. It downloads a video-only stream (≤1080p), then
   uses ffmpeg scene-change detection + `mpdecimate` (drop near-duplicate frames) to collapse each
   held slide to a single frame:

   ```bash
   bash "$(dirname "$SKILL_MD")/scripts/extract-slides.sh"   # scripts/ sits next to this skill's SKILL.md "<URL>" "/tmp/yt-slides-<video_id>"
   ```

   It writes `cand_NNN.jpg` thumbnails (~960px) and `times.txt` — one timestamp in **seconds** per
   candidate, in the same order as the files (line N ↔ `cand_NNN.jpg`). If it reports more than ~50
   candidates, re-run with a higher threshold appended, e.g. `... "/tmp/yt-slides-<video_id>" 0.55`.

   > If slides look soft, yt-dlp likely only fetched a low-res format (e.g. 360p) — this happens
   > when its JS runtime can't solve YouTube's n-challenge. Updating yt-dlp or installing a JS
   > runtime (`brew install deno`) restores the higher-resolution streams.

   **If the script warns `candidate/timestamp count mismatch`,** do NOT caption from `times.txt` —
   the line-to-file alignment is broken and every caption would land on the wrong slide. Re-run with
   a higher threshold (e.g. `0.55`), which usually resolves it. If it persists, read the timestamp
   for each kept frame off `_meta.txt` directly instead, or fall back to a text-only run and say so
   in the report.

3. **Vision pass — pick the real slides.** `Read` the `cand_*.jpg` thumbnails and decide which to keep:
   - **Keep** slides, diagrams, code, charts, terminal output — any text/content-bearing frame.
   - **Drop** pure presenter/audience/stage/transition/blank frames, and any near-duplicate of a
     slide you're already keeping.
   - **Keep a presenter-in-frame shot when the content matters** — a slide visible behind them, a
     live demo, a key diagram/code on screen. Content value wins over "no humans."
   - When two kept frames show the same slide, keep only the clearest.

   Map each kept candidate to its timestamp via the matching line of `times.txt`.

4. **Grab each kept slide at full resolution** straight into the vault attachments, numbered in
   chronological order (`01`, `02`, …):

   ```bash
   ffmpeg -hide_banner -loglevel error -ss <seconds> \
     -i /tmp/yt-slides-<video_id>/video.* -frames:v 1 -vf "scale='min(1280,iw)':-2" \
     "<vault root>/~Attachments/IMG-<SLUG>-slide-NN.png"
   ```

   `min(1280,iw)` caps width at 1280 but never **upscales** a low-res source (a 360p grab stays
   640×360 rather than being blown up into a blurry 1280-wide PNG).

5. **Caption each slide.** You already saw each slide in the vision pass — write a short, concrete
   caption describing what's *on* it (the title, the key point, the demo step). The transcript at
   that moment is usually a mid-sentence fragment, so use it only as context for wording, never
   paste it verbatim. This snippet prints the cue + `mm:ss` per timestamp to ground you:

   ```python
   import re
   vtt = '/tmp/yt-<video_id>.en.vtt'
   targets = [12.3, 95.0]  # one float per kept slide, in seconds (from times.txt)
   cues, t = [], None
   for line in open(vtt):
       m = re.match(r'(\d+):(\d+):([\d.]+)\s*-->', line)
       if m:
           h, mm, ss = m.groups(); t = int(h)*3600 + int(mm)*60 + float(ss)
       elif t is not None and line.strip() and '-->' not in line:
           txt = re.sub(r'<[^>]+>', '', line).strip()
           if txt: cues.append((t, txt))
   for sec in targets:
       near = [c for c in cues if c[0] <= sec + 1]
       print(f"{int(sec)//60:02d}:{int(sec)%60:02d} | " + (near[-1][1] if near else '(no transcript at this moment)'))
   ```

   Use the printed `mm:ss` for the gallery timestamp; write the caption yourself from the slide.

