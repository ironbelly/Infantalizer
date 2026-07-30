# Research Completeness + Cross-Validation Report

**Task:** TASK-RF-prep-chapter-materialize-20260709-004725
**Topic:** `/laf:prep` v-next Stage 0 — chapter materialization + `chapter-manifest.yaml`
**Analysis type:** completeness-verification + cross-validation (combined)
**Date:** 2026-07-09
**Analyst:** rf-analyst (single instance; no partition)
**Files analyzed (4):** `research/01-file-inventory-and-edits.md`, `research/02-boundary-contract-and-verification.md`, `research/03-skill-authoring-spec.md`, `research/04-mdtm-template-and-gate.md`
**Driving spec:** `.dev/brainstorms/20260709T001338Z-prep-chapter-ingestion/merged-requirements.md`
**Adversarial stance:** spot-checked load-bearing claims against live repo files (citations below).

---

## Method

- Read all 4 research files completely + `research-notes.md` + the driving spec (§1–§15).
- Spot-checked every contested / load-bearing fact against the actual repo (not just cross-file agreement):
  the `.claude/` mirror mechanism, `check_boundary.py` `classify()` default, the VENDOR row format +
  em-dash codepoint, the AC6 command (RAN it), prep-cordinator stage numbering, prep SKILL.md §1,
  path-contract §4 read-set + §5 write-ownership, the command file.
- No web research (none authorized; none needed — all facts are on-disk).

---

## Verdict: **PASS (conditional)** — 0 CRITICAL gaps; 1 IMPORTANT contradiction (mirror action for the new skill); 4 MINOR gaps/citation-drift.

The research set is **sufficient to build a per-file / per-edit checklist for all 8 BOM rows and AC1–AC7.**
Breadth is complete; cross-validation surfaced **one substantive contradiction** (File 01 vs File 02 on
the `.claude/` mirror ACTION for the new skill) that must be resolved in File 01's favor (verified against
the live repo), plus minor line-number citation drift in File 01 that is anchored to stable section
headers and therefore non-blocking. No CRITICAL gap blocks synthesis/task-building.

---

## A. Breadth Audit — §11 Bill-of-Materials (8 rows) → research coverage

| # | BOM file | Provenance | Edit-locus documented? | Covered by | Verdict |
|---|----------|-----------|------------------------|-----------|---------|
| 1 | `skills/chapter-materialize/SKILL.md` | NEW NATIVE | YES — 13-section outline, frontmatter verbatim, house-style rules | 03 §A/§B; 01 §7 (Rule-E clean); 02 Q1–Q4 | COVERED |
| 2 | `skills/chapter-materialize/resources/boundary-rules.yaml` | NEW NATIVE | YES — annotated YAML skeleton (5 layer keys + confidence mirror) | 03 §E; 02 Q2 (glob covers, no own row) | COVERED |
| 3 | `agents/prep-cordinator.md` | NATIVE `laf_sha256=—` | YES — `skills:` line after L11, STAGE-0 fenced insert after L46, count-words L20/L25/L44, gate refs | 01 §2; 04 Step 2c/3 | COVERED |
| 4 | `skills/prep/SKILL.md` | NATIVE | YES — §1 note after L19; Resources pointer after L125 | 01 §1; 04 Step 2d | COVERED |
| 5 | `skills/prep/resources/path-contract.md` | NATIVE | YES — §4 note, +3 §5 rows, NEW §6; §1/§2/§4 read-set byte-unchanged | 01 §3; 02 Q6; 04 Step 2d | COVERED |
| 6 | `source/README.md` | BUILD-NEW | YES — manifest + `.raw/` subsection (after L7 or EOF) | 01 §4 | COVERED |
| 7 | `.claude/commands/laf/prep.md` | NATIVE mirror (canonical) | YES — arg-hint L3; `--source-mode` body L18-20 | 01 §5; 04 Step 4 P3.3 | COVERED |
| 8 | `laf-adaptation/VENDOR.md` | NATIVE | YES — exact row, U+2014, NATIVE-group placement | 02 Q4; 01 §6 | COVERED |

**Breadth verdict: 8/8 BOM rows COVERED with a concrete, buildable edit locus.**

---

## B. Breadth Audit — Acceptance Criteria AC1–AC7 → research coverage

| AC | Requirement | Covered by | Buildable checklist item? | Verdict |
|----|-------------|-----------|---------------------------|---------|
| AC1 | Mode A dir + Mode B monolith → identical `ch-<NN>.txt` + manifest, no pre-split | 03 §B5 (precedence), §B6 (layers), §D (manifest schema) | YES | COVERED |
| AC2 | `Books/LWW/` (split + monolith both present) does NOT auto-pick → mode question | 03 §B5.4 + §C rows (mode ambiguity); spec §3 precedence carried verbatim | YES | COVERED |
| AC3 | Re-run vs `source/narnia/` + `source/tolkien/` adopts, zero byte rewrites (Mode C) | 03 §B10 (adopt), §D.1 (`provenance.class: ADOPTED`) | YES | COVERED |
| AC4 | No non-CERTAIN `ch-NN.txt` before greenlight; single-signal never CERTAIN | 03 §B6 confidence rule + §B7 deferred-write invariant; 04 Step 2b | YES | COVERED |
| AC5 | Every manifest row: confidence+provenance+`needs_human_review`; every discard = `normalization_event`+risk | 03 §D + §D.1 (explicit "missing any = release-blocking defect") | YES | COVERED |
| AC6 | `check_boundary.py` exit 0; `rewrite_phase_reads` byte-unchanged; no 9th file; no 2nd script | 02 Q1 (no script edit), Q5 (exact cmd+cwd, RAN), Q6 (read-set byte-stability check) | YES — **command is concrete + verified** | COVERED |
| AC7 | Greenlight cannot CONFIRM while any ambiguity/high-risk loss unresolved | 03 §B5/B8; 04 Step 2b (+1 checklist line), Step 2d §6 | YES | COVERED |

**AC verdict: 7/7 ACs COVERED.** The four adversarial sub-checks the spawn demanded all PASS:
- **Every BOM file's exact edit locus documented?** YES (Table A).
- **Manifest schema captured verbatim?** YES — 03 §D reproduces spec §5 lines 106–154 byte-for-byte
  (verified against spec; enum lists, comments, and field order match).
- **Verification command (AC6) concrete?** YES — `cd laf-adaptation && uv run python scripts/check_boundary.py`,
  exit 0, `BOUNDARY CONTRACT: PASS`. **I RAN it — passes today (baseline captured, see §D).**
- **Mirror action for the new skill unambiguous?** **NO — this is the one IMPORTANT contradiction.** See §C-1.

---

## C. Cross-Validation — where two files touch the same fact, do they AGREE?

The spawn named five shared facts to cross-check. Each was spot-checked against the live repo, not merely
compared for inter-file agreement.

### C-1. `.claude/` mirror mechanism + the ACTION for the NEW skill  — ⚠ **CONTRADICTION (IMPORTANT)**

**On the mechanism, the files AGREE and are CORRECT.** File 01 §0 states the `.claude/` tree mirrors
`laf-adaptation/` via **symlinks** (per-skill dir symlinks; per-file agent symlinks), so editing the
`laf-adaptation/` source auto-updates the mirror. File 02 Q7 also says the mirror is a "manual convention,
not machine-enforced." **VERIFIED against repo:**
- `.claude/skills/prep -> ../../laf-adaptation/skills/prep` (symlink) — and ALL 18 `.claude/skills/*`
  entries are dir symlinks (`ls -la .claude/skills`).
- `.claude/agents/prep-cordinator.md -> ../../laf-adaptation/agents/prep-cordinator.md` (symlink) — and all
  17 `.claude/agents/*.md` are file symlinks.
- `.claude/commands/laf/prep.md` is a **real file** (no `laf-adaptation/commands/` dir exists) — confirmed.
File 01's MIRROR MAP is factually correct and is the load-bearing operational finding.

**The CONTRADICTION is on the ACTION for the new `chapter-materialize` skill dir:**
- **File 01 §7 / §0** (CORRECT): after authoring, **create a symlink** `.claude/skills/chapter-materialize
  -> ../../laf-adaptation/skills/chapter-materialize` to match the existing per-skill-symlink convention.
  The dir symlink then covers `resources/` automatically; **no copy**.
- **File 02 Q7** (INCORRECT/misleading): recommends "**copy** the new skill dir into the `.claude/` mirror
  in lockstep and **`diff -r laf-adaptation/skills/chapter-materialize .claude/skills/chapter-materialize`**."
  A byte-copy is the WRONG action for this repo — every sibling skill is a symlink, not a copy; a `diff -r`
  of a symlink target against itself is degenerate, and a copied dir would DRIFT from source on future edits
  (the exact failure the symlink scheme avoids). File 04 Step 4 (P2.3, P3.x) inherits File 02's framing
  ("mirror both to `.claude/skills/chapter-materialize/`", "lockstep") — ambiguous between copy and symlink.

**Impact:** IMPORTANT, not CRITICAL. If the builder follows File 02/04's "copy + diff -r" literally, the
mirror will initially work but silently drift on later edits, and the `diff -r` check is meaningless. The
correct, repo-consistent action is a single `ln -s`. This MUST be disambiguated in the task file: the
`.claude/skills/chapter-materialize` action is **create a symlink**, not copy; and the "`diff -r` mirror
parity" verification item (File 02 Q7 mitigation, echoed in File 04 P5.2) should be replaced with a
**symlink-existence + target-resolution check** (e.g. `readlink .claude/skills/chapter-materialize`
resolves to the new source dir).

**Resolution direction (verified):** adopt File 01's symlink action; discard File 02's copy/`diff -r`
mitigation. File 02 is otherwise authoritative on the boundary-contract mechanics (§C-2..C-5 all agree
with it) — only its Q7 mirror-remediation is wrong for this repo's symlink scheme.

### C-2. `check_boundary.py` "no edit needed" (classify() default NATIVE) — ✅ **AGREE + VERIFIED**

Both File 01 (PATTERNS, §2) and File 02 (Q1) claim `chapter-materialize` auto-classifies NATIVE with ZERO
script edit, because `classify()` returns `"NATIVE"` by default for any non-upstream skill not in
`BUILD_NEW_SKILLS`, and `NATIVE_SKILLS` is NOT an allowlist. **VERIFIED against
`laf-adaptation/scripts/check_boundary.py`:**
- L46 `NATIVE_SKILLS = {"adaptation-tiers", "adaptation-rules", "source-fidelity"}`;
  L47 `BUILD_NEW_SKILLS = {"adaptation-safety"}`.
- `classify()` skills branch: `if sk in BUILD_NEW_SKILLS: return "BUILD-NEW"` else `return "NATIVE"`
  (the `return "NATIVE"` default fires for `chapter-materialize`). `NATIVE_SKILLS` is never read in
  `classify()`.
- Proof it is not an allowlist: `skills/prep/**` and `skills/thematic-fidelity/**` are NATIVE rows yet
  absent from `NATIVE_SKILLS` — confirmed in VENDOR.md L122–123.
Both files' warning "do NOT add `chapter-materialize` to `NATIVE_SKILLS`" is correct and consistent.
**No contradiction.**

### C-3. prep-cordinator stage-renumber — ✅ **AGREE (01 flags; 04 resolves)** + VERIFIED

File 01 §2 flags every locus that mentions the stage count and explicitly defers the renumber decision to
File 04. File 04 Step 3 RESOLVES it: **Approach A** — prepend a new `STAGE 0`, keep `STAGE 1..8`
byte-identical (Q-gate stays STAGE 5, greenlight stays STAGE 7), so no downstream renumber and no
"Stage 5"/"Stage 7" note breakage. **This is not a contradiction — it is a clean flag→resolve handoff.**
**VERIFIED against `laf-adaptation/agents/prep-cordinator.md`:** 98 lines; `skills:` block L5–11 (6 entries);
"8-stage" at L20; "8-section procedure" at L25; `## The 8 stages` at L44; fenced block STAGE 1..8 with
`STAGE 5 Q-GATE` and `STAGE 7 GREENLIGHT`. File 04's nuance is correct and important: **L25's "8-section"
refers to the prep SKILL's §-count (still 8), so it must NOT be changed to 9** — only the agent's
stage-count words (L20, and the L44 heading) become 9. This distinction is captured accurately.

### C-4. VENDOR row format — ✅ **AGREE + VERIFIED byte-exact**

File 01 §6 and File 02 Q4 both prescribe `| skills/chapter-materialize/** | NATIVE | — | — |` with the
em-dash = **U+2014**, single `/**` glob row (not per-file), placed in the NATIVE group. **VERIFIED:**
- `NO_HASH = "—"` at `check_boundary.py:50`.
- The two hash cells in the live `skills/adaptation-rules/**` row are **U+2014** (`0x2014`, bytes
  `e2 80 94`) — confirmed via `od`/python codepoint dump; the `-` inside `adaptation-rules` is ASCII
  U+002D, distinct.
- Existing NATIVE rows are single `/**` globs (VENDOR.md L118–123). File 02 Q2 verified the glob covers
  `resources/boundary-rules.yaml` (no separate row) via `manifest_covers()` + Rule F′ skipping NATIVE dirs.
**No contradiction; both files agree with each other and the code.**

### C-5. VENDOR row placement — ⚠ **MINOR discrepancy (cosmetic, non-blocking)**

File 01 §6 suggests inserting "right after line 118 (`skills/adaptation-rules/**`)". File 02 Q4 recommends
"the end of the NATIVE block, between L123 `skills/thematic-fidelity/**` and L124 `agents/chronicler.md`."
Both are inside the NATIVE group and both pass verify (File 02 Q4 confirmed verify does NOT check row
ordering). **Not a substantive contradiction** — either placement is verify-clean. Builder should pick one;
File 02's "end of NATIVE block" is marginally cleaner (keeps the hand-appended-rows pattern consistent).

---

## D. Evidence Quality + Verification Reproduction

| File | Evidenced claims | Unsupported claims | Rating |
|------|------------------|--------------------|--------|
| 01 file-inventory | Nearly all cited to `file:line` + `ls -la` evidence for symlinks; MIRROR MAP has a live evidence block | Line-number drift (§E-2) in a few §3 cites | Strong |
| 02 boundary-contract | Exceptional — every claim cites `check_boundary.py:line` with code excerpts; RAN the AC6 check | Q7 mitigation is wrong-for-repo (§C-1), not unsupported | Strong |
| 03 skill-authoring | Manifest schema + failure table carried verbatim w/ spec line cites; house-style facts cite model skills | None material | Strong |
| 04 mdtm-template | Template rules cite `02_..._template.md` line ranges; numbering resolution is evidence-based | Inherits 02's ambiguous "mirror both to .claude/" framing (§C-1) | Strong |

**AC6 command REPRODUCED by this analyst (adversarial re-run):**
```
$ cd laf-adaptation && uv run python scripts/check_boundary.py
BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.
EXIT_CODE=0
```
File 02 Q5's captured baseline is accurate and reproducible today. The AC6 verification item is concrete
and correct.

---

## E. Documentation-Staleness / Line-Number Drift Check

The research files cite the driving spec (a design doc, not code) and live repo files. No `[STALE DOC]` /
`[CODE-CONTRADICTED]` conditions found — the spec is the authoritative design source and the repo files
match the research descriptions structurally. Two minor citation-drift items (both anchored to stable
section headers, so non-blocking):

- **E-1 (MINOR):** File 01 §3 says path-contract `## 5. Write-ownership` is at "line 76" and the first
  write-ownership row (`work/prep/<slug>/*`) at "line 80." **Actual (verified):** `## 5.` heading is at
  **L75**; the `work/prep/<slug>/*` row is at **L79** (rows span L79–82). File 02 Q6 independently and
  CORRECTLY places `## 5.` at L75. Off-by-one in File 01; the EDIT-B locus ("insert after the
  `work/prep/<slug>/*` row") is still unambiguous because it anchors to row content, not the raw number.
- **E-2 (MINOR):** File 01 §3 line 110 labels the chronicler `kb/canon/*` row as "line 82," but verified it
  is at **L82** in a 4-row table that File 01 elsewhere describes as spanning "80–82" (actually 79–82). The
  table has 4 body rows, not 3. Non-blocking (builder inserts the 3 new rows relative to the
  `work/prep/<slug>/*` row, which is correctly identified).

Neither drift affects buildability: all EDIT loci in File 01 are additionally anchored to stable `## §N`
headers and to row-content strings, so a builder editing against section headers (as the path-contract's
own "import by reference" convention encourages) is not misled.

---

## F. Compiled Gaps

### CRITICAL (block synthesis/task-building)
- **NONE.**

### IMPORTANT (must be resolved in the task file before build)
- **G-1 — Mirror ACTION for the new skill is contradictory (§C-1).** File 01 says *create a symlink*;
  File 02 Q7 + File 04 say *copy + `diff -r`*. The repo uses per-skill **symlinks** (verified). The task
  file MUST specify: **create `.claude/skills/chapter-materialize` as a symlink** to
  `../../laf-adaptation/skills/chapter-materialize` (matching all 18 existing skill symlinks), and REPLACE
  the "`diff -r` mirror parity" verification item with a **`readlink`/symlink-resolution check**. Do NOT
  copy the dir (it would drift). *Source: File 01 §0/§7 (correct) vs File 02 Q7 + File 04 P2.3/P5.2.*

### MINOR (fix but non-blocking)
- **G-2 — path-contract §5 line-number drift (§E-1):** File 01 cites `## 5.` at L76 / first row at L80;
  actual L75 / L79. Anchor edits to row content, not raw line numbers.
- **G-3 — path-contract write-ownership table row count (§E-2):** File 01 implies 3 body rows; actual 4.
  Non-blocking (new rows inserted relative to the `work/prep/<slug>/*` row).
- **G-4 — VENDOR row placement (§C-5):** File 01 (after L118) vs File 02 (end of NATIVE block). Either is
  verify-clean; pick one (File 02's is marginally cleaner).
- **G-5 — File 04's "mirror both to `.claude/…`" phrasing (§C-1 knock-on):** P2.3/P3.x say "mirror" without
  specifying symlink-vs-copy. Disambiguate to "symlink" consistent with G-1.

---

## G. Contradiction Summary (both versions surfaced, never resolved silently)

| # | Fact | File A says | File B says | Repo truth (verified) | Severity |
|---|------|-------------|-------------|------------------------|----------|
| 1 | New-skill mirror action | 01: create symlink | 02 Q7 / 04: copy + `diff -r` | Symlinks everywhere → **symlink is correct** | IMPORTANT |
| 2 | VENDOR row placement | 01: after L118 | 02 Q4: end of NATIVE block | Ordering not checked → both valid | MINOR |
| 3 | path-contract `## 5.` line | 01: L76 | 02 Q6: L75 | **L75** → File 02 correct | MINOR |

All other cross-checked facts (mirror MECHANISM, classify() default, VENDOR row FORMAT + em-dash,
manifest schema, stage-numbering resolution, AC6 command) **AGREE across files and match the repo.**

---

## H. Depth Assessment

**Expected:** Deep (8-file BOM, boundary-contract subsystem, multi-signal split mechanism, MDTM gate mapping).
**Achieved:** Deep — the set delivers per-file edit loci, verbatim manifest schema + 16-row failure table,
code-traced boundary mechanics with excerpts, a RAN AC6 baseline, a resolved three-way stage-numbering map,
and a full phase/QA-gate plan. Investigation depth matches the tier.
**Missing depth elements:** None material. The one gap is a *contradiction to resolve* (G-1), not a
*missing investigation*.

---

## I. Recommendations (for the builder / task-builder)

1. **Resolve G-1 authoritatively in the task file:** the `.claude/skills/chapter-materialize` action is
   **`ln -s ../../laf-adaptation/skills/chapter-materialize`** (create a symlink), NOT a copy. Replace any
   "`diff -r` mirror parity" verification with a `readlink` symlink-resolution check. Propagate to File 04
   P2.3 / P3.x / P5.2 wording.
2. **Anchor path-contract edits to section headers + row content, not File 01's raw line numbers**
   (G-2/G-3); prefer File 02's L75 for `## 5.`.
3. **VENDOR row:** use File 02's placement (end of NATIVE block, before first BUILD-NEW row); byte-exact
   `| skills/chapter-materialize/** | NATIVE | — | — |` with U+2014 (G-4).
4. Carry the manifest schema (03 §D) and failure table (03 §C) VERBATIM — do not paraphrase (release-grade
   contract).
5. Keep the AC6 verification item exactly as File 02 Q5 states it: `cd laf-adaptation && uv run python
   scripts/check_boundary.py`, assert exit 0 + `BOUNDARY CONTRACT: PASS`.
6. Preserve the L25 "8-section procedure" wording (prep SKILL §-count) while changing agent stage-count
   words to 9 (File 04's distinction — do not over-apply the renumber).

---

## VERDICT: **PASS (conditional on resolving G-1 in the task file)**

- Breadth: **8/8 BOM rows + 7/7 ACs COVERED** with buildable, verified edit loci.
- Cross-validation: **1 IMPORTANT contradiction (G-1: new-skill mirror action — symlink vs copy)** must be
  resolved in File 01's (verified-correct) direction; **3 MINOR items** (G-2..G-5) are non-blocking
  citation/placement drift.
- **0 CRITICAL gaps.** The research is sufficient to build the task file; the builder must encode the
  symlink action (G-1) unambiguously and prefer verified line numbers where files disagree.

### Structured gap list (for the conditional)
- **IMPORTANT:** G-1 — new-skill `.claude/` mirror = **symlink** (not copy); fix File 04 mirror/parity items.
- **MINOR:** G-2 (path-contract §5 = L75/L79); G-3 (4 write-ownership rows, not 3); G-4 (VENDOR placement);
  G-5 (File 04 "mirror" phrasing → "symlink").



