# QA Report — Report Validation (EVIDENCE-QUALITY lens, Phase-0 vendored artifacts)

**Topic:** LAF `laf-adaptation/` Phase-0 vendored-artifact evidence integrity
**Date:** 2026-07-03
**Phase:** report-validation (evidence-quality lens)
**Lens:** EVIDENCE-QUALITY
**Fix authorization:** FALSE — REPORT ONLY
**Fix cycle:** N/A

---

## Overall Verdict: PASS

Adversarial stance held throughout. I assumed ≥5 evidence-quality errors were planted (hand-authored
hash, fabricated SHA, unverified license claim, uncited attribution) and actively hunted for them by
recomputing hashes, re-running the boundary tool, byte-comparing the license, and resolving the pinned
git SHA. **No evidence-quality defect was found.** Every claim I could recompute matched the artifact
it is supposed to describe.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1a | `laf_sha256` for agents/muse.md is COMPUTED, matches manifest | PASS | `sha256sum` = `18cafdc251a528f0186d2d74135ae94cad0d05d37d2bf8f399a134969409af8f` == VENDOR.md L23 |
| 1b | `laf_sha256` for agents/editor.md matches manifest | PASS | `sha256sum` = `2645f358fdc0f6b011479fa27195ba096c3836d2c6c4e7955bd78c1da82410e3` == VENDOR.md L22 |
| 1c | `laf_sha256` for skills/kb-management/SKILL.md matches manifest | PASS | `sha256sum` = `8953186d9bfa1e8599a0ef6364df7df35bf18ff6f82f753e5f3e18ffec4356c8` == VENDOR.md L44 |
| 1d | `laf_sha256` for skills/story-review/resources/prose-critique/analyze.py matches manifest | PASS | `sha256sum` = `a57a66caed3efa3a3c0486580d64a573a64cf8caac7deb13ead8e64c4780da80` == VENDOR.md L61 |
| 1e | Extra spot-checks: critic.md, writer.md, story-review/SKILL.md | PASS | critic=`9a0078e9…` (L21), writer=`c1b3e12f…` (L28), story-review=`f2a3996a…` (L54) — all match |
| 2a | boundary-init-summary.md claims exit 0 — reproduced | PASS | `uv run python …/check_boundary.py` → `EXIT_CODE: 0` |
| 2b | boundary-verify-phase0-summary.md claims default-verify exit 0 — reproduced | PASS | Same run: `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` exit 0 |
| 2c | Summaries' "56 manifest rows = 11 agents + 45 skill-tree" claim | PASS | `grep -c` data rows = 56; `ls agents/*.md`=11; `find skills` md/py = 45 |
| 3 | Pinned SHA `3338495f…` is actual HEAD of upstream checkout | PASS | `git -C …/creative-writing-skills rev-parse HEAD` = `3338495f0fabf778720effdda9386ab56d4ebf6e` (exact) |
| 4 | LICENSE-CWS == upstream LICENSE byte-for-byte | PASS | `cmp` exit 0 (no diff) |
| 5a | NOTICE claim "upstream ships no NOTICE file" | PASS | `ls` upstream NOTICE → "No such file or directory" |
| 5b | NOTICE claim "Apache-2.0" | PASS | upstream LICENSE header = "Apache License / Version 2.0, January 2004" |
| 5c | NOTICE claim "vendored at commit 3338495f…" | PASS | matches git HEAD (item 3) and VENDOR.md L4 |
| 6 | `upstream_sha256` column is COMPUTED, not fabricated (adversarial) | PASS | `cw/` mirror recompute: muse=`c8819ec8…`(L23), analyze.py=`a57a66ca…`(L61), writer=`373e605b…`(L28) all match |
| 7 | writer.md ADOPTED-PATCHED additive graft line present | PASS | `grep -n` → L12 `  - laf-adaptation:adaptation-rules` |

## Summary
- Checks passed: 17 / 17
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: FALSE)

## Issues Found
None. No fabricated SHA, no hand-authored hash, no unverified license claim, no uncited attribution.

## Adversarial notes (why the "0 findings" verdict is trustworthy)
- **Hashes are computed, not hand-authored.** All 7 `laf_sha256` values I recomputed match to the full
  64 hex chars. A hand-authored/typo'd hash would have diverged; none did.
- **`upstream_sha256` column is real.** I independently recomputed 3 upstream hashes against the
  `cw/` mirror (the CLAUDE.md-designated vendoring source) — muse, analyze.py, writer — all match.
- **Deliberate SHA divergence explained, not a defect.** The checkout also contains a top-level
  `agents/writer.md` with hash `6c85c952…` (the cut Mars source layer). The manifest correctly pins the
  `cw/agents/writer.md` value `373e605b…`. Picking the wrong source would have been a real defect; the
  manifest picked the right one.
- **ADOPTED-CLEAN no-op rows are genuine.** analyze.py shows `upstream_sha256 == laf_sha256`
  (`a57a66ca…`) because it carries no `creative-writing-skills:` token for the prefix rewrite to touch —
  consistent with the boundary summary's stated transform semantics, and confirmed by recompute.
- **Live tool re-run, not a cached claim.** I re-executed `check_boundary.py` myself (exit 0) rather
  than trusting the summary files' recorded exit code.

## Recommendations
- None blocking. Evidence quality of the Phase-0 vendored artifacts is sound. Green light from the
  EVIDENCE-QUALITY lens.
- (Advisory, non-blocking) The default `verify` mode skips Rules B/C (upstream-diff) — it relies on the
  recorded manifest for adopted-file integrity. That is by design (CI mode), and I closed the residual
  gap manually here by recomputing 3 `upstream_sha256` values against the checkout. No action required.

## Confidence
Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 4 | Grep: 0 (folded into Bash grep -c/-n) | Glob: 0 | Bash: 7
(No web research performed — all claims verified against local files and the local upstream checkout;
no external URL-bound/standards-bound claim required Tavily.)

## QA Complete
