---
title: "LAF 0.1 Architecture Decision — CWS Integration"
domain: architecture
strategy: systematic
decision: "C — Hybrid (adopt CWS domain-agnostic machinery, author LAF adaptation spine natively, build greenfield what is unshipped in both)"
adversarial_status: pass
convergence_score: 0.72
base_proposal: C
grafts: [B/per-tier-canon, B/sequential-fallback, A/quartet-invariant]
created: 2026-07-03T04:37:28Z
source_brief: seed-brief.md
---

# LAF 0.1 Architecture Decision Document

## 1. Path Chosen: **C — Hybrid**

**Decision:** Adopt `creative-writing-skills` (CWS) *domain-agnostic* machinery unchanged; author LAF's
*domain-specific* adaptation spine natively; build greenfield what neither system ships. Reject CWS's
plugin/Mars packaging (no ADR-006 reversal). Single-tree distribution.

**Why C beat A and B** (adversarial score 41 vs 33 vs 29; convergence 0.72):

- The two systems fail in **orthogonal layers**. CWS's review/kb/orchestration machinery is
  *domain-agnostic* — a continuity contradiction or a voice-drift critique is the same regardless of
  whether prose is original or adapted, so it is reusable **as-is**. LAF's tier axis + source-fidelity +
  safety are *irreducibly domain-specific* — there is nothing in CWS to fork, so "native" is the only
  option, not a fork cost. Canon-extraction is **greenfield in both** (verified: `chronicler.md` is
  unshipped vapor), so it carries zero fork premium on any path.
- **Path A (fork)** demotes the tier axis from spine to a skill hanging off a generative muse-centered
  pipeline, forces a **reversal of ADR-006** ("this is a prompt framework, not software") to inherit
  mars.toml + `cw/` dual trees + CI sync that LAF deliberately shed, and requires editing an upstream
  agent file (the "grafted muse"), violating clean-patch discipline. Its headline advantage — reuse
  mature machinery — is materially eroded because the one load-bearing agent LAF needs most
  (canon-extraction) does not exist.
- **Path B (native)** keeps the tier axis as a true spine (its strongest virtue) but **wounds
  constraint #4**: it folds `editor` into the coordinator and merges `continuity-checker` with the
  missing chronicler — collapsing the review quartet whose disciplined separation is the entire value
  proposition of the machinery LAF is trying to acquire. B's own self-named "single biggest risk" is
  under-baking that quartet.
- **Path C** keeps the full quartet (unlike B), keeps the tier axis as a native spine (unlike A), avoids
  the ADR-006 reversal (unlike A), and is the **only** proposal that ships an explicit anti-drift
  mechanism (the boundary contract). Its costs (two-provenance tax, boundary-drift) are the most
  *mitigable* because C ships the mitigations.

**Grafts absorbed into the base** (from the adversarial merge):
- **G1 (from B, non-optional):** per-tier canon state — the (work, tier, chapter) key + per-tier
  `continuity.md`. Closes C's latent "same character has divergent canonical state per tier" bug.
- **G2 (from B):** sequential multi-tier as a documented degradation mode (parallel is the default).
- **G3 (from A):** "quartet-intact" as an explicit written invariant — never fold `editor`; the four
  review modes are load-bearing.

---

## 2. Resulting Architecture

### 2.1 Agents — three-column classification

| ADOPT-FROM-CWS (vendored, patch-clean, unchanged files) | REIMPLEMENT-NATIVE (LAF-specific) | BUILD-NEW (greenfield in both systems) |
|---|---|---|
| `muse` (orchestrator; loads LAF skills additively via frontmatter) | `analyst` — source analysis, v2.0 protocol, confidence tagging | `chronicler` — **tier-aware** canon-extraction |
| `critic` (Read-only craft diagnosis; adaptation-quality focus loads `/adaptation-rules`) | `safety-verifier` — 6-section safety_check as a distinct agent | `tier-coordinator` — cross-tier consistency + fan-out |
| `editor` (holistic priority — **kept, never folded**, invariant G3) | `writer`→adaptation-mode (adopted agent + native skill; **not forked**) | |
| `reader-sim` (felt experience; persona fed the tier `developmental_basis`) | | |
| `continuity-checker` (canon contradiction — check duty only) | | |
| `brainstormer`, `outliner`, `character-sim`, `style-creator`, `web-researcher` (retained; dormant on the core adapt path) | | |

Two boundary cases handled explicitly (no agent-file edits):
- **`writer` is adopted, gains an adaptation mode via `skills:` frontmatter** loading `/adaptation-rules`.
  Preserves CWS's "one writer preserves voice" invariant — the agent is CWS's, the mode's knowledge is LAF's.
- **`reader-sim` is adopted, persona schema extended natively** with the tier's Piaget/Kohlberg
  `developmental_basis` as structured input — a data extension, no code change.

The review quartet remains **four distinct agents** (`critic`, `editor`, `reader-sim`,
`continuity-checker`); `safety-verifier` is a **fifth** distinct reviewer, not a collapse.

### 2.2 Skills — three-column

| ADOPT-FROM-CWS (unchanged) | REIMPLEMENT-NATIVE | BUILD-NEW |
|---|---|---|
| `writing-principles`, `creative-writing-craft`, `creative-writing-modes`, `story-review`, `story-memory`, `kb-management`, `shared-dao`, `llm-writing`, `writing-staffing`, `intent-modeling`, `grill-with-docs`, `creative-research` | `/adaptation-tiers` (tier axis), `/adaptation-rules` (thematic + character transforms + **Agency Externalization**), `/source-fidelity` (v2.0 CERTAIN/PROBABLE/UNCERTAIN) | `/adaptation-safety` (6-section check for safety-verifier); `children.md` + `ya.md` genre resources |

Agency Externalization lives **inside `/adaptation-rules`** (tier-conditional: MANDATORY T1–2, OPTIONAL
T3, FORBIDDEN T4–5) — never bolted onto the adopted `writing-principles`, to keep the adopted skill
patch-clean.

### 2.3 Config layout — LAF configs carried verbatim into the kb as native data

```
laf-adaptation/
├── CLAUDE.md                    # ADOPTED pattern + LAF conventions section
├── source/                      # BUILD-NEW: the work being adapted (read-only reference)
├── work/                        # ADOPTED as-is (provisional; constraint #5)
│   ├── analysis/                #   BUILD-NEW subdir: per-chapter analyst output (confidence-tagged)
│   ├── drafts/                  #   adopted
│   ├── critique-reports/        #   adopted
│   └── safety-reports/          #   BUILD-NEW subdir
└── kb/                          # ADOPTED lifecycle (work→kb promotion via kb-management)
    ├── canon/                   #   adopted layer, populated by BUILD-NEW chronicler
    ├── characters/  world/  timeline/  styles/  vocab.md  issues/    # adopted layers
    ├── tiers/                   #   NATIVE: tier_1/2/3/5 profiles (LAF configs as kb data; T4 interpolated)
    ├── adaptation-mapping/      #   NATIVE: universal_mappings + <work>_mapping
    └── adaptations/<work>/      #   NATIVE (graft G1): per-tier canon state
        └── tier-<N>/
            ├── decisions.md     #     per-tier adaptation decisions
            ├── continuity.md    #     per-tier running canon (what a Tier-N reader now "knows")
            └── chapters/ch-<NN>/{analysis.yaml, adapted.md, canon-delta.md}
```

The `kb/` container and lifecycle are adopted; `tiers/`, `adaptation-mapping/`, and `adaptations/<work>/`
are native layers riding inside it under the adopted `kb-management` rules.

### 2.4 Workflow (per source chapter)

```
1.  analyst (NATIVE)            → work/analysis/chN.yaml   [v2.0 protocol; ABORT on NO-ACCESS]
2.  muse (ADOPTED)              → reads analysis + kb/tiers/tier_N + kb/adaptation-mapping; builds brief
3.  writer adaptation-mode      → work/drafts/            [ADOPTED agent + NATIVE /adaptation-rules]
4.  critic ×N (ADOPTED)         → work/critique-reports/  [parallel focus areas; adaptation-quality]
5.  editor (ADOPTED)            → editorial memo (priority order)          ← quartet kept intact (G3)
6.  writer revision (ADOPTED)   → revised draft
7.  continuity-checker (ADOPTED)→ canon-contradiction pass
8.  safety-verifier (NATIVE)    → PASS / FAIL   [mandatory T1–2; runs AFTER continuity]
       └─ FAIL ──► back to step 3 (revision loop)          ← the loop LAF lacked (constraint #3)
9.  reader-sim (ADOPTED)        → felt-experience as tier developmental persona [after convergence]
10. tier-coordinator (BUILD-NEW)→ cross-tier consistency (parallel default; sequential fallback G2)
11. chronicler (BUILD-NEW)      → kb/canon + kb/timeline + kb/adaptations/<work>/tier-N/continuity.md
```

---

## 3. Integration Map — every LAF concept → landing site

| LAF concept | Lands in | Rides adopted or native? |
|---|---|---|
| **Five-tier axis** | `/adaptation-tiers` skill + `kb/tiers/tier_N.yaml`; passed as active-tier to every downstream agent | **Native** (no CWS equivalent) |
| **Thematic + character transform rules** | `/adaptation-rules` skill | **Native**, loaded by *adopted* writer + critic |
| **Agency Externalization** | inside `/adaptation-rules` (tier-conditional) | **Native**; enforced by writer, audited by safety-verifier + critic |
| **Concept mapping (universal + work)** | `kb/adaptation-mapping/` (cascade preserved: most-specific-wins) | **Native** layer inside *adopted* kb |
| **v2.0 Pragmatic Verification Protocol** | `/source-fidelity` skill + `analyst` agent | **Native** (build-new front-end) |
| **CERTAIN/PROBABLE/UNCERTAIN tags** | `/source-fidelity`; propagated via *adopted* `story-memory` fact-extraction | Native tag, **adopted** carrier |
| **safety_check (6-section)** | `/adaptation-safety` skill + `safety-verifier` agent | **Native** (build-new agent) |
| **Source analysis pipeline** | `analyst` → `work/analysis/` | **Native** front-end on *adopted* work/ dir |
| **Cross-chapter canon (tier-aware)** | `kb/canon/` + per-tier `kb/adaptations/<work>/tier-N/continuity.md` | **Adopted** base layer, **build-new** populator, **native** per-tier extension (G1) |
| **Quality critique** | *adopted* critic/editor/reader-sim quartet | **Adopted** as-is |
| **Revision loop on FAIL** | *adopted* writer→critic→writer cycle, triggered by native safety-verifier | **Adopted** loop, **native** trigger |
| **work_mapping_template** | `templates/` → copied to `kb/adaptations/<work>/work-mapping.yaml` at onboarding | **Native** content, *adopted* project-setup pattern |

---

## 4. Migration Plan (phased)

**Phase 0 — Vendor the adopted subset.** Copy CWS's 6 review/orchestration agents + 12 domain-agnostic
skills + `kb/` structure + `work/` split into `laf-adaptation/`. Record upstream commit SHA in
`VENDOR.md` (Apache-2.0 attribution). **No edits to vendored files.**

**Phase 1 — Author the native spine.** Port LAF configs (verbatim, zero rework) into `/adaptation-tiers`,
`/adaptation-rules`, `/source-fidelity`, `/adaptation-safety`. Build `analyst` + `safety-verifier`
agents. Wire `writer`'s adaptation mode via `skills:` frontmatter (skill-only change). Wire the
analysis→transform→safety-gate→verdict→revise loop.

**Phase 2 — Build greenfield.** `chronicler` (tier-aware canon-extraction, per-tier `continuity.md`,
G1) + `tier-coordinator` (parallel fan-out default, sequential fallback G2). These block on nothing
upstream. Add native kb layers.

**Phase 3 — Compose & prove (hard gate).** Run the full 11-step workflow on one Tolkien chapter at
Tier 1; then the same chapter at Tiers 1/3/5 through `tier-coordinator`. Gate on: v2.0 tags present,
safety PASS, per-tier canon written, quartet all four ran.

**Phase 4 — Upstream-sync protocol.** Periodic reconcile: `diff` the vendored subset against upstream;
apply non-conflicting patches to adopted files only. **Native files are never touched by sync.**

**Carried verbatim (zero rework):** all LAF configs (4 tier profiles, thematic/character rules, 2
concept maps), 4 prompts (re-homed as skill/agent bodies), work template.
**Adopted from CWS:** 6 agents + 12 skills + kb lifecycle + work/kb split.
**Cut:** CWS plugin/Mars packaging (mars.toml, `cw/` mirror, `sync_cw_skills.py`) — avoids ADR-006
re-litigation; `web-researcher` retained but dormant. LAF's standalone prompt *files* (logic re-homed).

---

## 5. Resolved Open Questions

### Report 1 §8.3
- **Q1.1 Continuity:** Adopted `kb/canon/` + `kb/timeline/`, populated by build-new tier-aware
  `chronicler` after each chapter settles; per-tier `continuity.md` tracks divergent canonical state (G1).
- **Q1.2 Quality assurance:** Adopted critic/editor/reader-sim quartet, unchanged. Adaptation quality
  (did T1 preserve emotional resonance? did T3 earn weight-not-gore?) is a `critic` focus area loading
  `/adaptation-rules`. Distinct from safety.
- **Q1.3 Iteration on FAIL:** Native `safety-verifier` FAIL re-enters the adopted writer→critic→writer
  loop at step 3. Loop is CWS's; trigger is LAF's.
- **Q1.4 Knowledge persistence:** Adopted `work/`→`kb/` lifecycle; native `work/analysis/` +
  `kb/tiers/` + `kb/adaptation-mapping/` + per-work `kb/adaptations/<work>/` (three-part keyed) ride
  inside it. Promotion only on muse accept.
- **Q1.5 Multi-tier coordination:** `analyst` runs **once** per chapter (shared, tier-invariant source
  analysis); `tier-coordinator` fans transforms **parallel by default**, **sequential fallback** for
  state-heavy works (G2), reconciling source-fidelity consistency across the tier outputs.

### Report 2 §8.3
- **Q2.1 Tier system location:** `/adaptation-tiers` skill + `kb/tiers/` — first-class native axis, not
  dissolved into vocab or a CLAUDE.md section (constraint #1).
- **Q2.2 Source-adaptation workflow:** Native `analyst` agent runs **before** muse/brainstormer as a
  pre-orchestration phase — adaptation's native entry point.
- **Q2.3 Transformation rules:** `/adaptation-rules` skill, loaded by the adopted writer in adaptation mode.
- **Q2.4 Confidence tagging:** Native `/source-fidelity` skill (analyst-owned); tags propagate through
  the adopted `story-memory` fact-extraction carrier.
- **Q2.5 Who runs safety_check:** A distinct native `safety-verifier` agent, running **after**
  `continuity-checker`. Not a continuity mode, not a critic focus (constraint #4 preserved).
- **Q2.6 Chapter- or session-driven:** **Chapter-driven** (LAF's unit of work) executed **through**
  CWS's session machinery. The muse session processes one chapter; the kb persists across chapters.
- **Q2.7 Multi-tier parallel or sequential:** **Parallel fan-out** per tier (default), reconciled by
  `tier-coordinator` enforcing shared source-canon with tier-differentiated framing; **sequential**
  documented degradation mode for state-heavy works (G2).

---

## 6. Critical Constraints Check — all 6 survive

| # | Constraint | Mechanism (how it survives under Path C) | Status |
|---|-----------|------------------------------------------|--------|
| 1 | **LAF tier axis** | `/adaptation-tiers` + `kb/tiers/` is a first-class native axis; adopted agents *consume* it as an explicit active-tier parameter, never dilute it into a persona/genre axis. Tier-coordinator is native. | ✅ |
| 2 | **Uncertainty discipline** | `analyst` + `/source-fidelity` mandate CERTAIN/PROBABLE/UNCERTAIN before any transform; step 1 ABORTs on NO-ACCESS. Enforced at the native front-end gate. | ✅ |
| 3 | **safety_check** | Native `safety-verifier` agent + `/adaptation-safety`; mandatory Tier 1–2; blocks promotion on FAIL and triggers the revision loop. | ✅ |
| 4 | **CWS quartet (4 distinct modes)** | `critic`, `editor`, `reader-sim`, `continuity-checker` adopted verbatim as four distinct agents; `safety-verifier` added as a *fifth*, not a merge. **Written invariant (G3): editor is never folded.** | ✅ |
| 5 | **work/ vs kb/ split** | Adopted `kb-management` lifecycle governs all layers incl. native ones; drafts/reports/analysis stay in `work/`; promotion to `kb/` only on muse accept. | ✅ |
| 6 | **skill-vs-agent distinction** | Boundary-contract rule #1: native knowledge enters adopted agents ONLY as loadable skills, never by editing agent files. Native stances are always agents; native knowledge always skills. Load-bearing in the composition mechanism itself. | ✅ |

---

## 7. Residual Risks & Required Mitigations (carried from adversarial cost analysis)

| Risk | Severity | Required mitigation (must ship) |
|------|----------|--------------------------------|
| Boundary drift ("just tweak an adopted agent") | High — architecture invites it | Boundary contract enforced: `VENDOR.md` SHA manifest + frontmatter-only integration; adopted files patch-clean; CI/pre-commit check that vendored files are unmodified |
| "Hybrid → everything half-done" | High | Phase 3 hard gate (full 11-step run on a real chapter across 3 tiers before 0.1 ships); finish-what-you-start discipline |
| Two-provenance maintenance / cognitive load | Medium (permanent) | Every file labeled vendored-vs-native; contributor doc; scope the adopted subset small |
| Upstream-sync of partial tree | Medium | Sync touches adopted files only; accept degradation to manual cherry-pick; pin to a known-good SHA |
| Latent divergent-canon bug | Closed by G1 | Per-tier `continuity.md` + (work,tier,chapter) key in chronicler/tier-coordinator |

---

## 8. Next Step

Handoff target = **design**. To turn this decision into a concrete architecture specification
(agent frontmatter schemas, skill `SKILL.md` bodies, kb file formats, the boundary-contract CI check,
the `/adaptation-safety` rubric, and the tier-coordinator reconciliation algorithm):

```
/sc:design @.dev/releases/current/0.1/brainstorm/merged-requirements.md
```
