# Research 06 — Verification & Proof Flow (Test/Verification/Data-flow)

**Topic:** Exact runnable commands per phase gate + P3 end-to-end proof feasibility.
**Track goal:** MDTM task to implement LAF adaptation-prep phase per `docs/native-prep/design/DESIGN.md`; `boundary-verification.md §5` defines the verification checklist.
**Scope:** RUNNABLE verify commands + current baselines (BEFORE any change) + P3 source feasibility.
**Method:** Every command below was actually executed; outputs pasted verbatim. Unrun items marked "Unverified."

---

## Path preflight (all gate files exist)

```
laf-adaptation/scripts/check_boundary.py          33298 B  present
laf-adaptation/agents/writer.md                    1541 B  present
laf-adaptation/agents/muse.md                      2595 B  present
config/concept_mapping/templates/tolkien_mapping.yaml  2930 B  present
docs/native-prep/design/DESIGN.md                 27557 B  present
docs/guides/ADDING_NEW_WORKS.md                    6022 B  present
```

---

## GATE 1 — Boundary check (Mode V) — RUN, baseline BEFORE any change

**Command:**
```bash
uv run python laf-adaptation/scripts/check_boundary.py
```
**Actual output (verbatim, exit 0):**
```
NOTE: verify running without --upstream — Rules B and C (upstream-diff checks) skipped; Rule A hash-match covers adopted-file integrity against the recorded manifest, plus Rules D/E/F.
BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.
```
**Baseline verdict: PASS.** Note the expected final line in the task brief is `"BOUNDARY CONTRACT: PASS"`; actual final line is `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` (same PASS token, longer suffix). A gate assertion should match the prefix `BOUNDARY CONTRACT: PASS`, not the full string.

**Caveat (coordinate with R3, who owns --init / Mode-V internals):** run WITHOUT `--upstream`, the tool prints a NOTE that Rules B and C (upstream-diff checks) are **skipped**; Rule A hash-match still covers adopted-file integrity, plus D/E/F. So the plain `check_boundary.py` verify command is a valid PASS/FAIL gate for adopted-body drift + native/collision rules, but it is NOT the full upstream-diff audit. R3 owns whether P0/P1/P3 gates need `--upstream <path>`.

---

## GATE 1b — Boundary provenance report — RUN, measurable delta baseline

**Command:**
```bash
uv run python laf-adaptation/scripts/check_boundary.py --report
```
**Actual provenance summary counts (verbatim, exit 0):**
```
laf-adaptation/ provenance summary (from VENDOR.md)
====================================================
  ADOPTED-CLEAN    55
  ADOPTED-PATCHED  1
  NATIVE           5
  BUILD-NEW        3
  TOTAL rows       64
```
**Current NATIVE rows (5):** `agents/analyst.md`, `agents/safety-verifier.md`, `skills/adaptation-rules/**`, `skills/adaptation-tiers/**`, `skills/source-fidelity/**`.
**Current BUILD-NEW rows (3):** `agents/chronicler.md`, `agents/tier-coordinator.md`, `skills/adaptation-safety/**`.

**Delta baseline for the "+3 NATIVE rows" claim:** NATIVE is currently **5**. DESIGN.md §5 P0 gate expects `check_boundary.py --init` to write "exactly the 3 rows in §5" — those 3 new prep rows are ON TOP of the current 5, so after P0 the report should show **NATIVE = 8** (5 + 3) and TOTAL rows = 67, IF the 3 prep rows are provenance-classed NATIVE. (Exact class of the 3 P0 rows = R3/R5 to confirm from §5; recorded here only as the measurable pre-change baseline: 5 NATIVE / 64 total.)

---

## GATE 2 — Unchanged-file proof (writer.md + muse.md byte-identical) — RUN

**Command:**
```bash
git diff --stat -- laf-adaptation/agents/writer.md laf-adaptation/agents/muse.md
```
**Actual output:** *(empty — no lines, exit 0)*
```

```
**Verdict: PASS (byte-identical / no working-tree change).** Empty `git diff --stat` output is the pass condition. This gate proves the two adopted agents are untouched.

**Caveat on interpretation:** `git diff` (no `--cached`, no ref) compares working tree vs HEAD. It proves "unchanged since last commit," which is the right gate DURING implementation. If a stronger "byte-identical to upstream-adopted hash" proof is wanted, that is Rule A inside `check_boundary.py` (already GREEN in Gate 1), not `git diff`. Note `writer.md` is provenance ADOPTED-PATCHED (Gate 1b), so it is intentionally NOT byte-identical to raw upstream — it is byte-identical to its recorded patched-adopted hash. `muse.md` is ADOPTED-CLEAN. The task's own instruction targets both, and both must stay unchanged by the prep work; `git diff --stat` empty is the correct in-flight proof.

---

## GATE 3 — Root 5-key validation (tolkien_mapping.yaml) — RUN

**Command (per ADDING_NEW_WORKS.md Step 6, retargeted to the shipped tolkien template):**
```bash
uv run --with pyyaml python -c "import yaml; d=yaml.safe_load(open('config/concept_mapping/templates/tolkien_mapping.yaml')); print(sorted(d))"
```
**Actual output (verbatim, exit 0):**
```
['characters', 'concepts', 'key_scenes', 'master_translation_table', 'work_metadata']
```
**Verdict: PASS — exactly the 5 expected keys.** `docs/guides/ADDING_NEW_WORKS.md:110-111` documents this identical command (against `narnia_mapping.yaml`) with the identical expected output:
```
# → ['characters', 'concepts', 'key_scenes', 'master_translation_table', 'work_metadata']
```
So the root/schema 5-key contract is: `characters, concepts, key_scenes, master_translation_table, work_metadata`. tolkien currently satisfies it exactly.

---

## P3 END-TO-END PROOF FEASIBILITY — source inventory + verdict

**Command:**
```bash
ls -laR laf-adaptation/source/
```
**Actual tree (verbatim):**
```
laf-adaptation/source/:
  README.md
  tolkien/

laf-adaptation/source/tolkien:
  ch-01.txt        (1362 B, 259 words)
```

**Readable source present: YES.** `laf-adaptation/source/tolkien/ch-01.txt` — 259 words, opens `"The Siege at the Grey City"`; contains Sauron, Denethor, Théoden, Éowyn, Nazgûl (Tolkien-adjacent high-fantasy register). It is a real readable chapter text, usable as the work-level `source_path` input. DESIGN.md §2/§6 forbids MEMORY-BASED at work granularity (`20-analysis-work-level.yaml` "MEMORY-BASED not acceptable", DESIGN.md:223) — this file satisfies the "readable text" requirement so P3 does NOT have to fall back to memory.

**CRITICAL PROVISIONING NOTE (from `laf-adaptation/source/README.md`):** `ch-01.txt` is an **ORIGINAL SYNTHETIC proof fixture** (PATH-B), NOT Tolkien's copyrighted prose — deliberately authored in a Tolkien-adjacent register so it aligns with the committed `kb/adaptation-mapping/tolkien-mapping.yaml` and exercises every transform class (violence→cooperation, agency externalization, death handling, martial→prosocial heroism, nightmare framing). For a real adaptation run, PATH-A (operator supplies a real chapter under their own rights, not committed) replaces it.

**⚠ WORK MISMATCH — P3 example vs available source (flag for task author):**
- DESIGN.md §7 **P3 gate (line 315)** names **Narnia**: `Run /laf:prep "The Lion, the Witch and the Wardrobe"` … `/laf:rewrite --work narnia`.
- The repo ships **NO Narnia source** and **NO narnia_mapping**. Confirmed:
  - `laf-adaptation/source/` contains only `tolkien/` (no narnia dir).
  - `find laf-adaptation -iname '*narnia*'` → **no results**.
  - `laf-adaptation/kb/adaptation-mapping/` contains only `tolkien-mapping.yaml` + `universal-mappings.yaml`.
  - `config/concept_mapping/templates/` — only `tolkien_mapping.yaml` present for a named work (narnia is the DOC EXAMPLE in ADDING_NEW_WORKS.md, not a shipped file).

**P3 feasibility verdict:**
- **As literally written (Narnia): NOT runnable today** — no Narnia readable source and no narnia mapping exist. P3-on-Narnia would require the operator to first provision `source/narnia/ch-01.txt` AND a `narnia` work-mapping (i.e., run the whole ADDING_NEW_WORKS flow for Narnia first).
- **P3 IS runnable today on Tolkien instead:** `/laf:prep "<Tolkien work>"` with `source = laf-adaptation/source/tolkien/ch-01.txt` (PATH-B synthetic fixture) + the committed `tolkien-mapping.yaml`. This is the path the shipped tree is provisioned for (source/README.md §"Provisioning contract (Phase-3 proof)").
- **Recommendation for the MDTM task:** the P3 gate step should either (a) substitute Tolkien for Narnia (matching the shipped fixture), or (b) explicitly require the operator to provision a Narnia source + mapping as a P3 pre-step. Flag this Narnia/Tolkien inconsistency between DESIGN.md P3 and the shipped source tree so it is resolved when the task is authored. (Design↔code cross-validation depth = R5; recorded here only because it directly gates P3 runnability.)

---

## §5 boundary-verification checklist — RUNNABLE verify commands (summary table)

| Gate | Runnable command | Pass condition | Baseline NOW |
|---|---|---|---|
| Boundary Mode V | `uv run python laf-adaptation/scripts/check_boundary.py` | final line begins `BOUNDARY CONTRACT: PASS` | **PASS** ✓ |
| Provenance report | `uv run python laf-adaptation/scripts/check_boundary.py --report` | prints summary; NATIVE count measurable | NATIVE=5, TOTAL=64 |
| Unchanged adopted agents | `git diff --stat -- laf-adaptation/agents/writer.md laf-adaptation/agents/muse.md` | empty output | **PASS** ✓ (empty) |
| Root 5-key schema | `uv run --with pyyaml python -c "import yaml; d=yaml.safe_load(open('config/concept_mapping/templates/tolkien_mapping.yaml')); print(sorted(d))"` | `['characters','concepts','key_scenes','master_translation_table','work_metadata']` | **PASS** ✓ (exact) |
| P0 init (R3 owns) | `check_boundary.py --init` (needs `--upstream`; see caveat) | writes exactly the 3 §5 rows | Unverified — R3 scope |
| P3 hard gate | `/laf:prep "<work>"` end-to-end, source=readable text, then `check_boundary.py` green | 8-file package; 20 has meaning+compound_scene; 30 min(text,context); dual-form (root 5-key + kb 6-key); rewrite reads by hardcoded path; boundary green | Runnable on **Tolkien** fixture; **NOT** on Narnia (no source/mapping) |

**Caveat carried for the `--init` gate (R3 owns deep analysis):** the P0 gate uses `check_boundary.py --init`. `--init` records/writes provenance rows and (per DESIGN.md §7 P0) is expected to pair with upstream context; the plain verify caveat above (Rules B/C skipped without `--upstream`) means an `--init` gate likely needs `--upstream <path>` to be meaningful. I only recorded the RUNNABLE **verify** command + its current PASS baseline; the `--init`/`--upstream` mechanics are R3's deep-dive.

**Dual-form promotion note (P3 gate detail, for cross-check):** P3 expects "dual-form promotion (root 5-key, kb 6-key)". Root 5-key is validated by Gate 3 above (confirmed = 5 keys). The **kb 6-key** form is the `kb/adaptation-mapping/*-mapping.yaml` shape (`kb/adaptation-mapping/tolkien-mapping.yaml` exists, 2930 B) — its 6-key validation command was NOT run here (out of my scope column; R1/R5 own the kb-mapping schema). Recorded so the task author knows P3 needs BOTH a root-5-key check AND a kb-6-key check.

---

## Status: Complete

**Summary of what was RUN (all exit 0):**
1. `check_boundary.py` → **BOUNDARY CONTRACT: PASS** (baseline, before any change). Caveat: without `--upstream`, Rules B/C skipped.
2. `check_boundary.py --report` → NATIVE=5, ADOPTED-CLEAN=55, ADOPTED-PATCHED=1, BUILD-NEW=3, TOTAL=64 (delta baseline for "+3 NATIVE").
3. `git diff --stat -- writer.md muse.md` → **empty = PASS** (adopted agents byte-unchanged vs HEAD).
4. `uv run --with pyyaml … tolkien_mapping.yaml` → exactly the 5 keys → **PASS**; matches ADDING_NEW_WORKS.md:110-111 expected.
5. `ls -laR laf-adaptation/source/` → only `tolkien/ch-01.txt` (259w, PATH-B SYNTHETIC fixture, NOT copyrighted Tolkien prose).

**Key flags for the task author:**
- P3 is runnable end-to-end **on the Tolkien synthetic fixture** today (readable source + committed tolkien mapping both present).
- P3 as literally written in DESIGN.md (**Narnia**) is **NOT runnable** — no Narnia source and no narnia mapping exist in the repo. Resolve the Narnia/Tolkien mismatch (substitute Tolkien, or add a "provision Narnia source+mapping" pre-step).
- The boundary verify command's final line is `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` (assert on prefix, not exact string).
