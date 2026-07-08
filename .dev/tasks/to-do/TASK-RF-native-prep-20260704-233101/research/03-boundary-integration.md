# Research: Boundary-Contract Integration Mechanics

**Track goal:** Build an MDTM task file to implement the LAF adaptation-prep phase per docs/native-prep/design/DESIGN.md; the boundary check must stay green.
**Scope:** BOUNDARY MECHANICS ONLY — `laf-adaptation/scripts/check_boundary.py` + `laf-adaptation/VENDOR.md`.
**Status:** Complete

---

## Q1. classify() for the 3 new artifacts → NATIVE (confirmed)

`classify()` is at `check_boundary.py:326-345`. For a NEW (non-upstream) file/dir, the
control flow is:
- `rel in declared` → returns the existing manifest class (line 327-328). For fresh
  artifacts not yet in VENDOR.md, this is skipped.
- `upstream_dir and upstream_has(...)` → adopted branch (329-332). New LAF artifacts are
  NOT upstream (CWS has no prep phase), so this is skipped.
- Non-upstream fallthrough (334-345):
  - `agents/prep-cordinator.md`: `parts[0] == "agents"` (line 336). `name = "prep-cordinator.md"`.
    `BUILD_NEW_AGENTS = {"chronicler.md", "tier-coordinator.md"}` (line 45) — `prep-cordinator.md`
    is NOT in it → falls to `return "NATIVE"` (line 339). **CONFIRMED NATIVE.**
  - `skills/prep/`: `parts[0] == "skills"` (line 340), `sk = "prep"`.
    `BUILD_NEW_SKILLS = {"adaptation-safety"}` (line 47) — `"prep"` not in it → `return "NATIVE"`
    (line 344). **CONFIRMED NATIVE.**
  - `skills/thematic-fidelity/`: same path, `sk = "thematic-fidelity"` not in `BUILD_NEW_SKILLS`
    → `return "NATIVE"` (line 344). **CONFIRMED NATIVE.**

**Row shape written by `do_init`:**
- Agent → one row per file (loop `do_init:378-386`); a non-adopted agent takes the `else`
  branch (385-386) → `(rel, cls, NO_HASH, NO_HASH)`. So `--init` would write exactly:
  `agents/prep-cordinator.md | NATIVE | — | —`. **CONFIRMED.**
- Skill dir → the `else` (non-adopted) branch of the skills loop (`do_init:405-407`):
  `rows.append((f"{skill_rel}/**", cls, NO_HASH, NO_HASH))`. So `--init` writes the glob rows:
  `skills/prep/** | NATIVE | — | —` and `skills/thematic-fidelity/** | NATIVE | — | —`.
  **CONFIRMED.** (`—` is `NO_HASH`, line 50.)

**Exemplars / resources need NO own rows — CONFIRMED.** For NATIVE/BUILD-NEW skills, `do_init`
emits only the single `skills/<name>/**` glob row (405-407); it does NOT enumerate per-file rows
(that per-file enumeration only happens in the `adopted` branch, 394-404). Coverage of nested
files is by prefix match in `manifest_covers` (`check_boundary.py:296-302`): `is_glob` rows
(path ends `/**`, line 178) match any `rel` that `startswith(r.path[:-2])` (line 300). Therefore:
- `skills/prep/resources/path-contract.md` is covered by `skills/prep/**`.
- Exemplars under `skills/adaptation-rules/resources/…` are covered by the EXISTING
  `skills/adaptation-rules/**` NATIVE row (VENDOR.md:113). Since `adaptation-rules` is an existing
  NATIVE glob row (not an adopted skill), any file dropped under it is glob-covered — no new row,
  no Rule F′ per-file requirement (Rule F′ targets only ADOPTED skill dirs — see Q3). This exactly
  matches DESIGN.md:272-273. **CONFIRMED — no own rows needed.**

---

## Q2. Does `--init` REQUIRE `--upstream`? → YES (hard early return)

`do_init` early return: `check_boundary.py:349-354`.
```
def do_init(upstream_dir, upstream_sha=None):
    if not upstream_dir:
        print("ERROR: --init requires --upstream <dir> ...", file=sys.stderr)
        return 2
```
`main()` wires `--init` → `do_init(args.upstream, args.upstream_sha)` (line 702). If `--upstream`
is absent (`args.upstream` defaults to `None`, line 691), `do_init` prints the ERROR and returns
exit code **2** before touching VENDOR.md. There is a second guard at 355-358 requiring a `cw/`
subtree under the checkout.

**Verdict: the 3 NATIVE rows CANNOT be produced by `--init` WITHOUT an upstream checkout.**
`--init` is the machine-generator, but it refuses to run without `--upstream`, and when it does
run it REWRITES THE ENTIRE manifest body from scratch (`_write_manifest_rows:443-457` truncates
everything after the separator row and re-emits all rows for the whole tree, not just the 3 new
ones). So even with an upstream checkout, running `--init` for these 3 rows regenerates every
adopted hash too.

**What the P0/P1 gate should run instead (no upstream tree available):** hand-add the 3 NATIVE
rows to VENDOR.md's manifest table by hand (matching the exact 4-cell format
`| path | NATIVE | — | — |`), then run plain verify (Mode V):
`uv run python laf-adaptation/scripts/check_boundary.py`. This is exactly what DESIGN.md's P1 gate
prescribes ("`check_boundary.py` (Mode V) green", DESIGN.md:313) and what the P0 gate's fallback
is when no upstream checkout exists. The DESIGN P0 gate text ("`check_boundary.py --init` writes
exactly the 3 rows", DESIGN.md:312) describes the IDEAL upstream-present path; without an upstream
tree the runnable equivalent is hand-add-3-rows + Mode V (proven in Q3). See VENDOR.md:46-49 note:
"Do not hand-edit the manifest table below — it is machine-generated" — this is the upstream-present
convention; the hand-add path is the no-upstream fallback, and it is safe for NATIVE `—/—` rows
because they carry no hashes to forge. **Unverified whether the task intends to acquire an upstream
checkout; the boundary mechanics make BOTH paths viable, but ONLY the hand-add+Mode-V path is
runnable with no upstream tree.**

---

## Q3. Mode V (no --upstream) after hand-adding the 3 NATIVE rows → PASSES (confirmed)

`verify()` is `check_boundary.py:485-655`. With NO `--upstream`, `upstream_dir is None`, so
`main()` calls `verify(None, None)` (line 705). Trace of which rules run in Mode V:

| Rule | Lines | Runs in Mode V? | Effect on the 3 new NATIVE rows |
|---|---|---|---|
| A (adopted laf_sha256 match) | 499-507 | Yes | Skips them — `if not r.is_adopted: continue` (500-501); NATIVE is not adopted. |
| A′ (ADOPTED-CLEAN re-derive) | 520-530 | Yes | Skips — `if r.cls != "ADOPTED-CLEAN": continue` (521-522). |
| C′ (ADOPTED-PATCHED reserved) | 534-536 | Yes | Skips — only fires on ADOPTED-PATCHED (535). |
| B (upstream diff) | 538-577 | **No** — inside `if upstream_dir:` (539) | Not run; the `else` at 598-601 prints the NOTE. |
| C (patched diff) | 578-597 | **No** — same `if upstream_dir:` block | Not run. |
| D (G3 quartet) | 603-608 | Yes | Independent of new rows; quartet already ADOPTED-CLEAN in VENDOR.md. |
| E (collision) | 610-626 | Yes | Takes the `else` branch (622-626) — see below. |
| F (manifest coverage) | 628-631 | Yes | Satisfied — see below. |
| F′ (adopted resources/**) | 633-647 | Yes | Does NOT touch new NATIVE skills (targets only ADOPTED skill dirs, 639-644). |

**Rule E in Mode V (the `else` branch, 622-626):** with no upstream tree, E cannot check for
upstream-name shadowing; instead it does a manifest-only best-effort collision check —
`adopted_paths = {x.path for x in rows if x.is_adopted}` and fails only if a NATIVE/BUILD-NEW
`r.path` is ALSO listed as an adopted row (624-626). `agents/prep-cordinator.md`, `skills/prep/**`,
`skills/thematic-fidelity/**` are not adopted paths → **no collision → PASS.**

**Rule F coverage (628-631):** iterates `disk_agents() + disk_skill_skillmds()`. Once the 3 rows
exist in VENDOR.md, `agents/prep-cordinator.md` matches its own exact row (`manifest_covers`
exact-match, 297-299); `skills/prep/SKILL.md` and `skills/thematic-fidelity/SKILL.md` are
glob-covered by their `/**` rows (300). So every managed file is manifested → **PASS.**
(Corollary: if the SKILL.md/agent files exist on disk but the rows are NOT hand-added, Rule F FAILS
loud with "`…: not in VENDOR.md manifest`" — so the hand-add is REQUIRED for green.)

**Parser gate (parse_manifest:220-275):** a hand-added NATIVE row must be `| path | NATIVE | — | — |`
(4 cells). The `else` branch at 270-273 requires `up == NO_HASH and laf == NO_HASH` for
NATIVE/BUILD-NEW — so both cells MUST be the em-dash `—` (or one of the accepted empties `""`,
`-`, `--`, `<hash>` which `_norm_hash` folds to NO_HASH, 181-185). A stray hash in a NATIVE row
is a loud parse error (272). Duplicate-path and 4-cell checks (236-237, 255-256) also apply.

**EXPECTED OUTCOME (exact):** After hand-adding the 3 rows and running plain
`uv run python laf-adaptation/scripts/check_boundary.py`, verify prints the Mode-V NOTE
(599-601, "Rules B and C … skipped") and, with no other violations, prints
**`BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.`** and returns exit code **0**
(654-655). **CONFIRMED: P0/P1 gates ARE runnable without the upstream tree** via hand-add + Mode V.

---

## Q4. Rule E — prep-cordinator / prep / thematic-fidelity do not collide (confirmed)

The 3 artifacts are greenfield in CWS — the upstream (creative-writing-skills) has no prep phase,
no `prep-cordinator` agent, and no `prep` or `thematic-fidelity` skill. In Mode U (`--upstream`
present, Rule E lines 614-621) the check would be:
- glob rows: `upstream_root(...).joinpath("skills", sk).exists()` for `sk ∈ {prep, thematic-fidelity}`
  → both FALSE upstream → no shadow.
- file row `agents/prep-cordinator.md`: `upstream_has(...)` → FALSE → no shadow.

In Mode V (no upstream) the `else` branch (622-626) only flags a native path also listed as adopted;
none of the 3 are. **CONFIRMED: no collision in either mode.** (Naming note: the file is spelled
`prep-cordinator` — one "o" — consistently in DESIGN.md:34,101,247 and §5:267; the classifier is
name-agnostic for NATIVE so the spelling does not affect the class, but the VENDOR row path MUST
match the on-disk filename exactly or Rule F fails.)

---

## Q5. Editing analyst.md (NATIVE) + tier-coordinator.md (BUILD-NEW) is body-edit-safe (confirmed)

VENDOR.md rows:
- `agents/analyst.md | NATIVE | — | —` (VENDOR.md:111) — carries `—`/`—`. **CONFIRMED.**
- `agents/tier-coordinator.md | BUILD-NEW | — | —` (VENDOR.md:117) — carries `—`/`—`. **CONFIRMED.**

Neither is hash-pinned. A body edit changes the file bytes but NOT the manifest row (the row has
no hash to drift). Trace: Rule A skips non-adopted (500-501); Rule A′ skips non-ADOPTED-CLEAN
(521-522); Rule C′ skips non-ADOPTED-PATCHED (535); Rule E finds no collision (they're existing
rows, and their paths aren't adopted); Rule F still matches their exact rows (row unchanged, file
still present). **CONFIRMED: editing the body of `analyst.md` or `tier-coordinator.md` does NOT
change their VENDOR row and does NOT trip any rule** — this is exactly what DESIGN.md's P1 gate
asserts ("Rules A/A′/C′/D still pass (no adopted body drift)", DESIGN.md:313). This is why the
design routes the meaning/compound_scene/Check-D additions into these two NATIVE/BUILD-NEW bodies
rather than any adopted agent.

**Contrast — hash-pinned adopted rows (any edit FAILS):**
- `agents/writer.md | ADOPTED-PATCHED | 373e605…290 | c1b3e12…534` (VENDOR.md:65) — hash-pinned.
  An on-disk edit → `sha256_text(read_text)` ≠ `laf_sha256` → Rule A fails ("modified since
  vendoring (laf_sha256 mismatch)", 506-507). ADOPTED-PATCHED is excluded from Rule A′ (517-519)
  but Rule A alone catches any writer.md edit. **CONFIRMED: editing writer.md WOULD fail Rule A.**
- `agents/muse.md | ADOPTED-CLEAN | c8819ec…9a4 | 18cafdc…8f` (VENDOR.md:60) — hash-pinned. An edit
  fails Rule A (laf_sha256 mismatch, 506-507) AND Rule A′ (prefix_unrewrite(disk) no longer hashes
  to the pinned upstream_sha256, 526-530). **CONFIRMED: editing muse.md WOULD fail Rule A/A′.**

Mechanism: hash-pinned = adopted-provenance rows (ADOPTED-CLEAN / ADOPTED-PATCHED, `is_adopted`,
172-174) carry 64-hex hashes and are integrity-checked; NATIVE/BUILD-NEW rows carry `—` and are
coverage-checked only (must exist + be manifested), never content-pinned.

---

## Q6. Dual-form promotion targets — underscore/5-key root vs hyphen kb; NOT boundary-managed

- **Root promotion target `config/concept_mapping/templates/`** — UNDERSCORE filenames with 5
  top-level keys. Verified on disk: `narnia_mapping.yaml`, `tolkien_mapping.yaml`; each has exactly
  the 5 top-level keys `work_metadata`, `characters`, `concepts`, `key_scenes`,
  `master_translation_table` (grep of `^[a-z_]+:`). **CONFIRMED underscore + 5-key.**
  (DESIGN P3 gate calls this "root 5-key", DESIGN.md:315.)
- **kb promotion target `laf-adaptation/kb/adaptation-mapping/`** — HYPHEN filenames. Verified on
  disk: `tolkien-mapping.yaml`, `universal-mappings.yaml`. **CONFIRMED hyphen.** (DESIGN P3 gate
  calls this the "kb 6-key" form, DESIGN.md:315 — the extra `meaning:` key per R10, DESIGN.md:253.)

**check_boundary does NOT manage either dir — CONFIRMED.** The checker only ever globs under
`agents/` and `skills/`:
- `disk_agents()` → `REPO/"agents"` (308); `disk_skill_dirs/files/skillmds()` → `REPO/"skills"`
  (312-322). REPO is `laf-adaptation/` (line 31).
- `config/concept_mapping/templates/` is OUTSIDE `laf-adaptation/` entirely (repo-root `config/`),
  so it is unreachable by any rule.
- `laf-adaptation/kb/adaptation-mapping/` is under `laf-adaptation/` but under `kb/`, NOT `agents/`
  or `skills/`, so no discovery function touches it and no manifest row references it.
This matches laf-adaptation/CLAUDE.md §1, which classifies `kb/adaptation-mapping/` as NATIVE
carried-verbatim "outside the Rule-F hash-pin glob". **CONFIRMED: dual-form promotion is invisible
to the boundary check — it neither helps nor hurts the green gate.**

---

## Status: Complete

**3-line summary:**
1. All 3 new artifacts (`agents/prep-cordinator.md`, `skills/prep/**`, `skills/thematic-fidelity/**`)
   classify() to **NATIVE** and `do_init` writes them as `… | NATIVE | — | —` (glob rows for the two
   skills); nested exemplars/`path-contract.md` need NO own rows (glob-covered).
2. **Mode-V-without-upstream verdict: PASSES.** `--init` HARD-REQUIRES `--upstream` (early return 2,
   349-354), but you do NOT need it — hand-add the 3 `—/—` rows to VENDOR.md then run plain
   `uv run python laf-adaptation/scripts/check_boundary.py`; Rule F coverage is satisfied by the exact
   + glob rows, Rule E's no-upstream `else` branch (622-626) finds no adopted-path collision, and
   B/C are skipped → **`BOUNDARY CONTRACT: PASS`, exit 0.** P0/P1 gates ARE runnable with no upstream tree.
3. Body-editing `analyst.md` (NATIVE) and `tier-coordinator.md` (BUILD-NEW) is safe — their `—/—`
   rows are not hash-pinned, so no rule trips; whereas any edit to `writer.md` (ADOPTED-PATCHED) or
   `muse.md` (ADOPTED-CLEAN) WOULD fail Rule A/A′. `check_boundary` does NOT manage the dual-form
   promotion dirs (root underscore/5-key `config/concept_mapping/templates/`, kb hyphen
   `laf-adaptation/kb/adaptation-mapping/`) — both are outside the agents/+skills/ glob.

---
