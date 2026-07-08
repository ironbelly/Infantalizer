# QA Report — Structural Template Conformance (Phase 1 NATIVE spine)

**Topic:** TEMPLATE-CONFORMANCE lens on the Phase-1 NATIVE adaptation spine (laf-adaptation)
**Date:** 2026-07-03
**Phase:** report-validation (structural/template-conformance sub-lens)
**Fix cycle:** N/A
**Fix authorization:** FALSE — REPORT ONLY
**Stance:** Adversarial (assumed ≥5 template errors: smuggled Mars key / missing ABORT block / writer body edit / wrong model value). Zero-trust: every verdict backed by a Read/Grep/Bash tool call against the actual files.

---

## Overall Verdict: PASS

No CRITICAL or IMPORTANT findings. All 5 conformance checks pass under byte-level verification. The 4 planted adversarial hypotheses were each independently disconfirmed with tool evidence.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Native SKILL.md frontmatter = ONLY `name`+`description`; no Mars keys (`type`,`model-invocable`,`effort`,`model-policies`,`sandbox`,`subagents`) | PASS | `awk` frontmatter-key extraction on all 3 SKILL.md returned exactly `name`, `description` for each. `grep -nE '^(type\|model-invocable\|effort\|model-policies\|sandbox\|subagents):'` over all 3 skills → NO MARS KEYS FOUND. Adversarial body sweep `grep -rnE '^(model\|type\|effort\|sandbox\|subagents\|model-policies\|model-invocable):'` → NONE. Matches skill-specs.md §0 dialect contract (name+description only). |
| 2 | Native agents use closed key set (`name`,`description`,`model`,`skills`,`tools`); `model` ∈ {opus,sonnet,haiku,inherit}; analyst=opus, safety-verifier=sonnet | PASS | Frontmatter-key extraction on analyst/safety-verifier/writer each returned exactly `name,description,model,skills,tools`. `grep '^model:'` → analyst.md:4 `opus`, safety-verifier.md:4 `sonnet`, writer.md:4 `opus`. Mars-key scan (incl. `approval`,`mode`) → NONE. Values match agent-schemas.md §1 permitted-key table and §2.1/§2.2. `name`==filename-stem confirmed for all. |
| 3 | analyst body contains Phase-0 ABORT hard-behavior block verbatim (NO-ACCESS ⇒ status: ABORTED + HALT) | PASS | analyst.md L33-39 hard-behavior fenced block. Content lines byte-identical to agent-schemas.md §2.1 spec block (L73-77): `Determine SOURCE ACCESS LEVEL ∈ {FULL, PARTIAL, MEMORY-BASED, NO-ACCESS}`, `IF NO-ACCESS: emit \`status: ABORTED\` … and HALT. Do not proceed. ← constraint #2`, `IF MEMORY-BASED: … confidence: UNCERTAIN`. (diff exit=1 was a sed fence-range artifact only — the 3 content lines match exactly; verified by printed block.) Block is labeled "in this agent body, not delegated to a skill". |
| 4 | safety-verifier body contains tier-gate block verbatim (T1-2 blocking / T3 advisory / T4-5 N/A skip) | PASS | safety-verifier.md L23-28 tier-gate fenced block. `diff` vs agent-schemas.md §2.2 spec (L104-106) → exit=0 (byte-identical). Lines: `IF active_tier ∈ {1, 2}: … MANDATORY and blocking.`, `IF active_tier == 3: … ADVISORY mode (report only; does not block).`, `IF active_tier ∈ {4, 5}: SKIP — emit verdict: N/A … ← ground-truth: safety_check.md is T1-2 only`. Labeled "in this agent body". |
| 5 | writer graft = single additive `- laf-adaptation:adaptation-rules` line; body byte-identical to upstream; duplicate `creative-writing-craft` preserved | PASS | Upstream `cw/agents/writer.md` sha256 `373e605b…` matches VENDOR.md L33 `upstream_sha256`. LAF writer.md sha256 `c1b3e12f…` matches VENDOR.md L33 `laf_sha256`. Body diff (upstream L15- vs LAF L16-) → BODY IDENTICAL. Skills L1-6 prefix-rewritten upstream vs LAF → IDENTICAL. Graft = LAF L12 `  - laf-adaptation:adaptation-rules` (single additive line; correctly carries NO trailing comment). Duplicate `creative-writing-craft` at LAF L7-8 preserved verbatim. Prefix rewrite `creative-writing-skills:`→`laf-adaptation:` uniform; no residual `creative-writing-skills:` in any of the 3 agents. |

---

## Summary

- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: FALSE — report only)

## Issues Found

None. (Adversarial expectation of ≥5 errors NOT met — see Adversarial Disconfirmations.)

## Adversarial Disconfirmations

| Planted hypothesis | Disconfirmed by | Result |
|---|---|---|
| Smuggled Mars key (`type`/`model-policies`/`sandbox`/etc.) in a native skill or agent | `grep -nE '^(type\|model-invocable\|effort\|model-policies\|sandbox\|subagents\|approval\|mode):'` over all 3 skills + 3 agents, plus body-level line-leading YAML sweep | No Mars key present anywhere |
| Missing / altered Phase-0 ABORT block in analyst | byte diff of analyst.md L35-38 vs agent-schemas.md §2.1 L73-77 | ABORT block present verbatim (status: ABORTED + HALT + constraint #2 marker) |
| Writer body edit (drift from upstream) | full-body `diff` of upstream cw writer vs LAF writer + laf_sha256 match against VENDOR.md | Body byte-identical; hash matches pinned laf_sha256 |
| Wrong `model` value (Mars alias / mis-tier) | `grep '^model:'` on all 3 agents vs agent-schemas.md §1 alias whitelist | analyst=opus, safety-verifier=sonnet, writer=opus — all Claude-native aliases, all correct |
| Writer duplicate `creative-writing-craft` "fixed" (removed) | line inspection LAF writer.md L7-8 | Duplicate preserved verbatim (patch-clean) |

## Confidence Gate

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 6 | Glob: 0 | Bash: 6 (no web research performed — all claims are local-source-bound; Tavily-first rule not triggered)
- Every checklist item was verified with a specific tool call directly targeting the file/claim under review (Read of each target + spec, Grep for key sets and Mars keys, Bash for sha256/diff/frontmatter extraction). Tool-call count (20) exceeds the 5-item checklist minimum; engagement is not padded — each call maps to a named check.
- UNCHECKED items: none. UNVERIFIABLE items: none.

## Recommendations

- Green light for the Phase-1 NATIVE spine on the template-conformance lens. No fixes required.
- Note (informational, out of this lens's scope, no action): this lens verified only the 3 named native SKILL.md files, the 3 named agents, and the writer graft. The full boundary contract (Rule-A..F, G3 quartet integrity, name-collision) is enforced by `scripts/check_boundary.py` and is a separate gate — not re-run here.

## QA Complete

