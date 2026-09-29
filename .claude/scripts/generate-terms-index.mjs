#!/usr/bin/env node
// Terms.md — one grep-able line per term, pointing at every note that carries it.
//
// THE PROBLEM THIS SOLVES, measured on 2026-08-29 against a 2,603-note vault:
// full-vault greps are FAST (0.85-0.98s), so speed was never the issue. RECALL is.
// `grep -ri "eval rubric"` returned ZERO while six notes on eval rubrics existed,
// because they say `rubric-grading`, not "eval rubric". `grep -ri "database
// partitioning"` returned zero while `System Design - Study Notes.md` covers it.
// Prose search only matches the words you happened to guess.
//
// The fix is not a vector index. The vault already carries a hand-written semantic
// layer that nothing indexes: `keywords`, `entities` and `claims` on ~405 notes, and
// `tags` on 793. Those are the author's own words for what a note is ABOUT, which is
// exactly what a fuzzy query is reaching for. Collapsing them into one file turns a
// 2,901-file scan into a single grep whose hits name their notes.
//
// NOT a replacement for Topics.md. That one reads `tags` only and answers "what
// concept pages exist, and what sits under them" — a curation view. This one answers
// "which notes touch this term" — a lookup. Different questions, both worth having.
//
// Rebuild:  node .claude/scripts/generate-terms-index.mjs   (from the vault root)

import { readFileSync, writeFileSync, readdirSync, statSync } from "node:fs";
import { join, relative, basename, extname } from "node:path";

const VAULT = process.env.VAULT_DIR || process.cwd();   // run from the vault root, or set VAULT_DIR
const OUT = join(VAULT, "Terms.md");

// Machinery, templates and attachments carry no authored meaning. ~Archive DOES stay
// in: "where did I write about X" is most often about work that is already finished,
// and the `~Archive/` in the path labels it without needing a separate section.
const SKIP = new Set([
  ".obsidian", ".git", ".claude", ".serena", ".specify", "_claude", "node_modules",
  "_Templates", "~Templates", "_Attachments", "~Attachments", "_Triage",
]);

// Fields holding the author's own words for what a note is about. `claims` is listed
// separately below because its values are whole sentences, not terms.
const TERM_FIELDS = ["tags", "keywords", "entities"];

function walk(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    if (SKIP.has(entry)) continue;
    const p = join(dir, entry);
    let st;
    try { st = statSync(p); } catch { continue; }
    if (st.isDirectory()) walk(p, out);
    else if (extname(entry) === ".md") out.push(p);
  }
  return out;
}

// Frontmatter only, and only the fields above. A real YAML parse would pull in a
// dependency to read six keys off a file whose front block is machine-written by our
// own skills; the two shapes below are the only two those skills emit.
function parseFront(text) {
  if (!text.startsWith("---")) return null;
  const end = text.indexOf("\n---", 3);
  if (end === -1) return null;
  return text.slice(4, end);
}

// Line-based on purpose. The regex form of this (`^field:\s*$([\s\S]*?)(?=^\S|$)`)
// silently returns nothing: under /m the `$` in that lookahead matches at the end of
// EVERY line, so the capture terminates at offset zero. It reported 0 claims across a
// vault holding 405 of them, and failed open rather than erroring.
function readList(head, field) {
  const lines = head.split("\n");
  const start = lines.findIndex((l) => l.startsWith(`${field}:`));
  if (start === -1) return [];

  const rest = lines[start].slice(field.length + 1).trim();
  if (rest.startsWith("[")) return rest.replace(/^\[|\]$/g, "").split(",");
  if (rest) return [rest];               // scalar, e.g. `tags: draft`

  const out = [];
  for (const line of lines.slice(start + 1)) {
    const m = line.match(/^\s+-\s+(.+)$/);
    if (!m) break;                        // first non-item line ends the block
    out.push(m[1]);
  }
  return out;
}

const clean = (s) => s.trim().replace(/^['"]|['"]$/g, "").trim();

const files = walk(VAULT);
const terms = new Map();   // term -> Map<field, Set<noteName>>
const claims = new Map();  // claim -> Set<noteName>
let withTerms = 0;

for (const file of files) {
  let head;
  try { head = parseFront(readFileSync(file, "utf8")); } catch { continue; }
  if (!head) continue;

  const name = basename(file, ".md");
  let any = false;

  for (const field of TERM_FIELDS) {
    for (const raw of readList(head, field)) {
      const term = clean(raw).toLowerCase();
      // Single characters and bare numbers are noise; they match everything.
      if (term.length < 2 || /^\d+$/.test(term)) continue;
      if (!terms.has(term)) terms.set(term, new Map());
      const byField = terms.get(term);
      if (!byField.has(field)) byField.set(field, new Set());
      byField.get(field).add(name);
      any = true;
    }
  }

  for (const raw of readList(head, "claims")) {
    const c = clean(raw);
    if (c.length < 8) continue;
    if (!claims.has(c)) claims.set(c, new Set());
    claims.get(c).add(name);
    any = true;
  }

  if (any) withTerms++;
}

// A term on one note still earns its line: the whole point is finding the ONE note
// that used a word you half-remember. Frequency ordering would bury exactly that.
const sorted = [...terms.entries()].sort(([a], [b]) => a.localeCompare(b));

const lines = [];
lines.push(`---
type: index
lifespan: durable
description: Every tag, keyword and entity in the vault, and the notes carrying it — one grep-able line per term
tags: [index, terms, lookup, generated]
generated-by: .claude/scripts/generate-terms-index.mjs
cssclasses:
  - brief
---

# Terms

> [!warning] **Generated. Do not edit by hand.**
> Rebuild with \`node .claude/scripts/generate-terms-index.mjs\` from the vault root.

> [!tip] **Grep this file instead of the vault.**
> Prose search only matches words you guessed right: \`grep -ri "eval rubric"\` finds nothing
> while six notes on the subject say \`rubric-grading\`. One \`grep -i rubric Terms.md\` finds
> them, because every term sits on its own line beside the notes that carry it.
>
> This is a **lookup** — which notes touch a term. For **curation** — which concept pages
> exist and what sits beneath them — a Topics.md curation page, if the vault keeps one.

**${sorted.length} terms** and **${claims.size} claims** across **${withTerms} notes**, from \`tags\`, \`keywords\`, \`entities\` and \`claims\` frontmatter. Notes without those fields do not appear here — that gap is real and is the reason this index supplements a vault-wide grep rather than replacing it.

## Terms
`);

for (const [term, byField] of sorted) {
  const notes = new Set();
  for (const set of byField.values()) for (const n of set) notes.add(n);
  const fields = [...byField.keys()].join("/");
  const links = [...notes].sort().map((n) => `[[${n}]]`).join(", ");
  lines.push(`- \`${term}\` · ${fields} · ${notes.size} — ${links}`);
}

if (claims.size) {
  lines.push(`
## Claims

One line per asserted claim. These are full sentences, so a grep for any word inside one hits it — which is what makes them the highest-recall part of this file.
`);
  for (const [claim, notes] of [...claims.entries()].sort(([a], [b]) => a.localeCompare(b))) {
    lines.push(`- \`${claim}\` — ${[...notes].sort().map((n) => `[[${n}]]`).join(", ")}`);
  }
}

writeFileSync(OUT, lines.join("\n") + "\n");
console.log(`Terms.md: ${sorted.length} terms, ${claims.size} claims, ${withTerms}/${files.length} notes → ${relative(VAULT, OUT)}`);
