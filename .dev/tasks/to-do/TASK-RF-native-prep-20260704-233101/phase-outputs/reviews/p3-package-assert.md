# P3 Package Assert — 8-file package + meaning/compound_scene fields

Package location: `work/prep/tolkien/` (from `p3-prep-run.md`).
Path contract: `laf-adaptation/skills/prep/resources/path-contract.md` §2 (8-file layout).

## (a) 8-file package present

| File | Present? |
|---|---|
| `00-work-context.md` | ✅ |
| `10-challenges.yaml` | ✅ |
| `20-analysis-work-level.yaml` | ✅ |
| `30-mapping.yaml` | ✅ |
| `40-prep-brief.md` | ✅ |
| `50-greenlight.md` | ✅ |
| `60-handoff-prompt.md` | ✅ |
| `70-traceability.md` | ✅ |

All 8 files specified by the path contract are present → **PASS**.

## (b) `20-analysis-work-level.yaml` carries meaning + compound_scene

```
55: meaning:                                # R10 — work-level meaning to preserve
63: compound_scene: true                    # R11 — siege co-occurs death + emotional + violence (all high)
64: compound_scenes:
```

The analyst diff from P1 produced both the `meaning:` block and the `compound_scene`/`compound_scenes` fields → **PASS**.

## (c) `30-mapping.yaml` per-entry confidence = min(text, context)

Programmatic verification (pyyaml) over every `_confidence` entry:
- top-level `meaning:` block present with `{value, text_confidence, context_confidence, confidence}` shape → **PASS**
- For every per-entry `_confidence: {text, context, eff}`, `eff` equals `min(rank(text), rank(context))` (CERTAIN=4 > PROBABLE=3 > UNCERTAIN=2) → **PASS** (sample: `{text: CERTAIN, context: PROBABLE, eff: PROBABLE}`).

## Overall: PASS

All three assertions checked against the actual on-disk package files. No missing file or field.
