# Research: Gap-Fill
Status: Complete
Date: 2026-07-04

Purpose: Resolve the 5 gaps found by the A.8 quality gate for the native-prep MDTM task file, with concrete decisions + runnable commands and file:line evidence.

---

## GAP 1 (IMPORTANT) — Runtime-vs-build-time promotion boundary

**Resolution: The dual-form mapping promotion is RUNTIME behavior of the `prep-cordinator` agent on greenlight, NOT a build-time file the implementation task hand-creates.**

### Evidence chain

- `prep-skill-specs.md:88-89` (`/prep §6 Greenlight`): "On confirm: **promote 30-mapping.yaml (dual-form) via /kb-management**; set status PENDING → CONFIRMED." Promotion is an action taken *when the phase runs*, gated on user confirmation.
- `package-schemas.md:190-192` (§4.1): "**On greenlight**, `/kb-management` writes two forms" — the trigger is greenlight (runtime), and the writer is `/kb-management`, not the task author.
- `path-contract.md:44-45` (§3): "**On `50-greenlight.md` → `CONFIRMED`**, `30-mapping.yaml` is promoted via `/kb-management` to **two** targets."
- `path-contract.md:82-83` (§5 write-ownership): `kb/adaptation-mapping/<slug>-mapping.yaml` and `config/concept_mapping/templates/<slug>_mapping.yaml` are both "Written by `/kb-management` **on greenlight (prep phase)**" — i.e. produced by running the phase, owned by the runtime agent.
- `prep-agent-schemas.md:72` (§1.2 STAGE 7): "GREENLIGHT write 50-greenlight.md; emit confirmation; HALT; **on CONFIRM promote 30 via /kb-management**." The promotion is literally step 7 of the agent's *runtime* procedure.
- Repo state confirms the greenlight-driven root file is the ONLY thing that ever produces a `<slug>_mapping.yaml` with meaning-strip: the current 0.1 kb copy `tolkien-mapping.yaml` is 5-key (`meaning` absent — verified below in GAP 2), and no `_mapping.yaml` is authored by hand as part of building the phase.

### What the BUILD-TIME task actually creates

The build-time deliverable is the **INSTRUCTIONS that cause the dual-form write**, never the written files:
- `/prep` SKILL.md §6 body text that says "promote 30-mapping.yaml (dual-form) via /kb-management" (`prep-skill-specs.md:88-89`).
- `prep-cordinator` STAGE 7 body text that calls `/kb-management` on CONFIRM (`prep-agent-schemas.md:72`).
- The dual-form contract table itself in `package-schemas.md §4.1` / `path-contract.md §3` (already authored as design; the task ships them into the `/prep` resource + agent/skill bodies).

The meaning-strip on the root copy (`package-schemas.md:196-197`, `:201`) is a *rule expressed in those instructions* for `/kb-management` to apply at run time — it is not a file the task pre-writes.

### DECISION: the task file MUST NOT have a build item that hand-creates any `<slug>_mapping.yaml`

Those files (`config/concept_mapping/templates/<slug>_mapping.yaml`, `laf-adaptation/kb/adaptation-mapping/<slug>-mapping.yaml`) appear **only when `/laf:prep` is actually run through greenlight** — i.e. they are P3 (Prove) run outputs, not P0-P2 authored artifacts.

### Build-time vs runtime artifact table

| Artifact | Authored by the implementation task (BUILD-TIME) | Produced by running the phase (RUNTIME / P3) |
|---|---|---|
| `laf-adaptation/skills/prep/SKILL.md` (incl. §6 promotion instruction) | ✅ P0 | — |
| `laf-adaptation/skills/prep/resources/path-contract.md` | ✅ P0 | — |
| `laf-adaptation/skills/thematic-fidelity/SKILL.md` | ✅ P0 | — |
| `laf-adaptation/agents/prep-cordinator.md` (incl. STAGE 7 `/kb-management` call) | ✅ P0 | — |
| `laf-adaptation/skills/adaptation-rules/resources/exemplars/*.md` | ✅ P0 | — |
| `analyst` NATIVE body diff (`meaning`, `compound_scene`, work-mode) | ✅ P1 | — |
| `tier-coordinator` BUILD-NEW body diff (Check D) | ✅ P1 | — |
| `.claude/commands/laf/prep.md` + `rewrite.md` | ✅ P2 | — |
| `ADDING_NEW_WORKS.md` pointer paragraph | ✅ P4 | — |
| `work/prep/<slug>/*` (the 8-file package) | ❌ | ✅ P3 (`prep-cordinator` writes; `path-contract.md:81`) |
| `kb/adaptation-mapping/<slug>-mapping.yaml` (6-key, meaning KEPT) | ❌ | ✅ P3 greenlight (`/kb-management`; `path-contract.md:82`) |
| `config/concept_mapping/templates/<slug>_mapping.yaml` (5-key, meaning STRIPPED) | ❌ | ✅ P3 greenlight (`/kb-management`; `path-contract.md:83`) |

**Rule for the task builder:** every P0-P4 build item authors *instructions/bodies*; the only place `<slug>_mapping.yaml` files come into existence is the P3 run.

---

## GAP 2 (IMPORTANT) — Runnable kb-6-key validation command (a P3 RUN gate, not a build-time check)

**The 6-key form (with top-level `meaning:`) does NOT exist in the repo today.** It is a P3 RUN OUTPUT, materialized only after `/laf:prep` executes through greenlight.

### Evidence the 6-key form is not yet present

The shipped 0.1 kb mapping is currently **5-key with no `meaning:`** — verified by running:

```
$ uv run --with pyyaml python -c "import yaml; d=yaml.safe_load(open('laf-adaptation/kb/adaptation-mapping/tolkien-mapping.yaml')); print('KEYS:', sorted(d)); print('len:', len(d)); print('meaning present:', 'meaning' in d)"
KEYS: ['characters', 'concepts', 'key_scenes', 'master_translation_table', 'work_metadata']
len: 5
meaning present: False
```

The 6-key `meaning:` extension is defined only as the P3 output form: `package-schemas.md:161` ("6-KEY 0.1 FORM (what lives at work/prep/<slug>/30-mapping.yaml and kb/adaptation-mapping/<slug>-mapping.yaml)"), `:162-166` (the `meaning:` block is "the 6th key; 0.1-only extension"), and `package-schemas.md:196` (kb copy "6-key … meaning: **kept**"). None of this exists on disk pre-run.

### Runnable P3-gate command — assert the 6-key OUTPUT (meaning PRESENT)

Run these **after** a `/laf:prep tolkien` run reaches greenlight (P3), against the prep-package derived mapping and the promoted 0.1 kb copy. Both must show 6 keys including `meaning`:

```bash
# (a) the derived prep-package mapping (work/prep/<slug>/30-mapping.yaml)
uv run --with pyyaml python -c "import yaml; d=yaml.safe_load(open('work/prep/tolkien/30-mapping.yaml')); print(sorted(d)); assert 'meaning' in d and len(d)==6, 'expected 6-key form with meaning'"

# (b) the promoted 0.1 kb copy (hyphen filename, meaning KEPT)
uv run --with pyyaml python -c "import yaml; d=yaml.safe_load(open('laf-adaptation/kb/adaptation-mapping/tolkien-mapping.yaml')); print(sorted(d)); assert 'meaning' in d and len(d)==6, 'kb copy must keep meaning (6-key)'"
```

### Runnable P3-gate command — assert the ROOT 5-key OUTPUT (meaning ABSENT)

The promoted root copy (underscore filename) must have `meaning:` STRIPPED back to the frozen 5-key schema (`package-schemas.md:197`, `path-contract.md:53-54,59-61`):

```bash
uv run --with pyyaml python -c "import yaml; d=yaml.safe_load(open('config/concept_mapping/templates/tolkien_mapping.yaml')); print(sorted(d)); assert 'meaning' not in d and len(d)==5, 'root copy must strip meaning (frozen 5-key)'"
```

Expected root keys: `['characters', 'concepts', 'key_scenes', 'master_translation_table', 'work_metadata']` (matches the shipped `tolkien_mapping.yaml` shape verified in GAP 2 evidence above; the frozen five per `ADDING_NEW_WORKS.md:104-106` Step 6 "same five top-level keys as the shipped schema").

### DECISION for the task builder

These three assertions belong to the **P3 (Prove) gate item**, to be RUN after the `/laf:prep tolkien` run completes greenlight — **NOT** as a static/build-time check. At build time the repo has no `work/prep/tolkien/` and no `tolkien` 6-key kb copy, so these commands would fail if run before P3.

---

## GAP 3 (IMPORTANT) — Commit the P3 invocation to Tolkien (NOT Narnia)

**The DESIGN.md §7 P3 row is internally inconsistent** and the repo ships NO Narnia source, so P3 must be pinned to the Tolkien fixture.

### Evidence of the DESIGN.md Narnia/Tolkien mismatch

`DESIGN.md:315` (§7, the P3 row) mixes a Narnia title with a Narnia slug:
> "**P3. Prove (HARD GATE)** — Run `/laf:prep "The Lion, the Witch and the Wardrobe"` end-to-end … `/laf:rewrite --work narnia` reads the package by hardcoded path …"

So the title is *The Lion, the Witch and the Wardrobe* and the rewrite slug is `narnia`.

### Evidence the repo cannot run a Narnia P3

Inspecting available sources:

```
$ ls -R laf-adaptation/source/
laf-adaptation/source/:
README.md
tolkien

laf-adaptation/source/tolkien:
ch-01.txt
```

- **No `laf-adaptation/source/narnia/` exists** (`ls laf-adaptation/source/narnia/` → "No such file or directory").
- **No `laf-adaptation/kb/adaptation-mapping/narnia-mapping.yaml`** — the 0.1 kb layer holds only `tolkien-mapping.yaml` + `universal-mappings.yaml`.
- The only root Narnia artifact is `config/concept_mapping/templates/narnia_mapping.yaml` (a pre-existing 5-key root template with no source and no 0.1 kb pair) — it cannot back an end-to-end prep run because prep requires a **readable source text** (Q1, mandatory text track: `prep-agent-schemas.md:54` "Elicited as a required input"; `prep-skill-specs.md:63-67` text track is REQUIRED, MEMORY-BASED never acceptable at work level).
- The shipped Tolkien fixture is a **synthetic, non-copyrighted** stand-in. `laf-adaptation/source/README.md` documents it: "This tree ships a PATH-B fixture: `source/tolkien/ch-01.txt` is an **ORIGINAL SYNTHETIC proof fixture** authored for LAF — it is NOT Tolkien's copyrighted prose." First 10 lines confirm ("The Siege at the Grey City / Dawn never came to the plain that morning; the dark lord's shadow lay over the world … Sauron did not ride among them … the Steward Denethor watched …") — Tolkien-adjacent original prose, aligned to the committed `tolkien-mapping.yaml`.

### COMMITTED P3 invocation strings (Tolkien, runnable end-to-end)

The task file's P3 gate item MUST use these exact strings:

| Step | Exact invocation |
|---|---|
| prep | `/laf:prep "The Lord of the Rings" --source laf-adaptation/source/tolkien/ch-01.txt` |
| slug | `tolkien` |
| rewrite | `/laf:rewrite --work tolkien` |

### Source-access / Phase-0 note

A real prep run would normally take a full-work source; the shipped **chapter fixture** (`source/tolkien/ch-01.txt`) is documented as **adequate for a work-level SMOKE prove of the pipeline** — the source README's "Provisioning contract (Phase-3 proof)" ships it precisely so the Phase-3 gate can prove mechanics without copyrighted prose. Because a readable text is supplied, the `/source-fidelity` Phase-0 source-access declaration is **FULL/PARTIAL, not MEMORY-BASED** — so Phase-0 does **NOT** ABORT the prep (`prep-agent-schemas.md:63` "NO-ACCESS ABORTS"; `prep-skill-specs.md:66-67` "the text track is mandatory, MEMORY-BASED is never acceptable" — supplying the fixture satisfies it).

### DECISION for the task builder

The P3 gate item MUST use the **Tolkien** strings above (title *The Lord of the Rings*, slug `tolkien`, `--work tolkien`), **NOT** the Narnia title/`--work narnia` from `DESIGN.md:315`. Flag the DESIGN.md P3 row as a known spec inconsistency the task deliberately corrects (no Narnia source ships).

---

## GAP 4 (MINOR) — P2 command-resolution (well-formedness) check

**The two command files do NOT exist yet** — confirmed at build time:

```
$ ls .claude/commands/
.claude/commands/:
(empty — no laf/ subdirectory)

$ ls .claude/commands/laf/
ls: cannot access '.claude/commands/laf/': No such file or directory

$ find . -path '*/commands/laf/*' -print   # → no results
```

This confirms `.claude/commands/laf/prep.md` + `rewrite.md` are P2 build-time deliverables (`DESIGN.md:314` "P2. Commands — Author `.claude/commands/laf/prep.md` + `rewrite.md`"; command bodies specified verbatim in `prep-agent-schemas.md:221-266` §5.1/§5.2).

### Runnable build-time well-formedness check (P2 gate)

After P2 authors the two files, run:

```bash
# 1. both command files present
ls .claude/commands/laf/          # must list: prep.md  rewrite.md

# 2. each has exactly one frontmatter description: line
grep -c '^description:' .claude/commands/laf/prep.md .claude/commands/laf/rewrite.md
# expected output:
#   .claude/commands/laf/prep.md:1
#   .claude/commands/laf/rewrite.md:1
```

Both `prep.md` and `rewrite.md` carry a frontmatter `description:` per the specced frontmatter (`prep-agent-schemas.md:225` `description: Onboard a new literary work …`; `:246` `description: Begin the chapter rewrite phase …`), so `grep -c '^description:'` returns `1` for each.

### Scope note

This is a **static well-formedness** check only. Actual `/laf:prep` / `/laf:rewrite` **slash-command resolution and delegation to `prep-cordinator`** (the `DESIGN.md:314` P2 gate's "`/laf:prep` resolves and delegates") is exercised by the **P3 run**, not by any static grep. The task builder should place the `ls` + `grep -c` check under P2 and the resolution/delegation proof under P3.
