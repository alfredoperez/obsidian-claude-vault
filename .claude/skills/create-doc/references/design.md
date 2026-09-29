# Design System — HTML Briefs (dark-mode Cohere)

The house style for self-contained HTML briefs and explainers. Read this before generating one. It is the single source of truth for color, type, spacing, and components — do not invent values outside it.

Derived from Cohere's design language (getdesign.md), rendered **dark-mode-first**: dark surfaces are the default canvas, light ink sits on top, and color arrives sparingly through coral/blue accents, status tints, and the occasional deep green or navy brand band. The feel is a quiet research-lab console: austere, tight, confident — not a dashboard, not marketing.

> **Fastest path:** copy the [Starter skeleton](#starter-skeleton) at the bottom, then fill in content with the [Components](#components). Everything below explains the choices behind that skeleton.

---

## Overview

- **Dark canvas, restrained color.** Near-black surfaces, light text, hairline borders. Accents (coral, blue) and status tints are used in small doses, never as broad fills.
- **Monumental but compact type.** One large, tight headline per brief; everything else settles into measured 15px body and small uppercase mono labels.
- **Flat depth.** No drop shadows. Depth comes from surface alternation (canvas → panel → nested), hairlines, and full-width brand bands.
- **Rounded, not cute.** Cards at 16px; signature media/callouts at 22px; pills fully round.
- **Mono labels as system markers.** Uppercase mono eyebrows tag sections, statuses, and categories — the research-lab cadence.

---

## Colors

All colors are CSS custom properties. Use the variable, never a raw hex, in component CSS.

### Surfaces

| Token | Value | Use |
|---|---|---|
| `--bg` | `#0a0b0d` | Page canvas (near-black, slightly warm). |
| `--panel` | `#15161b` | Default card / panel surface. |
| `--panel-2` | `#1c1d24` | Nested cards, code/tree blocks, table zebra. |
| `--mock-bg` | `#06080a` | Terminal / console mock background (darkest). |
| `--band-green` | `#003c33` | Deep enterprise green brand band (emphasis / CTA section). |
| `--band-navy` | `#071829` | Dark navy brand band (alternate emphasis). |

### Ink & rules

| Token | Value | Use |
|---|---|---|
| `--ink` | `#f3f4f6` | Primary text, headlines. |
| `--ink-2` | `#cdd2da` | Secondary body text on dark cards. |
| `--muted` | `#93939f` | Cohere Muted Slate — metadata, captions, eyebrows, de-emphasized labels. |
| `--line` | `#2a2b33` | Hairline borders and dividers. |
| `--chip` | `#1f2129` | Inline `code` and numbered-chip backgrounds. |

### Accents (use sparingly)

| Token | Value | Use |
|---|---|---|
| `--coral` | `#ff7759` | Primary accent: taxonomy/eyebrows, attention, "critical/must", removed. |
| `--coral-soft` | `#ffad9b` | Pale coral for chip borders / subtle marks. |
| `--blue` | `#4c6ee6` | Links, secondary emphasis, "info/next". |

### Status (standardized — use these names everywhere)

The old briefs renamed the same hexes per file (hot/cold/test vs done/todo/next vs p1/p2/p3). **Stop doing that.** One scheme:

| Token | Value | Means |
|---|---|---|
| `--ok` | `#3ecf8e` | shipped · done · success · "now" |
| `--warn` | `#e0a52e` | planned · todo · caution · "later" |
| `--info` | `#4c6ee6` | neutral highlight · next · informational (same as `--blue`) |
| `--crit` | `#ff7759` | must · critical · removed · rejected (same as `--coral`) |

Status tints follow one rule: **text = the status color; background = that color at 14% alpha; border (if any) = 28% alpha.** e.g. `--ok` chip → `color:var(--ok); background:rgba(62,207,142,.14)`.

### Gradients

Not a generic UI fill. Reserve subtle tints for `.callout` (a faint blue or coral vertical wash) and brand bands. Keep all other surfaces flat.

---

## Typography

Cohere's proprietary fonts (CohereText / Unica77 / CohereMono) are **not bundled**. Default to self-contained system fallbacks; the tight tracking below recreates the cadence. See [Known gaps](#known-gaps) for the optional web-font opt-in.

### Font stacks

```css
--font-display: 'Space Grotesk', 'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
--font-body:    'Inter', ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
--font-mono:    'SF Mono', ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, monospace;
```

### Hierarchy

| Role | Font | Size | Weight | Line height | Tracking | Notes |
|---|---|---:|---:|---:|---:|---|
| Brief title (`h1`) | display | 34px | 500 | 1.05 | -0.6px | One per brief. Compact and carved, not airy. |
| Section heading (`h2`) | display | 22px | 500 | 1.15 | -0.3px | Optional; pair with an eyebrow above. |
| Eyebrow (`.eyebrow`) | mono | 12px | 600 | 1.2 | 1.2px | UPPERCASE. Section/system marker. `--muted` or `--coral`. |
| Card heading (`h3`) | display | 16px | 600 | 1.25 | -0.1px | Card / list-item titles. |
| Subhead (`h4`) | body | 14px | 600 | 1.3 | 0 | Inside cards. |
| Body | body | 15px | 400 | 1.6 | 0 | Default copy. `--ink-2` on cards. |
| Small / caption | body | 13px | 400 | 1.5 | 0 | Metadata, descriptions. `--muted`. |
| Mono label (`.lbl`) | mono | 11px | 700 | 1.3 | 0.5px | UPPERCASE component labels. |
| Code | mono | 12.5px | 400 | — | 0 | Inline `code`, `--chip` bg. |

### Principles

- **One hero headline.** Don't stack giant type; after the title, drop to 15–22px.
- **Keep display tight.** Negative tracking on anything 22px+.
- **Avoid heavy bold.** Size, spacing, and surface contrast do the hierarchy work; 500–600 is plenty.
- **Mono = system marker.** Use uppercase mono for eyebrows, statuses, and category chips, not for prose.

---

## Layout

### Container

```css
.wrap { max-width: 1000px; margin: 0 auto; padding: 48px 24px 96px; }
```

Always 1000px (the old files drifted to 1040 — standardize on 1000).

### Spacing scale

8px base: `4, 8, 12, 16, 20, 24, 32, 40, 56, 80`. Sections breathe — `40px+` between major sections, generous empty space around the title and any brand band. Dense content (tables, decision lists) is fine where it serves scanning.

### Grids

- `.cols-2` → `repeat(2,1fr)`, `.cols-3` → `repeat(3,1fr)`, gap 14px.
- Comparison pairs use `.pair` (1fr 1fr).
- All collapse to one column at the single breakpoint (760px).

---

## Elevation & depth

Flat. No shadows.

| Level | Treatment | Use |
|---|---|---|
| Canvas | `--bg`, no border | Page background, section gaps. |
| Panel | `--panel` + 1px `--line`, radius 16 | Cards, the default container. |
| Nested | `--panel-2` + 1px `--line` | Cards inside cards, code/tree, mock chrome. |
| Brand band | full-width `--band-green` / `--band-navy` | One emphasis or closing section. |

---

## Shapes

Cohere radii:

| Token | Value | Role |
|---|---:|---|
| `--r-xs` | 6px | Inline code, tiny chips. |
| `--r-sm` | 8px | Numbered chips, small media. |
| `--r-md` | 16px | Cards, panels, tables (the workhorse). |
| `--r-lg` | 22px | Signature callouts / hero media. |
| `--r-pill` | 999px | Status pills, badges, CTA buttons. |

Don't drop major cards below 8px; don't round status pills to anything but full.

---

## Components

Each is a class in the starter CSS. Build briefs by composing these — don't hand-roll one-offs.

### `header` — brief title block
`h1` title + `.sub` (one-line summary, `--muted`, 15px) + optional `.meta` row (date · tag · status chips). Lots of space below.

### `eyebrow` — section marker
Uppercase mono label above a section or `h2`. `--coral` for the lead section, `--muted` elsewhere.

### `callout` — highlighted note
The one place a subtle gradient lives. Faint blue wash, 1px blue border at 35%, radius 22. Use for the thesis / the one line that matters. `<b>` inside goes `--ink`.

### `card` — base content block
`--panel`, 1px `--line`, radius 16, padding 18–20. Holds an `h3` + body, or any composition. The default unit.

Two utilities compose with it (don't make a separate "item" component — use these):
- **`.card-head`** — a title row that sits an `h3` next to status `badge`s.
- **`.card-meta`** — a muted one-line footer (`<b>` reads `--ink-2`).

`.card` + `.card-head` + `.card-meta` is the standard shape for any **titled item with tags and a note** — a feature, an option, a risk. Reach for it instead of inventing a one-off card.

### `grid` — `.cols-2` / `.cols-3`
Responsive card grids. Collapse to one column on mobile.

### `badge` / status pills
Pill, uppercase 11px bold, status-tinted (text = status color, bg = 14% alpha). Modifiers: `.is-shipped` (`--ok`), `.is-planned` (`--warn`), `.is-info` (`--info`), `.is-crit` (`--crit`). Use for shipped/planned tagging.

### `compare` — side-by-side
`.pair` grid → two `.side` panels. `.side.a` (the "before"/other, warm/coral tint at ~7%) vs `.side.b` (the "after"/ours, green tint at ~7%), each with a `.lbl` mono label up top. The core "X vs Y" device.

### `table` — comparison table
Full width, hairline rows, `th` uppercase 11px `--muted`. Left-align, top-valign. Use `td.a` / `td.b` to color the two compared columns (`--muted`-warm vs `--ok`).

### `decisions` — numbered list
Each row: a `.num` chip (`--chip` bg, `--coral` digit, radius 8) + title + `--muted` rationale. For locked decisions / ADR-style lists.

### `steps` / `flow`
`ol.steps` — counter chips down the left for a sequence. `.flow` — horizontal row of `.step` cards (each with a mono `.k` label) for a pipeline.

### `mock` — terminal / console
`--mock-bg`, mono, `white-space:pre-wrap`, radius 16. Colored spans: `.u` user input (`--ink`), `.s` system (`--muted`), `.a` agent (`--ok`), `.d` domain/path (`--blue`). For "what it feels like" moments. Keep it honest — no invented data.

### `band` — brand emphasis section
Full-bleed `--band-green` (or `--band-navy`) block, light text, for one thesis or the closing CTA. Use at most once or twice.

### `reject` / `note`
`--panel-2` box for "what we say no to" or asides. `<b>` goes `--ink`.

### `legend`
Inline key: `.dot` (9px round, status color) + label. Explains the status colors when a brief leans on them.

### `tag` chips
Coral-outline taxonomy chips (Cohere blog-filter style): transparent fill, `--coral-soft` border, `--coral` text, radius 30. For category/topic tagging.

### links & buttons
Links: `--blue`, underlined on hover. `.btn` (rare in briefs): near-white pill on dark, or `--coral` for the single primary CTA in a band.

---

## Do's & Don'ts

### Do
- Keep the canvas dark and flat; let panels and one brand band carry structure.
- Use one large, tight headline; settle into 15px body immediately after.
- Use uppercase mono eyebrows to mark sections and statuses.
- Use coral and blue in small doses — labels, links, one accent per area.
- Use 16px on cards, 22px on the signature callout, full-round on pills.
- Standardize status colors via `--ok/--warn/--info/--crit` and show a `legend` when used.

### Don't
- Don't turn coral, blue, green, or navy into broad decorative surface fills (bands excepted).
- Don't add drop shadows.
- Don't box everything — open rows, hairlines, and space are often enough.
- Don't stack multiple giant headlines or use heavy bold for hierarchy.
- Don't rename the status tokens per brief (the old hot/cold/test drift).
- Don't invent colors or radii outside this doc.

---

## Responsive

One breakpoint. Mobile-friendly because briefs are often reviewed on a phone.

```css
@media (max-width: 760px) {
  .wrap { padding: 32px 16px 64px; }
  .cols-2, .cols-3, .pair { grid-template-columns: 1fr; }
  h1 { font-size: 28px; }
}
```

---

## Iteration guide

1. Start from the [Starter skeleton](#starter-skeleton) — it carries the full token set and base CSS.
2. Open with `header` (title + one-line `.sub` + `.meta`). Follow with the thesis in a `callout`.
3. Pick components by intent: comparison → `compare` + `table`; decisions → `decisions`; a flow → `flow`/`steps`; a feel → `mock`; a thesis/close → `band`.
4. Tag anything shipped-vs-planned with status `badge`s; add a `legend` if you lean on status colors.
5. Keep it honest: placeholder frames over invented product data; mark `[DRAFT]`/`(planned)` where real.
6. End with forward momentum (a CTA `band` or a "what's next" card), not a summary.

---

## Known gaps

- **Proprietary fonts not bundled.** Cohere's CohereText/Unica77/CohereMono aren't available; we fall back to Space Grotesk / Inter / system mono. For sharper fidelity (and when strict offline self-containment isn't required), opt into web fonts by adding this to `<head>` — it degrades gracefully if blocked:
  ```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
  ```
  Default (no link) stays fully self-contained.
- **Dark-only.** This doc covers dark-mode. A light variant can be added later as a second theme.

---

## Starter skeleton

Copy this, set `<title>`, and fill `<!-- content -->`. The `<style>` block is the complete house system — inline, no external runtime deps.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BRIEF TITLE</title>
<style>
  :root{
    --bg:#0a0b0d; --panel:#15161b; --panel-2:#1c1d24; --mock-bg:#06080a;
    --band-green:#003c33; --band-navy:#071829;
    --ink:#f3f4f6; --ink-2:#cdd2da; --muted:#93939f; --line:#2a2b33; --chip:#1f2129;
    --coral:#ff7759; --coral-soft:#ffad9b; --blue:#4c6ee6;
    --ok:#3ecf8e; --warn:#e0a52e; --info:#4c6ee6; --crit:#ff7759;
    --font-display:'Space Grotesk','Inter',ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,sans-serif;
    --font-body:'Inter',ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
    --font-mono:'SF Mono',ui-monospace,SFMono-Regular,'JetBrains Mono',Menlo,Consolas,monospace;
    --r-xs:6px; --r-sm:8px; --r-md:16px; --r-lg:22px; --r-pill:999px;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 var(--font-body);-webkit-font-smoothing:antialiased}
  .wrap{max-width:1000px;margin:0 auto;padding:48px 24px 96px}

  h1{font:500 34px/1.05 var(--font-display);letter-spacing:-.6px;margin:0 0 8px}
  h2{font:500 22px/1.15 var(--font-display);letter-spacing:-.3px;margin:0 0 12px}
  h3{font:600 16px/1.25 var(--font-display);letter-spacing:-.1px;margin:0 0 6px}
  h4{font:600 14px/1.3 var(--font-body);margin:0 0 4px}
  p{margin:0 0 12px;color:var(--ink-2)}
  a{color:var(--blue);text-decoration:none}
  a:hover{text-decoration:underline}
  code{font:400 12.5px var(--font-mono);background:var(--chip);padding:1px 6px;border-radius:var(--r-xs);color:var(--ink)}

  .sub{color:var(--muted);font-size:15px;margin:0 0 14px}
  .meta{display:flex;gap:14px;flex-wrap:wrap;align-items:center;color:var(--muted);font-size:13px;margin-bottom:8px}
  .eyebrow{font:600 12px/1.2 var(--font-mono);text-transform:uppercase;letter-spacing:1.2px;color:var(--muted);margin:40px 0 12px}
  .eyebrow.lead{color:var(--coral)}
  .lbl{font:700 11px/1.3 var(--font-mono);text-transform:uppercase;letter-spacing:.5px}

  section{margin-top:8px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:var(--r-md);padding:18px 20px;margin-bottom:14px}
  .card.nested{background:var(--panel-2)}
  .card-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px}
  .card-head h3{margin:0}
  .card-meta{margin-top:10px;font-size:12.5px;color:var(--muted)}
  .card-meta b{color:var(--ink-2);font-weight:600}
  .grid{display:grid;gap:14px}
  .cols-2{grid-template-columns:repeat(2,1fr)}
  .cols-3{grid-template-columns:repeat(3,1fr)}

  .callout{background:linear-gradient(180deg,rgba(76,110,230,.12),rgba(76,110,230,.03));border:1px solid rgba(76,110,230,.35);border-radius:var(--r-lg);padding:18px 22px;margin:8px 0 18px}
  .callout b{color:var(--ink)}

  .badge{display:inline-block;font:700 11px/1 var(--font-mono);text-transform:uppercase;letter-spacing:.5px;padding:4px 10px;border-radius:var(--r-pill)}
  .is-shipped{color:var(--ok);background:rgba(62,207,142,.14)}
  .is-planned{color:var(--warn);background:rgba(224,165,46,.14)}
  .is-info{color:var(--info);background:rgba(76,110,230,.14)}
  .is-crit{color:var(--crit);background:rgba(255,119,89,.14)}

  .pair{display:grid;grid-template-columns:1fr 1fr;gap:14px}
  .side{border-radius:var(--r-md);padding:14px 16px;font-size:14px}
  .side.a{background:rgba(255,119,89,.07);border:1px solid rgba(255,119,89,.25)}
  .side.b{background:rgba(62,207,142,.07);border:1px solid rgba(62,207,142,.25)}
  .side .lbl{margin-bottom:6px}
  .side.a .lbl{color:var(--coral)}
  .side.b .lbl{color:var(--ok)}

  table{width:100%;border-collapse:collapse;font-size:13.5px;margin:4px 0}
  th,td{text-align:left;vertical-align:top;padding:9px 12px;border-bottom:1px solid var(--line)}
  th{color:var(--muted);font:700 11px/1.3 var(--font-mono);text-transform:uppercase;letter-spacing:.6px}
  td.a{color:var(--muted)} td.b{color:var(--ok)}

  .decisions{margin:4px 0}
  .dec{display:flex;gap:14px;align-items:flex-start;padding:13px 0;border-bottom:1px solid var(--line)}
  .dec:last-child{border-bottom:0}
  .num{flex:0 0 30px;height:30px;border-radius:var(--r-sm);background:var(--chip);color:var(--coral);display:flex;align-items:center;justify-content:center;font:700 13px var(--font-mono)}
  .dec .body{flex:1}
  .dec p{margin:4px 0 0;color:var(--muted);font-size:13px}

  ol.steps{counter-reset:s;list-style:none;margin:0;padding:0}
  ol.steps li{counter-increment:s;position:relative;padding:10px 0 10px 36px;border-bottom:1px solid var(--line);font-size:14px}
  ol.steps li:last-child{border-bottom:0}
  ol.steps li::before{content:counter(s);position:absolute;left:0;top:8px;width:24px;height:24px;border-radius:var(--r-sm);background:var(--chip);color:var(--coral);font:700 12px var(--font-mono);display:flex;align-items:center;justify-content:center}

  .flow{display:flex;gap:12px;flex-wrap:wrap}
  .flow .step{flex:1;min-width:150px;background:var(--panel);border:1px solid var(--line);border-radius:var(--r-md);padding:12px 14px}
  .flow .step .k{font:700 11px var(--font-mono);text-transform:uppercase;letter-spacing:.6px;color:var(--coral)}
  .flow .step p{margin:6px 0 0;font-size:13px;color:var(--muted)}

  .mock{background:var(--mock-bg);border:1px solid var(--line);border-radius:var(--r-md);padding:18px 20px;font:12.5px/1.7 var(--font-mono);white-space:pre-wrap;color:var(--ink-2);overflow-x:auto}
  .mock .u{color:var(--ink)} .mock .s{color:var(--muted)} .mock .a{color:var(--ok)} .mock .d{color:var(--blue)}

  .band{background:var(--band-green);border-radius:var(--r-lg);padding:28px 28px;margin:24px 0;color:#eafff6}
  .band.navy{background:var(--band-navy);color:#e7f0fb}
  .band h2,.band h3{color:#fff}

  .reject{background:var(--panel-2);border:1px solid var(--line);border-radius:var(--r-sm);padding:12px 16px;margin-bottom:8px;font-size:13.5px}
  .reject b{color:var(--ink)}

  .legend{display:flex;gap:18px;flex-wrap:wrap;margin-top:10px;font-size:12px;color:var(--muted)}
  .legend .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:middle}

  .tag{display:inline-block;font:600 12px var(--font-body);color:var(--coral);border:1px solid var(--coral-soft);border-radius:var(--r-pill);padding:3px 12px;margin:0 4px 4px 0}

  .btn{display:inline-block;font:600 14px var(--font-body);padding:10px 22px;border-radius:var(--r-pill);background:#f3f4f6;color:#0a0b0d}
  .btn.coral{background:var(--coral);color:#1a0d08}

  @media (max-width:760px){
    .wrap{padding:32px 16px 64px}
    .cols-2,.cols-3,.pair{grid-template-columns:1fr}
    h1{font-size:28px}
  }
</style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="meta"><span>2026-05-24</span> · <span class="badge is-shipped">shipped</span></div>
      <h1>Brief title</h1>
      <p class="sub">One-line summary of what this brief argues, in plain language.</p>
    </header>

    <div class="callout"><b>The thesis:</b> the single sentence the reader should leave with.</div>

    <!-- content: compose from Components above -->

  </div>
</body>
</html>
```
