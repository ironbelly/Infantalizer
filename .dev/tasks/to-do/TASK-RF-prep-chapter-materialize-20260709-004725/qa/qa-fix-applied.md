# QA Fix-Applied Report — M3 Final Gate (Step 6.5, serialized fix agent)

**Date:** 2026-07-09 · Repo root: `/config/workspace/Infantalizer`
**Input:** `qa/qa-consolidated-findings.md` (consolidated verdict FAIL; 3 PASS + 4 FAIL lenses)
**fix_authorization:** true · **Role:** single serialized fix agent

---

## VERDICT: FIXED (all applied)

All CRITICAL (C-1, C-2), IMPORTANT (I-1..I-6), and MINOR (M-1..M-4) findings applied in-place. WON'T-FIX
items left untouched by design (see note at end). All frozen-block, YAML-parse, boundary-check, and
STAGE-1..8 byte-stability guardrails re-verified GREEN post-edit.

---

## Fixes applied (finding ID → exact edit)

### C-1 — both-present negative guard (AC2 release-blocker)
**File:** `laf-adaptation/skills/chapter-materialize/SKILL.md` (Stage 0.2)
- **Rule 2 (`folder`):** appended a **negative guard** — rule 2 fires ONLY when the directory holds ≥2
  non-canonical per-chapter files AND NO co-present dominating monolith; if BOTH a split-set AND a
  dominating monolith are present, rule 2 does NOT fire and control falls through to rule 4. "Auto-detect
  must not guess `folder` in the both-present case."
- **Rule 4 (ambiguity → HALT):** added that the both-present case is reached **by construction** (rule 2's
  guard prevents `folder` from firing), and made the UNCERTAIN-mode write-block explicit: "no `ch-<NN>.txt`,
  no manifest, no `.raw/` copy is written while mode is unresolved"; clarified `--source-mode` may still
  force a mode but auto must HALT. Result: `Books/LWW/` (split `-1..-4.html` + `…copy*.html` monolith) now
  routes to `mode_confidence: UNCERTAIN` → HALT-ask instead of auto-picking `folder`.

### C-2 — forward `--source-mode` through prep-cordinator + surface mapping in SKILL
**Files:** `laf-adaptation/agents/prep-cordinator.md`, `laf-adaptation/skills/chapter-materialize/SKILL.md`
- **prep-cordinator `## Inputs`:** added a `source_mode` row — `--source-mode <auto|folder|file|adopt>`,
  optional, default `auto`; states it is forwarded into the inline chapter-materialize dispatch at STAGE 0
  with the flag→input_mode mapping (`folder`→folder, `file`→single-file, `adopt`→adopt-existing,
  `auto`→precedence).
- **prep-cordinator STAGE 0 (fenced pipeline entry + Stage-0 note):** stated the coordinator passes both
  `source_path` and `source_mode` into the inline dispatch; a `source_mode` override forces the mode.
- **SKILL.md Stage 0.2:** added a `--source-mode` → `input_mode` mapping table plus the mode-confidence
  rule (explicit override ⇒ `mode_confidence: CERTAIN` for the mode; `auto` ⇒ derived, and unresolved
  both-present ambiguity still HALTs). The override is no longer dead in the middle of the pipeline.

### I-1 — STAGE 0 ensures source_path FIRST, before the access declaration
**File:** `laf-adaptation/agents/prep-cordinator.md`
- **STAGE 0 fenced entry:** reworded to lead with "ensure source_path FIRST (elicit as a required input if
  --source omitted) BEFORE the /source-fidelity access declaration", then run the declaration + ABORT, then
  detect mode (forwarding source_mode).
- **Stage 0 note:** prepended the same source_path-first obligation with the rationale (Stage 0 needs the
  resolved source to run its access declaration).
- **Stage 1 (a/b) note:** made coherent — STAGE 1(a) now *re-affirms* the already-required `source_path`
  (elicited at STAGE 0 if `--source` omitted) rather than eliciting a second time.
- **No renumber:** STAGE 1..8 fenced pipeline lines left byte-stable (verified, see below).

### I-2 — Mode A completeness UNCERTAIN when no corroborating expected-count
**Files:** `laf-adaptation/skills/chapter-materialize/SKILL.md` (Stage 0.3),
`laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml` (`count_reconciliation`)
- **SKILL.md Stage 0.3:** added a "Mode A completeness" paragraph — when Mode A has NO corroborating
  expected-count signal (no TOC count, no whole-work heading count), chapter-set COMPLETENESS is treated as
  UNCERTAIN and an `ambiguous_split` gate item is raised: "possible incomplete split; operator confirm
  partial scope." Completeness is a separate axis from per-boundary confidence and blocks greenlight until
  the operator confirms scope. (Closes the silent 4-of-17 partial-split acceptance.)
- **boundary-rules.yaml:** added a `mode_a_completeness` sub-block under `count_reconciliation`
  (`requires_corroborating_expected_count: true`; `on_single_source_count_only: raise_ambiguous_split`;
  `gate_message: "possible incomplete split; operator confirm partial scope"`).

### I-3 — ADOPTED provenance may have absent/null raw_path/.raw/ (PROSE only)
**Files:** `laf-adaptation/skills/chapter-materialize/SKILL.md` (Idempotency/adopt),
`laf-adaptation/skills/prep/resources/path-contract.md` (§6 Retention)
- **SKILL.md:** added a prose bullet under `## Idempotency, collisions, backward-compat`: for
  `provenance.class: ADOPTED`, `raw_path` / `.raw/` MAY be absent/null (no retained upstream monolith);
  adopt writes/refreshes ONLY the manifest and creates no `.raw/` copy; the fields are structurally present
  for MATERIALIZED chapters, and their absence for ADOPTED is expected, not a fidelity gap. **Schema fenced
  block NOT touched** (guardrail honored).
- **path-contract §6 Retention bullet:** appended "(materialized chapters only; adopted sets may have no
  `.raw/`)" with U+2014 em dash preserved.

### I-4 — URL `--source` fetch-to-local stage
**File:** `laf-adaptation/skills/chapter-materialize/SKILL.md` (Stage 0.1 Inventory item 1)
- Added: when `--source` resolves to a URL it is FETCHED to a local file under `source/<slug>/.raw/` FIRST;
  that local path becomes the working `source_path` for all downstream stages; the original URL is recorded
  in `provenance`; inventory fields (size/ext/sha256) are computed on the fetched local file. Consistent
  with the command's existing statement.

### I-5 — disambiguate the two STAGE 7 PENDING→CONFIRMED flips
**File:** `laf-adaptation/agents/prep-cordinator.md` (Stage 7 chapter-manifest ratification note)
- Added an explicit "Two distinct `PENDING → CONFIRMED` flips happen at STAGE 7 — do not conflate them"
  clarification: (1) the STAGE 7 pipeline line's "set status PENDING → CONFIRMED" = the **`50-greenlight.md`
  file `status:`** (greenlight-gate file); (2) the ratification flip = **`chapter-manifest.review.status`**
  in `source/<slug>/chapter-manifest.yaml` (source-side manifest). Two files, two fields, both flipped on
  the same CONFIRM. (Editable Stage-7 note only; frozen STAGE 7 pipeline line untouched.)

### I-6 — invariants-review.md skill-section citations → real heading names
**File:** `.dev/tasks/to-do/.../phase-outputs/reviews/invariants-review.md`
- AC1: `normalization §8 identical` → ``## Format normalization & fidelity`` identical.
- AC5: `manifest v1 schema (SKILL.md §12)` → ``## Manifest output contract``; `§Normalization requires`
  → ``## Format normalization & fidelity`` requires.
- AC3: `SKILL.md §Idempotency` → ``## Idempotency, collisions, backward-compat``.
- Left intact: path-contract §2/§4/§5/§6 refs (real numbered sections) and spec §13 (spec ref).

### M-1 — CLAUDE.md row added to QA inventory
**File:** `.dev/tasks/to-do/.../phase-outputs/reports/qa-input-inventory.md`
- Added row #10: `laf-adaptation/CLAUDE.md` (count-correction edit; recorded in the task Deviations log;
  NATIVE, not hash-pinned — outside the Rule-F glob).

### M-2 — AC1 "identical" = chapter TEXT clarification
**File:** `laf-adaptation/skills/chapter-materialize/SKILL.md` (Manifest output contract note)
- Added: the canonical `ch-<NN>.txt` chapter TEXT is identical across Mode A/B; the manifest itself is NOT
  byte-identical across modes — its mode/provenance fields (`input_mode`, `provenance.source_kind`,
  `raw_sources[].role`, per-chapter markers) legitimately differ. AC1 constrains the chapter text set, not
  mode-specific provenance.

### M-3 — reconcile min_body_chars vs plausible_length_range (clarifying comment)
**File:** `laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml` (`content_sanity`)
- Added a comment: `min_body_chars` (500) = HARD non-empty floor (reject below outright);
  `plausible_length_range.min_chars` (1500) = SANITY band floor (below-band ⇒ PROBABLE/flag, not reject).
  So `min_body_chars` ≤ `plausible_length_range.min_chars` by design. Numbers left as-is (clarifying
  comment preferred per finding).

### M-4 — duplicate-monolith tie-break wording made consistent
**Files:** `laf-adaptation/skills/chapter-materialize/SKILL.md`,
`laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml`
- **SKILL.md:** reworded the "Duplicate-monolith canonical pick" bullet to the canonical order **"shortest
  filename → lexicographic order on ties"**, with byte-identity resolved by sha256 (only same-sha256 files
  are duplicates); points to the identically-worded note in boundary-rules.yaml.
- **boundary-rules.yaml:** added a matching "Canonical-pick tie-break" comment near `ignore_globs` stating
  the same order (sha256 identity → shortest filename → lexicographic). The two now agree.

---

## Guardrails re-verified (all GREEN)

| Guardrail | Method | Result |
|---|---|---|
| (a) 16-row failure table byte-identical to blueprint | `diff` SKILL.md L192–209 vs blueprint failure-table slice | **IDENTICAL** |
| (a) `chapter-manifest.yaml` v1 schema fenced block byte-identical | `diff` SKILL.md L224–272 (incl fences) vs blueprint schema slice | **IDENTICAL** |
| Two bolded invariant sentences verbatim | `grep -c` exact-string (confidence rule + deferred-write) | **1 each (intact)** |
| SKILL.md frontmatter (name+description only) | Read L1–8 | **unchanged** |
| (b) boundary-rules.yaml parses | `uv run --with pyyaml python -c yaml.safe_load` | **YAML OK** (7 top keys) |
| (c) `check_boundary.py` exits 0 PASS | `cd laf-adaptation && uv run python scripts/check_boundary.py` | **EXIT 0 — BOUNDARY CONTRACT: PASS (A–F)** |
| (d) STAGE 1..8 pipeline block byte-stable | `diff` HEAD vs worktree of `STAGE 1..STAGE 8` block | **IDENTICAL to HEAD** |
| path-contract §4 read-set fenced block (3 hardcoded paths) | `sed` extract of the fence | **3 paths intact, unchanged** |
| path-contract §2 8-file table | row count | **8 rows intact** |
| check_boundary.py byte-unchanged | `git diff --stat` | **empty (unchanged)** |
| VENDOR.md / prep SKILL.md not edited | `git diff --name-only` | **not in changeset** |
| U+2014 em dash preserved in path-contract edit | `grep` for `—` in the added clause | **present** |
| No second VENDOR row / no VENDOR edit | (VENDOR.md untouched) | **honored** |

Note: `chapter-materialize/SKILL.md` + `resources/boundary-rules.yaml` are untracked (`??`) — the whole
skill dir is new in this task — so they do not appear in `git diff --stat`; frozen-block fidelity was
verified against the blueprint by direct `diff`, not against git HEAD.

---

## WON'T-FIX (left untouched, by design)
- **`chapter_count: 17` "(illustrative)" annotation** — the only place to add it is INSIDE the frozen
  `chapter-manifest.yaml` v1 schema fenced block, which the guardrails forbid touching (must stay
  byte-identical to the blueprint). The finding marks this optional + non-blocking, so it was NOT applied
  to preserve the frozen-block invariant. (Trade-off: byte-identity guardrail wins over a cosmetic,
  explicitly-optional annotation.)
- **spec §4 STAGE 4/5 numbering trap** — upstream spec surface, out of scope (authored artifacts resolve
  it correctly).
- **prep SKILL "never restate a path" vs the 8-file assertion** — pre-existing, spec-mandated invariant
  assertion, not a forbidden path restatement.

---

## Files edited (authorized set only)
1. `laf-adaptation/skills/chapter-materialize/SKILL.md` — C-1, C-2, I-2, I-3, I-4, M-2, M-4
2. `laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml` — I-2, M-3, M-4
3. `laf-adaptation/agents/prep-cordinator.md` — C-2, I-1, I-5
4. `laf-adaptation/skills/prep/resources/path-contract.md` — I-3 (§6 Retention)
5. `.dev/tasks/to-do/.../phase-outputs/reviews/invariants-review.md` — I-6
6. `.dev/tasks/to-do/.../phase-outputs/reports/qa-input-inventory.md` — M-1

No other file modified.

## VERDICT: FIXED (all applied)
