# Phase 3 QA — Consolidated Findings (Serialized Fix input)

Gate: 1 PASS (boundary-preservation) + 5 FAIL. The 5 FAILs converge on 2 genuine in-scope defects + 1 minor mapping gap. The `check_boundary.py` FAIL observed at end-of-Phase-3 is ONLY the missing `chapter-materialize` VENDOR row (added in Phase 4, Step 4.3) — EXPECTED pre-Phase-4 sequencing state, NOT a Phase-3 defect (do not "fix" it here).

Files in scope (Phase 3 edited): prep-cordinator.md, prep/SKILL.md, .claude/commands/laf/prep.md.

## IMPORTANT

**I-1: prep-cordinator.md Stage-0 note — dangling `§5/§6` reference.** The note says chapter/manifest paths are "owned by path-contract §5/§6" but at end-of-Phase-3 §6 does not exist yet and §5 does not yet list those rows (both are added in Phase 4). Also flagged: the "never restate them here" phrasing reads as a self-contradiction against pre-existing dispatch-payload path mentions (L52/L77) — those pre-existing lines are OUT OF SCOPE, but our new note's phrasing should not over-claim. FIX: change the reference to a generic, non-dangling form that is valid both before and after Phase 4 — e.g. "owned by the path contract's write-ownership rows and its source-side chapter-manifest section (Phase-4 additions); this Stage-0 note does not restate the literal paths." Avoid citing a bare `§6` number that does not resolve until Phase 4.

**I-2: command file L11 — stale/restated stage count.** `.claude/commands/laf/prep.md:11` (a pre-existing line, but the file was edited this phase) says the coordinator "owns the 8-stage procedure" — now stale (coordinator is 9-stage) AND it restates a pipeline count the command is told not to restate. FIX: remove the specific count — change "owns the 8-stage procedure and the two HALT gates" to "owns the full prep procedure and the two HALT gates" (no count to go stale, satisfies the no-restate-pipeline rule).

## MINOR

**M-1: `--source-mode` value ↔ manifest `input_mode` mapping not stated.** The flag values `folder|file|adopt` map to manifest `input_mode` values `folder | single-file | adopt-existing`. FIX: add a one-line parenthetical mapping in the command's `--source-mode` sentence: "(these map to manifest `input_mode`: folder→folder, file→single-file, adopt→adopt-existing)".

## NOT-A-DEFECT (do not act)
- `check_boundary.py` exit 1 at end-of-Phase-3 = missing `chapter-materialize` VENDOR row → added in Phase 4 Step 4.3. Expected. The boundary-preservation lens confirmed no adopted body touched, both edited NATIVE files legal, command file outside the Rule-F glob.
- Pre-existing prep-cordinator L52/L77 path mentions (dispatch payload / write scope) — pre-existing, out of scope.
- Singular `ambiguous_split` vs array `ambiguous_splits[]` — defensible English, leave.
