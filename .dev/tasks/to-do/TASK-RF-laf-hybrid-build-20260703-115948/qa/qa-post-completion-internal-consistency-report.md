# QA Report — Internal-Consistency (Post-Completion, Cross-Phase)

**Topic:** laf-adaptation hybrid build — cross-phase internal consistency
**Date:** 2026-07-04
**Phase:** report-validation (internal-consistency lens)
**Fix cycle:** N/A
**Fix authorization:** FALSE (report only)
**Scope:** /config/workspace/Infantalizer/laf-adaptation/

---

## Overall Verdict: **FAIL** (internal-consistency lens)

7 distinct cross-phase inconsistencies found (F-1…F-7, F-3 in two facets). Two are IMPORTANT (F-3-REFINED inconsistent disclaimer application; F-6 CLAUDE.md active_tier claim wrong for 2/4 agents; F-4 pseudocode-vs-rule contradiction in adaptation-safety). None is a hard contract break — `check_boundary.py` PASSes, the verdict schema is byte-consistent, the (work,tier,chapter) keying is fully consistent, and the schema drift is correctly preserved+consumed. The FAIL is on the "any gap regardless of severity" rule for a consistency gate, driven by the IMPORTANT-severity doc/spec disagreements. The adversarial "≥10" prior did not materialize: the tree is substantially self-consistent; I found 7 real findings and explicitly could NOT find count-mismatches in the manifest (reconciles), the verdict schema (agrees 3-way), or the keying (agrees agent↔runtime↔§4). Forcing more would be fabrication.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | VENDOR.md manifest ↔ on-disk Rule-F glob | PASS (F-1 minor) | 15 agent rows = 15 disk agents; 12 SKILL.md rows + 4 `**` glob rows cover 16 disk skill dirs; `check_boundary.py` → PASS exit 0; editor/writer disk sha256 = manifest. 65 manifest rows vs 31 glob files = by-design (adopted resources hashed too). |
| 2 | Schema drift preserved + consumed (not normalized) | PASS | tier_1/2/3 = `conflict_to_cooperation`/`death_euphemism`; tier_5 = `conflict_handling`/`death_handling`; adaptation-rules SKILL L42-43 + tier-coordinator L125 consume key-tolerantly; whole-tree grep found no normalization; §2.2/§2.3 citations match design headings. |
| 3 | safety-verifier verdict schema 3-way (agent/skill/runtime) + `next` rule | PASS on schema+rule (F-4 IMPORTANT, F-5 minor) | Verdict block field-identical across safety-verifier.md L45-64, adaptation-safety SKILL L90-108, runtime ch-01-t1/t3; deterministic `next=revise iff blocking AND FAIL` agrees in both spec files + both runtime reports. F-4: SKILL L75 pseudocode contradicts the rule for T3-advisory-FAIL. |
| 4 | chronicler (work,tier,chapter) keying agent↔runtime↔kb-formats §4 | PASS | chronicler Inv.1-3 ↔ runtime path (`tolkien/tier-N/`) + `[ch-01]` entry stamps + `chapters/ch-01/`; Inv.3 verified (0 transformed names in shared canon, source names only); analysis.yaml promotion byte-identical (sha256 `cd46a709…`) ×3; §4.5 table matches invariants. |
| 5 | CLAUDE.md counts (15/16 target, 11 ADOPTED) ↔ reality | PASS (F-2 minor) | 11 adopted agents (10 CLEAN+1 PATCHED) ✓, 12 adopted skills ✓, 15 agents / 16 skill dirs on disk ✓. F-2: Phase-0 present-tense phrasing stale vs completed tree. |
| 6 | (extra) CLAUDE.md `active_tier` first-class claim ↔ agent bodies | FAIL (F-6 IMPORTANT) | writer.md 0 `active_tier` (adopted, no tier param); tier-coordinator.md takes plural `tiers` (L29) not singular `active_tier`; only safety-verifier + chronicler match the claim. |
| 7 | (extra) design-pack cross-refs disclaimer consistency | FAIL (F-3-REFINED IMPORTANT) | provenance-disclaimer present in 2 files (source-fidelity, analyst) covering skill-specs.md/chapter_analysis.md; absent in 7 files citing kb-formats.md/safety-rubric.md/safety_check.md/design_decisions. |
| 8 | (extra) analyst `status` enum ↔ runtime | PASS (F-7 minor) | 8 top-level keys match runtime exactly; `status: OK` emitted but only `ABORTED` declared in agent body. |
| 9 | (extra) tier_4 interpolation (no stored profile) | PASS | no tier_4.yaml in kb/tiers ✓; tier_4.md resource explicitly "INTERPOLATION, not a stored profile"; adaptation-tiers §Interpolation matches CLAUDE L93-94. |

## Summary
- Checks passed: 6 / 9 (checks 1,2,3,4,5 core PASS on their contract; 8,9 PASS)
- Checks with FAIL-severity findings: 2 (checks 6, 7) + F-4 within check 3
- IMPORTANT issues: 3 (F-3-REFINED, F-4, F-6)
- MINOR issues: 4 (F-1, F-2, F-5, F-7)
- CRITICAL / hard-contract-breaks: 0
- Issues fixed in-place: 0 (fix_authorization = FALSE, report-only)

## Issues Found
| # | Severity | Location | Issue (two conflicting values) | Required Fix |
|---|----------|----------|-------------------------------|--------------|
| F-1 | MINOR | VENDOR.md vs CLAUDE.md L9-10/37-38/52-53 | Manifest has 65 rows (incl. ~38 adopted resources); CLAUDE says Rule-F glob "ONLY covers agents/*.md + skills/**/SKILL.md" (31). | Clarify CLAUDE: manifest hash-pins adopted *resources* too; Rule-F is a *coverage-required* set, not the manifest's full extent. |
| F-2 | MINOR | CLAUDE.md L31-33, L125-126 | "11 ADOPTED present now / authored in Phases 1-2" (Phase-0 present tense) vs completed tree where all 15/16 are present. | Update present-tense clauses to reflect the completed tree, or label the block "Phase-0 snapshot". |
| F-3 | IMPORTANT | chronicler L30/43, safety-verifier L43/27, adaptation-safety L13, adaptation-rules L40/48, thematic L1, vocab L1, tier_4.md — vs source-fidelity L92-94 + analyst L57-60 | Dangling design-pack refs (kb-formats.md, safety-rubric.md, safety_check.md) disclaimed as "provenance-only" in 2 files but NOT in 7 others using the same reference class. | Add the same "build-time provenance, not a runtime dependency" disclaimer to the 7 files, OR vendor the referenced docs in-tree. |
| F-4 | IMPORTANT | adaptation-safety SKILL.md L75 vs L80-81 | Aggregation pseudocode `next=revise if overall==FAIL` → `revise` for T3-advisory-FAIL; deterministic rule → `promote`. | Rewrite L75: `next = "revise" if (mode=="blocking" and overall==FAIL) else "promote"`. |
| F-5 | MINOR | safety-verifier L43 (`safety-rubric.md §4`) vs adaptation-safety L13 (`prompts/verification/safety_check.md`) vs ch-01-t3 L30 (`safety-rubric §3`) | Same verdict/next contract cited under 3 different source-doc labels/sections. | Normalize the citation label + section number across the 3 files. |
| F-6 | IMPORTANT | CLAUDE.md L89-90 vs writer.md (0 active_tier), tier-coordinator.md L29 (`tiers` plural) | CLAUDE claims writer+tier-coordinator take `active_tier`; writer has no tier param, tier-coordinator takes plural `tiers`. | Rewrite CLAUDE L89-90 to name only safety-verifier+chronicler for `active_tier`; describe writer (skill-driven) and tier-coordinator (`tiers` set) correctly. |
| F-7 | MINOR | analyst.md L37/45/53-55 vs work/analysis/ch-01.yaml L3 | Agent declares only `status: ABORTED`; runtime emits `status: OK` (success value undeclared). | Declare the `status` enum (`OK | ABORTED`) in analyst's output contract. |

## Confidence Gate
- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: (via Bash grep) ~14 | Glob: (via Bash find) ~6 | Bash: 12
- All 9 items (5 assigned + 4 extras) verified with tool evidence (grep/find/sha256/check_boundary run + Read). No unchecked, no unverifiable items. No web research performed (all claims were local-tree-intrinsic; Tavily not needed).
- Self-audit: Every PASS/FAIL cites a specific tool result (sha256 hashes, grep line numbers, script exit code). The manifest reconciliation, verdict-schema 3-way agreement, and keying agreement were positively verified — I did not merely assert absence of problems. The adversarial ≥10 prior was tested and honestly not met; I report 7 rather than pad to 10.

## Recommendations
1. Fix F-4 (pseudocode) and F-6 (active_tier claim) first — these are the two spots where a mechanical executor could branch wrong or where the top-level convention doc misdescribes the agents.
2. Resolve F-3 by adding the existing provenance-disclaimer uniformly (cheapest fix; the convention already exists, it's just under-applied).
3. F-1/F-2/F-5/F-7 are documentation-hygiene; batch them.

## QA Complete

---

_Report written incrementally per Critical Rule 1. Findings appended per-check above._

## On-disk inventory (ground truth)
- `agents/*.md`: **15** (analyst, brainstormer, character-sim, chronicler, continuity-checker, critic, editor, muse, outliner, reader-sim, safety-verifier, style-creator, tier-coordinator, web-researcher, writer)
- `skills/**/SKILL.md`: **16** (adaptation-rules, adaptation-safety, adaptation-tiers, creative-research, creative-writing-craft, creative-writing-modes, grill-with-docs, intent-modeling, kb-management, llm-writing, shared-dao, source-fidelity, story-memory, story-review, writing-principles, writing-staffing)
- Total portable components on disk: **31**

---

## CHECK 1 — VENDOR.md manifest reconciles to on-disk Rule-F glob

**Method:** counted manifest data rows and Rule-F glob members on disk; ran `check_boundary.py`.

- Rule-F glob on disk = `agents/*.md` (15) + `skills/**/SKILL.md` (16) = **31 managed files**.
- VENDOR.md manifest data rows = **65** (15 agent rows + 12 adopted SKILL.md rows + ~34 adopted resource rows + 4 skills/`**` glob rows).
- Manifest agent coverage: 15/15 individual rows (10 ADOPTED-CLEAN, 1 ADOPTED-PATCHED [writer], 2 NATIVE [analyst, safety-verifier], 2 BUILD-NEW [chronicler, tier-coordinator]).
- Manifest skill-dir coverage: 12 ADOPTED dirs via per-file rows + 4 NATIVE/BUILD-NEW dirs (adaptation-rules, adaptation-safety, adaptation-tiers, source-fidelity) via `skills/X/**` glob rows = **16/16 dirs covered**.
- `manifest_covers()` (script L170-176) confirms every disk `agents/*.md` + `skills/**/SKILL.md` is covered (individual or glob).
- **Ran** `uv run python laf-adaptation/scripts/check_boundary.py` → `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` exit 0. Rule A (adopted-hash match) passes for all 47 adopted rows against disk; editor.md disk sha256 = manifest laf_sha256 (`2645f358…`); writer.md disk = `c1b3e12f…` = manifest.

**Verdict: PASS (reconciles) — with one MINOR documentation-scope inconsistency (F-1, below).**

The manifest ROW COUNT (65) does NOT equal the Rule-F glob file count (31), but this is BY DESIGN: `--init` (script L255-274) writes per-file rows for ADOPTED skill *resources* (SKILL.md + `resources/**`) so Rule A/B can hash-verify them, while Rule F (L400-403) only *requires* the 31 glob members be covered. Coverage is 1:1 and the check passes. The 65-vs-31 gap is a scope-of-manifest nuance, not a break.

## CHECK 5 — CLAUDE.md counts match reality

- CLAUDE.md L31-33 / L125-126: "**11 ADOPTED agents + 12 ADOPTED skills present now**" and "target: **15 agent files, 16 skill dirs**".
- Reality: manifest adopted agents = 10 ADOPTED-CLEAN + 1 ADOPTED-PATCHED = **11** ✓. Adopted skill dirs = **12** ✓. Disk totals = **15 agents / 16 skill dirs** ✓. NATIVE exemplars (analyst, safety-verifier / adaptation-tiers, adaptation-rules, source-fidelity) and BUILD-NEW (chronicler, tier-coordinator / adaptation-safety) all present and correctly classed in manifest ✓.
- The "15 agents / 16 skills target; 11 ADOPTED present" numbers all match reality.

**Verdict: PASS — with one MINOR temporal-framing inconsistency (F-2, below).**

CLAUDE.md is written in **Phase-0 present tense** ("present now", "authored in Phases 1–2", tree diagram L125-126 says "11 ADOPTED present now… +2 NATIVE +2 BUILD-NEW authored in Phases 1–2"). But the tree is now **COMPLETE** — all 15 agents + 16 skills are on disk. So CLAUDE.md's "present now" clauses describe a Phase-0 snapshot that no longer matches the completed tree's present state. The *target* counts are correct; the *present-tense* phrasing is stale relative to the finished build. Same applies to L124 (UPSTREAM-SYNC.md "authored in Phase 4; present in the completed tree" — that IS present, OK), L132 (source/ "not present at Phase 0"), L134 (templates/ "authored in Phase 1"). templates/work-mapping-template.yaml and UPSTREAM-SYNC.md are both present on disk, consistent with "completed tree". source/ IS present (source/tolkien/ch-01.txt) — consistent.

---

## CHECK 2 — schema drift preserved in YAMLs AND consumed key-tolerantly

**Preservation (kb/tiers/*.yaml):**
- tier_1.yaml L66/73: `conflict_to_cooperation` / `death_euphemism`
- tier_2.yaml L60/68: `conflict_to_cooperation` / `death_euphemism`
- tier_3.yaml L66/69: `conflict_to_cooperation` / `death_euphemism`
- tier_5.yaml L58/61: `conflict_handling` / `death_handling`
- Drift is PRESERVED exactly as designed (T1-T3 one schema, T5 the other). No file renamed a key. `grep` across the whole tree found no normalization of the vendored keys.

**Consumption (reader-tolerant):**
- `skills/adaptation-rules/SKILL.md` L39-43: documents the drift and prescribes `profile.get("conflict_to_cooperation") or profile.get("conflict_handling")` and the death pair — key-tolerant `.get(a) or .get(b)`. Explicitly says "Do NOT rename a key in `kb/tiers/*.yaml`". ✓
- `agents/tier-coordinator.md` L116/119/125: uses key-tolerant reads `death_euphemism`|`death_handling`, `conflict_to_cooperation`|`conflict_handling`, "per the carried-verbatim schema drift noted in CLAUDE.md §3". ✓
- `CLAUDE.md` L97-98: names the drift, mandates normalization "in the *reader* skills… never in the vendored file". ✓
- `skills/adaptation-rules/resources/thematic.md` L52: carries `death_handling:` verbatim from config (correct — it is the carried rule source, not a consumer).

**Section-number citations cross-check (against design `kb-formats.md`):** adaptation-rules SKILL.md L40 cites drift at `kb-formats.md §2.2`; design kb-formats.md §2.2 = "Schema-drift handling" ✓. thematic.md cites `§2.3` as authoritative rule source; §2.3 = "Canonicity: two rule sources reconciled" ✓. Citations are internally consistent.

**Verdict: PASS — drift consistently preserved AND consistently consumed; no file normalized it.**

One cross-phase reference issue surfaced here (F-3, dangling `kb-formats.md`) — see below; it does not break the drift-handling contract because the drift text is *self-contained* in CLAUDE.md §3 + adaptation-rules SKILL.md, and tier-coordinator points to CLAUDE.md §3 (which exists), not only to the missing file.

---

## CHECK 3 — safety-verifier verdict schema consistent across 3 places

**Schema fields (verdict block):** IDENTICAL across all three:
- `agents/safety-verifier.md` L45-64
- `skills/adaptation-safety/SKILL.md` L90-108
- runtime `work/safety-reports/ch-01-t1.md` L43-60 (and `ch-01-t3.md` L15-32)
- All carry: `work, chapter, tier, result{PASS|FAIL|N/A}, sections{forbidden_content, agency_externalization, emotional_safety, safe_home, nightmare_prevention, linguistic}, automatic_failures[], mode{blocking|advisory|skipped}, next{promote|revise}, evidence[]`. Field-for-field agreement. ✓

**The `next` rule (revise iff blocking AND FAIL):** the *deterministic* statement agrees across the two spec files:
- safety-verifier.md L79-84: "`next = revise` iff (`mode == blocking` AND `result == FAIL`); every other case `next = promote`". ✓
- adaptation-safety SKILL.md L78-85: same deterministic predicate, explicitly "align with safety-verifier.md". ✓
- Runtime ch-01-t1.md (T1 blocking PASS → `next: promote`) ✓; ch-01-t3.md (T3 advisory PASS → `next: promote`) ✓.

**Verdict: PASS on the schema + deterministic rule — but with one IMPORTANT intra-file contradiction (F-4).**

**F-4 (IMPORTANT):** `skills/adaptation-safety/SKILL.md` L75 aggregation pseudocode reads
`next = "revise" if overall == FAIL else "promote"`, while L69-72 sets `overall = FAIL` on ANY section FAIL **regardless of mode**. Taken literally, a **T3-advisory FAIL** yields `overall == FAIL` ⇒ pseudocode emits `next = revise`, which **directly contradicts** the deterministic rule (L80-81 and safety-verifier.md L79-84) that T3-advisory always promotes. The authors patched this with a prose caveat (L84-85: "read `overall == FAIL` as scoped to blocking mode") + inline comment (L75), but the *code block itself* is wrong for the T3-advisory-FAIL branch. Two conflicting values for the same input (T3, advisory, a failed section):
  - L75 pseudocode → `next = revise`
  - L80-81 deterministic rule → `next = promote`
An executor mechanically running the L64-75 block (which is what "machine-parseable" invites) branches wrong. The runtime reports don't expose this because both sampled reports are PASS. Recommendation (report-only): rewrite L75 as `next = "revise" if (mode == "blocking" and overall == FAIL) else "promote"` so the code matches the prose.

---

## CHECK 4 — chronicler (work, tier, chapter) keying consistent (agent ↔ runtime ↔ kb-formats §4)

**Agent (`agents/chronicler.md`):** Inv.1 keys every per-tier write by (work, tier, chapter); L69-80 materializes it as work+tier in path (`kb/adaptations/<work>/tier-<N>/`) + chapter in per-chapter path OR stamped on each running-state entry. Inv.2 no cross-tier bleed; Inv.3 no transformed name in shared canon.

**Runtime (`kb/adaptations/tolkien/`):** conforms exactly.
- Path structure: `kb/adaptations/tolkien/tier-{1,3,5}/` with `chapters/ch-01/{adapted.md, analysis.yaml, canon-delta.md}` + running `continuity.md`/`decisions.md`. work=tolkien + tier-N in path ✓.
- Chapter stamp on running-state entries: every continuity.md / decisions.md entry carries `[ch-01]` (e.g. tier-1 continuity L8-12, tier-3 L8-14, tier-5 L7-13; decisions L5-10). Header comments literally state `keyed (work=tolkien, tier=N, chapter)` ✓ — matches chronicler L52-53/L74-80.
- **Inv.3 verified:** `grep` of shared `kb/canon/tolkien/ch-01.md` for transformed names (Grumpy King, Sad Leader, Grumpy Rider, Big Tidy) → **0 hits**; shared canon uses only source names (Sauron, Denethor, Théoden, Nazgûl, Éowyn) ✓.
- **analysis.yaml promotion verified:** all three per-tier `chapters/ch-01/analysis.yaml` are byte-identical (sha256 `cd46a709…`) to `work/analysis/ch-01.yaml` — exactly the copy-on-accept chronicler L43-49 prescribes ✓.

**kb-formats §4 contract (design pack):** §4.5 "(work, tier, chapter) key — enforced everywhere" chronicler row = "Never writes tier-N fact into tier-M continuity; never promotes transformed names to shared canon" ↔ chronicler.md Inv.2 + Inv.3, exact match. §4.1-4.4 file layout (continuity.md, decisions.md, canon-delta.md, analysis.yaml/adapted.md) matches chronicler L30-41 write-targets and the on-disk layout ✓.

**Verdict: PASS — keying fully consistent across agent body, runtime artifacts, and the §4 contract.** (Same F-3 caveat: chronicler L30/43 cites `kb-formats.md §4` which is not shipped in-tree — see F-3.)

---

## F-3 (IMPORTANT) — dangling `kb-formats.md` cross-reference (cross-phase)

Four shipped files cite `kb-formats.md §N` as their authoritative contract source, but **`kb-formats.md` does not exist anywhere under `laf-adaptation/`** — it lives only in the design pack (`.dev/releases/current/0.1/design/kb-formats.md`, outside the shipped tree):
- `agents/chronicler.md` L30 ("per kb-formats.md §4"), L43 ("per kb-formats §4")
- `skills/adaptation-rules/SKILL.md` L40 ("per `kb-formats.md §2.2`"), L48 ("See … kb-formats for the cascade order")
- `skills/adaptation-rules/resources/thematic.md` L1 ("authoritative rule source per kb-formats.md §2.3")
- `kb/vocab.md` L1 ("scaffold placeholder … kb-formats.md §1")

The §-numbers ARE internally consistent with the design doc's headings (§2.2 schema-drift, §2.3 canonicity, §4 keying, §1 layout), so the citations are *accurate* — they just point at a file the shipped tree doesn't carry. Impact: a reader/executor working only inside `laf-adaptation/` cannot resolve any `kb-formats.md §N` reference. Not a contract break (the load-bearing contracts are also stated self-contained in CLAUDE.md §3, chronicler's three invariants, and the safety verdict block), but it is a genuine cross-phase dangling reference repeated in 4 files. Recommendation (report-only): either vendor `kb-formats.md` into the tree (e.g. as a `docs/` or `kb/README`), or rewrite the 4 citations to point at the in-tree contract locations.

---

**F-5 (MINOR):** Source-doc name drift for the same rubric contract: safety-verifier.md L43 cites `safety-rubric.md §4`; adaptation-safety SKILL.md L13 cites `prompts/verification/safety_check.md`; runtime ch-01-t3.md L30 cites `safety-rubric §3`, ch-01-t1.md L43-ref cites `safety-rubric.md §4`. Three different reference labels (`safety-rubric.md`, `prompts/verification/safety_check.md`, `safety-rubric §3` vs `§4`) point at the same verdict/next contract. None of these files exist in-tree (design-pack only), so the labels can't be reconciled by a reader. Non-breaking (schema is self-contained in the shipped files) but the citation labels disagree.

---

## F-3-REFINED (IMPORTANT) — the "build-time provenance" disclaimer is applied INCONSISTENTLY

The tree HAS a documented convention for the dangling design-pack `§`-references — but only in **2 of the ~7 files** that use them:
- `skills/source-fidelity/SKILL.md` L92-94: "any cross-tree `§`-style reference in this skill (e.g. to `skill-specs.md` or `chapter_analysis.md`) is **build-time design-pack provenance, not a runtime dependency**… The in-tree skill body is **self-sufficient**." ✓ (covers skill-specs.md, chapter_analysis.md)
- `agents/analyst.md` L57-60: "The `skill-specs.md §3.2` citation is a **build-time provenance pointer**… not a runtime dependency." ✓ (covers skill-specs.md)

But the following files cite design-pack docs with the SAME syntax and **NO disclaimer** (grep for provenance/build-time/self-sufficient/not-a-runtime → NO DISCLAIMER in each):
- `agents/chronicler.md` (kb-formats.md §4) — no disclaimer
- `agents/safety-verifier.md` (safety-rubric.md §4, safety_check.md) — no disclaimer
- `skills/adaptation-safety/SKILL.md` (prompts/verification/safety_check.md) — no disclaimer
- `skills/adaptation-rules/SKILL.md` (kb-formats.md §2.2) — no disclaimer
- `skills/adaptation-rules/resources/thematic.md` (kb-formats.md §2.3) — no disclaimer
- `kb/vocab.md` (kb-formats.md §1) — no disclaimer
- `skills/adaptation-tiers/resources/tier_4.md` (docs/design_decisions/001-…md, 003-…md) — no disclaimer

So the convention "cross-tree §-refs are provenance-only" is real and correct where stated, but is inconsistently applied: two files disclaim it, seven do not. A reader of chronicler/safety-verifier/adaptation-safety cannot tell whether `kb-formats.md §4` / `safety-rubric.md §4` is a runtime dependency (unresolvable ⇒ blocked) or merely provenance (ignore). This is the core cross-phase inconsistency: **same reference class, two different documentation treatments.**

---

## F-6 (IMPORTANT) — CLAUDE.md `active_tier` first-class claim disagrees with 2 of the 4 named agents

CLAUDE.md L89-90: "`active_tier` is an explicit input parameter in `writer`, `safety-verifier`, `tier-coordinator`, and `chronicler`."

Reality (grep `active_tier` per agent body):
- `safety-verifier.md`: 4 hits — L20 "`active_tier` — the tier being verified (you RECEIVE this)". ✓ takes it.
- `chronicler.md`: 1 hit — L26 inputs "`active_tier` (the partitioning key)". ✓ takes it.
- **`writer.md`: 0 hits — NO tier concept at all.** It is ADOPTED-PATCHED (body byte-identical to upstream CWS writer, which has no tier axis). It is tier-driven only via the `adaptation-rules` skill loaded in frontmatter — it does NOT take `active_tier` as an input parameter in its body. **Conflict:** CLAUDE.md says writer takes `active_tier`; writer.md has no such parameter (and by the boundary contract cannot, since its body is frozen upstream).
- **`tier-coordinator.md`: 0 hits of `active_tier`.** Its INPUT (L29) is `tiers ⊆ {1, 2, 3, 5}` — a **plural set**, because it is the multi-tier fan-out coordinator (it dispatches a singular `active_tier` to each per-tier transform; it does not itself receive one). **Conflict:** CLAUDE.md says tier-coordinator takes singular `active_tier`; the agent takes plural `tiers`.

Two conflicting values:
- CLAUDE.md L89-90: {writer, safety-verifier, tier-coordinator, chronicler} each take `active_tier`.
- Agent bodies: only {safety-verifier, chronicler} take `active_tier`; writer takes none; tier-coordinator takes `tiers` (plural set).

Recommendation (report-only): rewrite CLAUDE.md L89-90 to "`active_tier` is explicit in `safety-verifier` and `chronicler`; `writer` receives the tier axis via the loaded `/adaptation-rules` skill (its adopted body has no tier param); `tier-coordinator` takes the **set** `tiers` and dispatches a singular `active_tier` per transform."

---

## F-7 (MINOR) — analyst `status` enum under-declared vs runtime value

`agents/analyst.md` declares the `status` field's failure value (`ABORTED` on NO-ACCESS, L37/L45/L55) but **never declares the success value**. Runtime `work/analysis/ch-01.yaml` L3 emits `status: OK`. The agent's output-contract enumeration (L53-54: `status, metadata, essentials, characters, events, summary, transformation_flags, uncertainties`) lists `status` as a field but doesn't give its OK/ABORTED enum. The 8 top-level keys match runtime exactly ✓, and `OK` is the reasonable success token, but the contract under-specifies the `status` enum relative to what the runtime emits (a consumer branching on `status` has only `ABORTED` documented). Non-breaking; a documentation-completeness gap.

---
