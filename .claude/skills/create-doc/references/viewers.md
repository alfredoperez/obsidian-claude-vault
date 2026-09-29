# Viewers — terminal & code

Two "window" recipes for showing a command session or a source excerpt inside a brief. Self-contained, hand-highlighted (no `highlight.js`). Use these instead of the plain `mock` block when the content should *look* like a terminal or an editor. Swap colors to the theme palette (blocks below use Blueprint hexes; light themes use `--mock:#f4f6f9` with dark ink).

---

## Terminal window
Use for: a real command session — install flows, a pipeline run, "what you'd see."

Span classes: `.p` prompt · `.cmd` command · `.ok` success · `.ar` arrow/step · `.pa` path · `.o` output · `.er` error.

```html
<div class="term">
  <div class="bar"><i style="background:#ff8a80"></i><i style="background:#ffd277"></i><i style="background:#5ad1a8"></i><span class="t">claude — zsh — project</span></div>
  <div class="body"><span class="p">$</span> <span class="cmd">specify extension add companion --dev</span>
<span class="ok">✓</span> <span class="o">registered 4 lifecycle hooks</span>
<span class="ar">→</span> T001 done · <span class="pa">src/handler.ts</span>
<span class="er">✗</span> <span class="o">1 check failed</span></div>
</div>
```
```css
.term{background:var(--mock,#06121f);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.term .bar{display:flex;align-items:center;gap:7px;padding:9px 13px;background:var(--panel-2);border-bottom:1px solid var(--line)}
.term .bar i{width:11px;height:11px;border-radius:50%;display:inline-block}
.term .bar .t{margin-left:9px;font:11px var(--fm);color:var(--muted)}
.term .body{padding:14px 16px;font:12.5px/1.75 var(--fm);white-space:pre-wrap;color:var(--ink-2)}
.term .p{color:var(--accent)} .term .cmd{color:var(--strong,var(--ink))} .term .ok{color:var(--ok)}
.term .ar{color:var(--accent)} .term .pa{color:var(--accent-2,var(--accent))} .term .o{color:var(--muted)} .term .er{color:var(--crit,#ff8a80)}
```

---

## Code viewer
Use for: a focused source excerpt with a filename + line numbers — the mechanism, not a whole file. Highlight only what aids reading.

Span classes: `.kw` keyword · `.fn` function · `.str` string · `.com` comment · `.num` number · `.key` (yaml/json key).

```html
<div class="code">
  <div class="tabs"><span class="tab on">write-context.py</span><span class="tab">other.py</span></div>
  <div class="src">
    <pre class="ln">31
32
33</pre>
    <pre class="lines"><span class="kw">def</span> <span class="fn">journal_task_finish</span>(ctx, task):
    <span class="com"># finish-only: one event per task</span>
    <span class="kw">return</span> <span class="fn">write_atomic</span>(ctx)</pre>
  </div>
</div>
```
```css
.code{background:var(--mock,#06121f);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.code .tabs{display:flex;background:var(--panel-2);border-bottom:1px solid var(--line)}
.code .tab{padding:8px 15px;font:11px var(--fm);color:var(--muted);border-right:1px solid var(--line)}
.code .tab.on{color:var(--strong,var(--ink));border-top:2px solid var(--accent)}
.code .src{display:flex;overflow-x:auto}
.code pre{margin:0;font:12.5px/1.8 var(--fm)}
.code .ln{padding:13px 12px;text-align:right;color:#3d5a78;border-right:1px solid var(--line);background:rgba(8,24,40,.5);user-select:none}
.code .lines{padding:13px 16px;color:var(--ink-2)}
.code .kw{color:var(--accent-2,#5b9dff)} .code .fn{color:var(--accent)} .code .str{color:var(--ok)} .code .com{color:var(--muted);font-style:italic} .code .num{color:var(--warn)} .code .key{color:var(--accent)}
```
Single-tab, no gutter? A `tabs` with one `tab.on` + a single `<pre class="lines">` (drop the `.ln` column) is fine for a short config snippet.

Validated examples: `Projects/speckit companion/briefs/2026-06-11-terminal-code-uml-addendum.html` (dark) and `…-pluggable-hook-bus-and-auto-mode.html` (light code viewer).
