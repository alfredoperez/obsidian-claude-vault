# Image Sweep, Evict, and the Trash Manifest

Full procedures for the Tier-1 mechanical passes: the Step 2.5 orphaned-image sweep, the Step 2.6 evict (ballast) pass, and the canonical trash manifest schema. Load this before running either pass.

## Performance: build link maps in a single pass

Build the vault-wide inbound-link map (and the referenced-image set below) in a SINGLE pass — one scan collecting every link occurrence. Do NOT grep once per note; that's O(notes²) and won't scale to a full-vault pass.

## Step 2.5: Sweep orphaned images (Tier 1 — auto, reversible)

Orphaned images are mechanical and reversible, so unlike note verdicts they are actioned automatically. Skip this entire step if `--no-images`.

1. **Build the referenced-image set** by scanning the WHOLE vault — every `.md` AND every `.html` (briefs), `.canvas`, and `.excalidraw` file, since those embed images too — but EXCLUDE `_Triage/`, `.git/`, `node_modules/`, `.obsidian/`. **Never scan the trash manifest** (`_Triage/Trash/manifest.json`): it lists already-swept files, so reading it would both hide real orphans and fake false positives against itself. (A central attachment can be referenced from anywhere, so this scan is always vault-wide regardless of the note scope.) From each file collect every image reference, in all forms, recording BOTH the full path and the basename:
   - wikilink embeds/links `![[name]]` / `[[name]]` (strip `|alias`, `#heading`, and `|size`);
   - markdown `![alt](path)` / `[txt](path)` where `path` ends in an image extension (URL-decode `%20` etc.);
   - HTML `<img ... src="path">`.
   Image extensions (case-insensitive): `png jpg jpeg gif webp svg avif bmp heic`.
2. **Candidate images** = image files INSIDE the scope; a full-vault pass ALSO includes the central attachment dirs `~Attachments/` and `_Attachments/`. Never consider images already under `~Archive/`, `_Triage/`, `.obsidian/`, or template dirs.
3. **Orphaned** ⇔ NEITHER the image's vault-relative path NOR its basename appears in the referenced set.
4. **Conservative guards — a false delete is the worst outcome:**
   - **NEVER sweep a generated asset bundle.** A folder is a bundle if it contains a `carousel.pdf`, is named `create-carousel/`, or sits under `~Attachments/Carousels/`. Its images are a *unit* whose provenance lives in a record note elsewhere — they are deleted deliberately, as a folder, or not at all. An individual slide is never an orphan.
     *Why this exists:* the `/create-carousel` skill used to write its slide map with the filenames in **backticks** (`` `slide-01.png` ``), which is invisible to a link scan. This sweep therefore judged every slide of a *shipped* carousel an orphan and trashed it; a later Sweep hard-deleted the lot. They were only recoverable because `carousel.pdf` happened not to be an image. The skills now emit `![[slide-01.png]]` embeds, but **do not rely on that** — a bundle must survive a record that forgets to link it.
   - If a basename is shared by 2+ files and that basename is referenced anywhere, treat ALL of them as referenced — Obsidian resolves attachments by basename and can't disambiguate; never guess.
   - Any reference to the basename, even at a different path, spares the image.
   - **Beware accidental protection.** Because a basename reference anywhere spares every file with that name, generic names (`slide-01.png`, `cover.png`) can be shielded by an unrelated note's twin. That means a bundle can look safe while its high-numbered slides (`slide-08.png`+, which have no twin) are exposed. Never read "most of the folder is referenced" as "the folder is fine" — check per file.
   - When unsure, keep.
5. **Action — trash with grace (never hard-delete):** create `_Triage/Trash/<date>/` if missing; move each orphan there preserving its relative path; append to `_Triage/Trash/manifest.json` an entry in the **canonical shape** (see below).
6. **Scale guard:** if candidates exceed 50 OR >10% of all vault images, that usually signals a detection miss — list the count + a sample and confirm ONCE before sweeping (proceed if confirmed). Below that, sweep without prompting.
7. **`--dry-run`:** report the candidates and move nothing.

Report the outcome at the top of the Step-4 block.

## The trash manifest: canonical schema

Append to `_Triage/Trash/manifest.json` an entry in the **canonical shape**:

```json
{
  "originalPath": "~Attachments/Writing/foo.png",
  "trashedPath": "_Triage/Trash/2026-07-13/~Attachments/Writing/foo.png",
  "reason": "orphaned-image",
  "deletedAt": "2026-07-13T14:22:05.000Z",
  "size": 5255336
}
```

**Use these exact keys.** This manifest has two writers — this skill and the Command Center Triage page — and they forked. The old `{from, to, deleted_at}` shape this skill used to write was silently broken: Restore matches on `trashedPath` (so those files could never be recovered) and Sweep reads `deletedAt` (so `new Date(undefined)` → `NaN` → they were never cleared either). 209 images were stuck in that state — neither restorable nor sweepable. Command Center now normalizes both shapes on read, but write the canonical one. The image stays restorable from the manifest. groom-vault only moves INTO trash — it never empties it (the 14-day grace sweep is the Triage page's job).

## Step 2.6: Flag non-note ballast (the evict op — propose only, never auto-move)

Images aren't the only non-notes that accumulate. A vault should hold *notes about* code, not the code itself — but cloned repos, node projects, and render bundles drift in and silently double the vault's apparent size, depth, and search noise (one real case: `Projects/sdd/research/_fetched/` held 597 md across 3 nested `.git/` repos — 41% of the whole vault). These are **evict** candidates: they leave the vault entirely.

Unlike orphaned images, ballast is **never actioned automatically** — destinations differ (a code repo, `~Attachments/`, or deletion) and the files can be large/irreversible. Detect and *report* for the user to place:

1. **Nested git clones** — any directory containing its own `.git/` below the vault root (`find <vault> -type d -name .git -not -path '*/.obsidian/*'`, excluding the vault's own root `.git`). Each is a vendored repo, not notes.
2. **Code/render projects** — directories with `package.json` / `node_modules/`, or bundles of `.mp4`/render assets (e.g. a Remotion `ice-video/` project). The vault keeps the md brief; the project lives in a code repo.
3. **Loose non-note files in odd places** — scripts (`.sh`, `.py`), lockfiles (`package-lock.json`), binaries, or `.json`/`.yml` config at the vault root or a notes folder (not `~Attachments/`, `.obsidian/`, `.specify/`, or a skill's own dir).

Report each with its size and a suggested destination (`→ code repo`, `→ ~Attachments/`, `→ delete`). Surface the total MB reclaimed. Move nothing without explicit per-item confirmation.
