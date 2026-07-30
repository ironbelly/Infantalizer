# QA Report — Phase 2 Structural / Template Conformance

**Topic:** chapter-materialize skill authoring (Stage-0 source materialization)
**Date:** 2026-07-09
**Phase:** phase-gate (Phase 2 — authored chapter-materialize skill)
**Lens:** template-conformance
**Fix cycle:** N/A (fix_authorization: false — report only)

---

## Overall Verdict: PASS

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Frontmatter uses ONLY `name` + `description`; name == chapter-materialize | PASS | `awk` frontmatter extraction (SKILL.md lines 1-8) yields only `name:`, `description:`, and continuation lines — no `model`/`skills`/`tools`/Mars keys. `name: chapter-materialize` (line 2). Description block is 4-line `\|` abstract ending in "Load when …". Matches house-style model `source-fidelity/SKILL.md` (name+description only, read lines 1-8). |
| 2 | All 13 required sections present IN ORDER | PASS | Heading grep: (2) H1 `# Chapter Materialize — Stage-0 Source Materialization` L10 + Principle line L12-14 (prompt+YAML only, no runtime, check_boundary.py sole script/ADR-006); (3) `## Scope & non-runtime invariant` L16; (4) `## Stage 0.1 — Inventory…` L26; (5) `## Stage 0.2 — Detect input mode` L39; (6) `## Stage 0.3 — Boundary & plan (NO writes)` L55 with `### The five evidence layers` L60 (table) + `### Confidence rule (load-bearing)` L72; (7) `## Stage 0.4 — Commit (gated)` L80; (8) `## Stage 0.5 — Route to gate` L92; (9) `## Format normalization & fidelity` L100; (10) `## Idempotency, collisions, backward-compat` L114; (11) `## Failure modes (release-gating)` L126; (12) `## Manifest output contract` L149; (13) provenance footnote at tail (L208-210). All in blueprint order; no stray H2 after §12 (awk check clean). |
| 3 | No placeholder / TODO / "Builder to author" in EITHER file | PASS | `grep -nE 'TODO\|FIXME\|Builder to author\|TBD\|XXX\|PLACEHOLDER'` over SKILL.md + boundary-rules.yaml → NO-PLACEHOLDERS-FOUND. All `Builder to author` stubs from blueprint §E were fully authored (regex patterns, globs, length floors). |
| 4 | boundary-rules.yaml has schema_version + 5 layer keys + confidence_rule mirror | PASS | YAML parsed (pyyaml via uv): top keys = `schema_version` (=`laf.boundary_rules.v1`), `toc_anchor_map`, `body_heading_map`, `filename_map`, `content_sanity`, `count_reconciliation`, `confidence_rule`. 5 layers present:True; confidence_rule present:True. Mirror comment (L71-73) correctly cites SKILL.md §B6 as authoritative. |
| 5 | Heading hierarchy correct; failure table = header+separator+exactly 16 data rows; manifest schema fence at end of §12 | PASS | H1 single, H2 for stages, H3 only under Stage 0.3 (correct nesting). Failure table (awk-isolated L130-147): header L130 + separator L131 + 16 data rows L132-147 (enumerated). Manifest schema `\`\`\`yaml` fence L156-204 is the sole fence in SKILL.md and is the last content block of §12 before the footnote divider. |

### Acceptance-criteria sub-verifications

| AC clause | Result | Evidence |
|-----------|--------|----------|
| frontmatter name+description only | PASS | Item 1 above. |
| confidence rule verbatim AND bolded | PASS | `grep -F` hit L74 `**"CERTAIN requires ≥2 independent agreeing signals and no contradiction."**` + L76 `**Single-signal boundaries are capped at PROBABLE**` — both bolded, verbatim vs blueprint §3.1. |
| deferred-write invariant verbatim AND bolded | PASS | `grep -F` hit L84 `**"No \`ch-NN.txt\` for a PROBABLE/UNCERTAIN boundary is committed before the human resolves it."**` — bolded, verbatim vs blueprint §3.4. |
| failure table exactly 16 rows | PASS | Item 5; also `diff` blueprint §C rows vs SKILL L132-147 → FAILURE-TABLE-IDENTICAL (byte-for-byte). |
| manifest schema retains every field | PASS | `diff` blueprint §D block (L207-254) vs SKILL L157-204 → MANIFEST-SCHEMA-IDENTICAL (byte-for-byte, every field retained). |
| no placeholders | PASS | Item 3. |

### Supplementary functional verification (adversarial depth)

- boundary-rules.yaml + embedded manifest YAML both parse cleanly (pyyaml `safe_load`, no errors).
- All authored regex patterns compile (`re.compile`, 0 failures) and functionally match their examples: roman pattern matches `CHAPTER XVII` (True); spelled pattern matches `Chapter Twenty-One` (True).
- Sidecar non-membership note bolded + verbatim (L151, blueprint §2 item 12).
- Scope one-liner bolded + verbatim (L24, blueprint §2 item 3).
- Mode-detect precedence order confirmed adopt > folder > file > ambiguity-HALT (L44-51, blueprint §3.2).

## Summary
- Checks passed: 5 / 5 (lens) + 6 / 6 (acceptance criteria)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | — | — | None. Adversarial passes on failure-table row count, byte-level diff of both verbatim blocks, YAML parse, regex compile+match, frontmatter key scan, and section-order all clean. | — |

**Note on the adversarial "expect ≥5 errors" stance:** I actively hunted for the five most likely defect classes — (a) a 15- or 17-row failure table, (b) paraphrased (non-verbatim) failure/manifest blocks, (c) leftover `Builder to author` stubs in the YAML, (d) a stray `model:`/`tools:` frontmatter key copied from an agent template, (e) an out-of-order or missing section (esp. the un-headed provenance footnote or the `### Confidence rule` subsection). Each was tested with a specific tool call and each came back clean. The output is genuinely conformant; the 0-issue verdict is backed by 12 verification commands, not absence of checking.

## Actions Taken
None — fix_authorization is false; report-only mode.

## Recommendations
- None blocking. The two files pass structural/template conformance and are ready for the next gate.
- Advisory (out-of-lens, not a finding): `boundary-rules.yaml` lives inside a skill's `resources/` tree; per `laf-adaptation/CLAUDE.md` this is a permitted NATIVE addition but must not collide with an upstream filename (Rule E) — the blueprint §E already asserts `boundary-rules.yaml` is a novel name. Not verified against the upstream manifest here (outside the template-conformance lens); flag for whichever gate owns boundary-contract/Rule-E verification.

## Confidence Gate

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 0 (grep run via Bash) | Glob: 0 | Bash: 6
  - All lens items verified with direct tool evidence (Read of both target files + blueprint + house-style model; Bash for diff/awk/grep/YAML-parse/regex). No web research performed (no external claims in scope) — Tavily fallback line N/A.
- Every checklist item marked [x] VERIFIED with cited tool output above. 0 UNCHECKED, 0 UNVERIFIABLE.
- Tool-engagement minimum satisfied: 10 verification commands ≥ 5 lens items.

## QA Complete
