# QA Verification — Content/Operational Re-run (M3 fix cycle)

**Task:** TASK-RF-prep-chapter-materialize-20260709-004725
**Date:** 2026-07-09
**Phase:** doc-qualitative — operational-correctness + cross-artifact-coherence re-run (fix cycle)
**fix_authorization:** false (report-only)
**Scope:** the five fixed files, re-run of the two lenses that FAILed the M3 gate, plus fresh adversarial sweep.

---

## Overall Verdict: PASS

All 8 previously-flagged remediations (2 CRITICAL + 5 IMPORTANT + the cross-artifact enum-bridge)
verified operationally correct. Guardrails preserved byte-stable. Fresh adversarial sweep found ONE
new latent coherence seam, rated MINOR and non-blocking (no runnable path triggers it) — documented
below for the record; it does not gate PASS.

---

## Files verified (all Read end-to-end)

- `laf-adaptation/skills/chapter-materialize/SKILL.md`
- `laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml`
- `laf-adaptation/agents/prep-cordinator.md`
- `laf-adaptation/skills/prep/resources/path-contract.md`
- `.claude/commands/laf/prep.md`
- (evidence) `Books/LWW/` actual directory listing — confirms the both-present scenario is real.

---

## Item-by-item verification

| # | Finding | Verified? | Evidence |
|---|---------|-----------|----------|
| 1 | C-1 split+monolith HALTs (real, unambiguous guard) | PASS | SKILL.md Stage 0.2 rule 2 L57-60 negative guard + rule 4 L62-69 both-present→HALT |
| 2 | C-2 `--source-mode` flows cmd→coordinator→dispatch (not dead) | PASS | prep.md L3/26-29; prep-cordinator L38/52/80/83; SKILL L73-86 |
| 3 | I-1 STAGE 0 ensures source_path FIRST (runnable) | PASS | prep-cordinator L50-52, L57, L76-79, L93-97 |
| 4 | I-2 partial Mode A split → completeness UNCERTAIN → gate | PASS | SKILL L105-113; boundary-rules.yaml L88-91 `mode_a_completeness` |
| 5 | I-3 ADOPTED may have null raw_path/.raw/ (no schema contradiction) | PASS | SKILL L170-176; path-contract §6 L117 |
| 6 | I-4 URL --source has an implementing step (fetch to .raw/ first) | PASS | SKILL Stage 0.1 step 1, L29-33 |
| 7 | I-5 two STAGE 7 PENDING→CONFIRMED flips disambiguated | PASS | prep-cordinator L127-131 |
| 8 | Cross-artifact enum bridge stated at schema/skill side | PASS | SKILL L73-82 mapping table (folder→folder, file→single-file, adopt→adopt-existing) |
| 9 | Fresh adversarial sweep — no NEW blocking defect | PASS | see sweep below (1 MINOR seam, non-blocking) |

---

## Detailed operational confirmation

### C-1 (CRITICAL) — split+monolith HALTs, guard is real and unambiguous — RESOLVED
- Filesystem confirms the exact release-blocker case: `Books/LWW/` holds split fragments
  (`...-1.html`..`...-4.html`) AND monoliths (`...copy.html`, `...copy 2/3/5.html`, base `...Lewis.html`,
  `...pdf`).
- SKILL.md Stage 0.2 rule 2 (L57-60) now carries a negative guard: `folder` fires ONLY when the
  directory holds ≥2 non-canonical per-chapter files **AND NO co-present dominating monolith**. Both-present
  → rule 2 does NOT fire → falls through.
- Rule 4 (L62-69) explicitly names the `Books/LWW/` case, sets `mode_confidence: UNCERTAIN`, routes to the
  gate, and **blocks any `source/` write until resolved** (no `ch-<NN>.txt`, no manifest, no `.raw/`).
- Guard is discernible operationally: "dominating monolith" = a `raw_sources[].role: monolith` (Stage 0.1)
  full-work candidate distinguishable by byte size from front-matter. The both-present branch is reached
  "by construction" (rule 2's guard prevents `folder` from firing), so the ambiguity is not a dead branch.
- `--source-mode folder` may still force it (operator override, L69) — auto never guesses. Correct.

### C-2 (CRITICAL) — `--source-mode` end-to-end operable — RESOLVED
Full chain traced, no dead middle:
1. Command declares `--source-mode auto|folder|file|adopt` (prep.md L3, L26-29).
2. prep-cordinator `## Inputs` has a `source_mode` row (L38) and forwards it into the inline
   chapter-materialize dispatch at STAGE 0 (pipeline L52; note L79-83 "passes both `source_path` and
   `source_mode` into the inline chapter-materialize dispatch").
3. chapter-materialize SKILL L73-86 consumes it via the `--source-mode` → `input_mode` mapping table and
   forces the mode, bypassing auto-precedence; explicit override sets `mode_confidence: CERTAIN` for the
   mode; `auto` retains precedence + both-present HALT.

### I-1 (IMPORTANT) — STAGE 0 ensures source_path before access declaration — RESOLVED
STAGE 0 pipeline line (L50-52) leads with "ensure source_path FIRST (elicit as a required input if
--source omitted) BEFORE the /source-fidelity access declaration". Stage note L76-79 confirms ordering.
Double-elicitation avoided: STAGE 1(a) note (L93-97) states it "re-affirms the same required `source_path`
rather than eliciting a second time." Ordering is runnable.

### I-2 (IMPORTANT) — partial Mode A split no longer silently accepted — RESOLVED
SKILL L105-113 adds "Mode A completeness (single-source count is not a completeness proof)": with NO
corroborating expected-count signal, COMPLETENESS is UNCERTAIN → `ambiguous_split` gate item, blocking
greenlight until operator confirms scope. Mirrored as data in boundary-rules.yaml `count_reconciliation.
mode_a_completeness` (L88-91). Completeness is correctly modeled as a **separate axis** from per-boundary
confidence, so a 4-of-17 export whose four files each read CERTAIN still gates on completeness.
Adversarial check: a forced `--source-mode folder` sets mode CERTAIN but does NOT bypass the completeness
gate (which runs in Stage 0.3 boundary planning, independent of mode-detection) — no bypass hole.

### I-3 (IMPORTANT) — ADOPTED null raw_path/.raw/ — RESOLVED (prose only, schema untouched)
SKILL L170-176 states for `provenance.class: ADOPTED` the `raw_path`/`.raw/` MAY be absent/null; adopt
writes/refreshes ONLY the manifest, no `.raw/` copy. path-contract §6 retention note (L117) adds
"(materialized chapters only; adopted sets may have no `.raw/`)". No contradiction with the schema block
(the v1 fenced block is untouched; fields are structurally present for MATERIALIZED, expected-absent for
ADOPTED). Schema block byte-integrity preserved.

### I-4 (IMPORTANT) — URL --source has an implementing step — RESOLVED
SKILL Stage 0.1 step 1 (L29-33): a URL is FETCHED to `source/<slug>/.raw/` FIRST, the local path becomes
the working `source_path`, the URL is recorded in provenance, and all inventory fields are computed on the
fetched local file. Consistent with the command's existing statement (prep.md L18-20).

### I-5 (IMPORTANT) — two STAGE 7 flips disambiguated — RESOLVED
prep-cordinator L127-131 names them explicitly: (1) `50-greenlight.md` file `status:` PENDING→CONFIRMED,
and (2) separately `chapter-manifest.review.status` in `source/<slug>/chapter-manifest.yaml`. "Two
different files and two different fields, both flipped on the same CONFIRM." No conflation.

### Cross-artifact enum bridge (item 8) — RESOLVED
The `file→single-file`, `adopt→adopt-existing`, `folder→folder` bridge is now stated at the schema/skill
side (SKILL.md L73-82 mapping table + L230 schema enum `input_mode: folder | single-file |
adopt-existing`), not only in the command. Command (prep.md L28-29), coordinator (L38), and skill agree.

---

## Guardrails — confirmed preserved (DO-NOT-TOUCH set)

- **16-row failure-mode table** — counted: exactly 16 data rows. Intact.
- **Two bolded invariants** — verbatim present: "CERTAIN requires ≥2 independent agreeing signals and no
  contradiction." (L117) and "No `ch-NN.txt` for a PROBABLE/UNCERTAIN boundary is committed before the
  human resolves it." (L130).
- **STAGE 1..8 lines** — byte-stable; STAGE 0 prepended only (grep of `^STAGE [1-8]` shows all eight
  original lines unchanged, plus the new STAGE 0 at L50).
- **chapter-manifest v1 schema fenced block** — untouched (F5 handled via adopt-section prose L170-176, not
  by editing the schema).
- **M-3 / M-4 minor reconciliations** — both landed: `min_body_chars`(500) ≤ `plausible_length_range.min`
  (1500) with explanatory comment (boundary-rules.yaml L68-76); tie-break wording aligned "shortest
  filename → lexicographic" across SKILL L181 and YAML L57.

---

## Fresh adversarial sweep — NEW defects

**One latent coherence seam found. Rated MINOR. NON-BLOCKING. Not part of the fix scope's failures.**

- **N-1 (MINOR, coherence, non-blocking): I-4 URL fetch writes `.raw/` at Stage 0.1, before the Stage 0.2
  invariant "no `.raw/` copy is written while mode is unresolved."** The two statements are textually
  absolute but cannot operationally collide: a URL `--source` resolves to a single remote resource →
  post-fetch `source_path` is a single local file → deterministic Mode B (single-file). The Stage 0.2
  "no `.raw/` while unresolved" invariant fires only for the both-present **directory** ambiguity (rule 4),
  which a fetched-URL single file can never be. So no runnable path both fetches a URL to `.raw/` AND sits
  in the UNCERTAIN both-present state. This is a wording seam, not an execution break. OPTIONAL polish (not
  required for PASS): a one-clause note at Stage 0.1 step 1 or Stage 0.2 rule 4 that the URL-fetch `.raw/`
  write is the single-file ingest anchor and is out of scope of the both-present directory write-block.

No other new operational or coherence defect introduced by the fixes. No regression to any guardrail.
No new contradiction, dead reference, or unreachable gate detected.

---

## Self-Audit

**(a) Reliance list — structural items relied upon (not re-verified here):**
- Relied on the M3 structural lenses (manifest-schema-fidelity, confidence-rule-integrity,
  boundary-contract-domain — all PASS) for schema-block byte-integrity and boundary-contract conformance;
  I re-confirmed only the DO-NOT-TOUCH byte-stability signals relevant to whether a fix broke a guardrail.

**(b) Independent semantic checks (≥1 required):**
- Verified the C-1 both-present scenario is REAL by listing `Books/LWW/` (Bash `ls`) — the guard is not
  guarding a hypothetical; split `-1..-4.html` + monoliths `copy*.html`/base/`.pdf` all co-present.
- Traced the C-2 `--source-mode` chain across three artifacts by grep + read (cmd L3/26-29 →
  coordinator L38/52/80/83 → skill L73-86) to confirm no dead middle — a semantic flow check rf-qa's
  per-file structural pass cannot make.
- Verified I-2 completeness axis is independent of mode-detection by reasoning through a forced
  `--source-mode folder` on a 4-of-17 split (gate still fires at Stage 0.3) — an operational-simulation
  check, not a structural one.
- Counted the 16-row failure-mode table and grepped both bolded invariants verbatim to confirm fixes did
  not perturb the frozen guardrails.

**Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 6 | Grep/Bash: 4 | Glob: 0

---

## VERDICT: PASS

All 8 remediations (C-1, C-2, I-1..I-5, cross-artifact enum bridge) are operationally correct and
internally consistent. Guardrails preserved. One MINOR non-blocking coherence seam (N-1) noted for
optional polish; it does not represent a runnable defect and does not gate the verdict. No blocking
remaining or new gaps.
