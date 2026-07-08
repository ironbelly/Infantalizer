# HARD-GATE Condition 5 — check_boundary.py green

**Verdict:** ✅ **PASS**

**Command + result** (run AFTER the full 11-step T1 run + T1/3/5 fan-out):
- `uv run python laf-adaptation/scripts/check_boundary.py` → `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied`, **exit 0**.
- `uv run python laf-adaptation/scripts/check_boundary.py --upstream .dev/releases/current/0.1/creative-writing-skills`
  (SHA `3338495f0fabf778720effdda9386ab56d4ebf6e`) → same, **exit 0** (Rules B/C incl.).

**Plain-mode caveat:** plain `verify` mode (no `--upstream`) skips Rules B and C (ADOPTED-CLEAN ==
upstream-after-rewrite; writer.md diff frontmatter-only+additive) because it has no upstream tree to diff
against. Those two rules were confirmed to hold under the `--upstream` run above (checkout path
`.dev/releases/current/0.1/creative-writing-skills`, SHA `3338495f0fabf778720effdda9386ab56d4ebf6e`),
which was executed and also exited 0.

**Per-rule (A-F):** all PASS.
- A: 56 adopted files still match recorded `laf_sha256` — no adopted file drifted during the proof run.
- B: ADOPTED-CLEAN == upstream-after-rewrite.
- C: writer.md diff still frontmatter-only + additive.
- D: quartet {critic, editor, reader-sim, continuity-checker} intact & ADOPTED-CLEAN; editor never folded.
- E: no NATIVE/BUILD-NEW name collides with upstream.
- F: every `agents/*.md` + `skills/**/SKILL.md` manifested.

**Why this matters:** the boundary contract held **through** the proof run — the runtime artifacts
(drafts, canon, safety reports) were written under `work/` and `kb/`, never touching an adopted
`agents/*.md` or `skills/**/SKILL.md` body. This is constraint #6 enforced at runtime: producing
adaptations does not drift the adopted subset.

**Gaps:** none. exit 0 both modes; no adopted file drifted during execution.
