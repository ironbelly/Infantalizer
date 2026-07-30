# QA Verification — M3 Structural Round (post-fix re-verify)

**Topic:** chapter-materialize Stage-0 skill authoring — M3 final-gate fix verification
**Date:** 2026-07-09
**Phase:** fix-cycle (structural re-verification)
**Role:** M3 structural verification round · **fix_authorization:** false (report-only)
**Repo root:** `/config/workspace/Infantalizer`

---

## Overall Verdict: PASS

All 12 findings (C-1, C-2, I-1..I-6, M-1..M-4) have a real corresponding edit in the actual files.
All hard invariants (manifest v1 schema block, 16-row failure table, two bolded sentences,
path-contract §4 fence + §2 table, prep-cordinator STAGE 1..8 lines, VENDOR single row + U+2014,
check_boundary.py) are byte-stable / intact. `check_boundary.py` exits 0 PASS. `boundary-rules.yaml`
parses (7 top keys). No new structural issue introduced. Two fix-report *reporting inaccuracies*
noted below — neither is a structural defect (the on-disk state is correct in both cases).

---

## Part 1 — Every finding has a real edit

| Finding | File | Verified edit (quoted anchor) | Result |
|---|---|---|---|
| **C-1** | SKILL.md Stage 0.2 rule 2 | L57–60: *"**Negative guard (both-present): rule 2 fires ONLY when the directory holds ≥2 non-canonical per-chapter files AND NO co-present dominating monolith. If BOTH a split chapter-set AND a dominating monolith are present … rule 2 does NOT fire — fall through to rule 4 (ambiguity → HALT-ask). Auto-detect must not guess `folder` in the both-present case.**"* + rule 4 L64 *"reached by construction"* | PASS |
| **C-2** | prep-cordinator `## Inputs` + STAGE 0 + SKILL.md 0.2 | prep-cord L38 `source_mode` row (`--source-mode <auto\|folder\|file\|adopt>`, optional, default `auto`, forwarded into inline dispatch); L80 *"passes both `source_path` and `source_mode` … into the inline chapter-materialize dispatch"*; SKILL.md L73–82 `--source-mode` → `input_mode` mapping table | PASS |
| **I-1** | prep-cordinator STAGE 0 + notes | L50 *"ensure source_path FIRST (elicit as a required input if --source omitted) BEFORE the /source-fidelity access declaration"*; L93–95 STAGE 1(a) *"re-affirms the same required `source_path` rather than eliciting a second time"* | PASS |
| **I-2** | SKILL.md Stage 0.3 + boundary-rules.yaml | SKILL L105–113 *"Mode A completeness … NO corroborating expected-count signal … COMPLETENESS is treated as UNCERTAIN and an `ambiguous_split` gate item is raised — 'possible incomplete split; operator confirm partial scope.'"*; yaml L88–91 `mode_a_completeness:` sub-block (`requires_corroborating_expected_count: true`; `on_single_source_count_only: raise_ambiguous_split`; matching `gate_message`) | PASS |
| **I-3** | SKILL.md Idempotency + path-contract §6 | SKILL L170–176 *"Adopted sets may have no raw source (`raw_path` / `.raw/` MAY be absent/null)"* (schema block NOT touched); path-contract §6 Retention L118 *"(materialized chapters only; adopted sets may have no `.raw/`)"* with U+2014 present | PASS |
| **I-4** | SKILL.md Stage 0.1 item 1 | L29–33 *"**URL `--source`:** when `--source` resolves to a URL … it is FETCHED to a local file under `source/<slug>/.raw/` FIRST, and that local path becomes the working `source_path`"* | PASS |
| **I-5** | prep-cordinator Stage 7 note | L127–131 *"**Two distinct `PENDING → CONFIRMED` flips happen at STAGE 7 — do not conflate them:** (1) … `50-greenlight.md` file `status:` … (2) … `chapter-manifest.review.status` … two different files and two different fields"* | PASS |
| **I-6** | invariants-review.md | 3 corrected citations present (`## Format normalization & fidelity`, `## Manifest output contract`, `## Idempotency, collisions, backward-compat`) | PASS |
| **M-1** | qa-input-inventory.md | `laf-adaptation/CLAUDE.md` row present (1 occurrence) | PASS |
| **M-2** | SKILL.md Manifest contract note | L218–222 *"**AC1 'identical' scope.** The canonical `ch-<NN>.txt` chapter TEXT is identical across Mode A … the **manifest itself is NOT byte-identical** … AC1 constrains the chapter text set, not the manifest's mode-specific provenance."* | PASS |
| **M-3** | boundary-rules.yaml `content_sanity` | L68–74 clarifying comment: `min_body_chars (500)` = HARD non-empty floor; `plausible_length_range.min_chars (1500)` = SANITY band floor; *"min_body_chars (hard reject) <= plausible_length_range.min_chars (soft flag) by design"* | PASS |
| **M-4** | SKILL.md + boundary-rules.yaml | SKILL L181 *"pick the canonical by **shortest filename → lexicographic order** on ties"*; yaml L55–57 matching *"byte-identity resolved by sha256 … pick the canonical by shortest filename, then lexicographic order on ties"* — the two now agree | PASS |

### C-1 behavioral trace (AC2 release-blocker) — genuinely routes Books/LWW to HALT

Under `--source-mode auto`, `Books/LWW/` (split `-1..-4.html` **AND** `…copy*.html` monolith both present):

1. **Rule 1 adopt** — no `source/<slug>/ch-*.txt` exists → skip.
2. **Rule 2 folder** — negative guard fires: split-set AND dominating monolith both present → **rule 2 does NOT fire** → fall through.
3. **Rule 3 file** — `--source` is a directory, not a single file → skip.
4. **Rule 4 ambiguity** — reached *by construction* → `mode_confidence: UNCERTAIN` → HALT-ask; blocks any `source/` write (no `ch-<NN>.txt`, no manifest, no `.raw/`) while unresolved.

Confirmed: auto-detect routes to **HALT, not folder**. The `--source-mode folder` override remains a
clean, separate bypass (mapping table L77–82) → no contradiction introduced.

---

## Part 2 — Hard invariants NOT perturbed

| Invariant | Method | Result |
|---|---|---|
| Manifest v1 schema fenced block (SKILL.md) vs blueprint §D | `awk` extract both, `diff` (47 lines each) | **BYTE-IDENTICAL** |
| 16-row failure-mode table (SKILL.md) vs blueprint §C | `awk` extract both, `diff` (18 lines = hdr+sep+16 rows) | **BYTE-IDENTICAL** |
| Bolded sentence #1 (confidence rule) | `grep -c` exact string | **1 (verbatim)** |
| Bolded sentence #2 (deferred-write invariant) | `grep -c` exact string | **1 (verbatim)** |
| path-contract §4 read-set fenced block (3 hardcoded paths) | Read + diff context | **UNCHANGED** (additions land AFTER the fence) |
| path-contract §2 8-file table | row count + `git diff` filter | **8 rows, NO §2 row changed vs HEAD** |
| prep-cordinator STAGE 1..8 fenced lines | `awk` extract worktree vs `git show HEAD`, `diff` (16 lines) | **BYTE-IDENTICAL to HEAD** |
| VENDOR single chapter-materialize row + U+2014 | `git diff` + `grep` | **single `skills/chapter-materialize/** \| NATIVE \| — \| —` row; U+2014 intact** |
| check_boundary.py byte-unchanged | `git diff --stat HEAD` | **0 lines changed (unchanged)** |

---

## Part 3 — Runtime gates

| Gate | Command | Result |
|---|---|---|
| Boundary contract | `cd laf-adaptation && uv run python scripts/check_boundary.py` | **EXIT 0 — BOUNDARY CONTRACT: PASS (A–F)** |
| YAML parse | `uv run --with pyyaml python -c yaml.safe_load(boundary-rules.yaml)` | **OK — 7 top keys** (`schema_version, toc_anchor_map, body_heading_map, filename_map, content_sanity, count_reconciliation, confidence_rule`) |

---

## Part 4 — No new structural issue introduced

- C-1 negative guard does not conflict with the `--source-mode` override path (override mapping table bypasses auto-precedence cleanly; both-present ambiguity only HALTs under `auto`).
- I-2 `mode_a_completeness` is an *additive* sub-block under `count_reconciliation`; YAML still parses; completeness treated as a separate axis from per-boundary confidence (no regression to the CERTAIN rule).
- I-3 prose edits do NOT touch the frozen schema fenced block (verified byte-identical).
- All frozen guardrail blocks confirmed byte-stable — no fix bled into a protected region.

---

## Observations (fix-report reporting inaccuracies — NOT structural defects)

1. **path-contract diff under-described.** The fix report frames I-3 as a single §6 Retention-bullet
   append. The actual `git diff HEAD` for path-contract.md shows a larger additive delta: a §4 sidecar
   Note, three §5 write-ownership rows (`ch-<NN>.txt`, `chapter-manifest.yaml`, `.raw/*`), and the whole
   §6 "Source-side chapter manifest" section. **These are additive, coherent with the Stage-0 materialize
   work, and do NOT perturb the frozen §4 3-path fence or the §2 8-file table** (both verified
   byte-unchanged vs HEAD). Most of this delta predates the M3 fix cycle; the I-3 retention clause itself
   is present with U+2014. No structural impact — reporting completeness only.

2. **VENDOR.md "not edited" claim inaccurate.** The fix-report guardrail table states VENDOR.md is "not
   in changeset." `git diff HEAD` shows exactly **one** added row
   (`| skills/chapter-materialize/** | NATIVE | — | — |`). This is precisely the "VENDOR single row"
   guardrail the task required (the skill must have one NATIVE registration row), the U+2014 em dashes
   are intact, and `check_boundary.py` PASSES with it. The row is not in the M3 fix agent's authorized
   6-file set (it is the skill's earlier registration), so its presence is correct — only the fix report's
   "untouched" characterization is imprecise. No structural impact.

Neither observation changes the verdict: the on-disk state is correct in both cases.

---

## Confidence

**Verified:** 12/12 findings + 9/9 invariants + 2/2 runtime gates = 23/23 checks | **Unverifiable:** 0 |
**Unchecked:** 0 | **Confidence:** 100.0%

**Tool engagement:** Read: 6 | Grep: 0 (grep run via Bash) | Glob: 0 | Bash: 8
(Bash calls: boundary check, YAML parse, failure-table diff, schema-block diff, bolded-sentence grep,
STAGE-block diff, path-contract diff, VENDOR diff — each maps to a specific invariant/finding.)

## Summary
- Findings with real edits: 12 / 12
- Hard invariants byte-stable / intact: 9 / 9
- Runtime gates passing: 2 / 2
- New structural issues introduced: 0
- Fix-report reporting inaccuracies (non-structural): 2

## VERDICT: PASS
