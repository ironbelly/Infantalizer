# QA Report — Report Validation (TEMPLATE-CONFORMANCE lens)

**Topic:** laf-adaptation hybrid build — complete assembled tree, all phases
**Date:** 2026-07-04
**Phase:** report-validation (template-conformance lens)
**Fix cycle:** N/A
**Fix authorization:** FALSE (report only)
**Scope:** complete tree under `/config/workspace/Infantalizer/laf-adaptation/` — 15 agents, 16 skills, VENDOR.md, NOTICE, LICENSE-CWS, CLAUDE.md, UPSTREAM-SYNC.md
**Specs:** `.dev/releases/current/0.1/design/{boundary-contract.md §2, agent-schemas.md §1, skill-specs.md}`

---

## Overall Verdict: PASS (with 1 INFORMATIONAL observation; 0 CRITICAL/IMPORTANT/MINOR conformance defects)

The adversarial hypothesis (≥10 template-conformance errors: smuggled Mars key, malformed manifest row,
placeholder hash, missing root file) is **NOT borne out**. Every check was verified against actual files
with tool evidence. The one item that superficially trips a "Mars-key-anywhere" grep is a **correctly
preserved upstream-verbatim artifact** in adopted resource files, required by the boundary contract —
documented below as INFORMATIONAL, not a defect.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | No Mars keys in agent frontmatter | PASS | `grep -rnE '^(type\|model-invocable\|effort\|model-policies\|sandbox\|subagents\|approval\|mode):' agents/*.md` → NONE. All 15 agents dumped; only native keys present. |
| 1b | No Mars keys in SKILL.md frontmatter | PASS | All 16 SKILL.md frontmatter keys enumerated = `[name description]` only, every file. |
| 1c | No Mars keys in agent/SKILL bodies | PASS | `grep -rnwE 'model-policies\|model-invocable\|subagents\|sandbox\|effort'` on bodies → NONE (the lone `subagents` hit in shared-dao/SKILL.md:57 is the English word in prose, not a key). |
| 1d | No Mars model aliases | PASS | `grep -E '^model:\s*(opus[0-9]\|gpt\|deepseek\|...)'` → NONE. model ∈ {opus×6, sonnet×8, inherit×1}, all valid Claude aliases. |
| 2 | NATIVE/BUILD agents = Claude-native frontmatter, exact schema match | PASS | analyst/safety-verifier/chronicler/tier-coordinator frontmatter compared byte-wise to agent-schemas.md §2.1/§2.2/§5.1/§5.2 — exact match (analyst correctly omits the vendor-time comment line). model ∈ enum, skills fully-qualified, tools valid. |
| 2b | NATIVE/BUILD skills = name+description only | PASS | adaptation-{rules,safety,tiers}, source-fidelity frontmatter = `[name description]` only. |
| 2c | ADOPTED-PATCHED writer.md graft correct | PASS | Full read: duplicate `creative-writing-craft` preserved verbatim, single additive `- laf-adaptation:adaptation-rules` line, body byte-clean, native dialect. laf_sha256 matches disk; upstream≠laf hashes (patched) as expected. |
| 2d | Authored skill resources have no Mars keys | PASS | 10 native/build resource files (adaptation-safety/rules/tiers) scanned → all clean. |
| 3 | VENDOR.md 5 header fields + 3-line Invariants + 64-row manifest, no placeholder | PASS | All 5 fields present; exactly 3 invariant lines; manifest = 55 ADOPTED-CLEAN + 1 ADOPTED-PATCHED + 5 NATIVE + 3 BUILD-NEW = **64 rows** (= "56 adopted + 5 NATIVE + 3 BUILD-NEW"). No `<hash>`/`—`/empty cell in any adopted row. upstream_sha = real 40-hex. 3/3 spot-checked laf_sha256 MATCH disk. |
| 3b | Every agent + skill on disk is manifested; every manifested file exists | PASS | 15/15 agents match disk↔manifest; 4 native/build skill dirs covered by `**` rows; no unmanaged agent/SKILL. |
| 3c | G3 quartet ADOPTED-CLEAN + no NATIVE/BUILD name collision | PASS | critic/editor/reader-sim/continuity-checker all ADOPTED-CLEAN in manifest; authored names (analyst, safety-verifier, chronicler, tier-coordinator, adaptation-*) distinct from all adopted names. |
| 4 | NOTICE + LICENSE-CWS + CLAUDE.md + UPSTREAM-SYNC.md present & well-formed | PASS | All present, non-empty (48/201/137/75 lines). SHA + vendored_on consistent across VENDOR↔NOTICE. LICENSE-CWS = full 201-line Apache-2.0 text. |
| 5 | No placeholder/sentinel/TODO in authored files | PASS | Full-tree sweep for `<hash>/<full 40/TODO/FIXME/TBD/PLACEHOLDER/stub/<sha>/REPLACE_ME/...` → NONE in authored files. (Sole `<hash>` hit is a rejection-token literal in check_boundary.py:145 — the parser guarding against placeholders — not a leak.) All frontmatter blocks well-formed (2 `---`). No forbidden `rules/`/`templates/` subdir inside any skill. |

---

## Summary
- Checks passed: 13 / 13
- Checks failed: 0
- CRITICAL issues: 0 | IMPORTANT: 0 | MINOR: 0 | INFORMATIONAL: 1
- Issues fixed in-place: 0 (fix_authorization: FALSE — report only)

---

## Issues Found

| # | Severity | Location | Issue | Assessment |
|---|----------|----------|-------|-----------|
| 1 | INFORMATIONAL | 7 adopted resource files (see list) | Frontmatter carries Mars-ish keys `type: reference` and `model-invocable: true`. A naive "no Mars key anywhere" grep flags these. | **NOT a defect.** All 7 are `ADOPTED-CLEAN` resource sub-files, byte-identical to upstream (upstream_sha256 == laf_sha256, pure passthrough; disk matches manifest hash). The boundary contract (boundary-contract.md §3.2 Rule A) *requires* these to be byte-identical to upstream; stripping the keys would change the hash and **fail** `check_boundary.py`. The dialect contracts (agent-schemas §1, skill-specs §0) scope Mars-key prohibition to **agent frontmatter and SKILL.md frontmatter** — NOT adopted resource sub-files. CHECK 1's grep scope is explicitly "agents + all SKILL.md"; these hits are in `resources/*.md`, outside that scope. Authored files carry zero such keys (verified). Correct adoption, not smuggling. |

**Affected resource files (all ADOPTED-CLEAN, upstream-verbatim):**
`skills/story-review/resources/prose-critique.md:6`, `skills/creative-writing-craft/resources/style-analysis.md:6`,
`skills/story-memory/resources/writing-issues.md:6`, `skills/creative-writing-craft/resources/prose-writing.md:6`,
`skills/creative-writing-craft/resources/scene-construction.md:6`, `skills/story-memory/resources/story-reference-writing.md:6`,
`skills/story-memory/resources/fact-extraction.md:6`.

---

## Additional Observation (tree completeness, NOT a template-conformance defect)

Four `skills:` entries in **ADOPTED agents** point to skill dirs that LAF did not vendor:
`laf-adaptation:character-sim` (character-sim.md, muse.md), `laf-adaptation:reader-sim` (reader-sim.md, muse.md),
`laf-adaptation:story-planning` (brainstormer.md, muse.md, outliner.md), `laf-adaptation:project-setup` (muse.md).

- **Not a dialect/template error.** These are carried-verbatim upstream references, prefix-rewritten
  `creative-writing-skills:`→`laf-adaptation:` per contract, and frozen by the hash gate. Editing them
  out would break Rule A/C. LAF adopted 12 of upstream's skills (confirmed = 12); these 4 upstream skills
  were intentionally not adopted, leaving dangling *runtime-resolution* refs — a coverage/completeness
  matter, not a frontmatter-conformance matter.
- **All 4 AUTHORED (NATIVE/BUILD-NEW) agents** reference only skills that exist on disk. No authored
  dangling ref exists. This is the boundary contract behaving exactly as designed.
- Surfaced here for the record; a separate runtime-completeness lens (not template-conformance) should
  decide whether these upstream skills need vendoring or the adopted frontmatter's dangling refs are
  acceptable-by-contract.

---

## Confidence Gate

- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: (folded into Bash) | Glob: 0 | Bash: 11
  (No web research performed — all claims are source-truth-local; Tavily not required.)
- Every checklist item categorized VERIFIED with cited tool output (grep results, sha256 spot-checks,
  frontmatter dumps, manifest row enumeration).
- UNCHECKED: none. UNVERIFIABLE: none.
- **Self-audit:** The adversarial prompt asserted ≥10 errors. I did not confirm-absence lazily — I
  independently enumerated all 15 agent + 16 skill frontmatter blocks, all 64 manifest rows, spot-checked
  3 real sha256 hashes against disk, and ran a deep body/resource Mars-key scan that DID surface 7 hits —
  then proved each is a contract-required upstream-verbatim artifact rather than dismissing them. The one
  item that looks like a violation to a shallow pass is documented and explained, not hidden. A shallow
  reviewer would either (a) miss the 7 resource-file keys entirely, or (b) false-FAIL on them; this pass
  did neither.

---

## Recommendations
- **Template-conformance: green light.** The assembled tree is dialect-conformant end-to-end.
- Route the two non-conformance observations to the correct lens:
  1. The 7 adopted-resource `model-invocable`/`type` keys — no action (contract-required); note in review
     notes so the next reviewer doesn't re-flag them.
  2. The 4 dangling adopted-agent skill refs (`character-sim`, `reader-sim`, `story-planning`,
     `project-setup`) — evaluate under a **runtime-completeness** lens, not template-conformance.

## QA Complete
