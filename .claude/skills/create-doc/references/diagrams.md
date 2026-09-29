# Diagrams — inline recipes

Self-contained diagram archetypes for briefs. Each is **inline SVG or styled HTML** — zero dependencies. Pick by intent, copy the block, swap the content. Colors below use the Blueprint palette; **swap fills/strokes to your theme's tokens** (e.g. light themes: `#0a57d0` accent, `#f6f8fb` node fill, `#dde2e8` line). Keep one `<marker>` per arrow color.

For diagrams as standalone editable files (not embedded in a brief), use `create-diagram` instead. These are for *inside* a brief.

| Recipe | Use when |
|---|---|
| D1 Pipeline | an ordered sequence of stages |
| D2 Sequence | who-talks-to-whom over time |
| D3 Layers | stacked planes + what crosses between |
| D4 State machine | a lifecycle with terminal/branch states |
| D5 Capability matrix | entities × attributes, pass/partial/fail (HTML) |
| D6 Timeline | durations on a time axis |
| D7 Lean UML | a data model / type relationship |

---

## D1 · Pipeline / flow
```html
<svg viewBox="0 0 720 96" role="img" aria-label="pipeline">
  <defs><marker id="ar1" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#4dd0e1"/></marker></defs>
  <g font-size="13" fill="#dcefff" text-anchor="middle">
    <rect x="6" y="30" width="120" height="40" rx="6" fill="#0e2438" stroke="#16395a"/><text x="66" y="55">specify</text>
    <rect x="160" y="30" width="120" height="40" rx="6" fill="#0e2438" stroke="#16395a"/><text x="220" y="55">plan</text>
    <rect x="314" y="30" width="120" height="40" rx="6" fill="#0e2438" stroke="#16395a"/><text x="374" y="55">tasks</text>
    <rect x="468" y="30" width="120" height="40" rx="6" fill="#0e2438" stroke="#4dd0e1"/><text x="528" y="55">implement</text>
  </g>
  <g stroke="#4dd0e1" stroke-width="1.5" marker-end="url(#ar1)" fill="none">
    <line x1="128" y1="50" x2="156" y2="50"/><line x1="282" y1="50" x2="310" y2="50"/><line x1="436" y1="50" x2="464" y2="50"/><line x1="590" y1="50" x2="628" y2="50"/>
  </g>
  <circle cx="666" cy="50" r="22" fill="rgba(90,209,168,.12)" stroke="#5ad1a8"/><text x="666" y="54" font-size="11" fill="#5ad1a8" text-anchor="middle">done</text>
</svg>
```

## D2 · Sequence round-trip
Vertical lifelines + arrows over time; use a dashed box to mark a "blind"/gap region. (Full block in `2026-06-11-brief-diagram-and-section-sampler.html`, fig D2.) Skeleton:
```html
<svg viewBox="0 0 720 250">
  <defs><marker id="ar2" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#aecbe8"/></marker></defs>
  <!-- lane headers + dashed lifelines at x=80,270,460,640 -->
  <!-- solid arrows = calls; dashed return arrow = the only signal back -->
  <!-- a dashed rect with crit stroke marks a no-response / blind region -->
</svg>
```

## D3 · Layered architecture
```html
<svg viewBox="0 0 720 196">
  <defs><marker id="ar3" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#7193b3"/></marker></defs>
  <rect x="6" y="10" width="560" height="48" rx="8" fill="#0e2438" stroke="#16395a"/>
  <text x="26" y="32" font-size="13" fill="#dcefff">Layer A</text><text x="26" y="49" font-size="11" fill="#7193b3">sub-parts…</text>
  <rect x="6" y="74" width="560" height="48" rx="8" fill="#0e2438" stroke="#4dd0e1"/><text x="26" y="96" font-size="13" fill="#dcefff">Layer B</text>
  <rect x="6" y="138" width="560" height="48" rx="8" fill="#0e2438" stroke="#16395a"/><text x="26" y="160" font-size="13" fill="#dcefff">Layer C</text>
  <g stroke="#7193b3" stroke-width="1.3" fill="none" marker-end="url(#ar3)"><line x1="600" y1="60" x2="600" y2="134"/><line x1="660" y1="134" x2="660" y2="60"/></g>
  <text x="612" y="100" font-size="10.5" fill="#7193b3" transform="rotate(90 612 100)">down ↓</text>
  <text x="672" y="100" font-size="10.5" fill="#5ad1a8" transform="rotate(90 672 100)">up ↑</text>
</svg>
```

## D4 · State machine
```html
<svg viewBox="0 0 720 150">
  <defs><marker id="ar4" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#4dd0e1"/></marker></defs>
  <g font-size="11.5" text-anchor="middle">
    <rect x="6" y="44" width="92" height="34" rx="17" fill="#0e2438" stroke="#16395a"/><text x="52" y="65" fill="#aecbe8">state A</text>
    <rect x="150" y="44" width="84" height="34" rx="17" fill="#0e2438" stroke="#16395a"/><text x="192" y="65" fill="#aecbe8">state B</text>
    <rect x="618" y="44" width="96" height="34" rx="17" fill="rgba(90,209,168,.12)" stroke="#5ad1a8"/><text x="666" y="65" fill="#5ad1a8">terminal</text>
    <rect x="560" y="108" width="92" height="32" rx="16" fill="rgba(113,147,179,.1)" stroke="#7193b3"/><text x="606" y="128" fill="#7193b3">branch</text>
  </g>
  <g stroke="#4dd0e1" stroke-width="1.4" fill="none" marker-end="url(#ar4)"><line x1="98" y1="61" x2="146" y2="61"/></g>
  <line x1="666" y1="78" x2="640" y2="106" stroke="#7193b3" stroke-dasharray="4 3" fill="none" marker-end="url(#ar4)"/>
</svg>
```

## D5 · Capability matrix (HTML, not SVG)
Entities × attributes with colored pass/partial/fail cells. Needs these classes (swap to theme): `.c-ok{color/bg/border green}`, `.c-mid{amber}`, `.c-no{red}`, `td.rl{left label}`.
```html
<table class="matrix">
  <tr><th class="row">Entity</th><th>Attr 1</th><th>Attr 2</th><th>Attr 3</th></tr>
  <tr><td class="rl">Row A</td><td class="c-ok">yes</td><td class="c-mid">partial</td><td class="c-no">no</td></tr>
</table>
<div class="legend"><span><span class="dot c-ok"></span>full</span><span><span class="dot c-mid"></span>partial</span><span><span class="dot c-no"></span>none</span></div>
```
```css
table.matrix{width:100%;border-collapse:separate;border-spacing:4px;font:12px var(--fb)}
table.matrix th{color:var(--muted);font:700 9.5px var(--fm);text-transform:uppercase;padding:4px 6px;text-align:center}
table.matrix th.row{text-align:left;color:var(--accent)}
table.matrix td{text-align:center;padding:8px 6px;border-radius:5px;font:700 10px var(--fm)}
table.matrix td.rl{text-align:left;font:600 11.5px var(--fb)}
/* light-theme tints */
.c-ok{color:#1a7f4b;background:#e6f5ec;border:1px solid #b6e0c7}
.c-mid{color:#9a6700;background:#fbf1da;border:1px solid #ecd9a6}
.c-no{color:#c0392b;background:#fdecea;border:1px solid #e3a39b}
.legend .dot{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:middle}
```

## D6 · Timeline / gantt
```html
<svg viewBox="0 0 720 150">
  <line x1="90" y1="128" x2="700" y2="128" stroke="#16395a"/>
  <g font-size="11" fill="#7193b3"><text x="6" y="32">row A</text><text x="6" y="62">row B</text></g>
  <rect x="90" y="20" width="120" height="18" rx="4" fill="rgba(77,208,225,.25)" stroke="#4dd0e1"/>
  <rect x="210" y="50" width="150" height="18" rx="4" fill="rgba(77,208,225,.25)" stroke="#4dd0e1"/>
  <!-- per-item ticks as short vertical lines inside the last bar -->
  <g stroke="#5ad1a8" stroke-width="2"><line x1="470" y1="108" x2="470" y2="126"/></g>
</svg>
```

## D7 · Lean UML — class / data shape
Two boxes (3-compartment header + attributes), one relationship. **Lean rule: name + attributes + one relationship, no method noise.** Composition = filled diamond at the owner end.
```html
<svg viewBox="0 0 720 224">
  <defs><marker id="amul" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#4dd0e1"/></marker></defs>
  <rect x="20" y="34" width="234" height="156" rx="6" fill="#0e2438" stroke="#4dd0e1"/>
  <rect x="20" y="34" width="234" height="30" rx="6" fill="rgba(77,208,225,.12)" stroke="#4dd0e1"/>
  <text x="137" y="54" font-size="13" fill="#dcefff" text-anchor="middle" font-weight="600">ClassA</text>
  <line x1="20" y1="64" x2="254" y2="64" stroke="#16395a"/>
  <g font-size="12" fill="#aecbe8" font-family="monospace"><text x="34" y="86">field: Type</text></g>
  <rect x="466" y="34" width="234" height="156" rx="6" fill="#0e2438" stroke="#16395a"/>
  <rect x="466" y="34" width="234" height="30" rx="6" fill="rgba(113,147,179,.1)" stroke="#16395a"/>
  <text x="583" y="54" font-size="13" fill="#dcefff" text-anchor="middle" font-weight="600">ClassB</text>
  <line x1="466" y1="64" x2="700" y2="64" stroke="#16395a"/>
  <!-- composition diamond + line -->
  <path d="M254,112 L286,100 L318,112 L286,124 Z" fill="#4dd0e1"/>
  <line x1="318" y1="112" x2="462" y2="112" stroke="#4dd0e1" stroke-width="1.4" marker-end="url(#amul)"/>
  <text x="332" y="105" font-size="11" fill="#7193b3" font-family="monospace">1</text>
  <text x="440" y="105" font-size="11" fill="#7193b3" font-family="monospace" text-anchor="end">1..*</text>
</svg>
```

Full validated versions of D1–D7 live in `Projects/speckit companion/briefs/2026-06-11-brief-diagram-and-section-sampler.html` and `…-terminal-code-uml-addendum.html` — copy from there if a skeleton above is too terse.
