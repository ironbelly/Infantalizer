# Follow-on Brainstorm Prompt — `/laf:rewrite` v-next (chapter-file ingestion)

> Paste-ready. This is the second deliverable requested: a brainstorm prompt that will spec the next
> version of the **rewrite** command so it ingests the individual chapter files + manifest that the
> prep-v-next spec (`merged-requirements.md`, this directory) now materializes.

## Ready-to-run command

```bash
/sc:brainstorm "Next version of /laf:rewrite that ingests the individual per-chapter source files and chapter-manifest.yaml produced by /laf:prep v-next, and drives per-chapter adaptation across chapters 1..N" \
  --depth deep --proposals 3 --strategy systematic \
  --personas architect,analyzer,refactorer --codebase --no-research \
  --output .dev/brainstorms/rewrite-chapter-ingestion
```

(`--depth deep` because the read-set contract and per-chapter state carry more branching than prep did;
`--no-research` — this is internal framework design, no external libraries.)

## Seed context to hand the brainstorm (paste as the opening brief)

**Upstream artifact (MUST read first):**
`.dev/brainstorms/20260709T001338Z-prep-chapter-ingestion/merged-requirements.md` — the prep-v-next spec
that now materializes `source/<slug>/ch-<NN>.txt` + `source/<slug>/chapter-manifest.yaml`.

**Grounding files (read for the current rewrite contract):**
- `.claude/commands/laf/rewrite.md` — current `/laf:rewrite --work <slug>`; hardcoded read-set; hands
  chapter 1 to `muse`, chapters 2..N re-read the same work-level package.
- `laf-adaptation/skills/prep/resources/path-contract.md` §4 `rewrite_phase_reads` =
  `[30-mapping.yaml, 40-prep-brief.md, 10-challenges.yaml]` (**frozen** — the central question below).
- `laf-adaptation/CLAUDE.md` — boundary contract, ADR-006 (framework not software, one script), provenance
  classes, tier axis, `chronicler` writes canon on muse-accept in the rewrite phase.
- `laf-adaptation/agents/` — `muse` (rewrite orchestrator), `analyst` (tier-invariant source analysis;
  currently reads a chapter `source_path` at rewrite time), `tier-coordinator`, `chronicler`,
  `safety-verifier`.

**Problem statement:** Today `/laf:rewrite --work <slug>` reads only the work-level prep package and
implicitly locates chapter text by convention; there is no formal chapter-set input. Now that prep-v-next
emits a canonical chapter set + `chapter-manifest.yaml`, the rewrite command should ingest **individual
chapter files** as first-class input and drive the per-chapter 11-step workflow across chapters 1..N from
that manifest — while honoring the same LAF constraints (no new script/runtime, no adopted-body edit,
`check_boundary.py` green, tier axis first-class, `chronicler` owns canon writes).

**Open questions the proposals MUST diverge on and resolve:**
- **RQ1 — Read-set change:** Does `rewrite_phase_reads` gain a 4th entry (`chapter-manifest.yaml`), or does
  rewrite discover chapters by the `source/<slug>/ch-<NN>.txt` convention (manifest as audit-only)? This is
  the deferred seam (R1/R15) from the prep spec — resolve it with an explicit justification for touching or
  not touching the frozen contract.
- **RQ2 — Per-chapter analysis granularity:** Does rewrite now run per-chapter source-fidelity `analyst`
  passes (deferred from prep, N1), and if so where — a pre-rewrite analysis stage per chapter, or inline in
  `muse`'s 11-step workflow? Keyed by `(work, chapter)` and, for canon, `(work, tier, chapter)`.
- **RQ3 — Chapter selection & range:** How does the operator target chapters — `--chapter N`, `--chapters
  1-5`, all-by-default? How does resume/idempotency work across a multi-chapter run (which chapters are
  done, which are in-flight)? Interaction with `chronicler`'s per-(work,tier,chapter) state.
- **RQ4 — Manifest trust & drift:** If a chapter file changed since prep (hash mismatch vs
  `chapter-manifest.yaml.output_sha256`), what does rewrite do — halt, re-verify, re-prep? How does rewrite
  handle a `review.status: PENDING` (un-greenlit) or partial chapter set?
- **RQ5 — Command surface:** `--work <slug>` only (discover manifest), or add `--source`/`--manifest`
  overrides? Keep the existing greenlight guard (`50-greenlight.md: CONFIRMED`) and add a manifest guard?
- **RQ6 — Boundary/tier fidelity:** Where does per-chapter tier fan-out (`tier-coordinator` across
  {1,2,3,5}) sit relative to chapter iteration? Does the safety gate (`safety-verifier`) run per (chapter,
  tier)? Keep all new knowledge in NATIVE skills / `muse` frontmatter — no adopted-body edit.

**Constraints (carry verbatim):** framework not software (ADR-006, one script); no adopted-body edits
(native knowledge via `skills:` frontmatter); `source/` read-only; `chronicler` is the only canon writer in
the rewrite phase; tier axis first-class; `check_boundary.py` must stay green; prefer extending `muse` +
the existing 11-step per-chapter workflow over new commands/agents.

**Success criteria:** `/laf:rewrite --work <slug>` ingests the prep-v-next chapter set + manifest and drives
per-chapter adaptation for chapters 1..N with a clear resume story, an explicit resolution of the
`rewrite_phase_reads` question (RQ1), a per-chapter analysis decision (RQ2), manifest-drift handling (RQ4),
zero adopted-body edits, and `check_boundary.py` green.
```
