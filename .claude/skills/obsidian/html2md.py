#!/usr/bin/env python3
"""Convert an html-page 'brief' into an Obsidian-native markdown note.

Maps the house design system onto native Obsidian constructs:
  header            -> frontmatter + H1
  tabs/panels       -> H2 sections (the Outline pane IS the tab bar)
  callout(.warn/.ok)-> > [!note] / [!warning] / [!success]
  band              -> > [!tip]
  grid.cols-N/card  -> > [!cards|N] with nested > > [!card]
  table.matrix      -> markdown table, c-ok/c-mid/c-no -> emoji
  tk + details.tkd  -> > [!ticket] with nested collapsible > > [!example]-
  ph                -> > [!phase]
  .yml / .demo      -> fenced code blocks
  ol.steps          -> ordered list
  badge / pill      -> inline code
  svg               -> flagged for a mermaid/excalidraw redraw
"""
import re, sys, html
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

CELL = {"c-ok": "c-ok", "c-mid": "c-mid", "c-no": "c-no"}
CALLOUT = {"warn": "warning", "ok": "success", "crit": "danger", "info": "info"}

warnings = []

# Every class the converter understands. Anything NOT in here is recorded in the
# discovery log so a new component is reviewed, not silently flattened to prose.
KNOWN = {
    "wrap", "meta", "sub", "subtitle", "tabs", "tab", "panel", "sec", "eyebrow", "secintro",
    "callout", "lead", "warn", "ok", "crit", "info", "band", "grid", "card", "card-head",
    "cols-2", "cols-3", "cols-4", "g2", "g3", "g4", "tk", "tkd", "top", "id", "row", "l",
    "ph", "yml", "lab", "k", "v", "demo", "demolab", "mock", "steps", "fig", "cap", "legend",
    "dot", "c-ok", "c-mid", "c-no", "matrix", "rl", "badge", "pill", "mut", "chip",
    "b-info", "b-ok", "b-warn", "b-crit", "p-s", "p-m", "p-l", "det", "dl", "drow", "dwrap",
    "ai", "a", "b", "g", "r", "s", "c", "num", "active", "open", "pair", "side", "lbl",
    "flow", "step", "arrow", "n", "dec", "decisions", "is-shipped", "is-crit", "is-info",
    "add", "tight", "str", "body", "img",
    "term", "bar", "t", "p", "cmd", "o", "com", "ar", "win", "fn",
}

current_file = ""
discovered = {}   # class -> {"files": set, "sample": str}


def note_unknown(el):
    for cl in cls(el):
        if cl in KNOWN:
            continue
        d = discovered.setdefault(cl, {"files": set(), "sample": ""})
        d["files"].add(current_file)
        if not d["sample"]:
            d["sample"] = re.sub(r"\s+", " ", str(el))[:110]


def cls(el):
    return el.get("class", []) if isinstance(el, Tag) else []


def inline(node):
    """Render inline content to markdown."""
    if isinstance(node, NavigableString):
        return re.sub(r"\s+", " ", str(node))
    if not isinstance(node, Tag):
        return ""
    c = cls(node)
    kids = "".join(inline(k) for k in node.children)
    kids_stripped = kids.strip()

    if node.name in ("b", "strong"):
        return f"**{kids_stripped}**" if kids_stripped else ""
    if node.name in ("i", "em"):
        return f"*{kids_stripped}*" if kids_stripped else ""
    if node.name == "code":
        return f"`{kids_stripped}`" if kids_stripped else ""
    if node.name == "a":
        href = node.get("href", "")
        return f"[{kids_stripped}]({href})" if href else kids_stripped
    if node.name == "br":
        return " "
    if node.name == "span":
        # badges and pills become inline code; label spans are handled by the caller
        if "badge" in c or "pill" in c:
            return f"`{kids_stripped}`" if kids_stripped else ""
        if "dot" in c:
            for k, v in CELL.items():
                if k in c:
                    return v
            return ""
        if "mut" in c:
            return f"*{kids_stripped}*" if kids_stripped else ""
        return kids
    return kids


def text_of(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)) if el else ""


BLOCK_TAGS = {"div", "p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "table",
              "section", "details", "svg", "figure", "header", "blockquote", "pre"}


def children_blocks(el, depth=0):
    """Walk children, grouping runs of inline content into single paragraphs
    so <b>/<code>/<i> don't each become their own block."""
    out, buf = [], []

    def flush():
        if buf:
            t = "".join(buf).strip()
            t = re.sub(r"\s+", " ", t)
            if t:
                out.append(t)
            buf.clear()

    for k in el.children:
        if isinstance(k, Tag) and k.name in BLOCK_TAGS:
            flush()
            out.extend(block(k, depth))
        else:
            buf.append(inline(k))
    flush()
    return [x for x in out if x]


def code_block(el, lang):
    """.yml / .demo divs: <span class='lab'> are comments, <span class='k'> keys."""
    parts = []
    for k in el.children:
        if isinstance(k, NavigableString):
            parts.append(str(k))
        elif isinstance(k, Tag):
            # .lab is display:block in the stylesheet — it owns its own line
            nl = "\n" if "lab" in cls(k) else ""
            parts.append(k.get_text() + nl)
    raw = "".join(parts)
    raw = html.unescape(raw).strip("\n")
    lines = [ln.rstrip() for ln in raw.split("\n")]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return f"```{lang}\n" + "\n".join(lines) + "\n```"


def quote(text, level=1):
    p = "> " * level
    return "\n".join(p + ln if ln.strip() else p.rstrip() for ln in text.split("\n"))


def rows_of(el):
    """.row = <span class='l'>label</span>text  ->  **label** text"""
    out = []
    for r in el.find_all(class_="row", recursive=False):
        lab = r.find(class_="l")
        label = text_of(lab) if lab else ""
        if lab:
            lab.extract()
        body = "".join(inline(k) for k in r.children).strip()
        out.append(f"**{label}** {body}" if label else body)
    return out


def table_md(el):
    rows = el.find_all("tr")
    if not rows:
        return ""
    is_matrix = "matrix" in cls(el)
    out, header_done = [], False
    for tr in rows:
        cells = tr.find_all(["th", "td"])
        vals = []
        for c in cells:
            cc = cls(c)
            chip = next((CELL[k] for k in CELL if k in cc), None)
            txt = "".join(inline(k) for k in c.children).strip()
            txt = txt.replace("|", "\\|")
            if is_matrix and chip:
                txt = f'<span class="{chip}">{txt}</span>'
            vals.append(txt or " ")
        out.append("| " + " | ".join(vals) + " |")
        if not header_done and cells and cells[0].name == "th":
            out.append("|" + "|".join([" --- "] * len(cells)) + "|")
            header_done = True
    if not header_done and out:
        n = out[0].count("|") - 1
        out.insert(1, "|" + "|".join([" --- "] * n) + "|")
    return "\n".join(out)


def block(el, depth=0):
    """Render a block-level element to markdown. Returns list of chunks."""
    if isinstance(el, NavigableString):
        t = re.sub(r"\s+", " ", str(el)).strip()
        return [t] if t else []
    if not isinstance(el, Tag):
        return []
    c = cls(el)
    n = el.name
    out = []

    if n in ("script", "style", "button"):
        return []

    note_unknown(el)

    # --- code-ish blocks
    if "yml" in c:
        return [code_block(el, "yaml")]
    if "demo" in c:
        lab = el.find(class_="demolab")
        title = text_of(lab) if lab else "output"
        title = title.lstrip("# ").strip() or "output"   # some labels are code comments
        if lab:
            lab.extract()
        cb = code_block(el, "text")
        return [f"> [!terminal] {title}\n" + quote(cb)]

    # --- callouts
    if "callout" in c:
        kind = next((CALLOUT[k] for k in CALLOUT if k in c), "note")
        chunks = children_blocks(el, depth + 1)
        # promote a leading **bold lead** to the callout title, else Obsidian
        # prints the type name ("Note") in the title bar, which says nothing
        title = ""
        if chunks:
            m = re.match(r"\*\*(.{3,90}?)\*\*[  ]*", chunks[0])
            if m:
                title = m.group(1).strip()
                rest = chunks[0][m.end():].strip()
                if rest:
                    chunks[0] = rest
                else:
                    chunks.pop(0)
        head = f"> [!{kind}] {title}" if title else f"> [!{kind}]"
        return [head + "\n" + quote("\n\n".join(chunks).strip())]

    if "band" in c:
        h = el.find(["h3", "h2"])
        title = text_of(h) if h else ""
        if h:
            h.extract()
        inner = "\n\n".join(children_blocks(el, depth + 1))
        return [f"> [!tip] {title}\n" + quote(inner.strip())]

    # --- pair: a before/after compare (.pair > .side.a|.side.b > .lbl)
    # Same shape as a cards grid, different class names. Tint the two sides apart
    # — matched boxes make the reader work out which is which.
    if "pair" in c:
        tints = ["blue", "green", "amber"]
        cards = []
        for i, side in enumerate(el.find_all(class_="side", recursive=False)):
            lab = side.find(class_="lbl")
            title = text_of(lab) if lab else ""
            if lab:
                lab.extract()
            inner = "\n\n".join(children_blocks(side, depth + 1))
            head = f"> [!card|{tints[i % 3]}] {title or chr(8203)}"
            cards.append(head + "\n" + quote(inner.strip()))
        if cards:
            return ["> [!cards|2]\n" + "\n>\n".join(quote(cd) for cd in cards)]
        return children_blocks(el, depth)

    # --- term: a terminal viewer (title bar + transcript). Output, not source.
    if "term" in c:
        bar = el.find(class_="bar")
        tspan = bar.find(class_="t") if bar else None
        title = text_of(tspan) if tspan else "terminal"
        body_el = el.find(class_="body") or el
        lines, cur = [], ""
        for k in body_el.children:
            if isinstance(k, Tag):
                kc = cls(k)
                if "bar" in kc:
                    continue
                t = text_of(k)
                if "p" in kc:            # a prompt char starts a new line
                    if cur.strip():
                        lines.append(cur.strip())
                    cur = t + " "
                else:
                    cur += t + " "
            else:
                cur += re.sub(r"\s+", " ", str(k))
        if cur.strip():
            lines.append(cur.strip())
        body = "\n".join(lines)
        return [f"> [!terminal] {title}\n" + quote("```console\n" + body + "\n```")]

    # --- mock: a "what it feels like" block. Output, not source -> terminal.
    if "mock" in c:
        return ["> [!terminal] what it looks like\n" + quote(code_block(el, "text"))]

    # --- dec: one locked decision. <b>Decision:</b> ... -> a titled callout.
    if "dec" in c and "decisions" not in c:
        b = el.find("b")
        title = text_of(b).rstrip(":").strip() if b else "Decision"
        if b:
            b.extract()
        body = "".join(inline(k) for k in el.children).strip()
        return [f"> [!decision] {title}\n" + quote(body)]

    # --- decisions: a row of chips, each a settled call.
    if "decisions" in c:
        chips = [text_of(sp).lstrip("\u2713 ").strip()
                 for sp in el.find_all(class_="chip", recursive=False)]
        chips = [x for x in chips if x]
        if chips:
            return ["> [!success] Locked\n" + quote("\n".join(f"- {x}" for x in chips))]
        return children_blocks(el, depth)

    # --- flow: a horizontal step chain -> a real mermaid pipeline.
    if "flow" in c:
        steps = [re.sub(r"^\d+\s*", "", text_of(sp))
                 for sp in el.find_all(class_="step", recursive=False)]
        steps = [x for x in steps if x]
        if len(steps) >= 2:
            nodes = " --> ".join(f'S{i}["{x}"]' for i, x in enumerate(steps))
            return ["> [!figure] " + " \u2192 ".join(steps) + "\n>\n"
                    "> ```mermaid\n> flowchart LR\n>   " + nodes + "\n> ```"]
        return children_blocks(el, depth)

    # --- cards grid
    if "grid" in c:
        # column count: `cols-3` in newer briefs, `g3` in the early ones
        ncol = next((x.split("-")[1] for x in c if x.startswith("cols-")),
                    next((x[1:] for x in c if re.fullmatch(r"g[234]", x)), "2"))
        # a grid's children are usually `.card`, but early briefs use `.panel`
        # or bare divs. Falling through with an empty card list would emit an
        # EMPTY cards callout and silently swallow the whole grid.
        items = el.find_all(class_="card", recursive=False)
        if not items:
            items = [k for k in el.children if isinstance(k, Tag) and k.name == "div"]
        if not items:
            return children_blocks(el, depth)
        cards = []
        for card in items:
            h = card.find(["h3", "h4"])
            title = text_of(h) if h else ""
            if h:
                h.extract()
            chunks = children_blocks(card, depth + 1)
            # a titleless callout renders as the literal word "Card" — lift a lead line
            if not title and chunks and len(chunks[0]) < 90 and "\n" not in chunks[0]:
                title = chunks.pop(0).strip("*_ ")
            inner = "\n\n".join(chunks)
            tint = ["blue", "green", "amber"][len(cards) % 3]
            head = f"> [!card|{tint}] {title}" if title else f"> [!card|{tint}] \u200b"
            cards.append(head + "\n" + quote(inner.strip()))
        joined = "\n>\n".join(quote(cd) for cd in cards)
        return [f"> [!cards|{ncol}]\n" + joined]

    # --- tickets
    if "tk" in c:
        top = el.find(class_="top")
        tid = text_of(top.find(class_="id")) if top and top.find(class_="id") else ""
        h = top.find(["h3", "h4"]) if top else None
        title = text_of(h) if h else ""
        pill = top.find(class_="pill") if top else None
        size = f" · `{text_of(pill)}`" if pill else ""
        if top:
            top.extract()
        body = rows_of(el)
        for r in el.find_all(class_="row", recursive=False):
            r.extract()
        # Whatever is LEFT — <p>, the nested <details> collapse, a `.body` div
        # holding a <ul> — must be recursed into, not enumerated. Listing only the
        # child types you expect is how a ticket's list of acceptance criteria gets
        # silently swallowed.
        body.extend(children_blocks(el, depth + 1))
        head = f"> [!ticket] {tid} · {title}{size}".replace(" ·  · ", " · ")
        return [head + "\n" + quote("\n\n".join(b for b in body if b))]

    if n == "details" or "tkd" in c:
        s = el.find("summary")
        title = text_of(s) if s else "details"
        if s:
            s.extract()
        inner = "\n\n".join(children_blocks(el, depth + 1))
        return [f"> [!example]- {title}\n" + quote(inner.strip())]

    if "dwrap" in c:
        chunks = []
        for r in el.find_all(class_="drow", recursive=False):
            dl = r.find(class_="dl")
            label = text_of(dl) if dl else ""
            if dl:
                dl.extract()
            body = "".join(inline(k) for k in r.children).strip()
            chunks.append(f"**{label}** {body}" if label else body)
            r.extract()
        chunks.extend(children_blocks(el, depth + 1))
        return [x for x in chunks if x]

    # --- phases
    if "ph" in c:
        top = el.find(class_="top")
        pid = text_of(top.find(class_="id")) if top and top.find(class_="id") else ""
        h = top.find(["h3", "h4"]) if top else None
        title = text_of(h) if h else ""
        bdg = top.find(class_="badge") if top else None
        tag = f" · `{text_of(bdg)}`" if bdg else ""
        if top:
            top.extract()
        body = rows_of(el)
        for r in el.find_all(class_="row", recursive=False):
            r.extract()
        body.extend(children_blocks(el, depth + 1))
        head = f"> [!phase] {pid} · {title}{tag}"
        return [head + "\n" + quote("\n\n".join(b for b in body if b))]

    # --- figure / svg
    if ("fig" in c and el.find("svg")) or n == "svg":
        cap = el.find(class_="cap")
        caption = text_of(cap) if cap else ""
        svg = el if n == "svg" else el.find("svg")
        label = (svg.get("aria-label") if svg else "") or ""
        # The SVG's <text> nodes ARE content. Dropping them loses the diagram's
        # labels silently — preserve every one, so a redraw is a rewrite rather
        # than a reconstruction from memory.
        labels = [t for t in (text_of(x) for x in (svg.find_all("text") if svg else [])) if t]
        title = caption or label or "untitled"
        warnings.append(f"SVG figure needs a redraw: “{title}”")
        lines = [
            f"> [!warning] Diagram to redraw — {title}",
            "> The original was an inline SVG. Redraw as Mermaid (`flowchart LR`) or embed an",
            "> Excalidraw file. Every label from the original is preserved below, so nothing is",
            "> lost — this is a rewrite, not a reconstruction.",
        ]
        if labels:
            lines.append(">")
            lines += [f"> - {x}" for x in labels]
        return ["\n".join(lines)]

    if "legend" in c:
        items = []
        for sp in el.find_all("span", recursive=False):
            dot = sp.find(class_="dot")
            chip = next((CELL[k] for k in CELL if dot and k in cls(dot)), "")
            if dot:
                dot.extract()
            label = text_of(sp)
            items.append(f'<span class="{chip} chip-key"></span> {label}' if chip else label)
        return ["> [!legend]\n> " + "  ".join(items)]

    # --- plain structures
    if n == "table":
        return [table_md(el)]
    if n in ("h2",):
        return [f"### {text_of(el)}"]
    if n in ("h3", "h4"):
        return [f"#### {text_of(el)}"]
    if n == "p":
        if "secintro" in c or "sub" in c:
            return [f"*{text_of(el)}*"]
        t = "".join(inline(k) for k in el.children).strip()
        return [t] if t else []
    if n in ("ul", "ol"):
        items = []
        for i, li in enumerate(el.find_all("li", recursive=False), 1):
            t = "".join(inline(k) for k in li.children).strip()
            items.append(f"{i}. {t}" if n == "ol" else f"- {t}")
        return ["\n".join(items)]
    if "row" in c:
        lab = el.find(class_="l")
        label = text_of(lab) if lab else ""
        if lab:
            lab.extract()
        body = "".join(inline(k) for k in el.children).strip()
        return [f"**{label}** {body}" if label else body]
    if "subtitle" in c:
        return [f"*{text_of(el)}*"]
    if "eyebrow" in c:
        # A standalone eyebrow is a kicker with real content ("Flags for you to
        # decide"). Only the ones that restate their section heading are dropped,
        # and that check lives in convert() where the heading is known.
        t = text_of(el)
        return [f"#### {t}"] if t else []
    if "tabs" in c:
        return []

    # generic container: recurse, grouping inline runs
    return children_blocks(el, depth)


def convert(path: Path):
    global current_file
    current_file = path.name
    soup = BeautifulSoup(path.read_text(), "html.parser")
    for t in soup(["script", "style"]):
        t.decompose()

    # Take the title from <header> when there is one, else from the first <h1>.
    # NEVER promote the h1's PARENT to "header" — that parent is usually the
    # page wrapper, and extracting it would delete the whole document.
    header = soup.find("header")
    h1_el = (header.find("h1") if header else None) or soup.find("h1")
    h1 = text_of(h1_el) if h1_el else path.stem
    sub_el = (header.find(class_="sub") if header else None) or soup.find(class_="sub")
    sub = text_of(sub_el)
    meta = (header.find(class_="meta") if header else None) or soup.find(class_="meta")
    date, badges = "", []
    if meta:
        for s in meta.find_all("span"):
            t = text_of(s)
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", t):
                date = t
            elif "badge" in cls(s):
                badges.append(t)

    # tab labels -> section names
    tabmap = {b.get("data-tab"): text_of(b) for b in soup.find_all("button", class_="tab")}

    body = []
    # `.panel` is overloaded: a TAB panel in tabbed briefs, but just a styled
    # box in the early ones. Only take the tab path when tabs actually exist,
    # otherwise everything outside those boxes gets silently dropped.
    panels = soup.find_all(class_="panel") if tabmap else []
    if panels:
        for p in panels:
            pid = p.get("id") or p.get("data-tab")
            name = tabmap.get(pid, "")
            sec = p.find("section") or p
            eyebrow = sec.find(class_="eyebrow")
            eb = text_of(eyebrow) if eyebrow else ""
            h2 = sec.find("h2")
            title = text_of(h2) if h2 else name
            if h2:
                h2.extract()
            if eyebrow:
                eyebrow.extract()
            body.append(f"## {name or title}")
            if title and name and title.lower() != name.lower():
                body.append(f"### {title}")
            # keep the eyebrow unless it just restates the heading it sits above
            if eb:
                head_words = set(re.findall(r"[a-z]{3,}", f"{name} {title}".lower()))
                eb_words = set(re.findall(r"[a-z]{3,}", eb.lower()))
                overlap = (len(eb_words & head_words) / len(eb_words)) if eb_words else 1.0
                if overlap < 0.6:
                    body.append(f"#### {eb}")
            # walk the PANEL, not just the <section> — bands/callouts sit outside it
            body.extend(children_blocks(p))
    else:
        main = soup.find(class_="wrap") or soup.body
        for el in (header if header and header.name == "header" else None, h1_el, sub_el, meta):
            if el is not None and el is not main:
                el.extract()
        body.extend(children_blocks(main))

    fm = ["---", f"title: {h1}"]
    if sub:
        fm.append(f'sub: "{sub.replace(chr(34), chr(39))}"')
    if date:
        fm.append(f"date: {date}")
    fm.append("type: brief")
    for i, b in enumerate(badges):
        fm.append(f"{'kind' if i == 0 else 'status'}: \"{b}\"")
    fm += ["cssclasses:", "  - brief", "---", ""]

    out = "\n".join(fm) + f"# {h1}\n\n"
    if sub:
        out += f"*{sub}*\n\n"
    out += "\n\n".join(x.strip() for x in body if x and x.strip()) + "\n"
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out


# --- component discovery catalog ---------------------------------------------

CATALOG_HEADER = """---
title: Brief components — discovery catalog
description: Every HTML class the converter met. Unmapped ones flatten to plain prose until they are given a markdown equivalent.
type: reference
lifespan: durable
---
# Brief components — discovery catalog

Generated by `brief2md.py`. Each row is a class found in an HTML brief.

- **mapped** — the converter renders it as a real component.
- **unmapped** — content survives, but it flattens to plain prose. Decide whether it deserves a component.
- **ignored** — decoration, or belongs to a different design system (slide decks, diagrams).

To map one: add a branch in `brief2md.py`, a rule in `vault.css`, and a line in `brief/SKILL.md`.

"""


def write_catalog(dst: Path, mapped_note="mapped"):
    """Merge the run's discoveries into one reviewable markdown table."""
    rows = {}
    if dst.exists():
        for line in dst.read_text().splitlines():
            m = re.match(r"\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|(.*?)\|(.*?)\|\s*(\w[\w-]*)\s*\|", line)
            if m:
                rows[m.group(1)] = {
                    "files": int(m.group(2)),
                    "sample": m.group(3).strip(),
                    "proposed": m.group(4).strip(),
                    "status": m.group(5).strip(),
                }
    for cl, d in discovered.items():
        prev = rows.get(cl, {})
        rows[cl] = {
            "files": max(len(d["files"]), prev.get("files", 0)),
            "sample": prev.get("sample") or "`" + d["sample"].replace("|", "\\|")[:70] + "`",
            "proposed": prev.get("proposed", "—"),
            "status": prev.get("status", "unmapped"),
        }
    body = ["| Class | Files | Sample | Proposed markdown | Status |",
            "| --- | --- | --- | --- | --- |"]
    for cl, d in sorted(rows.items(), key=lambda kv: -kv[1]["files"]):
        body.append(f"| `{cl}` | {d['files']} | {d['sample']} | {d['proposed']} | {d['status']} |")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(CATALOG_HEADER + "\n".join(body) + "\n")
    return len(rows)


if __name__ == "__main__":
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".md")
    dst.write_text(convert(src))
    print(f"wrote {dst}")
    for w in warnings:
        print(f"  ! {w}")
