#!/usr/bin/env bash
# extract-slides.sh — reduce a YouTube video to a small set of timestamped
# candidate "slide" frames for the process-youtube skill.
#
# Strategy: download a video-only stream (<=1080p, no audio — captions come from
# yt-dlp separately), then let ffmpeg do the cheap visual reduction:
#   - select='gt(scene,T)'  fires on slide changes / camera cuts
#   - mpdecimate            drops frames near-identical to the previous one,
#                           so a slide held for 30s collapses to a single frame
#   - eq(n,0)               always keeps the very first frame (opening slide)
# Output is a handful of ~960px thumbnails (cheap for a vision pass) plus a
# times.txt with one pts_time (seconds) per candidate, aligned by line order.
#
# Usage: extract-slides.sh <youtube-url> <workdir> [scene-threshold]
#   scene-threshold defaults to 0.4. Raise it (0.5-0.6) to get fewer candidates.

set -euo pipefail

URL="${1:?usage: extract-slides.sh <url> <workdir> [threshold]}"
WORKDIR="${2:?usage: extract-slides.sh <url> <workdir> [threshold]}"
THRESHOLD="${3:-0.4}"

command -v yt-dlp >/dev/null 2>&1 || { echo "slides-helper: yt-dlp not found" >&2; exit 3; }
command -v ffmpeg >/dev/null 2>&1 || { echo "slides-helper: ffmpeg not found" >&2; exit 3; }

mkdir -p "$WORKDIR"

# 1) Download a video-only stream up to 1080p (slides are static text — resolution
#    makes them legible). Fallbacks cover videos that only ship combined formats.
yt-dlp -q --no-warnings \
  -f "bv*[height<=1080]/b[height<=1080]/bv*/b" \
  -o "$WORKDIR/video.%(ext)s" "$URL"

VIDEO="$(find "$WORKDIR" -maxdepth 1 -name 'video.*' | head -n1)"
[ -n "$VIDEO" ] || { echo "slides-helper: video download produced no file" >&2; exit 4; }

# 2) Reduce to candidate frames + a parallel metadata dump.
META="$WORKDIR/_meta.txt"
rm -f "$WORKDIR"/cand_*.jpg "$META" "$WORKDIR/times.txt"
ffmpeg -hide_banner -loglevel error -i "$VIDEO" \
  -vf "select='gt(scene,$THRESHOLD)+eq(n,0)',mpdecimate,scale=960:-2,metadata=print:file=$META" \
  -fps_mode vfr "$WORKDIR/cand_%03d.jpg"

# 3) Build times.txt: one pts_time (seconds) per emitted candidate, in order.
#    metadata=print writes a "frame:N pts:X pts_time:Y" header per emitted frame.
grep -oE 'pts_time:[0-9.]+' "$META" | sed 's/pts_time://' > "$WORKDIR/times.txt" || true

CAND_COUNT="$(find "$WORKDIR" -maxdepth 1 -name 'cand_*.jpg' | wc -l | tr -d ' ')"
TIME_COUNT="$(wc -l < "$WORKDIR/times.txt" | tr -d ' ')"

echo "slides-helper: $CAND_COUNT candidates, $TIME_COUNT timestamps (threshold $THRESHOLD)"
if [ "$CAND_COUNT" != "$TIME_COUNT" ]; then
  echo "slides-helper: WARNING candidate/timestamp count mismatch — captions may be misaligned" >&2
fi
