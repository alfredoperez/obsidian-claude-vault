# Sections — named composition blocks

Reusable section patterns so a brief is **composed, not hand-built**. The base components (`header`, `callout`, `card`, `table`, `compare`, `decisions`, `flow`/`steps`, `mock`, `band`, `badge`, `legend`, `tag`) live in [`design.md`](./design.md) — use those first. This file adds the recurring patterns that aren't in the skeleton. Class colors follow the active theme's tokens.

| Block | Use when |
|---|---|
| Definition card | a titled item with a plain "what it is" + a verdict/answer line (backlog items, features, options) |
| Trace card | a mechanism walk-through step (flow → exact commands → what lands) |
| Tally trio | three counted buckets as a scannable summary |
| Verdict groups | many items sorted into outcome buckets, each under an eyebrow |
| Harvest table | "from each X, what to pull" — a source → takeaway table |

---

## Definition card
A titled item with a labelled **what** + **verdict**. The workhorse for "explain N things, each standalone."
```html
<div class="card item">
  <div class="top"><h3>Item name</h3><span class="badge b-mut">id</span><span class="badge b-ok">verdict</span></div>
  <p><span class="wl">what</span>One plain-English sentence on what it is.</p>
  <p><span class="vl">verdict</span>The status/answer and why.</p>
</div>
```
```css
.item{margin-bottom:13px}
.item .top{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-bottom:9px}
.item .top h3{font-size:15px}
.item p{font-size:14px;color:var(--ink-2);margin:0 0 7px;line-height:1.55} .item p:last-child{margin-bottom:0}
.item .wl{color:var(--muted);font:700 10px var(--fm);text-transform:uppercase;letter-spacing:.5px;margin-right:7px}
.item .vl{color:var(--accent);font:700 10px var(--fm);text-transform:uppercase;letter-spacing:.5px;margin-right:7px}
```

## Trace card
For a per-step mechanism account: what fires → the exact commands (a `mock`/code block) → what lands. Compose a `.card.item` with a `mock`/code block between the `what` and `lands` lines. Label lines `flow` / `lands` via the same `.wl`/`.vl` spans.

## Tally trio
Three counted buckets after a big grouped section.
```html
<div class="grid cols-3">
  <div class="card"><span class="k">bucket</span><h3 style="font-size:22px;color:var(--ok)">5</h3><p>what it counts.</p></div>
  <div class="card"><span class="k">bucket</span><h3 style="font-size:22px;color:var(--warn)">5</h3><p>…</p></div>
  <div class="card"><span class="k">bucket</span><h3 style="font-size:22px;color:var(--muted)">9</h3><p>…</p></div>
</div>
```
(`.card .k` = the mono kicker label; defined in `design.md`/the theme example.)

## Verdict groups
Many items sorted into outcome buckets. Lead with a `legend` mapping the dot colors to verdicts, then an `eyebrow` + intro per group, then `.card.item`s. Keeps a long list scannable by *outcome* instead of one flat table. (Canonical use: the SDD-backlog mapping brief.)

## Harvest table
"From each source, the one thing worth taking."
```html
<table>
  <tr><th style="width:30%">Source (won't adopt wholesale)</th><th>Idea worth harvesting</th></tr>
  <tr><td><b>thing #2</b></td><td class="add">the specific takeaway →where it applies.</td></tr>
</table>
```
Use `.add`/`.warnc`/`.del` spans (theme status colors) to tag the takeaway's strength.

---

**Rhythm.** Open with `header` → thesis `callout` → body blocks → close with a `band` ("what's next"/recommendation), never a flat summary. Eyebrows mark sections; the lead eyebrow takes the accent (`.lead`).
