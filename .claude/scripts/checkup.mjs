#!/usr/bin/env node
// checkup.mjs — run every read-only health check over the vault and say what needs attention.
//
//   node .claude/scripts/checkup.mjs           from the vault root
//   node .claude/scripts/checkup.mjs --json
//   VAULT_DIR=/path/to/vault node .claude/scripts/checkup.mjs
//
// A vault-only cut of the kaiju checkup. The original also graded published articles, skill
// usage and upstream drift; those need the kaiju repo. What is left is what any vault can answer:
// notes without a lifespan, wikilinks that resolve to nothing, canvases that do not parse,
// expired ephemera still in the live tree, how stale Terms.md is, how long since the last groom.
//
// It changes nothing, on purpose. Every fix is named and run separately.

import { existsSync, statSync, readFileSync, readdirSync } from "node:fs";
import { join, relative, basename, extname } from "node:path";

const VAULT = process.env.VAULT_DIR || process.cwd();
const JSON_OUT = process.argv.includes("--json");
const SKIP = new Set([".obsidian", ".git", ".claude", "node_modules", "~Templates", "_Templates"]);

function walk(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    if (SKIP.has(entry)) continue;
    const p = join(dir, entry);
    let st; try { st = statSync(p); } catch { continue; }
    if (st.isDirectory()) walk(p, out); else out.push(p);
  }
  return out;
}
function front(text) {
  if (!text.startsWith("---")) return null;
  const end = text.indexOf("\n---", 3);
  return end === -1 ? null : text.slice(4, end);
}

// Drop fenced blocks (line-based, so a ```` fence around a ``` sample pairs correctly) and inline code.
function stripCode(text) {
  const out = []; let fence = null;
  for (const line of text.split("\n")) {
    const m = line.match(/^\s*(`{3,})/);
    if (m) { if (!fence) fence = m[1].length; else if (m[1].length >= fence) fence = null; continue; }
    if (!fence) out.push(line.replace(/`[^`]*`/g, ""));
  }
  return out.join("\n");
}

const files = walk(VAULT);
const notes = files.filter((f) => extname(f) === ".md");
const rel = (f) => relative(VAULT, f);
const checks = [];
const add = (name, status, detail, fix) => checks.push({ name, status, detail, fix });

// ── 1. every note declares a lifespan ────────────────────────────────────────
{
  const missing = notes.filter((f) => {
    if (/^(README|LICENSE)/.test(basename(f)) || rel(f).startsWith("_Triage/")) return false;
    const fm = front(readFileSync(f, "utf8"));
    return !fm || !/^lifespan:/m.test(fm);
  });
  add("Notes declare a lifespan", missing.length ? "attention" : "ok",
    missing.length ? `${missing.length} note(s) without one: ${missing.slice(0, 5).map(rel).join(", ")}${missing.length > 5 ? ", …" : ""}` : `all ${notes.length} stamped`,
    "add `lifespan: ephemeral | project | durable` — the author decides, never a script");
}

// ── 2. wikilinks resolve (any file type; ~ and _ folders are real targets) ───
{
  const byBase = new Map();
  const byPath = new Set();
  for (const f of files) {
    const r = rel(f); byPath.add(r); byPath.add(r.replace(/\.md$/, ""));
    const b = basename(f);
    (byBase.get(b) || byBase.set(b, []).get(b)).push(r);
    const noExt = b.replace(/\.md$/, "");
    (byBase.get(noExt) || byBase.set(noExt, []).get(noExt)).push(r);
  }
  const broken = [];
  for (const f of notes) {
    // fenced and inline code are not links — Obsidian does not resolve them, and the component
    // reference is full of illustrative ones
    const text = stripCode(readFileSync(f, "utf8"));
    for (const m of text.matchAll(/!?\[\[([^\]|#]+?)(?:[#|\\][^\]]*)?\]\]/g)) {
      const target = m[1].trim();
      if (!target || byPath.has(target) || byBase.has(target) || byBase.has(basename(target))) continue;
      broken.push(`${rel(f)} → [[${target}]]`);
    }
  }
  add("Wikilinks resolve", broken.length ? "attention" : "ok",
    broken.length ? `${broken.length} broken: ${broken.slice(0, 4).join("; ")}${broken.length > 4 ? "; …" : ""}` : "every link lands on a file",
    "fix the link or restore the file; aliases inside tables escape their pipe as [[Note\\|Alias]] and are not broken");
}

// ── 3. canvases parse ─────────────────────────────────────────────────────────
{
  const canvases = files.filter((f) => extname(f) === ".canvas");
  const bad = [];
  for (const c of canvases) {
    try {
      const j = JSON.parse(readFileSync(c, "utf8"));
      const ids = new Set((j.nodes || []).map((n) => n.id));
      for (const e of j.edges || []) if (!ids.has(e.fromNode) || !ids.has(e.toNode)) throw new Error(`edge ${e.id} dangles`);
    } catch (e) { bad.push(`${rel(c)} (${e.message})`); }
  }
  add("Canvases parse", bad.length ? "attention" : "ok",
    bad.length ? bad.join("; ") : `${canvases.length} canvas file(s), all valid JSON with resolved edges`,
    "open the file; a dangling edge fails silently in Obsidian");
}

// ── 4. expired ephemera still in the live tree ───────────────────────────────
{
  const today = new Date().toISOString().slice(0, 10);
  const expired = notes.filter((f) => {
    if (rel(f).startsWith("~Archive/")) return false;
    const fm = front(readFileSync(f, "utf8")) || "";
    const exp = fm.match(/^expires:\s*["']?(\d{4}-\d{2}-\d{2})/m)?.[1];
    return exp && exp < today;
  });
  add("Ephemera past their expiry", expired.length ? "note" : "ok",
    expired.length ? `${expired.length} note(s): ${expired.slice(0, 4).map(rel).join(", ")}` : "nothing overdue",
    "/groom vault --dry-run proposes the archive moves");
}

// ── 5. Terms.md freshness ────────────────────────────────────────────────────
{
  const terms = join(VAULT, "Terms.md");
  if (!existsSync(terms)) add("Terms.md lookup", "note", "not generated yet", "node .claude/scripts/generate-terms-index.mjs");
  else {
    const t = statSync(terms).mtimeMs;
    const newer = notes.filter((f) => basename(f) !== "Terms.md" && statSync(f).mtimeMs > t).length;
    add("Terms.md lookup", newer > 0 ? "note" : "ok", newer > 0 ? `${newer} note(s) written since it was built` : "current", "node .claude/scripts/generate-terms-index.mjs");
  }
}

// ── 6. how long since the vault was groomed ──────────────────────────────────
{
  const trash = join(VAULT, "_Triage/Trash");
  let days = null;
  if (existsSync(trash)) days = Math.floor((Date.now() - statSync(trash).mtimeMs) / 864e5);
  add("Vault grooming", days === null ? "note" : days > 45 ? "attention" : "ok",
    days === null ? "never run" : `last sweep about ${days} day(s) ago`, "/groom vault --dry-run");
}

// ── report ───────────────────────────────────────────────────────────────────
if (JSON_OUT) { console.log(JSON.stringify(checks, null, 2)); process.exit(0); }
const ICON = { ok: "ok  ", attention: "LOOK", note: "note" };
const needs = checks.filter((c) => c.status === "attention");
const nts = checks.filter((c) => c.status === "note");
console.log("");
for (const c of checks) console.log(`  ${ICON[c.status]}  ${c.name.padEnd(30)} ${c.detail}`);
console.log("");
if (!needs.length && !nts.length) { console.log("Nothing needs attention."); process.exit(0); }
if (needs.length) { console.log(`${needs.length} thing(s) to look at:\n`); for (const c of needs) console.log(`  ${c.name}\n    ${c.detail}\n    → ${c.fix}\n`); }
if (nts.length) { console.log("Worth knowing, not urgent:\n"); for (const c of nts) console.log(`  ${c.name} — ${c.detail}  → ${c.fix}`); console.log(""); }
console.log("Nothing here changed anything. Every fix above is a separate, deliberate command.");
