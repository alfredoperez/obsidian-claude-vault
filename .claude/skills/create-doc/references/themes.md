# Themes — the reading registry

Named themes for HTML briefs, curated for **reading and comprehension**, not decoration. Pick one per brief by the job it does. **Default: Hyperlegible.**

Each theme is a token set the [`design.md`](./design.md) skeleton consumes. The fastest reliable path: **copy the full `<style>` block from the canonical example brief listed for your theme, then swap the content** — don't re-derive component colors. The `:root` blocks below are the source of truth for each palette.

> Describe type by **category** (humanist sans, transitional serif, grotesque, mono), never by font name, in any prose you write. Render real fonts via a Google Fonts `<link>` only when fidelity matters; otherwise the system fallbacks in each stack keep the brief self-contained.

| Theme | Mode | Type | Use when |
|---|---|---|---|
| **Hyperlegible** (default) | light | hyperlegible humanist sans, larger base | the default — anything read end-to-end, shared, or printed; accessibility-first |
| **Slate** | soft dark | humanist sans | low-fatigue dark-mode long reads; UI-ish content at night |
| Paper | light | transitional serif | long-form narrative reasoning; print |
| Dark Editorial | warm dark | transitional serif on dark | narrative / decision briefs read at night |
| Blueprint | dark | grotesque + mono, cyan grid | technical / architecture; scanning structure, diagrams, capability tables |
| Manuscript | sepia | old-style serif | cozy extended reading, low blue light |
| Notebook | light | humanist sans + mono, grid | technical content in light mode (Blueprint's light twin) |

Canonical full-style examples to copy from (in the vault, `Projects/speckit companion/briefs/`):
- **Hyperlegible** → `2026-06-11-pluggable-hook-bus-and-auto-mode.html`
- **Blueprint** → `2026-06-11-capability-tiered-architecture-auto-mode-config-website.html`
- **All seven side by side** → `2026-06-11-seven-reading-themes.html` (the per-theme `--t*` token blocks)

---

## Hyperlegible (default) — light, accessibility-first

Larger base (16.5px), near-black ink on white, one strong accessible blue. Body + headings in a hyperlegible humanist sans. Status colors are darkened for AA contrast on white.

```css
:root{
  --bg:#ffffff; --panel:#f6f8fb; --panel-2:#eef2f7; --mock:#f4f6f9;
  --ink:#1f2428; --ink-2:#3c444c; --strong:#0a0d10; --muted:#69727c; --line:#dde2e8; --line-2:#cfd6de;
  --acc:#0a57d0; --note:#eaf1fd; --note-bd:#bcd5f5;
  --ok:#1a7f4b; --warn:#9a6700; --crit:#c0392b; --info:#0a57d0;
  --fb:'Atkinson Hyperlegible',ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
  --fm:'JetBrains Mono',ui-monospace,'SF Mono',Menlo,monospace;
  --r:6px; --r-lg:11px;
}
body{font:16.5px/1.62 var(--fb)}  /* larger base — part of the legibility */
```
Light-theme component notes: badges/callouts use **pale tints** (`background` ~ status color at very low alpha, `border` a light tint, `color` the darkened status); no dotted grid (keep it clean for reading); `compare` sides use `#fdf2f0`/`#eef7f1`. Copy them from the canonical Hyperlegible example.

## Slate — soft dark (the dark companion)

Off-white ink (never pure white) on slate (never black) to kill halation.

```css
:root{
  --bg:#1b2027; --panel:#222a33; --panel-2:#1f262e; --line:#2c333d;
  --ink:#c2cad3; --ink-2:#aeb8c2; --strong:#e9eef3; --muted:#8a96a3;
  --accent:#7fb3d5; --ok:#5ad1a8; --warn:#ffd277; --crit:#ff8a80; --info:#7fb3d5;
  --fb:'Inter',ui-sans-serif,system-ui,sans-serif; --fm:'JetBrains Mono',ui-monospace,monospace;
}
```

## Paper — light editorial serif

```css
:root{
  --bg:#f7f4ee; --panel:#efe8da; --ink:#403b33; --strong:#1c1a16; --muted:#8a8270; --line:#ddd5c4;
  --accent:#a8512c; --note:#efe8da;
  --fb:'Newsreader',Georgia,'Times New Roman',serif; --fh:var(--fb);
  --flabel:'Inter',ui-sans-serif,system-ui,sans-serif; --fm:'JetBrains Mono',monospace;
}
body{font-size:16.5px}
```

## Dark Editorial — serif on warm dark

```css
:root{
  --bg:#14110e; --panel:#1c1813; --ink:#cec5ba; --strong:#f2ece3; --muted:#8c8174; --line:#312a23;
  --accent:#d99a5b; --note:rgba(217,154,91,.1);
  --fb:'Newsreader',Georgia,serif; --flabel:'Inter',system-ui,sans-serif; --fm:'JetBrains Mono',monospace;
}
body{font-size:16.5px}
```

## Blueprint — dark navy, cyan grid, mono labels (technical)

```css
:root{
  --bg:#0a1929; --panel:#0e2438; --panel-2:#0c1d30; --mock-bg:#06121f;
  --ink:#dcefff; --ink-2:#aecbe8; --muted:#7193b3; --line:#16395a; --grid:rgba(77,208,225,.04);
  --accent:#4dd0e1; --accent-2:#5b9dff; --ok:#5ad1a8; --warn:#ffd277; --del:#ff8a80; --chip:#0e2740;
  --fh:'Space Grotesk','Inter',ui-sans-serif,system-ui,sans-serif;
  --fb:'Inter',ui-sans-serif,system-ui,sans-serif; --fm:ui-monospace,'JetBrains Mono',Menlo,monospace;
}
/* body gets the faint engineering grid */
body{background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:30px 30px}
/* eyebrows prefixed //  and ★ ; callouts/tables use dashed borders */
```

## Manuscript — sepia, old-style serif

```css
:root{
  --bg:#f3e8d0; --panel:#ebdebf; --ink:#4a4030; --strong:#2a2316; --muted:#8a7c5e; --line:#ddccab;
  --accent:#8a5a2b; --note:#ebdebf;
  --fb:'Lora',Georgia,serif; --flabel:'Inter',system-ui,sans-serif; --fm:'JetBrains Mono',monospace;
}
body{font-size:16px}
```

## Notebook — light technical, sans + mono, grid

```css
:root{
  --bg:#fbfbf8; --panel:#f1f4f5; --ink:#36424c; --strong:#14202a; --muted:#73808b; --line:#dde2e5;
  --accent:#1f6f8b; --note:#eef4f5;
  --fb:'Inter',ui-sans-serif,system-ui,sans-serif; --flabel:'JetBrains Mono',monospace; --fm:'JetBrains Mono',monospace;
}
body{background-image:linear-gradient(rgba(31,111,139,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(31,111,139,.05) 1px,transparent 1px);background-size:24px 24px}
```

---

**Google Fonts link** (only when you want exact rendering; degrades to system fallbacks if blocked):
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Inter:wght@400;500;600;700&family=Newsreader:opsz,wght@6..72,400;6..72,600&family=Lora:wght@400;600&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
```
