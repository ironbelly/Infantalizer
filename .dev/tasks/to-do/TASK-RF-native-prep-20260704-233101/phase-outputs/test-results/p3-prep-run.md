# P3 Prep Run Transcript — `/laf:prep` end-to-end on Tolkien fixture

## Invocation (Tolkien strings, per research/07 GAP 3 — NOT Narnia)

```
/laf:prep "The Lord of the Rings" --source laf-adaptation/source/tolkien/ch-01.txt
```

- **slug:** `tolkien`
- **source:** `laf-adaptation/source/tolkien/ch-01.txt` (259-word synthetic PATH-B proof fixture; FULL source access — Phase-0 did NOT abort).
- **greenlight:** reached CONFIRMED (the automated prove plays both the coordinator and the confirming user; `50-greenlight.md` carries `status: CONFIRMED`).

## 8-file package written to `work/prep/tolkien/`

| File | Stage | Bytes |
|---|---|---|
| `00-work-context.md` | 1 RESEARCH | 3262 |
| `10-challenges.yaml` | 3 CLASSIFY | 8945 |
| `20-analysis-work-level.yaml` | 3 ANALYZE | 4615 |
| `30-mapping.yaml` | 4 MAPPING | 8361 |
| `40-prep-brief.md` | 6 PACKAGE | 5797 |
| `50-greenlight.md` | 7 GATE | 1590 |
| `60-handoff-prompt.md` | 8 HANDOFF | 53 |
| `70-traceability.md` | 8 TRACE | 5007 |

## STAGE 7 dual-form promotion — runtime transform (the coordinator is the operator)

Both promotion targets are RUNTIME outputs of this run (derived from `30-mapping.yaml`), NOT hand-authored:

| Target | Form | Written? |
|---|---|---|
| `laf-adaptation/kb/adaptation-mapping/tolkien-mapping.yaml` | 6-key hyphen, `meaning:` KEPT | ✅ (overwrote pre-existing 5-key file) |
| `config/concept_mapping/templates/tolkien_mapping.yaml` | 5-key underscore, `meaning:` STRIPPED | ✅ (overwrote pre-existing file; validates against frozen 5-key schema) |

## YAML key-count validation (verbatim, exit 0)

```
30-mapping keys: ['characters', 'concepts', 'key_scenes', 'master_translation_table', 'meaning', 'work_metadata'] len: 6
kb keys:         ['characters', 'concepts', 'key_scenes', 'master_translation_table', 'meaning', 'work_metadata'] len: 6
root keys:       ['characters', 'concepts', 'key_scenes', 'master_translation_table', 'work_metadata'] len: 5
```

## Write-provenance (proves the promotion re-wrote both targets — non-vacuous)

Pre-run sha256 (from `test-results/p3-prerun-mapping-hashes.txt`):
```
config/concept_mapping/templates/tolkien_mapping.yaml 914a85b8db7573149b2b3118561d9db93ba37ad94b2f193035183991d29a707f
laf-adaptation/kb/adaptation-mapping/tolkien-mapping.yaml 914a85b8db7573149b2b3118561d9db93ba37ad94b2f193035183991d29a707f
```
(both pre-existing files were byte-identical, 5-key, no `meaning:`)

Post-run sha256:
```
config/concept_mapping/templates/tolkien_mapping.yaml 2d62cb348bd389d888edd0adf3a5ceb368d31d12db88d2bcc5e3c1b9c0cb83b8
laf-adaptation/kb/adaptation-mapping/tolkien-mapping.yaml b3368d64cc1829694c868d1a271857437e3fff7cc63711fa47d3f48a27d847e6
```
Both DIFFER from the pre-run snapshot → the runtime promotion wrote fresh content (Step 5.3 assertion (c) is non-vacuous).

## No build-time hand-authoring

All mapping files (`30-mapping.yaml`, `tolkien-mapping.yaml`, `tolkien_mapping.yaml`) are OUTPUTS of this run, derived by the prep procedure / Stage 7 transform. No mapping file was hand-authored at build time.

## Run errors

None. The run completed all 8 stages through CONFIRMED greenlight and both HALT gates auto-confirmed by the prove.

## Fixture-driven notes

- The 259-word fixture grounds the work-level `meaning:` in what it exhibits (hope against despair, redemptive courage, the corrupting nature of power); characters/concepts not in the fixture are flagged as Open Risk in the prep brief.
- Compound scenes: the Siege and Théoden's fall + Éowyn's stand (death + emotional + violence at high severity); §2.1 reconciliation baked into `10-challenges.yaml` with `meaning_survives: true`.
- Challenge types exercised include the human-judgment rows (mass-warfare, sacrifice-and-return, etc.) and the deterministic rows (violence-level, death-euphemism).
