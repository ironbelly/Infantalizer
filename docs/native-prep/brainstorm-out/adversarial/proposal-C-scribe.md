# Proposal C — Scribe voice ("the package IS the contract; consolidate the skills")

> Persona: scribe. Lens: the *standardized package* is the real product; the agent/skill inventory should
> be **as small as possible** and the *path contract* should be the single source of truth that everything
> else references. C is the **radical-consolidation** proposal: fewer skills than A/B, one canonical
> "prep" skill that owns the whole phase, and the path contract promoted to a **referenced contract
> document** rather than scattered across skill bodies.

## C.1 Headline

A and B both propose 4 new NATIVE skills (`prep-protocol`, `work-mapping`, `challenge-taxonomy`,
`thematic-fidelity`). C argues this is **skill-sprawl**: four skills for one phase creates the same
"curated doc set" problem the prep phase is supposed to *solve*, just internalized. C's differences:

1. **ONE new NATIVE skill — `prep`** — owns the entire phase procedure, the path contract, the
   challenge taxonomy, the mapping-authoring rules, AND the meaning-preservation stance, in one
   skill with clearly delimited sections. The boundary contract is a *contract*, not a maximization
   target.
2. **The path contract is promoted to a referenced doc** — `laf-adaptation/skills/prep/resources/path-contract.md` — that BOTH the prep skill and the rewrite command import by reference. This is the single
   hardcodable source of truth for "what files the prep phase emits and the rewrite phase reads."
3. **Meaning-preservation attaches to NATIVE/BUILD-NEW agents ONLY** — no second `writer.md` patch line.
   `thematic-fidelity` is a section *inside* the `prep` skill (work-level) and a section inside the
   `tier-coordinator` body (Check D, BUILD-NEW-editable). The ADOPTED `writer` is never touched again;
   meaning reaches it via the scene brief the muse builds (which already carries tier + rules), not via a
   new skill line.
4. **Compound-scene protocol is a NATIVE skill section, not a file inside an adopted skill's resources/**
   — avoiding the "muddies the upstream-sync boundary" warning A flagged (A.11).

## C.2 The single `prep` skill

`laf-adaptation/skills/prep/SKILL.md` — one NATIVE skill, frontmatter `name: prep`, with these sections:

```
# Prep — the adaptation-prep phase
## §1 Path contract        (imports resources/path-contract.md by reference)
## §2 Challenge taxonomy   (typed dimensions, governing-rule routing, human_judgment_dimension flag — from B)
## §3 Work-level analysis  (two-track: context + text, dual confidence — from B)
## §4 Mapping authoring    (derive <work>-mapping.yaml from §2+§3, per-entry confidence — from A/B)
## §5 Meaning preservation (work-level stance: capture meaning per scene; this is Check D's input)
## §6 Question-gate coverage rule (from B)
## §7 Greenlight + handoff (the paste-able prompt template)
## §8 Traceability         (auto-emit 70-traceability.md — from B; here it's a section, not a separate skill)
```

**The boundary-contract argument for consolidation:** every new NATIVE skill is a file that must not
collide with an upstream name (Rule E), must be classified in VENDOR.md, and adds to the surface area a
contributor must understand. Four skills for one phase is exactly the kind of "document set brought to
the table" the prep phase exists to replace. One skill with clear sections is easier to maintain, easier
to sync, and easier for the next phase to reference (`- laf-adaptation:prep`).

## C.3 The path contract as a referenced doc

`laf-adaptation/skills/prep/resources/path-contract.md`:

```yaml
# The prep-phase path contract — THE single source of truth.
# Imported by: skills/prep/SKILL.md §1, commands/rewrite.md, commands/prep.md
prep_package_root: "work/prep/<work-slug>/"
files:
  00-work-context.md:        {kind: RESEARCH,     confidence_track: context}
  10-challenges.yaml:        {kind: DERIVED,      derived_from: [20]}
  20-analysis-work-level.yaml: {kind: SOURCE,     confidence_track: [text, context]}
  30-mapping.yaml:           {kind: DERIVED,      derived_from: [20, 10], promoted_on_greenlight_to:
                              [config/concept_mapping/templates/<work>_mapping.yaml,
                               kb/adaptation-mapping/<work>_mapping.yaml]}
  40-prep-brief.md:          {kind: SYNTHESIS,    audience: human}
  50-greenlight.md:          {kind: GATE,         status: PENDING|CONFIRMED}
  60-handoff-prompt.md:      {kind: HANDOFF,      template: "/laf:rewrite --work <work-slug>"}
  70-traceability.md:        {kind: DERIVED,      derived_from: [all]}
rewrite_phase_reads: [30-mapping.yaml, 40-prep-brief.md, 10-challenges.yaml]
```

**Why this is the scribe's core contribution:** the path contract is referenced by *three* consumers
(prep skill, prep command, rewrite command) from ONE file. A and B embed the path list in prose across
multiple skill bodies, which drifts. C makes the contract a versioned, importable doc — this is the
spec-kit `constitution.md` pattern (enrichment §3) applied to the path layout.

## C.4 Meaning-preservation without touching `writer` again

C's disagreement with A.8 is structural: **the ADOPTED-PATCHED `writer.md` should not get a second
additive line.** Reasoning:

- The boundary contract's *demonstration* is that `writer` gets exactly ONE additive line
  (`adaptation-rules`). Adding a second (`thematic-fidelity`) weakens the "minimal patch" exemplar and
  sets a precedent for patch-creep.
- Meaning-preservation reaches the writer **through the scene brief** the muse builds — the muse already
  reads the work-level `meaning` field (via `prep`/`thematic-fidelity` attached to muse, which is
  ADOPTED... — see C.5's caveat) and injects "preserve this meaning" into the brief. The writer obeys the
  brief; it does not need a new skill line.
- Check D lives in `tier-coordinator` (BUILD-NEW, editable) — that is the *check*, and it does not need
  the writer to have the skill.

**C.5's honest caveat (for the debate):** the muse is ADOPTED. To get the work-level `meaning` into the
scene brief, EITHER (a) `prep` is attached to muse via a new additive line (same patch-creep problem, just
moved), OR (b) the `meaning` field is carried in `kb/adaptation-mapping/` (which muse already reads) so
muse picks it up with NO body change. C chooses **(b)**: the work-level `meaning` map is promoted to
`kb/adaptation-mapping/<work>/meaning.yaml` on greenlight, and muse — which already reads
`kb/adaptation-mapping/` — consumes it with zero adopted-body edits. **This is the cleanest
boundary-respect of all three proposals.**

## C.5 Compound-scene protocol — a `prep` skill section, not an adopted-resource file

A.6 puts `compound-scenes.md` inside `adaptation-rules/resources/`. CLAUDE.md §1 explicitly says this is
"permitted but muddies the upstream-sync boundary" and "prefer adding a NATIVE skill." C follows that
preference: the compound-scene protocol is **§2.1 of the `prep` skill** (challenge taxonomy includes the
compound-scene flag + reconciliation method). The `analyst` (NATIVE) emits the `compound_scene` flag; the
reconciliation method is loaded from the `prep` skill at prep time and baked into the per-challenge entry
of `10-challenges.yaml` so the rewrite phase reads it from the package, not from a skill the writer loads.

## C.6 Where C AGREES with A and B

- 0.1 owns the phase; root gets a pointer (T1, T7).
- A NATIVE `prep-cordinator` agent (C keeps A/B's orchestrator — consolidation is about SKILLS, not the
  agent; one orchestrator agent is correct).
- The fixed-path contract (C reorganizes it into a referenced doc but keeps the same files, including
  B's `70-traceability.md`).
- Check D in `tier-coordinator`; meaning field in `analyst`.
- The `/laf:rewrite --work <slug>` handoff.

## C.7 Where C DIFFERS (the debate axes)

| Axis | A | B | C |
|---|---|---|---|
| New NATIVE skills | 4 | 4 (+traceability) | **1** (`prep`) |
| Path contract location | prose in skill bodies | prose + matrix file | **referenced doc imported by 3 consumers** |
| `writer.md` for meaning | 2nd additive line | 2nd additive line | **no writer edit; meaning via kb/adaptation-mapping/** |
| Compound-scene protocol | file in adopted resources/ | file in adopted resources/ | **section in `prep` skill** |
| Traceability | absent | separate concern | **§8 of `prep` skill** |
| Surface area | medium | high | **low** |

## C.8 Risk C introduces (self-critique)

- **Single-skill size.** One `prep` skill with 8 sections is a large skill file. If sections need to be
  independently versioned or reused outside prep, the consolidation hurts. *Mitigation:* the path-contract
  IS split out (referenced doc); the other sections are cohesive (they all serve the one phase) so a
  single file is appropriate.
- **Muse reads `kb/adaptation-mapping/` today — does it read a NEW file there without a body edit?**
  C.5(b) depends on muse already scanning the directory generically. If muse reads only specific files,
  `meaning.yaml` would need to be merged into the existing mapping file (the promoted `30-mapping.yaml`),
  not a separate file. *Resolution:* fold `meaning` INTO `30-mapping.yaml` as a top-level key, so the
  promoted mapping carries meaning and muse needs no change. (C adopts this refinement.)
- **Loss of skill-level reusability.** A's `thematic-fidelity` skill could attach to multiple agents; C's
  in-skill section cannot. *Counter:* in practice it attaches to exactly the prep phase + tier-coordinator
  body; a separate skill is speculative generality (scope discipline, framework rule #8).

## C.9 Positions on T1–T8

Same as A/B except:
- **T4:** meaning-preservation reaches adopted agents via the **promoted mapping file** (muse reads it
  already), NOT via new skill lines on adopted agents. Cleanest boundary respect.
- **T5:** path contract promoted to a **referenced, importable doc** (single source of truth across prep
  + rewrite commands).
- **T6:** compound-scene + mapping-authoring + taxonomy are **sections of one `prep` skill**, not 3-4
  skills + an adopted-resource file.

## C.10 Open questions C adds

1. Is one large `prep` skill harder to maintain than 4 small ones? (C: no — cohesion beats modularity
   here; the sections are not independently reused.)
2. Does folding `meaning` into `30-mapping.yaml` overload the mapping's schema? (C: no — it's a
   top-level `meaning:` key, parallel to `work_metadata:`.)
