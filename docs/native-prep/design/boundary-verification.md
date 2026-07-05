---
title: "Boundary-Check Verification Plan"
parent: DESIGN.md
status: draft
---

# Boundary-Check Verification Plan

The prep phase must leave `check_boundary.py` **green**. This spec gives the corrected, boundary-classified
change-list, the exact `VENDOR.md` delta, and the per-rule (A–F) expectation each change must satisfy —
all grounded in the live `laf-adaptation/scripts/check_boundary.py` and `VENDOR.md`.

Run after P0, P1, and P3:

```
uv run python laf-adaptation/scripts/check_boundary.py            # Mode V (no upstream) — expect PASS
uv run python laf-adaptation/scripts/check_boundary.py --report   # provenance summary — expect +3 NATIVE rows
```

---

## 1. Corrected change-list (boundary-classified)

| # | Change | Class | Boundary-safe? — why | Req |
|---|---|---|---|---|
| 1 | `.claude/commands/laf/prep.md` | harness surface (outside tree) | ✅ not in `laf-adaptation/`; not manifested, not required by Rule F | R1 |
| 2 | `.claude/commands/laf/rewrite.md` | harness surface (outside tree) | ✅ same | R9 |
| 3 | `agents/prep-cordinator.md` | NATIVE (new) | ✅ new file; `classify()`→NATIVE; no upstream collision (Rule E) | R4 |
| 4 | `skills/prep/SKILL.md` | NATIVE (new) | ✅ new dir → `skills/prep/**` glob; Rule F-covered | R5 |
| 5 | `skills/prep/resources/path-contract.md` | NATIVE resource | ✅ covered by `skills/prep/**` glob — no own row | R3 |
| 6 | `skills/thematic-fidelity/SKILL.md` | NATIVE (new) | ✅ new dir → `skills/thematic-fidelity/**` glob | R5 |
| 7 | `skills/adaptation-rules/resources/exemplars/*.md` (×3) | NATIVE (under a **NATIVE** skill) | ✅ covered by the EXISTING `skills/adaptation-rules/**` glob row (`VENDOR.md` line 113); DERIVED-marked | R13 |
| 8 | `agents/analyst.md` body edit (meaning, compound_scene, work-mode) | NATIVE-body edit | ✅ NATIVE, NO_HASH row (`VENDOR.md` line 111) — body not pinned | R10, R11 |
| 9 | `agents/tier-coordinator.md` body edit (Check D) | BUILD-NEW-body edit | ✅ BUILD-NEW, NO_HASH row (`VENDOR.md` line 117) — body not pinned | R10 |
| 10 | `agents/writer.md` | **NO CHANGE** | ✅ stays ADOPTED-PATCHED at exactly its 1 additive line; meaning routes via promoted mapping (D6) | D6 |
| 11 | `agents/muse.md` | **NO CHANGE** | ✅ stays ADOPTED-CLEAN; reads `meaning:` as data; a skill line would violate Rule C′ (ADOPTED-PATCHED reserved for writer.md) | D6 |
| 12 | `config/…/_mapping.yaml` + `kb/adaptation-mapping/…-mapping.yaml` | runtime output (promotion) | ✅ generated on greenlight; not part of the manifested set | R2, R8 |
| 13 | `docs/guides/ADDING_NEW_WORKS.md` pointer | NATIVE doc edit (outside Rule-F glob) | ✅ | R14 |
| 14 | root v1.0 new machinery | NONE | ✅ out of scope (root promotion is a 5-key file only) | R14 |

**Deltas from the spec's change-list** (see [`DESIGN.md §6`](DESIGN.md)):
- Rows 1-2 reclassified from "VENDOR NATIVE update" → **harness surface, not VENDOR-tracked** (C1,
  user-confirmed).
- Row 7 reclassified from "NATIVE files in **adopted** resources/" → **NATIVE files under a NATIVE skill**
  (C3): `adaptation-rules` is NATIVE, so the boundary concern is moot and **no new VENDOR row** is needed.
- Row 11 (`muse` unchanged) made explicit — it is the mechanism that keeps meaning-preservation
  adopted-body-free.
- The spec's change-list #13 ("VENDOR rows for #1-#6, #8-#9") is superseded: only **3** NATIVE rows are
  added (§2), and they are **auto-generated** by `--init`, never hand-written.

---

## 2. `VENDOR.md` delta — exactly 3 rows, auto-generated

`check_boundary.py --init --upstream <checkout>` regenerates the manifest from disk. Given the P0 files, it
deterministically appends (in the NATIVE group, sorted by path):

```
| agents/prep-cordinator.md    | NATIVE | — | — |
| skills/prep/**               | NATIVE | — | — |
| skills/thematic-fidelity/**  | NATIVE | — | — |
```

Traced through the real code:
- `disk_agents()` finds `agents/prep-cordinator.md`; `classify()` → not `declared`, not `upstream_has`,
  `parts[0]=="agents"`, name ∉ `BUILD_NEW_AGENTS {chronicler, tier-coordinator}` ⇒ **NATIVE** (line 44-45,
  338-339).
- `disk_skill_dirs()` finds `prep/` and `thematic-fidelity/`; neither is `upstream_root/skills/<name>` ⇒
  the `else` branch writes one `skills/<name>/** | NATIVE | — | —` glob row each (`classify()` → skill,
  sk ∉ `BUILD_NEW_SKILLS {adaptation-safety}` ⇒ NATIVE) (line 405-407).
- `agents/analyst.md`, `agents/tier-coordinator.md` rows are **unchanged** — NATIVE/BUILD-NEW rows carry
  `—`/`—`, and editing a NO_HASH body does not change its row.
- `skills/prep/resources/path-contract.md` and the exemplars get **no rows** — glob-covered.

> Do **not** hand-edit the manifest table (it is machine-generated — `VENDOR.md` line 47-49). If a fresh
> upstream checkout is unavailable, `--init` may be skipped: the 3 rows can be appended by re-running the
> documented flow, but the canonical path is `--init`.

---

## 3. Per-rule expectations (Mode V — the CI/pre-commit gate)

| Rule | What it checks | Expectation after the prep phase |
|---|---|---|
| **A** | every adopted file matches its recorded `laf_sha256` | **PASS** — no adopted file touched. `writer.md`, `muse.md`, all 10 ADOPTED-CLEAN agents + adopted skills byte-unchanged |
| **A′** (CH-1) | every ADOPTED-CLEAN body re-derives to its pinned `upstream_sha256` | **PASS** — no ADOPTED-CLEAN body edited |
| **C′** (CH-3) | `ADOPTED-PATCHED` reserved for `writer.md` only | **PASS** — no new ADOPTED-PATCHED file (muse stays ADOPTED-CLEAN; C2/row 11) |
| **D** | G3 quartet intact (`critic/editor/reader-sim/continuity-checker` ADOPTED-CLEAN); `editor.md` never folded | **PASS** — untouched |
| **E** | no NATIVE/BUILD-NEW name collides with an upstream file | **PASS** — `prep-cordinator`, `prep`, `thematic-fidelity` do not exist upstream (CWS has no prep phase) |
| **F / F′** (CH-2) | every `agents/*.md` + `skills/**/SKILL.md` manifested; adopted `resources/**` manifested | **PASS** — new agent row + 2 new skill globs cover the new SKILL.md files; no new files under an *adopted* skill (exemplars are under NATIVE `adaptation-rules`) |
| parser / path-safety (CH-4/6) | manifest rows well-formed, no traversal | **PASS** — `--init` writes valid rows |

**Mode U** (`--upstream <checkout>`, the absolute guarantee) additionally runs Rules B/C and the HEAD-pin
(CH-5). Nothing in the prep phase affects adopted bodies, so Mode U is unaffected — but it should still be
run once at P3 if an upstream checkout at the pinned SHA (`3338495f…`) is available.

---

## 4. Non-manifested additions (intentionally outside the Rule-F glob)

Per `laf-adaptation/CLAUDE.md`, several managed dirs are deliberately outside the hash-pin glob. The prep
phase's non-manifested additions and their class:

| Addition | Class | Why not manifested |
|---|---|---|
| `.claude/commands/laf/*.md` | harness surface | outside `laf-adaptation/` entirely |
| `skills/prep/resources/path-contract.md` | NATIVE | glob-covered by `skills/prep/**` (manifested, just not its own row) |
| `skills/adaptation-rules/resources/exemplars/*.md` | NATIVE | glob-covered by `skills/adaptation-rules/**` |
| `work/prep/<slug>/*` | runtime output | `work/` is provisional runtime state, never manifested |
| `config/…_mapping.yaml`, `kb/adaptation-mapping/…-mapping.yaml` | runtime output (promotion) | outside `agents/`+`skills/` glob; `kb/adaptation-mapping/` is NATIVE carried-verbatim, not pinned |
| `docs/guides/ADDING_NEW_WORKS.md` | NATIVE doc | outside `laf-adaptation/` |

---

## 5. Verification checklist (copy into the P3 gate)

```
[ ] check_boundary.py (Mode V) → BOUNDARY CONTRACT: PASS
[ ] --report shows exactly +3 NATIVE rows (prep-cordinator, prep/**, thematic-fidelity/**)
[ ] git diff shows agents/writer.md and agents/muse.md UNCHANGED (0 bytes)
[ ] agents/analyst.md diff is additive-only (new inputs + meaning/compound_scene outputs); chapter defaults intact
[ ] agents/tier-coordinator.md diff adds only Check D; no frontmatter change
[ ] each exemplar opens with the `@kind method-illustration; source-fidelity: DERIVED` marker
[ ] no file written under work/ or kb/canon/ by the prep phase except the package + promotion targets
[ ] root config/concept_mapping/templates/<slug>_mapping.yaml validates to the 5-key schema (no meaning:)
[ ] kb/adaptation-mapping/<slug>-mapping.yaml carries the 6th meaning: key
```

Green on all boxes = the prep phase respects the boundary contract and closes all four evaluation gaps
natively.
