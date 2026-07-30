# Enrichment: Codebase Context (quality_tier: primary — direct Read of source-of-truth files)

Gathered by direct Read of the LAF tree (not Auggie — this is an in-repo framework, files read directly).

## Command surfaces (current)

- `.claude/commands/laf/prep.md` — `/laf:prep "<title>" [--source <path-or-url>]`. Delegates entire run to
  the `prep-cordinator` agent (opus). Source path is a REQUIRED input (elicited if `--source` omitted).
  URL is fetched to a local file first. No chapter concept.
- `.claude/commands/laf/rewrite.md` — `/laf:rewrite --work <slug>`. Reads the 3-file `rewrite_phase_reads`
  set by hardcoded path, confirms greenlight `CONFIRMED`, hands chapter 1 to `muse`; chapters 2..N re-read
  the same work-level package. **No chapter-source path is named in the read-set** — the implicit gap.

## Prep skill + path contract (hard constraints)

- `laf-adaptation/skills/prep/SKILL.md` — 8-stage native prep: two-track work-level research (context +
  text), source-fidelity-gated analysis, challenge taxonomy (`10-challenges.yaml`), derived scored mapping
  (`30-mapping.yaml` + top-level `meaning:`), question gate (§5), greenlight (§6), handoff (§7),
  traceability (§8). Analyst runs `granularity=work`.
- `laf-adaptation/skills/prep/resources/path-contract.md` — SINGLE source of truth:
  - Package: `work/prep/<slug>/` with fixed files `00`–`70`.
  - `rewrite_phase_reads` = `[30-mapping.yaml, 40-prep-brief.md, 10-challenges.yaml]` (frozen).
  - Promotion (greenlight, dual-form): `kb/adaptation-mapping/<slug>-mapping.yaml` (6-key, keeps
    `meaning:`) + `config/concept_mapping/templates/<slug>_mapping.yaml` (5-key, strips `meaning:`).
  - Write-ownership table: prep-cordinator writes `work/prep/<slug>/*`; chronicler writes canon in the
    rewrite phase only.

## Source layout convention

- `laf-adaptation/source/README.md` — `source/<work>/ch-<NN>.txt`, one chapter/file, UTF-8, read-only.
  Nothing in `source/` is transformed in place. Provisioning is currently MANUAL / operator-supplied.
- Live: `source/narnia/ch-01..04.txt` (real public-domain LWW prose), `source/tolkien/ch-01.txt`
  (synthetic PATH-B fixture). `ch-01.txt` begins `CHAPTER I\nLucy Looks into a Wardrobe\n...` — the
  boundary/title signal a splitter would key on.
- Raw inputs present: `Books/LWW/*.html` (both a monolithic ~217KB copy AND split `-1..-4.html`),
  `Books/LWW/....pdf`. This is the exact "folder of per-chapter files" vs "single file" duality the ask
  names.

## LAF framework rules (govern any design)

From `laf-adaptation/CLAUDE.md` + ADR-006:

- **Prompt + YAML-config framework, NOT software.** Exactly ONE script (`scripts/check_boundary.py`, a
  validator — not a runtime). A new heavyweight splitter binary/CLI would violate ADR-006.
- **Provenance classes:** ADOPTED (never edit body), ADOPTED-PATCHED (writer.md only), NATIVE, BUILD-NEW.
  New capability must be NATIVE (new skill / prep-cordinator procedure), never an adopted-body edit.
- **Boundary contract** enforced by `check_boundary.py` (Mode V): adopted bodies hash-pinned; NATIVE
  knowledge enters adopted agents only via `skills:` frontmatter; no name collisions with upstream.
- **Anti-hallucination:** `/source-fidelity` mandates CERTAIN/PROBABLE/UNCERTAIN tags + ABORT-on-NO-ACCESS
  before any transform. Chapter-boundary/title extraction is a fidelity-governed act.
- **work/ vs kb/ vs source/ split:** source read-only; work/ is lifecycle; kb/ is promoted canon.

## Agents in play

- `prep-cordinator` (opus) — owns the prep procedure + HALT gates; tools: Agent(web-researcher, analyst,
  tier-coordinator), Read/Write/Glob/Grep/Web*. Natural owner of a materialization stage.
- `analyst` (NATIVE) — source-chapter analysis, confidence-tagged; ABORTS on NO-ACCESS; currently work-level.
- `muse` (rewrite phase) — consumes the prep package for per-chapter production.

## Implication for the spec

The design space is bounded by: (1) extend prep, don't fork the framework; (2) express splitting as a
prompt/agent + YAML-declared procedure with confidence gating, not a runtime; (3) add a chapter manifest
in a way that respects the frozen `rewrite_phase_reads` contract; (4) route ambiguous splits to the
existing human question/greenlight gate; (5) keep `check_boundary.py` green.
