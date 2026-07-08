# P0 Output Inventory

Aggregate manifest of all 9 P0-created files (for the Phase Gate P0 QA lens agents to verify against).

| File | Lines | Type | Frontmatter keys / line-1 marker |
|---|---|---|---|
| `laf-adaptation/agents/prep-cordinator.md` | 87 | agent (NATIVE) | `name description model skills tools` (5 keys) |
| `laf-adaptation/skills/prep/SKILL.md` | 116 | skill (NATIVE) | `name description` (2 keys; `description: \|`) |
| `laf-adaptation/skills/prep/resources/path-contract.md` | 78 | skill resource | (no frontmatter — resource) |
| `laf-adaptation/skills/thematic-fidelity/SKILL.md` | 57 | skill (NATIVE) | `name description` (2 keys; `description: \|`) |
| `laf-adaptation/skills/adaptation-rules/resources/exemplars/sacrifice-and-return.md` | 30 | exemplar (NATIVE, DERIVED) | line-1 marker ✅ byte-for-byte |
| `laf-adaptation/skills/adaptation-rules/resources/exemplars/betrayal-and-redemption.md` | 33 | exemplar (NATIVE, DERIVED) | line-1 marker ✅ byte-for-byte |
| `laf-adaptation/skills/adaptation-rules/resources/exemplars/petrification-body-horror.md` | 34 | exemplar (NATIVE, DERIVED) | line-1 marker ✅ byte-for-byte |
| `.claude/commands/laf/prep.md` | 16 | command (harness, outside boundary) | `description argument-hint` |
| `.claude/commands/laf/rewrite.md` | 21 | command (harness, outside boundary) | `description argument-hint` |

## Notes

- All 9 expected P0 files present (none MISSING).
- prep-cordinator agent: 5-key frontmatter in order `name/description/model/skills/tools`, `model: opus`,
  `tools: >` folded form (orchestrator with `Agent(...)`), no Mars keys; `name:` = filename stem `prep-cordinator` (single 'o').
- Both SKILL.md files: exactly `name` + `description: |` (literal block), no Mars keys, no `rules/`/`templates/` subdirs.
- Both commands: exactly `description` + `argument-hint`.
- All 3 exemplars carry the verbatim DERIVED marker on line 1.
- Boundary (Mode V) PASS, `--report` NATIVE = 8 (see `test-results/p0-boundary-summary.md`).
