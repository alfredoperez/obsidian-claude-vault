#!/usr/bin/env python3
"""
md_convert.py — convert markdown to PDF and/or DOCX, the efficient way.

Toolchain (no LaTeX):
  - DOCX: pandoc <md> -o <out>.docx --standalone        (direct, clean, handles tables + accents)
  - PDF : pandoc <md> -> standalone HTML (+CSS) -> Chrome --headless=new --print-to-pdf

Hard-won lessons baked in:
  1. Use Chrome `--headless=new`. The OLD `--headless` writes the PDF then HANGS
     without exiting and freezes a batch. We also wrap each render in a timeout and
     treat "timed out but file exists" as success (the PDF is written before the hang).
  2. Unique --user-data-dir per call -> no singleton-profile lock.
  3. macOS Unicode: filenames with accents (ó í ñ) may be NFC or NFD on disk; Python
     glob with accented literals SILENTLY misses them. Match via os.listdir +
     unicodedata.normalize("NFC", name).endswith(suffix). See find_in_dir().
  4. Clean markdown first: strip YAML frontmatter, drop nav/wikilink-only lines,
     turn [[wikilinks]] into plain text.
  5. Idempotent: skip an output that already exists (use --force to override).

Usage:
  # one file, both formats, next to the source
  md_convert.py notes.md

  # combine several md into ONE doc (page-break between), only PDF, to a dir
  md_convert.py "Sesión 8 - Notas.md" "Sesión 8 - Transcripción.md" \
      --combine "Sesión 8" --pdf --out ./out

  # whole folder of .md -> pdf+docx into ./out
  md_convert.py ./mydir --out ./out
"""
import argparse, os, re, shutil, subprocess, sys, tempfile, unicodedata

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]
DEVNULL = subprocess.DEVNULL

CSS = """<style>
@page { size: letter; margin: 18mm 16mm; }
body { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; font-size: 11.5pt; line-height: 1.5; color: #1a1a1a; }
h1 { font-size: 20pt; margin: 0 0 4pt; color: #111; }
h1:not(:first-of-type) { page-break-before: always; padding-top: 4pt; }
h2 { font-size: 14pt; margin: 18pt 0 6pt; padding-bottom: 3pt; border-bottom: 1.5px solid #d0d0d0; color: #1d3557; }
h3 { font-size: 12pt; margin: 12pt 0 4pt; color: #333; }
blockquote { border-left: 3px solid #9bb4cc; margin: 8pt 0; padding: 2pt 12pt; color: #444; font-style: italic; }
ul, ol { margin: 4pt 0; padding-left: 20pt; } li { margin: 2pt 0; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 10.5pt; }
th, td { border: 1px solid #c4c4c4; padding: 4pt 8pt; text-align: left; vertical-align: top; }
th { background: #f0f3f7; }
hr { border: none; border-top: 1px solid #ddd; margin: 14pt 0; }
code { background: #f3f3f3; padding: 1px 4px; border-radius: 3px; font-size: 10pt; }
.page-break { page-break-before: always; }
</style>"""

# Lines that are pure Obsidian navigation; drop them from rendered output.
NAV_MARKERS = ("Índice del curso", "Transcripción completa:", "Notas de esta sesión:")


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if os.path.exists(c):
            return c
    sys.exit("No Chrome/Chromium/Edge found — install Google Chrome for PDF rendering.")


def ensure_pandoc():
    if shutil.which("pandoc"):
        return
    sys.exit("pandoc not found. Install it: brew install pandoc")


def clean(md: str) -> str:
    """Strip YAML frontmatter, drop nav-only lines, flatten [[wikilinks]]."""
    md = re.sub(r"^---\n.*?\n---\n", "", md, count=1, flags=re.S)
    md = "\n".join(l for l in md.splitlines() if not any(k in l for k in NAV_MARKERS))
    md = re.sub(r"\[\[([^\]]+)\]\]", r"\1", md)
    return md.strip()


def find_in_dir(folder, suffix):
    """Unicode-safe file lookup by suffix (avoids glob's NFC/NFD blind spot)."""
    suffix = nfc(suffix)
    for name in os.listdir(folder):
        if nfc(name).endswith(suffix):
            return os.path.join(folder, name)
    return None


def chrome_pdf(chrome: str, html_path: str, pdf_path: str, uid, timeout: int = 40) -> bool:
    """Render HTML->PDF. Unique profile + --headless=new + timeout-kill safety net."""
    prof = tempfile.mkdtemp(prefix=f"chromeprof-{uid}-")
    try:
        p = subprocess.Popen(
            [chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
             f"--user-data-dir={prof}", f"--print-to-pdf={pdf_path}", f"file://{html_path}"],
            stdout=DEVNULL, stderr=DEVNULL)
        try:
            p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            p.kill()  # old-headless-style hang; PDF is already written by now
        return os.path.exists(pdf_path)
    finally:
        shutil.rmtree(prof, ignore_errors=True)


def render(chrome: str, name: str, md_body: str, out_dir: str, want_pdf: bool,
           want_docx: bool, uid, force: bool) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    results = {}
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(md_body)
        mp = f.name
    try:
        if want_docx:
            out = os.path.join(out_dir, f"{name}.docx")
            if force or not os.path.exists(out):
                subprocess.run(["pandoc", mp, "-o", out, "--standalone"], check=True)
            results["docx"] = out
        if want_pdf:
            out = os.path.join(out_dir, f"{name}.pdf")
            if force or not os.path.exists(out):
                hp = os.path.join(tempfile.gettempdir(), f"{name}.html")
                hdr = os.path.join(tempfile.gettempdir(), "md_convert_header.html")
                with open(hdr, "w", encoding="utf-8") as h:
                    h.write(CSS)
                subprocess.run(["pandoc", mp, "-o", hp, "--standalone",
                                f"--include-in-header={hdr}", "--metadata", f"title={name}"], check=True)
                ok = chrome_pdf(chrome, hp, out, uid)
                if not ok:
                    results["pdf_failed"] = out
                else:
                    results["pdf"] = out
            else:
                results["pdf"] = out
    finally:
        os.unlink(mp)
    return results


def collect_inputs(inputs):
    """Expand dirs to their .md files; keep files as-is. Returns list of paths."""
    files = []
    for p in inputs:
        if os.path.isdir(p):
            for name in sorted(os.listdir(p)):
                if nfc(name).endswith(".md"):
                    files.append(os.path.join(p, name))
        elif os.path.isfile(p):
            files.append(p)
        else:
            print(f"⚠️ skip (not found): {p}", file=sys.stderr)
    return files


def main():
    ap = argparse.ArgumentParser(description="Convert markdown to PDF and/or DOCX.")
    ap.add_argument("inputs", nargs="+", help="markdown files and/or directories")
    ap.add_argument("--pdf", action="store_true", help="produce PDF (default: both if neither flag given)")
    ap.add_argument("--docx", action="store_true", help="produce DOCX")
    ap.add_argument("--out", default=None, help="output dir (default: next to each source)")
    ap.add_argument("--combine", default=None, help="combine all inputs into ONE output with this basename")
    ap.add_argument("--force", action="store_true", help="overwrite existing outputs")
    args = ap.parse_args()

    want_pdf = args.pdf or not (args.pdf or args.docx)
    want_docx = args.docx or not (args.pdf or args.docx)

    ensure_pandoc()
    chrome = find_chrome() if want_pdf else ""
    files = collect_inputs(args.inputs)
    if not files:
        sys.exit("No markdown inputs found.")

    if args.combine:
        body = ("\n\n<div class=\"page-break\"></div>\n\n"
                .join(clean(open(f, encoding="utf-8").read()) for f in files))
        out_dir = args.out or os.path.dirname(os.path.abspath(files[0]))
        r = render(chrome, args.combine, body, out_dir, want_pdf, want_docx, 0, args.force)
        print(f"{'⚠️' if 'pdf_failed' in r else '✅'} {args.combine} -> {out_dir}")
        return

    for i, f in enumerate(files):
        name = nfc(os.path.splitext(os.path.basename(f))[0])
        body = clean(open(f, encoding="utf-8").read())
        out_dir = args.out or os.path.dirname(os.path.abspath(f))
        r = render(chrome, name, body, out_dir, want_pdf, want_docx, i, args.force)
        print(f"{'⚠️' if 'pdf_failed' in r else '✅'} {name}")


if __name__ == "__main__":
    main()
