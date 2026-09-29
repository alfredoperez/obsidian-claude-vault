# Link harvesting

How `capture-youtube` turns a video's description and spoken callouts into link cards in
`Sources/links/`, which surface in the existing `Sources/links/Links.base`.

The point: creators put their real resources in the description or say them out loud, and both
die with the video. Everything found is recorded; only the substantive ones become cards.

---

## 1. Where links come from

### Pass A — the description

The description arrives in the Step 3 `--dump-json` payload as `.description`. Scan it for URLs:

```python
import re, json
meta = json.load(open('/tmp/yt-<video_id>.json'))
desc = meta.get('description') or ''
URL_RE = re.compile(r'https?://[^\s<>()\[\]"\'`]+')
raw = [u.rstrip('.,;:!?)') for u in URL_RE.findall(desc)]
```

Also catch bare-domain mentions that creators write without a scheme
(`github.com/foo/bar`, `docs.example.com`) — `\b(?:[\w-]+\.)+[a-z]{2,}/[^\s]*` with a
TLD sanity check.

### Pass B — spoken callouts

Read the **timestamped** transcript (`Sources/videos/raw/<slug>.timestamped.md`) and pull:

- Dictated URLs — "github dot com slash anthropics slash…" → normalise to a real URL.
- Named resources without a URL — a repo, a paper, a tool, a book, a course. Resolve to the
  obvious canonical URL only when you are confident; otherwise record the name with no URL and
  let it stay a manifest row rather than guessing.
- "Link's in the description" moments — these do not produce a link themselves; they raise
  confidence that a matching description URL is substantive. Note the `[mm:ss]`.

Every Pass B hit carries the `[mm:ss]` where it was said.

---

## 2. Normalise, then dedupe

Apply in order:

1. Expand `youtu.be/<id>` → `https://www.youtube.com/watch?v=<id>`.
2. Follow obvious shorteners (`bit.ly`, `t.co`, `lnkd.in`) with a single `curl -sIL -o /dev/null -w '%{url_effective}'`
   so the card records the real destination. If it fails, keep the short URL and flag it.
3. Strip tracking params: `utm_*`, `si`, `feature`, `ref`, `ref_src`, `fbclid`, `gclid`, `igshid`.
4. Drop the trailing slash on bare-domain URLs; keep paths as-is.
5. Dedupe case-insensitively on the normalised URL. When the same URL appears in both passes,
   keep it once and attach the Pass B `timestamp`.

---

## 3. Classify: substantive or noise

Every URL gets exactly one verdict and, when dropped, a one-word reason.

| Verdict | What it covers |
|---|---|
| `substantive` | Source repos, docs sites, papers / arXiv, tools and products the talk actually uses, courses, articles the argument leans on, specs and RFCs, datasets, the speaker's own project being demoed |
| `noise` | Sponsor and affiliate links, discount codes, socials (X/LinkedIn/Instagram/TikTok/Threads/Bluesky), merch, Patreon / Ko-fi / Buy-Me-A-Coffee, newsletter and Discord signups, the channel's own other videos and playlists, chapter-timestamp links, "subscribe" links, generic homepage links to the creator |

Drop reasons to use verbatim so the manifest stays scannable: `sponsor`, `affiliate`, `social`,
`merch`, `membership`, `newsletter`, `own-video`, `chapter-link`, `subscribe`, `self-promo`.

**Edge calls:**

- The creator's *own repo for the thing being demoed* is `substantive`, not `self-promo`.
- A sponsor that *is* the subject of the talk is `substantive` (flag it in the card's `why`).
- A book link on Amazon: `substantive` if the talk builds on the book, `affiliate` if it is a
  list-of-my-favourites dump.
- When genuinely unsure, mark `substantive` and let the confirmation step catch it. Over-including
  costs one line in a shortlist; over-dropping loses the resource silently.

---

## 4. Confirm before writing

Never create cards unprompted. Print the shortlist and wait:

```
Found 19 links. 6 substantive, 13 dropped (5 sponsor, 4 social, 2 own-video, 1 merch, 1 newsletter).

  1. github.com/foo/bar          repo      [04:12] "the whole thing is open source"
  2. arxiv.org/abs/2401.12345    paper     description only
  3. modelcontextprotocol.io     docs      [11:48]
  ...

Create these 6 as link cards in Sources/links/? (all / numbers / none)
```

Accept `all`, a subset (`1 3 5`), or `none`. Dropped links are never lost — the full list with
reasons goes into the capture manifest either way.

Skip existing cards: before writing, `grep -rl "<url>" Sources/links/` (from the vault root)
and report matches as "already carded" rather than creating a duplicate.

---

## 5. Card format

Identical to the `capture` skill's link-card schema so `Links.base` picks them up with no
schema change, plus two YouTube-specific fields.

Path: `Sources/links/<Title>.md` (title-cased from the page or repo name, illegal filename
characters replaced with `-`).

````markdown
---
url: https://github.com/foo/bar
description: "One line, what it is — from the page's own meta description where possible."
host: github.com
category: <see table below>
tags: [<3-5 tags: topic, language, domain>]
added: YYYY-MM-DD
lifespan: durable
why:
from_video: "[[<Video Title>]]"
timestamp: "04:12"
---

```cardlink
url: https://github.com/foo/bar
title: foo/bar
description: ...
host: github.com
```

## Notes
````

- `why:` stays **blank**. It is the user's field, filled by hand later.
- `timestamp:` only when the link was spoken; omit entirely for description-only links.
- `from_video:` is always set — it is what the "From videos" view filters on.
- The ` ```cardlink ` block follows the Auto Card Link plugin format. Fetch the page for real
  title/description where possible; on fetch failure, fill from what the transcript said and
  note it in `## Notes`.

**Categories** — reuse the values already on disk in `Sources/links/`:
`claude-code-skill`, `design-resource`, `design-tool`, `typography`, `dev-tool`, `inspiration`.
Add a new value only when none fit, and say so in the report.

---

## 6. Back-reference in the video note

Add a `## Links` section to the video note, next to `## Reference Snapshot`:

```markdown
## Links
- **[04:12]** [[foo-bar]] — the reference implementation the talk walks through
- [[MCP Docs]] — spec the whole second half depends on
- `arxiv.org/abs/2401.12345` — cited but not carded (paper, no card requested)
```

Links that were found but not carded still appear here as plain text, so the note is complete
even when the user declined the card.
