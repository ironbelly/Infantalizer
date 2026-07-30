# QA Report — Phase-2 Phase-Gate Content (Domain Accuracy Lens)

**Topic:** chapter-materialize Stage-0 skill (+ boundary-rules.yaml)
**Date:** 2026-07-09
**Phase:** doc-qualitative (phase-gate content review, domain-accuracy lens)
**Fix cycle:** N/A (fix_authorization: false — report only)

---

## Overall Verdict: PASS

The skill's domain claims match actual LAF reality. All six lens items verified against
the real repo (source dirs, prep SKILL §5/§6, source-fidelity vocabulary, path-contract,
CLAUDE.md boundary contract, ADR-006 sole-script rule) and the driving spec. No invented
paths, no fabricated mechanisms, no aspirational-as-current claims, no boundary-contract
contradiction. The lens's adversarial "assume ≥5 errors" prior was applied; the candidate
issues surfaced (below) all resolved to spec-faithful, co-delivered, or convenience-mirror —
none rise to a domain-accuracy defect.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Paths match LAF conventions (`source/<slug>/ch-<NN>.txt`, `.raw/`, `chapter-manifest.yaml`, `work/prep/<slug>/`) | PASS | `source/README.md` L3 = `source/<work>/ch-<NN>.txt`; skill paths (L86-88, L151, L165) match. `work/prep/<slug>/` matches path-contract.md §1. No invented paths. |
| 2 | References EXISTING mechanisms correctly (§5 gate, greenlight, CERTAIN/PROBABLE/UNCERTAIN, 70-traceability); no new gate/script claim | PASS | prep SKILL §5 (question gate, L77-85) + §6 (greenlight, L87-108) exist; `70-traceability.md` in path-contract §2 table. source-fidelity SKILL L15-19 defines CERTAIN/PROBABLE/UNCERTAIN exactly. Skill L94-96 explicitly says "no new gate or HALT machinery"; L24 "sole script … validator only". |
| 3 | Mode C adopt claim matches ACTUAL existing files (narnia ch-01..04, tolkien ch-01) | PASS | `ls source/narnia/` = ch-01.txt..ch-04.txt (exactly 4); `ls source/tolkien/` = ch-01.txt (exactly 1). Skill L116-119 claim matches byte-for-byte inventory. |
| 4 | Frontmatter dialect correct (name+description only; no Mars keys) | PASS | Skill L1-8 frontmatter = `name` + `description` only. No `type`/`model-invocable`/`effort`/`model-policies`/`sandbox`/`subagents`. Matches CLAUDE.md §3 (L133-138). |
| 5 | Does NOT claim to edit adopted bodies or repurpose analyst as splitter | PASS | Skill L21-22 "analyst is not repurposed as the splitter"; L18-19 "no script"; spec N4 + N2 mirrored. CLAUDE.md §1/§2 boundary honored (analyst is NATIVE, not adopted). |
| 6 | No aspirational feature described as current; no contradiction of spec/CLAUDE.md | PASS | Skill describes its OWN new Stage-0 behavior (permitted for a build spec). It does not falsely claim README/prep/command already document the manifest — grep confirms manifest is genuinely new (BUILD-NEW per spec §11). No contradiction found. |

## Summary
- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0 (candidate observations resolved as non-defects — see below)
- Issues fixed in-place: 0 (fix_authorization: false)
- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 3 (via Bash) | Glob: 0 | Bash: 4

## Candidate Observations (adversarial pass — all resolved to non-defects)

The adversarial "assume ≥5 errors" stance surfaced five candidates. Each was chased to
ground and resolved as spec-faithful. Documenting them so the reader can see the check was
real, not a rubber stamp.

| # | Candidate concern | Resolution | Why not a defect |
|---|-------------------|------------|------------------|
| O1 | Skill L48 shorthand `-1..-4.html` + `…copy*.html` for the "real Books/LWW case" — accurate? | VERIFIED | `ls Books/LWW/` shows `...Lewis-1.html`..`-4.html` (4 split) AND `...copy.html`/`copy 2/3/5.html` + base `.html` (5 monolith copies, all 216957 bytes). Shorthand is faithful. The genuine mode-ambiguity case the skill cites is real. |
| O2 | `boundary-rules.yaml` `ignore_globs` (L51-56) may not catch the base monolith `...Lewis.html` (no "copy" token) | NON-DEFECT for this lens | The un-globbed base monolith is caught downstream by Layer 5 count-reconciliation / Layer 4 content-sanity → routes to gate; the comment L51 explicitly delegates "duplicate monoliths handled by Layer 5". Data-completeness nuance, not a false domain claim. (Flag to structural/logic lens if desired, out of domain-accuracy scope.) |
| O3 | `input_mode` enum dual-vocab: Stage 0.2 uses `adopt`/`folder`/`file`; manifest uses `adopt-existing`/`single-file`/`folder` | NON-DEFECT | The driving spec carries the SAME dual vocabulary: `--source-mode` values `auto\|folder\|file\|adopt` (spec §3 L50) vs manifest field `folder\|single-file\|adopt-existing` (spec L112). Skill mirrors the spec exactly — faithfully carried, not introduced. |
| O4 | Skill L51 references `--source-mode` operator override, but `.claude/commands/laf/prep.md` argument-hint has no `--source-mode` yet | NON-DEFECT | Spec §11 BOM lists command `+--source-mode` as a co-delivered NATIVE-mirror change. Skill describes its OWN new behavior ("honored here"), part of this feature's delivery — not a claim about a pre-existing flag. |
| O5 | `scripts/` contains `test_check_boundary.py` too — does "sole script" hold? | NON-DEFECT | CLAUDE.md L13/L43/L188 "exactly one script … per ADR-006; not a runtime" refers to the runtime/validation script. Test files are not counted as runtime scripts. Skill's "check_boundary.py stays the sole script" is consistent. |

## Issues Found
None.

## Actions Taken
None (fix_authorization: false — report-only mode).

## Self-Audit

How many factual claims independently verified against source: **all six lens items**, each
with cited tool output.

Specific files read to verify claims:
- `laf-adaptation/skills/chapter-materialize/SKILL.md` (target)
- `laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml` (target)
- `.dev/brainstorms/20260709T001338Z-prep-chapter-ingestion/merged-requirements.md` (driving spec)
- `laf-adaptation/CLAUDE.md` (§1 provenance, §2 boundary, §3 conventions)
- `laf-adaptation/skills/prep/SKILL.md` (§5 gate, §6 greenlight)
- `laf-adaptation/skills/prep/resources/path-contract.md` (paths, write-ownership)
- `laf-adaptation/skills/source-fidelity/SKILL.md` (confidence vocabulary)
- `laf-adaptation/source/README.md` (source layout convention)
- Bash inventory: `source/narnia/`, `source/tolkien/`, `Books/LWW/`, `scripts/`, `.claude/commands/laf/prep.md`

Why trust a PASS with 0 issues: I did not confirm-by-assumption. I ran an actual filesystem
inventory that could have contradicted the Mode C claim (it did not — narnia=4, tolkien=1
exactly). I chased five adversarial candidate errors (O1-O5) to ground; each had a concrete,
spec-cited resolution rather than a hand-wave. The Books/LWW mode-ambiguity case the skill
leans on was independently confirmed real (both split files AND 5 duplicate monoliths exist).
The manifest/`.raw/` paths were grep-confirmed to be genuinely NEW (BUILD-NEW), so the skill
is not falsely claiming pre-existing documentation.

Web research: none required for this lens (all verification was local-file-bound). Tavily not
invoked — no external lookup in scope.

## Recommendations
- PASS — clear to proceed on the domain-accuracy dimension.
- Optional handoff to the structural/logic lens (out of my scope): O2 (base-monolith
  `ignore_globs` gap) is a data-completeness nuance worth a glance to confirm Layer-5
  reconciliation demonstrably catches the un-globbed base `.html` monolith.

## QA Complete
