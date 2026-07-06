# QA Report — ACTIONABILITY lens (Phase-2 greenfield agent/skill bodies)

**Topic:** LAF hybrid build — Phase-2 BUILD-NEW bodies actionability
**Date:** 2026-07-03
**Phase:** doc-qualitative (ACTIONABILITY overlay)
**Fix cycle:** N/A (fix_authorization: FALSE — REPORT ONLY)
**Stance:** Adversarial / zero-trust. Assumed ≥5 actionability gaps present; hunted for them.

---

## Overall Verdict: FAIL

An executor cannot run several of these instructions without inventing missing scaffolding.
Two of the three chronicler invariants are not mechanically checkable as written (no defined
write-format to inspect, no name-transform oracle). The tier-coordinator's Check B and Check C
depend on tier-profile concepts (`disclosures`, `permitted_at`, `maturity`) that have **zero
backing** in the actual `kb/tiers/*.yaml` profiles. The numbered workflow the coordinator/
chronicler/verifier all key off (steps 1–11) has **no canonical definition** anywhere in the
tree. The adaptation-safety FAIL→step-3 loop is the one bright spot — its `next` field is
genuinely deterministic, and the one ambiguity (T3 advisory FAIL) is explicitly resolved.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | chronicler's three invariants concrete & testable | FAIL | Inv.1 & Inv.3 not mechanically checkable (F-1, F-2); Inv.2 checkable-in-principle but blocked by same missing write-format (F-1) |
| 2 | tier-coordinator reconcile → actionable CONFLICT entries; parallel/sequential heuristic concrete | FAIL | Check A actionable; Check B & Check C reference undefined profile concepts (F-3, F-4); heuristic concrete but references a work_metadata path never shown to be populated (F-5) |
| 3 | adaptation-safety FAIL→step-3 loop actionable; `next` deterministic | PASS (with note) | `next` predicate is deterministic; T3-advisory-FAIL ambiguity is explicitly resolved in safety-verifier.md:79-84 (F-6 is a MINOR cross-file duplication risk, not an ambiguity) |

## Summary
- Checks passed: 1 / 3 (item 3, with a MINOR note)
- Checks failed: 2
- Critical issues: 2 (F-3, F-4 — checks that cannot execute against real data)
- Important issues: 3 (F-1, F-2, F-5)
- Minor issues: 1 (F-6)
- Issues fixed in-place: 0 (REPORT ONLY)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F-1 | IMPORTANT | chronicler.md:43-48 (Inv.1 & Inv.2) | "Key every per-tier write with `(work, tier, chapter)`" and "never write a tier-N fact into another tier's continuity.md" are **not testable** because the body never defines the concrete write format that carries the key. There is no frontmatter schema, no header line, no stamped field an executor can inspect after the fact. `story-memory` (the loaded skill) points to `resources/writing-artifacts.md` for layout but chronicler never says the key lives in the path, the body, or a header — so an executor cannot answer "did I key this write by (work,tier,chapter)?" except by trusting the file path, which only encodes `(work,tier,chapter)` for `canon-delta.md` (path has `tier-<N>/chapters/ch-<NN>`) and **not** for `continuity.md` / `decisions.md` (path has only `tier-<N>/`, no chapter). So for the append-style files the (…,chapter) coordinate has nowhere to live. | Specify the concrete carrier: e.g. "each promoted fact is written as a list entry prefixed `- [work=<work> tier=<N> ch=<NN>] <fact>`" OR a per-entry YAML stamp `{work, tier, chapter, fact}`. Then Inv.1 becomes grep-checkable and Inv.2 becomes "grep continuity.md for `tier=<M>` where M≠N ⇒ violation". |
| F-2 | IMPORTANT | chronicler.md:49-51 (Inv.3) | "Never promote a tier-transformed name into shared `kb/canon/`" is **unactionable without a name-transform oracle**. The executor is given source names ("Sauron") and transformed names ("Grumpy King") only as prose examples — there is no lookup the executor can consult to decide, for an arbitrary token in a canon write, whether it is a tier-transformed name or a legitimate source fact. The mapping that actually holds these pairs (`kb/adaptation-mapping/<work>-mapping.yaml` → `characters.*.tier_1.name`, `master_translation_table`) is **never referenced by chronicler.md**. grep confirms chronicler cites no translation table. | Add the check mechanism: "Before appending to `kb/canon/`, load `<work>-mapping.yaml`; reject any token that matches a `tier_<N>.name` or `master_translation_table[].tier_<N>` value." That turns Inv.3 into a set-membership test instead of a judgment call. |
| F-3 | CRITICAL | tier-coordinator.md:64-74 (Check B) | Check B asserts `disclosures(adapted[tier]) ⊆ permitted_at(disclosure, tier_profile[tier])`, but **no tier profile contains a `disclosures` or `permitted_at` concept**. grep across `kb/tiers/*.yaml` returns only one hit for the whole disclosure vocabulary — the string `journey_or_sleep` inside tier_1's `death_euphemism.strategy` — and zero for `permitted_at`. The example ("a death that tier-1 defers (journey_or_sleep)") maps to a `transformation_rules.death_euphemism.strategy` value, not to any enumerable set of "permitted disclosures". An executor has no data structure to compute `permitted_at()` against, so Check B cannot run and cannot emit a `{type: disclosure_leak, tier, disclosure}` entry. | Either (a) define a concrete `disclosures:` / `permitted_disclosures:` block in each `tier_<N>.yaml` that `permitted_at()` reads, or (b) rewrite Check B in terms of concepts that DO exist in the profiles (e.g. `thresholds.violence.forbidden`, `death_euphemism.mode`), and state the exact profile keys the check reads. Until one is done, Check B is a spec of a function with no inputs. |
| F-4 | CRITICAL | tier-coordinator.md:76-87 (Check C) | Check C's `maturity()` is declared "ordinal, derived from the element's governing `mode:` on the transformation ladder (`mandatory` < `optional` < `preserve`), plus the tier's violence/moral-ambiguity threshold levels" — but this recipe is **not executable as written**. (a) grep shows `maturity` is defined nowhere outside this file — no lookup table maps a rendered element to an ordinal. (b) The ladder `mandatory < optional < preserve` does not match the actual profile vocabulary: tier_3's `death_euphemism.mode` is `"direct_but_gentle"` and `villain_motivation.mode` is `"can_be_internal"` — neither is on the stated 3-value ladder, and `preserve` never appears as a `mode:` value in any profile. (c) "plus the tier's threshold levels" gives no combination rule (add? tuple-compare? which dominates on tie?). So the executor cannot compute a comparable ordinal and cannot decide `nondecreasing_by_tier`. | Pin `maturity()` to real profile fields with an explicit total order: e.g. "maturity = (`thresholds.violence.level`, `thresholds.moral_ambiguity.level`) compared lexicographically" — both keys exist in every profile (tier_1 violence.level=0, tier_3=4, tier_5 present). Drop or redefine the `mode:` ladder to the actual enumerated `mode:` values per key. |
| F-5 | IMPORTANT | tier-coordinator.md:45-48 (selection heuristic) | The heuristic is concrete in *form* (check `work_metadata.key_challenges` for markers `parallel_plotlines`/`unreliable_narrator`/`nested_timeline`, OR `mode: sequential`), which is good. But it is **not verifiably actionable** against real data: the only `key_challenges` structure that exists is the **template** (`templates/work-mapping-template.yaml:6-9`), whose entries are free-text placeholders `"[Challenge 1]"` / `"[Challenge 2]"` — not an enum. The three markers the heuristic greps for are coordinator-invented tokens with no declared source; nothing constrains a real `<work>-mapping.yaml` to use those exact strings. An executor testing "does key_challenges include a state-heavy marker?" has no controlled vocabulary to match against. Note also two of the three markers collide with tier-profile keys (`parallel_plotlines` is a `narrative_complexity` boolean in tier_1/tier_3), inviting confusion about which structure is authoritative. | Define the controlled marker vocabulary in one place (e.g. add an enumerated `state_heavy_markers:` list to the mapping schema/template) and have the heuristic reference it, so `key_challenges` values are matchable tokens rather than free text. |
| F-6 | MINOR | adaptation-safety/SKILL.md:75 vs safety-verifier.md:79-84 | The task flagged T3-advisory-FAIL as a candidate `next` ambiguity. It is **NOT ambiguous** — but the resolution lives in the *other* file. SKILL.md:75 says only `next = "revise" if overall == FAIL else "promote"` with an inline comment "tier 3 advisory: next always promote, report-only"; the authoritative deterministic predicate (`next = revise IFF mode==blocking AND result==FAIL`; advisory-FAIL → promote) is spelled out in safety-verifier.md:79-84. The two are consistent, so the loop IS actionable. The risk is duplication drift: SKILL.md's one-line rule, read alone, would compute `next=revise` for a T3 advisory FAIL (because `overall==FAIL`), contradicting its own comment. | Make SKILL.md:75 self-consistent: replace the one-liner with the same `mode==blocking AND result==FAIL` predicate used in safety-verifier.md, so the rubric file alone yields the correct `next` for advisory FAIL without relying on the reader also having the agent body open. |

---

## Per-check reasoning (why not actionable)

### Check 1 — chronicler's three invariants
- **Inv.1 (key by (work,tier,chapter))** — the *intent* is clear, the *test* is not. An executor asked "did I key this write?" must inspect something; the body never says what carries the key. For `continuity.md`/`decisions.md` the path lacks a chapter coordinate entirely, so the third coordinate is homeless. **Not testable as written.** (F-1)
- **Inv.2 (no cross-tier bleed)** — checkable *in principle* (grep the wrong tier's continuity.md for the fact), but only once Inv.1 gives facts an inspectable, tier-stamped form. Blocked by the same gap. (F-1)
- **Inv.3 (no transformed name in shared canon)** — requires deciding, per token, "is this a tier-transformed name?" No oracle is wired in; the mapping that holds the answer is never referenced. **Unactionable without the lookup.** (F-2)

### Check 2 — reconcile CONFLICT entries + heuristic
- **Check A (unsourced)** — ACTIONABLE. `source_trace(element) not in shared_analysis` reads a real artifact (`work/analysis/ch-<NN>.yaml`), and emits a well-formed `{type: unsourced, tier, element}`. The caller action (re-dispatch offending tier's writer) is stated at lines 114-116. Good.
- **Check B (disclosure_leak)** — NOT ACTIONABLE. `permitted_at()` has no backing data in the profiles. (F-3)
- **Check C (monotonicity)** — NOT ACTIONABLE. `maturity()` is under-specified and its stated ladder doesn't match real `mode:` values. (F-4)
- **Heuristic** — concrete decision shape, but the marker vocabulary is ungrounded free-text in the only existing schema. (F-5)
- CONFLICT *entry shape* itself is fine (`{type, tier, element/disclosure, detail}`, lines 114) and the caller action is concrete — the failure is that two of three producers of those entries can't run.

### Check 3 — adaptation-safety FAIL→step-3 loop
- `verdict.evidence` gives concrete located revision targets (`{section, word, location}` / `{subject, cause_given, external}`) — genuinely actionable revision notes. ACTIONABLE.
- Aggregation `result` is deterministic (auto-fails dominate → any section FAIL → PASS). ACTIONABLE.
- `next` is deterministic: the SKILL.md one-liner is loose, but safety-verifier.md:79-84 pins it to `mode==blocking AND result==FAIL`, and the **(mode,result) matrix is fully covered** — skipped→promote, PASS→promote, advisory(any result)→promote, blocking+FAIL→revise. **No (mode,result) combination is ambiguous**, including T3 advisory FAIL (→ promote, report-only). The task's suspected ambiguity does not survive cross-file reading. Only a MINOR duplication-drift risk remains. (F-6)

---

## Self-Audit
1. **Factual claims verified against source:** 11 — every referenced structure was grep'd/read: `key_challenges` (template only, placeholders), `disclosures`/`permitted_at` (0 hits in profiles), `journey_or_sleep` (1 hit, tier_1 death_euphemism), `maturity` (0 hits outside coordinator), `mode:` vocabulary mismatch (tier_3 `direct_but_gentle`/`can_be_internal` not on the stated ladder), `master_translation_table` (in template, uncited by chronicler), workflow steps 1-11 (defined nowhere; only referenced by the 3 agents themselves), `thresholds.violence.level` (exists per profile), safety `next` matrix (safety-verifier.md:79-84), continuity.md path lacks chapter coordinate.
2. **Files read:** chronicler.md, tier-coordinator.md, adaptation-safety/SKILL.md, safety-verifier.md, tier_1.yaml, tier_3.yaml, work-mapping-template.yaml; grep'd tier_2.yaml, tier_5.yaml, universal-mappings.yaml, story-memory/SKILL.md, and the whole kb/ + agents/ + skills/ trees for disclosure/maturity/workflow-step vocabulary.
3. **Why trust this found real gaps:** every FAIL is anchored to a grep result showing an *absence* in real source (the disclosure vocabulary, the maturity table, the name-transform oracle wiring, the workflow definition) or a *mismatch* between the body's stated vocabulary and the actual YAML enum — not to opinion. The one PASS was stress-tested by building the full (mode,result) matrix and confirming no cell is undefined.
4. **Web research:** none performed (all verification was local-file-bound); Tavily not invoked.

- **Confidence:** Verified: 3/3 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- **Tool engagement:** Read: 6 | Grep: 4 (multi-pattern) | Glob: 0 | Bash: 4

## Cross-cutting note (beyond the 3 checks, surfaced adversarially)
The numbered workflow (steps 1–11) that chronicler ("step 11"), tier-coordinator ("step 10",
"steps 3-9"), and safety-verifier ("step 8", "return to step 3") all branch on has **no canonical
definition** in the tree — grep for a workflow spec returns only these three files referencing each
other's step numbers. Every "return to workflow step 3 (writer)" / "proceed to reader-sim (step 9)"
instruction is therefore a dangling reference: an executor cannot resolve "step 3" to an actual
dispatchable action without a workflow map that does not exist. This underlies the actionability of
all three checks and should be treated as an IMPORTANT gap in its own right.

## Recommendations
- Resolve F-3 and F-4 before this is executable at all — Check B and Check C are currently
  specifications of functions with no inputs.
- Resolve F-1/F-2 to make chronicler's invariants machine-verifiable rather than aspirational.
- Ground the heuristic vocabulary (F-5) and de-duplicate the `next` rule (F-6).
- Author (or point to) the canonical numbered workflow so all inter-step references resolve.

## QA Complete
