# QA Report — SOURCE-FIDELITY lens (Phase-0 vendored files)

**Topic:** Byte-fidelity of vendored creative-writing-skills (laf-adaptation) vs upstream Claude-lowered source
**Date:** 2026-07-03
**Phase:** doc-qualitative (SOURCE-FIDELITY lens)
**Fix cycle:** N/A (REPORT ONLY — fix_authorization: FALSE)
**Stance:** Adversarial / zero-trust — direct byte comparison via sha256 + cmp + recursive path diff

UPSTREAM: `/config/workspace/Infantalizer/.dev/releases/current/0.1/creative-writing-skills/cw/`
VENDORED: `/config/workspace/Infantalizer/laf-adaptation/`
Prefix rewrite applied to upstream bytes before hashing: `creative-writing-skills:` → `laf-adaptation:`

---

## Overall Verdict: PASS

All four assigned fidelity checks pass with zero breaches. The adversarial hypothesis of ≥5 fidelity breaches (a "fixed" quirk, a silent body edit, a dropped resource, a normalized key) is **NOT supported** by direct byte comparison. The vendoring was performed cleanly: the ONLY transformations are (a) the mechanical `creative-writing-skills:` → `laf-adaptation:` namespace rewrite in the 11 agent files, and (b) the single additive graft line in `writer.md`. No adopted content body was silently edited, no resource was dropped, no upstream quirk was "fixed", no key was normalized.

**Assigned-check issue count: 0.**
Two out-of-scope observations recorded (do not affect the fidelity verdict).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1a | 10 ADOPTED-CLEAN agents byte-identical to prefix-rewritten upstream | PASS | 10/10 sha256 MATCH |
| 1b | ≥8 skill files (incl. resources) byte-identical | PASS | 45/45 skill files MATCH (33 of them resources) |
| 2 | writer.md: additive graft is ONLY frontmatter delta; body byte-identical; duplicate `creative-writing-craft` preserved | PASS | body sha256 MATCH; single-line diff; duplicate line intact |
| 3 | No adopted resource dropped/added across 12 skills | PASS | recursive relative-path diff clean; 45/45 files, 12/12 skills |
| 4 | LICENSE-CWS == upstream ../LICENSE verbatim | PASS | `cmp` identical; sha256 match |

---

## Check 1 — ADOPTED-CLEAN byte-identity (agents + skill files)

**Method:** `sha256( prefix_rewrite(upstream_bytes) )` vs `sha256( vendored_bytes )`. Prefix rewrite replaces the byte sequence `creative-writing-skills:` with `laf-adaptation:` in the upstream file before hashing.

### 1a — 10 clean agents (writer.md excluded → Check 2)

All 10 MATCH:

| agent | sha256 (upstream-rewritten == vendored) |
|-------|------------------------------------------|
| brainstormer | `5c827effb5dc03364e339f3657356218dcb00288a596efc427e2c3e79a5752bc` |
| character-sim | `c7fcfc91a6d60bd4af3f555ce6e6c148f0a39887ff57ef136838b15c15ae75ed` |
| continuity-checker | `28a3c7eb7870ec29972da3da80c2baee093d621c5df4f3c3aa3ef56a364861cc` |
| critic | `9a0078e943c564010b8e1211e98b5a3b781ab9d7628f4ce06c39243d026ec21b` |
| editor | `2645f358fdc0f6b011479fa27195ba096c3836d2c6c4e7955bd78c1da82410e3` |
| muse | `18cafdc251a528f0186d2d74135ae94cad0d05d37d2bf8f399a134969409af8f` |
| outliner | `d7b4b6e169c68da805178f4199129296afbeee52080abbb0ffb05059d13c2aaa` |
| reader-sim | `902a04a3aae0f784b3556c67c1a21bf4ffd69942d6a257bda06991ca58051bcf` |
| style-creator | `655ed29aba168a709bd7be95bbaa226d87bb9e0f72e3299d15d67a1d569251b4` |
| web-researcher | `fe3716801468128ec3f8408735c7b0bd03b333b76717e68097ba4420b9dc0ab3` |

**Load-bearing confirmation (anti-false-positive):** raw upstream `brainstormer.md` sha = `aa736c5d...fa73` ≠ vendored `5c827eff...52bc`; they match ONLY after the prefix rewrite. This proves the rewrite is genuinely load-bearing on agents (upstream actually carries the `creative-writing-skills:` token, which the vendored files correctly carry as `laf-adaptation:`), not a case where the file was left untouched-and-wrong. The token appears in all 11 upstream agent files and 0 upstream skill files.

### 1b — all 45 adopted skill files (superset of the required ≥8 spot-check)

Rather than spot-check 8, I hashed **all 45** skill files across the 12 adopted skills after prefix rewrite. Result: **45 checked, 33 of them resources, 0 mismatches.** Every skill file — SKILL.md and every resource under `resources/` — is byte-identical to upstream. (The prefix rewrite is a no-op on skill files since none contain the token, so the byte-identity of skill content is genuine and unmasked.)

Zero `creative-writing-skills:` token leaked into any vendored agent or skill file (grep count = 0 in vendored tree).

---

## Check 2 — writer.md additive graft

- **Body:** `sha256(prefix_rewrite(upstream body)) == sha256(vendored body)` = `174b2238cb242963a9adff2e8aa6cdfb918ba46fc02350ed1ffa5133c6aab145` → **BYTE-IDENTICAL**.
- **Frontmatter delta (only difference):** a single added line at position 11 of the skills list:
  ```
  +  - laf-adaptation:adaptation-rules
  ```
  This is the sole frontmatter delta beyond the mechanical prefix rewrite. No other field added, removed, or reordered.
- **Upstream duplicate PRESERVED:** the upstream `skills:` list contains `creative-writing-craft` **twice** (lines 7 and 8). The vendored file preserves BOTH occurrences (`laf-adaptation:creative-writing-craft` appears twice). The duplicate was **NOT deduped / "fixed"** — quirk faithfully carried through.

---

## Check 3 — no adopted resource dropped (recursive path diff, 12 skills)

Recursive `find . -type f | sort` relative-path diff, upstream `cw/skills/<name>/` vs vendored `laf-adaptation/skills/<name>/`:

| skill | up files | vn files | diff |
|-------|---------|---------|------|
| creative-research | 1 | 1 | clean |
| creative-writing-craft | 10 | 10 | clean |
| creative-writing-modes | 2 | 2 | clean |
| grill-with-docs | 1 | 1 | clean |
| intent-modeling | 1 | 1 | clean |
| kb-management | 1 | 1 | clean |
| llm-writing | 1 | 1 | clean |
| shared-dao | 1 | 1 | clean |
| story-memory | 7 | 7 | clean |
| story-review | 16 | 16 | clean |
| writing-principles | 3 | 3 | clean |
| writing-staffing | 1 | 1 | clean |
| **TOTAL** | **45** | **45** | **no missing / no extra** |

Matches the expected 45-files-across-12-skills total exactly. The 6 upstream skills NOT adopted (`character-sim`, `creative-writing-muse`, `interactive-artifact`, `project-setup`, `reader-sim`, `story-planning`) are absent by design — they are not in the 12-skill adopted set and are out of scope for a drop check.

**name-key normalization probe:** spot-checked `name:` key inside SKILL.md for creative-writing-craft, story-memory, story-review, writing-principles → all verbatim, no normalization.

---

## Check 4 — LICENSE-CWS verbatim

- `cmp /…/creative-writing-skills/LICENSE  /…/laf-adaptation/LICENSE-CWS` → **identical (no output, exit 0)**.
- sha256 both = `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`; size 11357 both.

---

## Out-of-Scope Observations (do NOT affect fidelity verdict — flagged for orchestrator)

These fall outside the four assigned fidelity checks (which concern byte-fidelity of *adopted* agent/skill/LICENSE artifacts). Recorded because the adversarial sweep surfaced them; they are Phase-0-completeness / later-phase questions, not fidelity breaches of adopted content.

1. **[OUT-OF-SCOPE] `.claude-plugin/plugin.json` present upstream, absent in vendored, not mentioned in VENDOR.md.** Upstream `cw/.claude-plugin/plugin.json` (488 B: plugin name/description/author/homepage for `creative-writing-skills`) has no vendored counterpart. This is a plugin *manifest* — not an adopted agent/skill body/resource — so it is not covered by Checks 1–4, and it would require namespace rewriting rather than verbatim adoption. Its exclusion is plausibly intentional, but it is NOT documented as an exclusion in VENDOR.md. Recommend the orchestrator confirm the exclusion is deliberate and record it.

2. **[OUT-OF-SCOPE] writer.md graft target `laf-adaptation:adaptation-rules` does not resolve in Phase-0.** No `skills/adaptation-rules/` directory exists anywhere under `laf-adaptation/`, and `adaptation-rules` is not referenced in VENDOR.md. Check 2 confirms the graft *line* is the correct, intended additive delta — this observation is only that its referenced skill is not yet present. This is likely intentional forward-wiring to a skill authored in a later phase; it is a completeness/sequencing question, not a fidelity breach. Recommend the orchestrator confirm `adaptation-rules` is scheduled for a later phase (else writer.md carries a dangling skill reference).

---

## Self-Audit

**(a) Reliance list — rf-qa structural PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was supplied in the spawn prompt. Ran standalone: relied on nothing; verified all four checks independently by direct byte comparison.

**(b) Independent semantic/fidelity checks (≥1 required, INV-019):**
- Byte-identity via sha256 with load-bearing-rewrite confirmation — verified by `uv run python /tmp/prefix_rewrite.py` on all 11 agents + all 45 skill files, cross-checked against raw-upstream mismatch to prove the rewrite is not masking untouched-wrong content.
- Upstream-quirk-preservation (duplicate `creative-writing-craft`) — verified by `cat -A` + `difflib.unified_diff` on writer.md frontmatter, confirming the duplicate is carried, not deduped.
- Drop detection — verified by recursive `find | sort` relative-path diff per skill, not by file-count alone (a count match can hide a rename+add; path diff cannot).
- Token-leak check — verified `grep -rl 'creative-writing-skills:'` returns 0 in vendored agents and skills.

---

## Confidence Gate

- **Confidence:** "Verified: 4/4 assigned checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 1 | Grep: (within Bash) | Glob: (within Bash) | Bash: 9"
- Byte comparison was performed by hashing/cmp inside Bash rather than Read, which is the correct tool for byte-fidelity verification (Read renders/normalizes content and can mask byte-level deltas). Every Bash call mapped to a specific assigned check or a specific adversarial probe.
- UNCHECKED: none. UNVERIFIABLE: none.

## Self-Audit answers
1. Factual claims independently verified: 100% — every one of 11 agent hashes, 45 skill-file hashes, 45 relative-path listings, 1 body-hash, 1 frontmatter diff, and 1 LICENSE cmp was computed live, not asserted.
2. Files/dirs compared: all 11 upstream+vendored agents; all 45 upstream+vendored skill files across 12 skills; upstream ../LICENSE vs vendored LICENSE-CWS; upstream .claude-plugin/plugin.json; writer.md graft target search.
3. Trustworthiness of 0-breach verdict: the verdict rests on cryptographic hash equality (sha256) and `cmp`, not judgment. The load-bearing-rewrite counter-check rules out the "identical because untouched-and-wrong" false-positive. Path diffs (not counts) rule out rename-hidden drops.
4. Web research: none performed (all verification is local byte comparison); Tavily-first N/A this review.

## QA Complete
