---
name: create-doc
description: >
  Produce a standalone document for SOMEONE ELSE from a note or a brief — HTML, PDF, or
  Word (.docx). Use when the user says '/create-doc', 'page', 'doc', 'brief', 'report',
  'explainer', 'make this visual', 'render this as a page', 'convert these notes to PDF',
  'make a Word doc from this markdown', 'export these .md files so GoodNotes / Word /
  Pages can open them', or wants a design, decision, comparison, or plan captured as a
  browsable or printable artifact. The format is a flag (`--html` / `--pdf` / `--docx`),
  and HTML documents pick a named reading theme. This is the EXPORT path — for notes that
  stay inside the vault, use the `obsidian` skill instead.
argument-hint: "<topic, note path, or folder> [--html|--pdf|--docx] [--theme <name>] [--out <dir>] [--combine <name>]"
metadata:
  author: alfredo
  source: kaiju
---

# Create Doc

Take a note or a brief and produce **a document that leaves the vault**: a self-contained
HTML page, a PDF for reading and annotating, or a Word `.docx` for editing. Same job every
time — package thinking for a reader who isn't you. Only the output format changes.

> **The audience distinction is the whole point.**
> `obsidian` writes **notes for the user, inside the vault** — searchable markdown, backlinks,
> graph, Bases. `create-doc` writes **documents that leave it** — sent to someone, published,
> presented, printed, annotated in GoodNotes, edited in Word.
>
> Do not reach for this as the default. HTML in an Obsidian vault is dark matter: no search,
> no backlinks, no graph. ~140k words were once locked in HTML pages that way. If the artifact
> is going to live in the vault and be read by Alfredo, it's a markdown note and `obsidian`
> owns it.

## When to Use

- User says `/create-doc`, "make a page/doc/report/brief/explainer", "make this visual",
  "render this as a page" **and the artifact is going somewhere** (a person, a repo, a
  publication, a presentation).
- A design discussion, set of decisions, comparison, or execution plan needs to travel as a
  browsable artifact — including as raw material for an article.
- User wants vault notes openable in **GoodNotes** (→ PDF), or editable in
  **Word / Pages / Google Docs** (→ .docx).
- User wants one output per source file, or several markdown files **combined** into one
  document (e.g. a session's Notes + Transcript).

Do **not** use this for notes the user wants to keep as markdown in the vault (`obsidian`),
or for diagrams (`create-diagram`).

## Inputs

- **Topic / content** — a topic passed as argument, one or more `.md` file paths, a folder
  of `.md` files, or content drawn from the current conversation. Often the doc summarizes
  work just discussed.
- **Format** — `--html`, `--pdf`, `--docx`. Default: `--html` for a topic or conversation;
  `--pdf --docx` (both) when the input is existing markdown files.
- **`--theme <name>`** — the reading theme for HTML. Default **Hyperlegible**. See *Themes and
  styles* below.
- **`--out <dir>`** — output directory. Default: the folder of the work it documents (HTML),
  or alongside each source file (PDF/DOCX).
- **`--combine <name>`** — merge several markdown files into one document with page breaks.

## Themes and styles

Documents have a **named visual system**, the same way decks do. Seven reading themes are
registered in `references/themes.md`, each a token set that the `references/design.md`
skeleton consumes:

| Theme | Mode | Use when |
|---|---|---|
| **Hyperlegible** (default) | light | anything read end-to-end, shared, or printed; accessibility-first |
| **Slate** | soft dark | low-fatigue dark-mode long reads |
| Paper | light serif | long-form narrative reasoning; print |
| Dark Editorial | warm dark serif | narrative / decision briefs read at night |
| Blueprint | dark, cyan grid | technical / architecture; scanning structure and tables |
| Manuscript | sepia | cozy extended reading, low blue light |
| Notebook | light, grid | technical content in light mode (Blueprint's light twin) |
| **Print** | paper | the PDF lane's typeset system (the `CSS` constant in `scripts/md_convert.py`) |

**Picking a theme.** Default to Hyperlegible unless the content argues otherwise (technical
architecture → Blueprint; narrative decision brief → Paper or Dark Editorial). When the user
wants to *see* options rather than read theme names, render the same first screen under three
genuinely distinct themes and let them react — the "show, don't tell" move that
`presentation-style` uses for decks.

**Scope today, honestly.** The seven reading themes are HTML-only. The PDF lane renders
through the single **Print** theme bundled in `scripts/md_convert.py`, and `.docx` inherits
pandoc's default styling. Extending a reading theme to PDF means swapping that script's `CSS`
constant for the theme's token block; extending it to Word means a pandoc `--reference-doc`.
Neither is wired yet. This skill is the intended home for both, mirroring the
`presentation-theme` / `presentation-style` split (theme = the reusable token system and its
identity brief; style = showing real rendered options and applying the pick).

**Growing the system.** A recurring need belongs in `references/*.md`, not in one document.
Add to `themes.md`, `design.md`, `diagrams.md`, `viewers.md`, `sections.md` — or a new file —
rather than inventing one-off CSS. Capture once, reuse forever.

## Workflow

### Step 1: Pick the format

- Going to a person or a publication, needs layout, comparisons, diagrams, status colors →
  **HTML** (Step 2).
- Going to GoodNotes / Notability / print / a fixed page to annotate on top of → **PDF**
  (Step 3).
- Going to someone who will **edit the words** in Word / Pages / Google Docs → **DOCX**
  (Step 3).

**What GoodNotes actually does:** it imports a PDF as a **fixed page you annotate *on top of***
— handwriting, highlights, text boxes, drawings — and it can *search* the text, but you
**cannot edit or reflow the original printed words**. PDF is for annotating; `.docx` is for
editing. Offer both when the user cares about editing.

---

### Step 2: HTML lane

#### 2a. Calibrate — theme + components

**Pick a theme** from `references/themes.md` (default **Hyperlegible**). Copy the full
`<style>` token set from its canonical example listed in `themes.md`, or build from its
`:root` block. Describe type by *category*, never font name.

**Read `references/design.md`** for the component vocabulary and layout (header, callout,
card, table, compare, decisions, flow/steps, mock, band, badge, legend). Layout, spacing,
and component structure are shared across themes; only the token palette changes per theme.

**Load recipe references on demand** — read one only when the document actually needs it:

| Reference | Read it when the document needs… |
|---|---|
| `references/themes.md` | always — pick/apply the theme (default Hyperlegible) |
| `references/design.md` | always — the component + layout system |
| `references/diagrams.md` | a pipeline, sequence, layers, state machine, matrix, timeline, or lean UML |
| `references/viewers.md` | a terminal session or a code excerpt with chrome |
| `references/sections.md` | definition cards, trace cards, tally trios, verdict groups, harvest tables |

Do not invent colors, radii, or one-off components outside these references.

#### 2b. Settle the content

Identify what the document argues and the components that fit (from `design.md`):

- comparison → `compare` + `table`
- locked decisions → `decisions`
- a pipeline / sequence → `flow` or `steps`
- "what it feels like" → `mock`
- a thesis or closing → `callout` / `band`

Pull the substance from the conversation or the source note. If key content is missing or
ambiguous, ask the user briefly rather than inventing it. Keep it honest: placeholder frames
over invented data, real status tagged with `badge`s (`shipped` / `planned`), drafts marked
`[DRAFT]` / `(planned)`.

#### 2c. Generate the HTML

Produce **one self-contained `.html` file**: inline `<style>` (the theme's token set +
components), no external runtime deps. The font stacks in `references/themes.md` carry system
fallbacks, so a document stays self-contained by default; add the optional Google Fonts
`<link>` from `themes.md` only when exact rendering matters (Hyperlegible and the serif themes
benefit most) and offline isn't a concern.

Open with `header` (title + one-line `.sub` + `.meta`), state the thesis in a `callout`,
compose the body from components, and end with forward momentum (a `band` CTA or a "what's
next" card), not a summary.

**The date is a field inside the document, not in the filename.** Put today's date in the
`.meta` row of the header (alongside project/status), and optionally as
`<meta name="date" content="YYYY-MM-DD">` in `<head>`. The filename stays clean.

#### 2d. Save next to the work (clean slug, no date)

Pick a kebab slug from the topic. Save as **`<slug>.html`** — no date prefix, no dedicated
archive folder.

- **Default home = the folder of the work it documents.** Drop the `.html` beside the related
  markdown (e.g. `Projects/<project>/product/<feature>/<slug>.html` next to that feature's
  `prd.md`, or `specs/<NNN>-<slug>/<slug>.html` in a code repo so it travels with the PR).
- If there's no obvious sibling folder, save to the most relevant project folder. If you
  genuinely can't tell where it belongs, ask.
- **No `index.md` upkeep.** Don't maintain a separate index.

---

### Step 3: PDF / DOCX lane

1. **Preflight.** Ensure `pandoc` (`brew install pandoc` if missing) and Google Chrome exist.
   The helper checks both.
2. **Decide shape.** One output per file, or combine several into one (Notes + Transcript →
   one doc)? Which formats?
3. **Run the helper** at `scripts/md_convert.py`:
   ```sh
   # one folder of notes → PDF + DOCX into ./out
   python3 scripts/md_convert.py "/path/to/folder" --out "/path/to/out"

   # combine two files into one PDF, page-break between them
   python3 scripts/md_convert.py "Sesión 8 - Notas.md" "Sesión 8 - Transcripción.md" \
       --combine "Sesión 8" --pdf --out ./out

   # just Word docs, written next to each source
   python3 scripts/md_convert.py ./folder --docx
   ```
   Toolchain, no LaTeX: `.docx` via `pandoc` directly; PDF via `pandoc` → standalone HTML
   (+ the bundled Print CSS) → headless Chrome.
4. **Place / zip** if asked: copy outputs next to the source files, or `zip -r -X` into
   Downloads. Match files to source folders with NFC-normalized names (see Tips), not raw glob.

The helper exposes `clean()`, `find_in_dir()`, `chrome_pdf()`, and `render()` — reuse or adapt
them inline if a one-off needs custom layout.

---

### Step 4: Report

Report the saved path(s), the theme used (HTML), counts produced and where they landed
(PDF/DOCX), and which if any PDFs failed to render. If the user is on a phone (or asks), also
render the key sections inline in chat as a quick markdown preview — but the file is the
deliverable.

## Examples

**Input:** "make a doc comparing our caching options"

**Output:** `Projects/<project>/<area>/caching-options.html` (beside the related notes) —
Hyperlegible theme, a `header` whose `.meta` line carries the date, a thesis `callout`, a
`compare` block (option A vs B), a `table` of tradeoffs, status `badge`s, and a closing
recommendation `band`. Clean filename, no date prefix, no index entry. Path reported back.

**Input:** "convert all the notes in this course folder to PDF and Word, one file per session
combining notes + transcript, and put them next to the markdown."

**Output:** For each `Sesión N - …/` folder, a `Sesión N - <título>.pdf` and `.docx` (notes
first, page break, transcript) written into that folder; a short report of 2×N files produced.

## Quality Checklist

- [ ] The document is genuinely leaving the vault — otherwise it's an `obsidian` markdown note
- [ ] Format chosen deliberately (annotate → PDF, edit → DOCX, browse/present → HTML)
- [ ] **HTML:** theme picked from `references/themes.md` (default Hyperlegible) and its token
      set used; `references/design.md` read and only its components used; diagram/viewer/section
      recipes loaded as needed
- [ ] **HTML:** one self-contained `.html` — inline CSS, no external runtime deps (web-font
      `<link>` only if needed); accents sparing; flat, no shadows; one tight `h1`; uppercase
      eyebrows on sections; status colors use `--ok/--warn/--info/--crit`
- [ ] **HTML:** saved as `<slug>.html` (clean, no date) **next to the work it documents**; the
      date is a field inside the document; ends with forward momentum, not a summary
- [ ] **PDF/DOCX:** `pandoc` + Chrome verified before rendering; Chrome called with
      `--headless=new` (never bare `--headless`), unique `--user-data-dir`, per-file timeout
- [ ] **PDF/DOCX:** frontmatter stripped, `[[wikilinks]]` flattened, nav-only lines dropped;
      accented filenames matched via NFC normalization; idempotent (re-run fills only missing
      outputs unless `--force`)
- [ ] Content is honest — no invented data; drafts/planned items tagged
- [ ] Paths and failures reported

## Tips

- **Reuse, don't reinvent.** The skeleton already encodes the system. Compose components;
  resist new CSS. If you genuinely need a new pattern repeatedly, add it to `design.md`, not
  to one file.
- **Self-contained by default.** A Google Fonts `<link>` is an external dep — only add it on
  request.
- **Co-locate, don't archive.** A document lives beside the markdown it documents, so the
  related work travels together. No dated filenames, no per-project `briefs/` folder, no index.
  (Older pages still under a `briefs/` folder are fine where they are.)
- **Working in a code repo is fine.** The design system is bundled with this skill, so it
  resolves regardless of the current directory; save the document beside the spec or feature
  it belongs to.
- **Chrome `--headless` hangs.** The legacy `--headless` writes the PDF and then *does not
  exit*, freezing a batch. Always use `--headless=new`, wrap each render in a ~40s timeout, and
  treat "timed out but the file exists" as success — the PDF is written before the hang.
- **Singleton-profile lock.** Give every Chrome invocation a **unique** `--user-data-dir` (a
  fresh temp dir), or a second concurrent/looped call blocks.
- **macOS Unicode gotcha.** Filenames with accents (ó, í, ñ) can be stored NFC or NFD. Python
  `glob` patterns containing accented literals **silently miss** them. Match with `os.listdir`
  + `unicodedata.normalize("NFC", name).endswith(suffix)` instead.
- **Clean before render.** Strip the YAML frontmatter, drop Obsidian nav lines, and convert
  `[[wikilinks]]` to plain text so they don't render as literal `[[brackets]]`.
- **Combine with page breaks.** Join documents with `<div class="page-break"></div>`; the
  bundled CSS turns it into a hard page break (and starts every new `<h1>` on a fresh page).
- **GoodNotes import = annotate, not edit.** If the user wants to change the text, hand them
  the `.docx`, not the PDF.
