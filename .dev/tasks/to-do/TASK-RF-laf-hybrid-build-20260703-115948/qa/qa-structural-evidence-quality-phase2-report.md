# QA Report — Research Gate (EVIDENCE-QUALITY lens, Phase-2 greenfield)

**Topic:** laf-adaptation Phase-2 evidence quality
**Date:** 2026-07-03
**Phase:** research-gate (evidence-quality lens)
**Fix cycle:** N/A
**Fix authorization:** FALSE — REPORT ONLY

---

## Overall Verdict: FAIL

Evidence-quality lens found **2 genuine defects** (0 CRITICAL fabrications, 1 IMPORTANT, 1 MINOR).
The adversarial brief predicted ≥5 evidence-quality errors including "a fabricated ya.md claim"; I
ran every listed ya.md claim to ground and **found no ya.md fabrication** — ya.md is verbatim-clean
against `tier_5_young_adult.yaml`. The two real defects are in **children.md**: a Denethor T3 quote
that is **silently truncated/paraphrased** while presented inside quote marks as a source carry (F1),
and a **mis-attribution** of that example to the plural "transform prompts" (F2). Under zero-trust
evidence-quality standards a paraphrase presented as a verbatim quote is a FAIL-class defect, so the
gate FAILS on F1 alone.

**Honesty note (self-audit):** my initial pass drafted 6 findings; on verification F3 and F4 (both
suspected ya.md rewordings) did NOT hold — the cited YAML keys matched verbatim. I am reporting the
verified count of **2**, not the suspected count of 6. Inflating to hit the brief's "≥5" expectation
would itself be a QA fabrication.

---

## Confidence

**Confidence:** Verified: 3/3 checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 12 | Grep: 0 | Glob: 0 | Bash: 1

Tool-count note: Grep=0 is intentional and not padding-suspect — every claim under the three checks
is a short quoted string that Read of the (small) source files resolves directly; the cited-vs-actual
comparison is a full-text diff, not a token search. 12 Reads ≥ 3 checks, so the engagement floor is met.

All three assigned checks fully verified against source files (5 target files + 4 design specs +
2 transform prompts + 3 tier YAMLs, all Read directly this session). No web lookups required
(all claims are local-source-bound).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Spec claims in chronicler/tier-coordinator/adaptation-safety cite real spec lines | PASS (with 1 MINOR) | reconcile() 3 checks match tier-coordinator.md §3 A/B/C verbatim; 6 safety sections match safety-rubric.md §1 verbatim; see F5, F6 |
| 2 | children.md worked examples appear in transform prompts, not invented | FAIL | Sauron+Éowyn examples real & verbatim; **Denethor T3 quote is paraphrased/truncated** (F1); **T1 Denethor mis-attributed to "transform prompts" plural** (F2); Éowyn attribution correct |
| 3 | ya.md claims trace to tier_5_young_adult.yaml keys | **PASS** | ALL brief-listed keys verified verbatim: core_principle (YAML L72), when_to_intervene 3 items (L73-76), when_not_to_intervene 3 items (L77-80), unreliable_narrator:true (L38), irony:full_range (L39), agency_externalization forbidden reason "Patronizing; undermines character complexity" (L54-56), supplementary_approach 4 items (L82-87). No fabrication found. F3/F4 were false-positives (see below) |

---

## Finding Detail (cited-vs-actual)

### F1 — IMPORTANT — children.md Denethor T3 "quote" is a paraphrase, not a verbatim carry
**Location:** `skills/adaptation-safety/resources/children.md` lines 66-70
**children.md presents (as a block quote attributed to "the transform prompts"):**
> Tier 3: "Denethor had given up hope… When Faramir was carried in wounded, something broke inside him… Denethor was lost to his despair. But Faramir survived."

**Actual source** — `prompts/transformation/tier_3_transform.md` line 63 (the real T3 Denethor example):
> "Denethor had given up hope. The palantír had shown him only darkness. When Faramir was carried in wounded, something broke inside him. Gandalf found him preparing a terrible thing. But Pippin was already running to find help. They pulled Faramir from danger just in time. Denethor was lost to his despair. But Faramir survived."

The children.md rendering **silently deletes four sentences** ("The palantír had shown him only darkness.", "Gandalf found him preparing a terrible thing.", "But Pippin was already running to find help.", "They pulled Faramir from danger just in time.") and stitches the remainder with `…` ellipses. This is an editorial compression presented inside quote marks as if lifted from the prompt. Per the doc's own framing ("the Denethor scene, from the transform prompts"), a reader will treat this as the source text. It is not — it is a paraphrase. **This is the "paraphrased [source] check" the adversarial brief predicted.** Evidence-quality FAIL: a quote must be verbatim or explicitly marked as abridged.

### F2 — MINOR — children.md mis-attributes the Denethor example to the plural "transform prompts"
**Location:** `children.md` line 66: "**Worked T1→T3 example** (the Denethor scene, from the transform prompts)"
The T1 Denethor line ("The city leader was very sad. He closed all the windows. Gandalf opened them and let the sunshine in.") does **not** appear in `tier_1_transform.md` (whose worked example is the Éowyn scene, line 71-73). Both the T1 and T3 halves of the Denethor example live **only** in `tier_3_transform.md` (lines 61 and 63). The plural "transform prompts" implies the T1 half came from the tier-1 prompt; it did not. Attribution should read "from the tier-3 transform prompt." Contrast the Éowyn example (line 34), correctly attributed "from the tier-1 transform prompt."

### F3 — WITHDRAWN (adversarial false-positive) — ya.md `when_to_intervene` is verbatim
Initial suspicion: ya.md reworded the intervene triggers. **Verification:** ya.md lines 30-33
("Genuinely archaic language", "Historical context needed", "Cultural references now obscure")
match `tier_5_young_adult.yaml` lines 73-76 **verbatim**. No defect. Retained as audit trail of the
zero-trust check that cleared the claim.

### F4 — WITHDRAWN (adversarial false-positive) — ya.md `core_principle` citation is exact
Initial suspicion: ya.md conflates `core_principle` with the profile `description`.
**Verification:** ya.md line 12 attributes *"Adaptation means accessibility, not sanitization."* to
`adaptation_philosophy` → `core_principle`. YAML line 72 `core_principle: "Adaptation means
accessibility, not sanitization."` — **exact match**. ya.md correctly cites core_principle (not the
similar-but-distinct `description` at YAML line 8). No defect. Retained as audit trail.

**Full ya.md re-verification (all brief-listed keys, all CLEAN):** unreliable_narrator:true (YAML L38),
irony:"full_range" (L39), parallel_plotlines/flashbacks (L35-37), agency_externalization.mode:forbidden
reason "Patronizing; undermines character complexity" (L54-56), conflict/death/villain mode:preserve
(L58-66), when_not_to_intervene difficult themes/moral complexity/character deaths (L77-80),
supplementary_approach character-guide/timeline/context-notes/discussion-questions (L82-87),
violence level 8 forbidding gratuitous_sexual_violence+torture_pornography (L20-23), moral_ambiguity
level 9 tragic_endings/antiheroes/no_clear_right_answer (L30-33), archaic_handling:footnote_optional
(L45), approach:preserve_original (L44), sentence_structure preserve_author_voice (L48), Kohlberg 5
social-contract (L16-17). Every one traces verbatim. **ya.md contains zero fabricated claims.**

### F5 — reconcile() three checks vs tier-coordinator.md §3 — PASS (verbatim)
tier-coordinator.md agent §"reconcile() — the three consistency checks" (Check A source-fidelity,
Check B downward-disclosure leak, Check C framing monotonicity) match design spec
`tier-coordinator.md §3` Checks A/B/C **verbatim**, including the pseudocode blocks and the
`journey_or_sleep` deferral example. The maturity() ordinal note (`mandatory < optional < preserve`)
matches design line 109-112. No fabrication.

### F6 — 6 safety sections vs safety-rubric.md §1 — PASS (verbatim)
`skills/adaptation-safety/SKILL.md` Sections 1-6 (Forbidden Content, Agency Externalization,
Emotional Safety, Safe Home, Nightmare Prevention, Linguistic) match `safety-rubric.md §1`
verbatim including TIER 1/TIER 2 forbidden token lists, permitted-emotion sets, the 12-words/sentence
ceiling, the Automatic-Failures override list, and the verdict YAML contract. Cross-checked the
forbidden-token list against `tier_1_preschool.yaml.linguistic.forbidden` (line 49:
kill/die/dead/evil/wound/blood/weapon) — SKILL.md's superset (adds killed/slay/slew/murder/gore/stab/
attack/fight/sword/death) is the safety_check.md carry, consistent with the design's "verbatim from
safety_check.md" provenance. No fabrication.

**Additional Check-1 spot-checks (all PASS):** chronicler.md's three invariants (key-by-(work,tier,
chapter); no cross-tier bleed; no tier-transformed name into shared kb/canon) match agent-schemas.md
§5.1 lines 251-254 verbatim in substance. chronicler run-gate ("only on muse-accept, per tier, AFTER
tier-coordinator returns RECONCILED") matches agent-schemas §5.1 + tier-coordinator.md §5. The
"Sauron is Grumpy King in tier-1 / Dark Lord in tier-5" divergent-canon example matches agent-schemas
§5.1 line 217-218. No uncited or fabricated spec claim found in the three agent/skill files.

---

## Summary
- Checks passed: 1 of 3 fully PASS (Check 1 PASS-with-1-MINOR; Check 3 PASS); **Check 2 FAIL**
- Genuine defects: **2** (IMPORTANT: 1 [F1], MINOR: 1 [F2])
- Critical/fabrication issues: **0** (no invented spec citations; no fabricated ya.md claim)
- Withdrawn-on-verification (false-positives): 2 (F3, F4) — cleared, documented as audit trail
- Issues fixed in-place: **0** (fix_authorization: FALSE — report only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F1 | IMPORTANT | children.md L66-70 | Denethor T3 text is inside quote marks and attributed to the transform prompt, but 4 sentences are silently deleted and joined with `…` — a paraphrase masquerading as a verbatim carry | Either quote `tier_3_transform.md` L63 in full, or mark the block explicitly as "abridged" / "excerpt (…)"; do not present a compressed rewrite as the source quote |
| F2 | MINOR | children.md L66 | "from the transform prompts" (plural) implies the T1 half came from tier_1_transform.md; both halves live only in tier_3_transform.md (tier-1 prompt's example is Éowyn, not Denethor) | Change attribution to "from the tier-3 transform prompt" |

## Actions Taken
None — `fix_authorization: FALSE`. Report-only. All findings documented with cited-vs-actual evidence
for the fix-cycle agent.

## Recommendations
1. **Block synthesis on F1.** A paraphrase presented as a verbatim source quote is exactly the
   evidence-quality defect this gate exists to catch; it must be corrected before the children.md
   craft resource is trusted as a reference. Fix = restore full quote or explicitly mark abridged.
2. **Fix F2 attribution** in the same edit pass (one-line change).
3. **No action on ya.md or the reconcile()/safety spec citations** — verified clean; do not churn them.
4. Re-run this evidence-quality lens as a fix-cycle after F1/F2 are edited; expect verified count → 0.

## QA Complete
