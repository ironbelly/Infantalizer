# Current Framework Map (grounded)

> Standalone context for a fresh session. A compact, path-cited map of what the Literary Adaptation
> Framework (LAF) does natively today, so the brainstorm knows exactly what exists to change. The repo
> ships **two layers** encoding the same domain model (five developmental tiers, agency externalization,
> anti-hallucination source-fidelity, safety verification) in two substrates. Do not conflate them. For
> the fuller auto-generated map see `docs/INDEX.md`.

## Layer A — Root v1.0 (prompt + YAML; the simple, user-facing layer)

**Location:** `config/`, `prompts/`, `templates/`, `docs/`. No executable code.

**Pipeline (one tier at a time, no orchestration):**
```
source chapter
  -> prompts/analysis/chapter_analysis.md        (5-phase anti-hallucination: Phase 0 source declaration
                                                   with ABORT-on-NO-ACCESS -> essentials -> dual-pass
                                                   documentation -> transformation flags -> confidence tags)
  -> prompts/transformation/tier_N_transform.md   (ONLY tier_1 and tier_3 ship)
        + config/age_profiles/tier_{1,2,3,5}_*.yaml   (no tier_4 file; interpolated)
        + config/transformation_rules/{thematic,character}.yaml
        + config/concept_mapping/{universal_mappings, templates/<work>_mapping}.yaml
  -> prompts/verification/safety_check.md          (6-section; mandatory for Tier 1-2)
  -> adapted chapter + transformation log + confidence report
```

**Key config content:**
- `thematic.yaml` — violence, conflict, agency_externalization, death_handling, villain_motivation,
  heroism, keyed by tier with `mode:` (mandatory/optional/forbidden).
- `character.yaml` — Tier-1 archetypes, heroism-translation subroutine, and ad-hoc `special_handling`
  for hard characters (Gollum, Denethor).
- `concept_mapping/templates/{tolkien,narnia}_mapping.yaml` — per-work overrides (cascade:
  universal -> work -> age profile -> transformation rules; most-specific wins).

**What root LACKS:** any orchestration or critique loop; a cross-tier reconciliation tool; tier_2/4/5
transform prompts (only T1+T3, per ADR-006); any meaning/theme-preservation concept; any research,
onboarding, or prep phase.

## Layer B — LAF 0.1 CWS Hybrid (agents + skills; the capable layer)

**Location:** `laf-adaptation/`. Vendors the domain-agnostic machinery from `haowjy/creative-writing-skills`
(CWS) and grafts LAF's domain spine on top under a hard **boundary contract**. Canonical guide:
`laf-adaptation/CLAUDE.md`.

**Provenance classes (every file is one):** ADOPTED-CLEAN (vendored byte-identical after a prefix
rewrite; never edit the body), ADOPTED-PATCHED (only `agents/writer.md` — adopted body + one additive
`skills:` line), NATIVE (LAF domain spine), BUILD-NEW (greenfield in both systems).

**Boundary contract (constraint #6, load-bearing):** native knowledge enters ADOPTED agents ONLY via
`skills:` frontmatter — never by editing an adopted body. Enforced by
`laf-adaptation/scripts/check_boundary.py` (Rules A-F), an opt-in pre-commit hook, and
`.github/workflows/boundary.yml`. **Any new capability must be a NATIVE skill, additive frontmatter, a
new NATIVE agent/command, or an edit to a BUILD-NEW body — never an adopted-body edit.**

**Agents (15):** 11 adopted-provenance (incl. `writer` ADOPTED-PATCHED, and the review/orchestration
crew `muse`, `critic`, `editor`, `reader-sim`, `continuity-checker`, `brainstormer`, `outliner`,
`style-creator`, `character-sim`, `web-researcher`); 2 NATIVE (`analyst`, `safety-verifier`); 2
BUILD-NEW (`chronicler`, `tier-coordinator`).

**Skills (16):** 12 ADOPTED; 3 NATIVE (`adaptation-tiers`, `adaptation-rules`, `source-fidelity`); 1
BUILD-NEW (`adaptation-safety`).

**The per-chapter 11-step workflow:**
```
analyst -> muse -> writer -> critic -> editor -> writer -> continuity-checker
        -> safety-verifier -> reader-sim -> tier-coordinator -> chronicler
```
- `analyst` (NATIVE, tier-invariant): runs once per chapter; executes `/source-fidelity`'s 5-phase
  protocol; Phase-0 ABORT-on-NO-ACCESS; emits `work/analysis/ch-NN.yaml` (status, essentials,
  characters, events, summary, `transformation_flags`, uncertainties), every fact confidence-tagged.
- `muse` (ADOPTED orchestrator): reads analysis + `kb/tiers/` + `kb/adaptation-mapping/`; builds the
  scene brief; owns the verdict; dispatches specialists.
- `writer` (ADOPTED-PATCHED): drafts; receives the operative tier via scene brief + `/adaptation-rules`.
- `safety-verifier` (NATIVE) + `/adaptation-safety` (BUILD-NEW): 6-section rubric; machine verdict block;
  **blocking** for T1-2, **advisory** for T3, **skipped** for T4-5; blocking FAIL re-enters the writer
  loop with located evidence.
- `tier-coordinator` (BUILD-NEW): fans one chapter across `tiers` subset of {1,2,3,5} (T4 interpolated
  on demand); `reconcile()` runs three checks — A source-fidelity consistency (every tier's element
  traces to the shared analysis; unsourced = hallucination), B disclosure-leak (a lower tier must not
  reveal what its threshold defers), C framing monotonicity (maturity non-decreasing in tier); emits
  `work/analysis/ch-NN-cross-tier.md`, status RECONCILED | CONFLICT. Runs before `chronicler`; never
  writes canon.
- `chronicler` (BUILD-NEW): writes per-tier canon to `kb/adaptations/<work>/tier-<N>/` keyed
  (work, tier, chapter), **only on muse-accept**.

**Tiers:** `/adaptation-tiers` ships all five tiers plus a rigorous Tier-4 interpolation rule (T3 floor,
T5 ceiling, conservative midpoint; `agency_externalization = FORBIDDEN` at T4-5). Profiles in
`kb/tiers/tier_{1,2,3,5}.yaml` are byte-faithful copies of root `config/age_profiles/` (deliberate
schema drift absorbed in the reader skills, never in the data).

**kb / work split (constraint #5):** in-flight artifacts live under `work/` (`analysis/`, `drafts/`,
`critique-reports/`, `safety-reports/`); promoted canon lives under `kb/` via the adopted
`kb-management` lifecycle.

**What 0.1 LACKS relative to the objective:**
- No **thin user entry point** ("name a novel and go").
- No **autonomous high-level research phase** wired to a prep pipeline (`web-researcher` exists but is a
  specialist, not an onboarding stage).
- No **prep-roadmap builder/executor**, no **clarifying-question gate**, no **standardized initial
  document/guide package** generation, no **greenlight -> next-phase-prompt** emission.
- No **thematic/meaning-preservation invariant** (source-fidelity = factual only).
- No **explicit compound-scene protocol** (multi-rule scenes rely on emergent critique quality).
- **Work-mapping is authored, not derived** — `ADDING_NEW_WORKS.md` documents a human process; nothing
  generates `<work>-mapping.yaml` from the analysis.

## Where the prep phase must attach

The prep phase sits **upstream of the existing per-chapter workflow**: it takes a novel, runs
research + source-fidelity-gated analysis at the work level, authors the per-work mapping and
challenge classification, assembles the standardized package, and hands off. It should reuse the
existing NATIVE spine (`source-fidelity`, `adaptation-tiers`, `adaptation-rules`, `analyst`) and the
adopted `web-researcher`/`kb-management` machinery rather than reinventing them — respecting the
boundary contract throughout.

## Key references in-repo
- `docs/INDEX.md` — full auto-generated map of both layers.
- `laf-adaptation/CLAUDE.md` — canonical 0.1 guide (provenance model, boundary contract, conventions).
- `laf-adaptation/agents/tier-coordinator.md`, `agents/analyst.md`;
  `skills/{source-fidelity,adaptation-rules,adaptation-tiers,adaptation-safety}/SKILL.md`.
- `docs/design_decisions/` — ADR-001 (five tiers), ADR-003 (agency externalization), ADR-006 (not
  software; only T1+T3 shipped).
