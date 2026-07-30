# Adversarial Merge Log — prep-chapter-ingestion

3 proposals across a heterogeneous fleet: architect (claude-opus-4-8), analyzer (gpt-5.5), refactorer
(glm-5.2). Base selection: **refactorer** (smallest-diff skeleton) as the structural base, grafting the
architect's contract precision and the analyzer's fidelity/failure-mode rigor.

## Convergence matrix (all 6 open questions)

| OQ | architect | analyzer | refactorer | Converged? | Decision |
|---|---|---|---|---|---|
| OQ1 ownership | prep, Stage 0 | prep, Stage 0 | prep, Stage 0 | ✅ unanimous | prep owns it; new Stage 0; **no new command** |
| OQ2 granularity | work-level | work-level | work-level | ✅ unanimous | analysis stays work-level; per-chapter deferred to rewrite spec |
| OQ3 split mech | NATIVE skill + YAML | prompt+YAML, no script | NATIVE skill + YAML | ✅ unanimous | one NATIVE skill, prompt+YAML, no runtime, confidence-tagged |
| OQ4 manifest | source sidecar | source sidecar | source sidecar | ✅ unanimous | `source/<slug>/chapter-manifest.yaml`; **`rewrite_phase_reads` UNCHANGED** |
| OQ5 normalization | strip + `.raw/` anchor | track loss as events | inline strip, transparent-uncertainty | ⚠️ partial | strip inline **+** retain `.raw/` **+** record normalization events (all three merged) |
| OQ6 idempotency/gate | hash-keyed, §5 gate | 2 gates, no-overwrite | Mode C adopt, §5 gate | ⚠️ partial | hash-keyed no-overwrite; adopt existing; non-CERTAIN writes deferred to greenlight (analyzer safety via refactorer's single gate) |

Convergence score: **0.86** → PASS (≥0.65).

## Divergences resolved

1. **Skill name** — `chapter-split` (arc) / `chapter-materializer` (ana) / `chapter-matrix` (ref).
   → **`chapter-materialize`**: covers detect + split + folder-adopt + normalize; name-collision-free
   (Rule E); aligned to the "materialization" stage name.
2. **Manifest filename** — `manifest.yaml` (arc, ref) / `chapter-manifest.yaml` (ana).
   → **`chapter-manifest.yaml`**: self-documenting, avoids a generic `manifest.yaml` clash if `source/`
   later holds other manifests. (Overrode the 2-vote majority on clarity grounds — a merge-author call.)
3. **Command surface** — new `--source-mode` (arc) / zero new flags (ref) / four new flags (ana).
   → **auto-detect default + ONE optional override `--source-mode auto|folder|file|adopt`**. Refactorer's
   minimalism is the floor; the analyzer's decisive counter — the real `Books/LWW/` folder holds BOTH
   split files AND monolith copies, so auto-detect CAN misfire — forces (a) the override flag and (b)
   ambiguous auto-detection routes to the human gate rather than guessing. Dropped `--slug` (derivable),
   `--chapter-count` (deferred), `--allow-overwrite` (collisions route to the gate, not a flag).
4. **Gate count** — one §5 gate (arc, ref) vs two gates (ana, "never write a guessed boundary").
   → **Single reused §5 gate + deferred-write rule**: CERTAIN chapters materialize immediately;
   PROBABLE/UNCERTAIN/collision/mode-ambiguity defer their `ch-NN.txt` writes and raise §5 questions;
   greenlight-confirm commits the deferred writes. Analyzer's safety invariant (no guessed write before
   human confirmation) is preserved without adding a second HALT mechanism.
5. **Split confidence rule** — architect's regularity ladder + **analyzer's "CERTAIN requires ≥2
   independent agreeing signals"** merged into one rule (§6 of merged spec). Single-signal boundaries are
   capped at PROBABLE — an analyzer release-blocker, adopted.

## Grafts from each lens

- From **refactorer**: the minimal bill-of-materials (1 skill + 1 sidecar + 1 contract subsection + 1
  frontmatter line), Mode C zero-resplit adoption, "analyst is not the splitter" separation, the explicit
  REFUSE list (scope discipline).
- From **architect**: `.raw/` fidelity anchor, the STAGE-0 sequencing diagram, precise path-contract diff
  rows, the "automates the provisioning README already specifies" justification for writing into `source/`.
- From **analyzer**: the 14-row failure-mode table, multi-signal CERTAIN rule, `normalization_events` +
  `needs_human_review` manifest fields, the 7 release-blocking risks, the "auto-detect must not guess when
  both split-set and monolith are present" invariant.

## Unresolved tensions (surfaced, not hidden)

- **R1 — manifest not in `rewrite_phase_reads`:** the manifest is authoritative for the chapter set but the
  frozen read-set doesn't include it, so a future rewrite could drift from it. Deliberately deferred: the
  rewrite spec (next brainstorm) is the right place to justify a 4th read-entry or a convention-based read.
- **R2 — work-level analysis vs deferred-uncertain chapters:** if a boundary is UNCERTAIN, work-level
  analysis should not proceed over a half-materialized set. v-next resolves this by halting at §5 before
  Stage 2 when chapter uncertainty exists; a cleaner sequencing is left to implementation.
