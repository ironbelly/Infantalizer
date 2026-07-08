# QA Report — Internal Consistency (Phase-2 Greenfield)

**Topic:** rf-qa INTERNAL-CONSISTENCY lens on Phase-2 BUILD-NEW files (chronicler, tier-coordinator, adaptation-safety)
**Date:** 2026-07-03
**Phase:** synthesis-gate (internal-consistency lens)
**Fix cycle:** N/A
**Fix authorization:** FALSE — REPORT ONLY
**Stance:** ADVERSARIAL — zero-trust; assume >=5 inconsistencies exist.

**Scope files (under `/config/workspace/Infantalizer/laf-adaptation/`):**
- `agents/chronicler.md`
- `agents/tier-coordinator.md`
- `skills/adaptation-safety/SKILL.md`

**Spec (ground-truth) files:**
- `.dev/releases/current/0.1/design/tier-coordinator.md` §3
- `.dev/releases/current/0.1/design/safety-rubric.md` §4
- `.dev/releases/current/0.1/design/kb-formats.md` §4

---

## Overall Verdict: **FAIL**

Checks 2 and 4 PASS (byte-faithful reproduction). Checks 1 and 3 FAIL: chronicler's
write-targets omit the `chapters/ch-<NN>/{analysis.yaml, adapted.md}` promotion that
kb-formats §4 assigns to chronicler; and adaptation-safety's `next`-field emission contract
diverges from the safety-verifier output contract for the T3-advisory-FAIL case. One MINOR
underspecification (T4 canon persistence) noted.

**Issue count: 5** (0 CRITICAL / 3 IMPORTANT / 2 MINOR)

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | chronicler (work,tier,chapter) keying + kb-formats §4 graft-G1 dir shape | **FAIL** | Read chronicler.md L30-40 (Write targets) + kb-formats.md L31-39, L191, L248-253. `continuity.md`/`canon-delta.md`/`decisions.md` paths + `(work,tier,chapter)` key are faithful, but `chapters/ch-<NN>/{analysis.yaml, adapted.md}` promotion is omitted despite §4 L191 "Written by `chronicler` on accept". |
| 2 | tier-coordinator reconcile() 3 checks (A/B/C) vs tier-coordinator.md §3 | **PASS** | Diffed agent L53-87 vs spec L71-112. All three code blocks byte-identical; conflict types (`unsourced`/`disclosure_leak`/`monotonicity`), predicates, maturity ladder ordering all faithful. Prose compressed (examples dropped) but no logic drift. |
| 3 | adaptation-safety verdict schema (full form) vs safety-rubric §4 + safety-verifier contract | **FAIL** | Diffed verdict block across SKILL L81-100, spec L96-115, safety-verifier L45-64: **byte-identical, full form** (schema PASS). BUT `next`-emission contract diverges for T3-FAIL: SKILL formula (L75) computes `next=revise`; safety-verifier deterministic rule (L79-84) mandates `next=promote` for advisory. |
| 4 | sequential-mode heuristic markers (parallel_plotlines, unreliable_narrator, nested_timeline) | **PASS** | Diffed agent L45-48 vs spec L60-63 (identical but `**OR**`/`**or**` cosmetic). All 3 markers present exactly once each in both. `work_metadata.key_challenges` path confirmed real in kb-formats §3.2 L150. |

---

## Summary
- Checks passed: 2 / 4
- Checks failed: 2
- Critical issues: 0
- Issues found: 5 (IMPORTANT: 3, MINOR: 2)
- Issues fixed in-place: 0 (fix_authorization: FALSE — REPORT ONLY)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | chronicler.md L30-40 (Write targets) vs kb-formats.md §4 L191, §4.4 L253 | kb-formats §4 L191 states the graft-G1 layer `kb/adaptations/<work>/tier-<N>/` is "**Written by `chronicler` on accept**", and §4.4 defines `chapters/ch-<NN>/adapted.md` as "the accepted tier-N adaptation prose". chronicler's Write-targets block lists only `continuity.md`, `canon-delta.md`, `decisions.md` — it **omits promoting `adapted.md`** into `chapters/ch-<NN>/`. Worse, chronicler's INPUT `adapted_path` (L27) already points to the *final kb path* `kb/adaptations/.../chapters/ch-<NN>/adapted.md`, implying something else already wrote it there — but no agent in scope writes it (grep: only tier-coordinator *reads* `adapted.md` as reconcile input; the draft lives at `work/drafts/...` per safety-verifier L19). The kb `adapted.md` promotion is unowned. | Add `kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/adapted.md` to chronicler's Write-targets as an on-accept promotion (copy the accepted `work/drafts/` tier-N draft), OR correct chronicler's `adapted_path` input to point at the `work/drafts/` source and explicitly assign the kb-path promotion to chronicler. Reconcile with §4 L191. |
| 2 | IMPORTANT | chronicler.md L28 (input) + L30-40 (Write targets) vs kb-formats.md §4 L36, §4.4 L250-252 | kb-formats §4 L36 / §4.4 L250-252 define `chapters/ch-<NN>/analysis.yaml` as "**the promoted copy of `work/analysis/ch-<NN>.yaml`... promoted only on muse-accept (constraint #5)**" — a chronicler-on-accept action (§4 L191). chronicler receives `analysis_path = work/analysis/ch-<NN>.yaml` (un-promoted source, L28) but **never writes/promotes** it to `chapters/ch-<NN>/analysis.yaml`. The per-chapter `analysis.yaml` promotion is unowned. | Add `kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/analysis.yaml` to chronicler's Write-targets as an on-accept copy of `analysis_path`, per §4.4 L250-252 + §4 L191. |
| 3 | IMPORTANT | adaptation-safety/SKILL.md L75 (aggregation `next`) vs safety-verifier.md L79-84 (deterministic `next` rule) + safety-rubric.md §4.1 L117-127 | The `next`-emission contract **diverges for the T3-advisory-FAIL case**. SKILL/spec aggregation formula (`next = "revise" if overall == FAIL else "promote"`) has NO T3 special-case in `overall` (N/A only for tiers {4,5}), so a T3 section-FAIL → `overall=FAIL` → **`next=revise`**. But safety-verifier's "Deterministic `next` rule" (L79-84) explicitly states `mode==advisory (T3, even on FAIL) → promote`, i.e. **`next=promote`**, matching spec §4.1's "advisory: proceed non-blocking". adaptation-safety does NOT carry the deterministic clarification, so its emitted `next` for T3-FAIL contradicts the safety-verifier output contract Check 3 requires agreement with. | Add the safety-verifier "Deterministic `next` rule" to adaptation-safety's aggregation block, OR change the SKILL/spec formula to `next = revise iff (mode==blocking AND overall==FAIL) else promote` so T3-advisory-FAIL emits `promote` consistently across all three files. |
| 4 | MINOR | adaptation-safety/SKILL.md L75 (and safety-rubric.md §3 L86 — inherited from spec) | The inline comment on the `next` formula — `# tier 3 advisory: next always "promote", report-only` — **contradicts the formula it annotates**: the formula computes `next=revise` for a T3-FAIL (overall==FAIL), but the comment claims T3 is always `promote`. Intra-file self-contradiction; the comment asserts the intended behavior the formula fails to implement. (Root cause shared with Issue 3; flagged separately as a self-contained readability/correctness defect that also exists verbatim in the spec.) | Fixing Issue 3 (adding the deterministic rule / correcting the formula) resolves this; until then the comment is misleading and should not be trusted as the contract. |
| 5 | MINOR | chronicler.md (silent on T4) vs kb-formats.md §2.4 L116-120 + tier-coordinator.md §Tier-4-handling L131-134 | tier-coordinator treats T4 as "an ordinary tier" for reconcile (L133) and, on RECONCILED, chronicler "runs per tier" (L120) without excluding T4 — which would write `kb/adaptations/<work>/tier-4/` canon. The specs are explicit only that the T4 **profile** is "never stored" (§2.4); they are **silent** on whether T4 **canon** (`continuity.md`, etc.) is persisted. This is an underspecification, not a hard contradiction (the `tier-<N>` dir shape permits `<N>=4` structurally), but chronicler should state whether T4 canon is written or excluded to avoid a divergent-canon ambiguity for the interpolated tier. | Add an explicit T4 statement to chronicler (either "T4 canon IS persisted under tier-4/ despite the profile being ephemeral" or "chronicler excludes T4"), and cross-reference kb-formats §2.4. Note: outside the 4 mandated checks; flagged for completeness. |

---

## Notes on what PASSED (adversarial confirmation, not assumption)
- **Check 2 (reconcile logic):** all three algorithm blocks are **byte-identical** to spec §3 — verified by direct `sed` diff, not by trusting agent claims. The only textual deltas are dropped illustrative examples in prose and "It is/A coarse" wording — zero logic impact.
- **Check 3 schema block:** the verdict YAML is **full-form and byte-identical** across all three files (work/chapter/tier/result/sections{6}/automatic_failures/mode/next/evidence). No abbreviated form. The FAIL is strictly in the `next`-emission *behavioral* contract, not the schema shape.
- **Check 4:** markers and the `work_metadata.key_challenges` source path are correct and grounded in kb-formats §3.2.
- **Status/step wiring (bonus):** RECONCILED/CONFLICT + `conflicts`-empty gate and workflow step 10→11 ordering are consistent between chronicler and tier-coordinator and match spec §5.

---

## Confidence Gate

Checklist item categorization (4 mandated checks):
- [x] Check 1 — VERIFIED (Read chronicler.md + kb-formats.md §4; grep for adapted.md/analysis.yaml ownership)
- [x] Check 2 — VERIFIED (sed diff of both code+prose blocks agent vs spec)
- [x] Check 3 — VERIFIED (sed diff of verdict block across 3 files; diff of aggregation + deterministic-next rule)
- [x] Check 4 — VERIFIED (sed diff of heuristic; grep marker counts; kb-formats §3.2 field confirmation)

- **Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 8 (each Bash call performs a targeted grep/sed verification mapped to a specific check; no padding)
- No UNCHECKED items. No UNVERIFIABLE items. No external/web lookups required (all claims are intrinsically local).

---

## QA Complete
