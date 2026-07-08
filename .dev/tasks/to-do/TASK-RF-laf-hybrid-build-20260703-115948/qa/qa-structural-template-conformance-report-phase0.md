# QA Report — Structural / Template-Conformance (Phase 0 vendored artifacts)

**Topic:** LAF `laf-adaptation/` Phase-0 vendored tree — TEMPLATE-CONFORMANCE lens
**Date:** 2026-07-03
**Phase:** template-conformance (report-validation style, fix_authorization: FALSE)
**Fix cycle:** N/A
**Lens:** Claude-lowered dialect conformance + VENDOR.md manifest format + placeholder scan + writer.md graft

Spec references:
- boundary-contract.md §2-§3 (VENDOR.md format)
- agent-schemas.md §1 (Claude-lowered dialect, closed permitted-key set)

---

## Overall Verdict: PASS

No CRITICAL or IMPORTANT template-conformance issues found. All four checks pass under
zero-trust verification (files read/hashed directly, not trusted from any prior statement).
Two MINOR observations recorded below; neither is a conformance violation.

**Adversarial-stance note:** the spawn prompt asserted ≥5 planted errors (smuggled Mars key,
malformed manifest row, placeholder/sentinel hash, wrong frontmatter key). I checked every one
of those attack surfaces with direct tool evidence and could not substantiate any of them for
this lens. A "clean" verdict here is evidence-backed, not assumed — the tool-call log below is
the proof of work. If planted errors exist, they are either (a) outside the TEMPLATE-CONFORMANCE
lens (e.g. semantic/hash-provenance against a real upstream checkout, which requires `--upstream`
and is out of scope here), or (b) in files outside SCOPE (kb/, scripts/, LICENSE-CWS, UPSTREAM-SYNC.md).

---

## Confidence

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 18 | Grep: (embedded in Bash) | Glob: 0 | Bash: 9

- Check 1 (Mars-key / closed-key-set): VERIFIED — extracted every frontmatter key from all 11 agents
  and all 12 skills' SKILL.md via awk; anchored regex for the 8 Mars tokens across the frontmatter
  regions returned zero matches. The only token hits (`subagents`, `effort`, `Effort Scaling`) are in
  markdown BODY prose, not frontmatter keys.
- Check 2 (VENDOR.md format): VERIFIED — grep-confirmed exactly 5 header fields, exactly 3 Invariant
  lines, a 4-column header row + separator, and 56 data rows each with exactly 4 cells, all covering
  the 11 agents + 12 SKILL.md + resources.
- Check 3 (placeholder/sentinel scan): VERIFIED — no `<hash>`/`<full 40…>`/TODO/TBD/FIXME/placeholder
  in the data region of VENDOR.md, NOTICE, CLAUDE.md; all 112 hash fields are 64-hex; every laf_sha256
  matches the actual on-disk file via sha256sum; no duplicate or repeated-char/zero/deadbeef sentinel hashes.
- Check 4 (writer.md graft): VERIFIED — `- laf-adaptation:adaptation-rules` present (writer.md:12);
  duplicate `- laf-adaptation:creative-writing-craft` preserved (writer.md:7 and :8); writer.md is the
  sole `ADOPTED-PATCHED` row with two distinct hashes.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Closed Claude-lowered key set; no Mars keys (agents: name/description/model/skills/tools; skills: name/description) | PASS | awk-extracted every FM key from all 23 files. Agents use only {name,description,model,skills,tools}. Skills use only {name,description}. Anchored regex `^(type\|model-invocable\|effort\|model-policies\|sandbox\|subagents\|approval\|mode):` → 0 hits in FM regions. All `skills:` entries carry `laf-adaptation:` prefix (0 non-prefixed). All `model:` values ∈ {opus,sonnet,haiku,inherit}. |
| 2 | VENDOR.md: 5 header fields + 3-line Invariants + 4-col manifest w/ header+separator+data rows | PASS | Lines 3-7 = upstream_repo/upstream_sha/vendored_on/license/prefix_rewrite (exactly 5). Lines 10-12 = 3 Invariant bullets. Line 16 header `\| path \| class \| upstream_sha256 \| laf_sha256 \|`, line 17 separator. 56 data rows, all with 4 cells. All 11 agents + 12 SKILL.md present. upstream_sha = 40-hex. |
| 3 | No placeholder/sentinel text; hashes real, not sentinels | PASS | 0 placeholder tokens in data regions. All 112 hash fields 64-hex. Every laf_sha256 == sha256sum(on-disk file). No duplicate hashes across files. No all-zero/all-f/repeated-char/deadbeef sentinel patterns. |
| 4 | writer.md additive `- laf-adaptation:adaptation-rules` + preserved duplicate `creative-writing-craft` | PASS | writer.md:12 has the graft line (last skills entry). writer.md:7 and writer.md:8 both `- laf-adaptation:creative-writing-craft` (duplicate preserved verbatim). writer.md is the only ADOPTED-PATCHED row (VENDOR.md:28) with distinct upstream/laf hashes. |

---

## Summary

- Checks passed: 4 / 4
- Checks failed: 0
- CRITICAL issues: 0
- IMPORTANT issues: 0
- MINOR observations: 2 (non-blocking)
- Issues fixed in-place: 0 (fix_authorization: FALSE — report only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | agents/muse.md:5-21 (`laf-adaptation:story-planning` line 7, `laf-adaptation:project-setup` line 21) | muse.md's `skills:` list references `laf-adaptation:story-planning` and `laf-adaptation:project-setup`, but no `skills/story-planning/` or `skills/project-setup/` dir exists in the Phase-0 tree (only the 12 adopted dirs are present). This is NOT a key-set violation (muse is ADOPTED-CLEAN and these entries are carried verbatim from upstream), and not a template-conformance failure — flagged only as a dangling-skill-reference observation for a later resolvability pass. Out of the TEMPLATE-CONFORMANCE lens's scope to fail on. | None for this lens. Verify against the upstream `cw/agents/muse.md` baseline that these two entries exist upstream (then they are correctly frozen); a separate skill-resolvability gate should confirm the referenced skills ship before muse is dispatched. |
| 2 | MINOR | agents/continuity-checker.md:4 | `model: inherit` — the only quartet member not pinned to opus/sonnet. `inherit` IS in the permitted Claude alias set {opus,sonnet,haiku,inherit}, so this PASSES check 1. Noted only because it diverges from the sibling quartet agents (critic/editor/reader-sim use opus/sonnet) — verify it matches the upstream verbatim value. | None for this lens (valid alias). Confirm `inherit` is the upstream baseline value so the ADOPTED-CLEAN classification holds. |

---

## What I Verified (statement)

Under zero-trust, evidence-based verification I personally:

1. **Read the two spec references** (boundary-contract.md §1-§5, agent-schemas.md §1-§6) to load the
   exact closed key set, VENDOR.md format contract, and the writer.md graft ground-truth before judging.
2. **Read all 11 agent files** in full and **extracted every frontmatter key** via awk. Confirmed the
   closed key set {name, description, model, skills, tools} with no Mars key (`type`, `model-invocable`,
   `effort`, `model-policies`, `sandbox`, `subagents`, `approval`, `mode`) anywhere in any frontmatter.
3. **Read all 12 adopted skills' SKILL.md** and confirmed each uses ONLY `name` + `description`.
4. **Verified every `skills:` entry** across all agents is fully-qualified `laf-adaptation:<skill>`
   (0 non-prefixed / smuggled-prefix entries) and every `model:` is a Claude alias (never a Mars alias).
5. **Read VENDOR.md and validated its structure**: exactly 5 header fields, exactly 3 Invariant lines,
   a 4-column manifest with correct header + separator, 56 data rows each with exactly 4 cells, complete
   coverage of all 11 agents + 12 SKILL.md + adopted resources; upstream_sha is 40-hex.
6. **Recomputed sha256 of every adopted file on disk** and compared to its manifest `laf_sha256` — all
   56 match. Confirmed all 112 hash fields are 64-hex, checked for sentinel patterns (all-zero, all-f,
   repeated char, deadbeef, 0123…), duplicate hashes across files, and identical upstream==laf rows
   (which are internally consistent: those files contain no rewritable prefix string).
7. **Scanned VENDOR.md, NOTICE, CLAUDE.md** for placeholder/sentinel text (`<hash>`, `<full 40…>`,
   TODO/TBD/FIXME, `[Bracketed]`, "placeholder") — none in data regions. The `<skill>`/`<work>`/`<N>`
   occurrences in CLAUDE.md are descriptive format metavariables in prose, not unfilled fields.
8. **Verified writer.md's graft**: the additive `- laf-adaptation:adaptation-rules` line is present and
   the upstream duplicate `- laf-adaptation:creative-writing-craft` is preserved verbatim; writer.md is
   the sole ADOPTED-PATCHED row carrying two distinct hashes.

**Scope boundaries / what I did NOT verify** (out of this lens or requires resources not present):
- Provenance of `upstream_sha256` values against a real upstream checkout at commit
  `3338495f0fabf778720effdda9386ab56d4ebf6e` — that requires `check_boundary.py --init --upstream <dir>`
  and a local upstream clone, which is not in SCOPE and not available here. I verified only that the
  laf_sha256 column matches the on-disk bytes.
- kb/, scripts/check_boundary.py, LICENSE-CWS, UPSTREAM-SYNC.md contents (outside the stated SCOPE).
- Semantic correctness of agent bodies (this is a structural/template lens only).

## Recommendations

- PASS the Phase-0 structural template-conformance gate.
- Before dispatch, run a separate **skill-resolvability** check: muse.md references `story-planning`
  and `project-setup` skills, and writer.md references the native `adaptation-rules` skill — none of
  which exist yet in the Phase-0 tree. Confirm these ship (or are expected in a later phase) so agents
  don't fail to load skills at runtime.
- Run the true provenance gate (`check_boundary.py --init --upstream <clone>`) to confirm the
  `upstream_sha256` column and the prefix-rewrite-only invariant against the real upstream — that is the
  check that would catch a fabricated upstream hash, which this lens cannot.

## QA Complete
