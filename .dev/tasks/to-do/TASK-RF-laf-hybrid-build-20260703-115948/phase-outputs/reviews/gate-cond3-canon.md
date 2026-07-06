# HARD-GATE Condition 3 — per-tier canon written

**Verdict:** ✅ **PASS**

**Evidence** (`laf-adaptation/kb/adaptations/tolkien/tier-{1,3,5}/`, per kb-formats.md §4.1-§4.3):

| Tier | continuity.md | chapters/ch-01/canon-delta.md | decisions.md | chapters/ch-01/analysis.yaml + adapted.md |
|------|---------------|-------------------------------|--------------|-------------------------------------------|
| T1 | ✓ | ✓ | ✓ | ✓ + ✓ |
| T3 | ✓ | ✓ | ✓ | ✓ + ✓ |
| T5 | ✓ | ✓ | ✓ | ✓ + ✓ |

continuity.md + canon-delta.md exist for **each** tier run (T1, T3, T5).

**Chronicler keying invariant:** every per-tier write is keyed `(work, tier, ch-01)` — `work=tolkien` and
`tier=N` are encoded in the path `kb/adaptations/tolkien/tier-<N>/`, and `chapter=ch-01` is encoded in the
`chapters/ch-01/` path and stamped `[ch-01]` on each continuity/decisions entry.

**No transformed-name promotion to shared canon:** `grep -rli "grumpy king" kb/canon/ kb/timeline/` → NONE.
"Grumpy King" appears **only** under the per-tier tier-1 canon and the work-mapping config
`kb/adaptation-mapping/tolkien-mapping.yaml`, never in shared `kb/canon/`/`kb/timeline/`. Shared
`kb/canon/tolkien/ch-01.md` holds source names (Sauron, Denethor, Théoden, Éowyn, Nazgûl). Confirmed by grep.

**No cross-tier bleed:** each tier's continuity.md holds only that tier's renderings (T1 transformed, T3
transition, T5 near-source); no tier-N fact appears in another tier's continuity.

**Gaps:** none. Per-tier canon written for all three tiers with the keying invariant intact and no shared-canon leak.
