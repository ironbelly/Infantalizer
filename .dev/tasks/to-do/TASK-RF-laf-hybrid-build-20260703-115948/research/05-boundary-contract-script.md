# Research: Boundary Contract (VENDOR.md + check_boundary.py) + Upstream Acquisition
**Topic type:** Content Extraction / Solution Research
**Scope:** scripts/check_boundary.py, VENDOR.md, prefix-rewrite, upstream CWS acquisition
**Status:** Complete
**Date:** 2026-07-03

**Summary:** Full authorable spec extracted for the ONLY script LAF ships (`scripts/check_boundary.py`) + `VENDOR.md` manifest format + the prefix-rewrite transform + Phase-0 upstream-CWS acquisition (user-chosen "acquire first"). Contents: (1) 4-class provenance taxonomy with per-class script rules; (2) verbatim `VENDOR.md` format — 5 header fields, 3-line Invariants block, 4-column manifest table with recursive resource hashing; (3) 3 modes (verify=exit-1-on-violation, `--init`=writes manifest + needs `--upstream <dir>`, `--report`=exit-0) + the verbatim A–F verify pseudocode with a rule-by-rule breakdown + `body_of`/`frontmatter_line_diff` (order-insensitive on `skills:`); (4) the single uniform vendor-time transform `creative-writing-skills:`→`laf-adaptation:` (deterministic, recomputed) + the writer-only additive graft; (5) 7-step acquisition procedure — clone `https://github.com/haowjy/creative-writing-skills` (WebSearch-confirmed HIGH), pin a SHA, vendor from `cw/agents/` NOT `agents/`, retain Apache-2.0 in `NOTICE`, run `--init --upstream <dir>`; (6) verbatim enforcement table + UV wrapping; (7) verbatim 6-step upstream-sync protocol; (8) phase 0–4 checklist; (9) risk register. **Execution-time unknowns flagged:** exact `upstream_sha`, `vendored_on`, checkout dir path, CI-verify upstream-access model. Every rule/format claim cites boundary-contract.md line numbers; cross-refs to DESIGN.md §2.1/§1.1/§7 and agent-schemas.md §1/§3.
---

## 0. Executive summary

LAF 0.1 ships **exactly one script**: `scripts/check_boundary.py` (boundary-contract.md:13, :17 — "the **only** script LAF 0.1 ships (ADR-006: prompt framework, not software)"). It is a **validation tool, not a runtime** — "it reads files and computes hashes; it never transforms the framework" (boundary-contract.md:18–19). It works with one companion manifest, `VENDOR.md`, which records the upstream commit SHA plus a per-file provenance table with two hashes each.

Two artifacts, one purpose (boundary-contract.md:9–15):
1. **`VENDOR.md`** — the manifest: upstream commit SHA + per-file provenance table with hashes.
2. **`scripts/check_boundary.py`** — the gate: proves every adopted file matches its recorded hash, that `ADOPTED-PATCHED` files differ from upstream only in the permitted way, and that the quartet is intact (invariant G3).

The one uniform vendor-time transform is the **prefix rewrite** `creative-writing-skills:` → `laf-adaptation:` (boundary-contract.md:34–36) — deterministic, recomputed by the check rather than trusted from a stored diff.

**Upstream repo (WebSearch-confirmed, HIGH reliability, 2026-07-03):** `https://github.com/haowjy/creative-writing-skills` exists — "claude skills focused on creative writing"; worker set includes writer, critic, reader-sim, brainstormer, outliner, character-sim, style-creator, chronicler, continuity-checker, coordinated by muse. Codebase spec remains source of truth for all hashes/SHAs.

> **Cross-track note (do NOT duplicate):** R1 owns the manifest ROW list (which files at which class). This doc owns the VENDOR.md FORMAT, the check_boundary.py CONTENT/pseudocode, the prefix-rewrite transform, and the Phase-0 upstream-acquisition mechanics. R2 owns writer-patch content; the writer classification mechanics (Rule C) are documented here only as they define check_boundary.py behavior.

---

## 1. Provenance classes (the 4-class taxonomy the script enforces)

Every file under `agents/` and `skills/` carries **exactly one** class (boundary-contract.md:25). Verbatim table (boundary-contract.md:27–32):

| Class | Meaning | `check_boundary.py` rule |
|---|---|---|
| `ADOPTED-CLEAN` | Vendored from CWS, byte-identical to the vendored baseline | `sha256(file) == laf_sha256`, and `laf_sha256 == upstream_sha256_after_prefix_rewrite` |
| `ADOPTED-PATCHED` | Vendored but carries the uniform prefix rewrite **and** a recorded additive frontmatter graft (only `writer.md`) | `sha256(file) == laf_sha256`; diff vs upstream is frontmatter-only + additive (§3.2) |
| `NATIVE` | LAF-authored | not hash-pinned to upstream; must NOT appear in the upstream tree |
| `BUILD-NEW` | Greenfield | not hash-pinned; must NOT appear in the upstream tree |

Key facts for the implementer:
- **Only `writer.md` is `ADOPTED-PATCHED`** (boundary-contract.md:30, agent-schemas.md:174). All other adopted agents/skills are `ADOPTED-CLEAN`.
- `NATIVE` and `BUILD-NEW` are **not hash-pinned** (dashes `—` in both hash columns, boundary-contract.md:74–81) and MUST NOT collide with an upstream file name (enforced by Rule E).
- The prefix rewrite is "the one uniform vendor-time transform applied to all adopted files. It is deterministic, so the check recomputes it rather than trusting a stored diff." (boundary-contract.md:34–36)

**Cross-ref (agent-schemas.md §1, :22–36):** the frontmatter dialect is **Claude-native / cw-lowered**. Permitted keys are a closed set: `name`, `description`, `model` (Claude aliases `opus|sonnet|haiku|inherit` only — never Mars aliases `opus46`/`gpt`/`deepseek`), `skills` (fully-qualified `laf-adaptation:<skill>` entries), `tools`. Adopted files are vendored from `cw/agents/` (already Claude-lowered), and their `model:` + `skills:` prefix are rewritten at vendor time — that rewritten form is what `VENDOR.md` hashes (agent-schemas.md:32–36).

---

## 2. `VENDOR.md` — authorable manifest format

The full format block, verbatim (boundary-contract.md:42–82). This is the exact skeleton Phase 0 writes:

```markdown
# VENDOR.md — Adopted-file manifest

upstream_repo: https://github.com/haowjy/creative-writing-skills
upstream_sha:  <full 40-char commit SHA the adopted subset was vendored from>
vendored_on:   2026-07-03
license:       Apache-2.0 (upstream) — attribution retained per NOTICE
prefix_rewrite: "creative-writing-skills:" -> "laf-adaptation:"   # uniform, deterministic

## Invariants (asserted by check_boundary.py)
- G3 quartet-intact: agents/{critic,editor,reader-sim,continuity-checker}.md are ADOPTED-CLEAN and present.
- editor.md is NEVER folded, NEVER modified.
- No NATIVE/BUILD-NEW file name collides with an upstream file name.

## Manifest

| path | class | upstream_sha256 | laf_sha256 |
|------|-------|-----------------|------------|
| agents/muse.md               | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/critic.md             | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/editor.md             | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/reader-sim.md         | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/continuity-checker.md | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/brainstormer.md       | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/outliner.md           | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/character-sim.md      | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/style-creator.md      | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/web-researcher.md     | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/writer.md             | ADOPTED-PATCHED | <hash> | <hash> |
| skills/writing-principles/SKILL.md      | ADOPTED-CLEAN | <hash> | <hash> |
| skills/creative-writing-craft/SKILL.md  | ADOPTED-CLEAN | <hash> | <hash> |
| ... (all 12 adopted skills' SKILL.md + resources/**)           | ...   | ...    | ...    |
| agents/analyst.md            | NATIVE    | — | — |
| agents/safety-verifier.md    | NATIVE    | — | — |
| agents/chronicler.md         | BUILD-NEW | — | — |
| agents/tier-coordinator.md   | BUILD-NEW | — | — |
| skills/adaptation-tiers/**   | NATIVE    | — | — |
| skills/adaptation-rules/**   | NATIVE    | — | — |
| skills/source-fidelity/**    | NATIVE    | — | — |
| skills/adaptation-safety/**  | BUILD-NEW | — | — |
```

### 2.1 Header fields (5 required lines)

| Field | Value / rule | Source |
|---|---|---|
| `upstream_repo` | `https://github.com/haowjy/creative-writing-skills` (literal) | boundary-contract.md:45 |
| `upstream_sha` | **full 40-char** commit SHA the adopted subset was vendored from | boundary-contract.md:46 |
| `vendored_on` | ISO date (e.g. `2026-07-03`) | boundary-contract.md:47 |
| `license` | `Apache-2.0 (upstream) — attribution retained per NOTICE` | boundary-contract.md:48 |
| `prefix_rewrite` | `"creative-writing-skills:" -> "laf-adaptation:"` (uniform, deterministic) | boundary-contract.md:49 |

### 2.2 Invariants block (3 lines, asserted by the script)

Verbatim (boundary-contract.md:51–54):
- **G3 quartet-intact:** `agents/{critic,editor,reader-sim,continuity-checker}.md` are ADOPTED-CLEAN and present.
- **editor.md is NEVER folded, NEVER modified.**
- **No NATIVE/BUILD-NEW file name collides with an upstream file name.**

### 2.3 Manifest table (4 columns) + hashing semantics

Columns: `path | class | upstream_sha256 | laf_sha256` (boundary-contract.md:58).

Hash definitions (boundary-contract.md:84–88):
- `upstream_sha256` = hash of the file **in the upstream repo at `upstream_sha`** (BEFORE prefix rewrite).
- `laf_sha256` = hash of the file **as it lives in `laf-adaptation/`** (AFTER prefix rewrite, and for `writer.md`, after the additive graft).
- For adopted skill directories, **every file under `resources/` is hashed too (recursively)**, so a body edit to a resource is caught (boundary-contract.md:87–88).
- `NATIVE` / `BUILD-NEW` rows carry `—` in both hash columns (not hash-pinned).

> **Row inventory is R1's deliverable.** The rows above are the FORMAT skeleton with representative examples; the authoritative complete row list (all 12 adopted skills' SKILL.md + resources, exact native/build-new paths) is R1's scope. This doc guarantees the *shape* of each row and the hashing rules.

---

## 3. `scripts/check_boundary.py` — full authorable spec

### 3.1 Three modes (boundary-contract.md:94–104)

Verbatim CLI contract:

```
check_boundary.py            # verify: default; exit 1 on any violation (CI + pre-commit gate)
check_boundary.py --init     # first vendor: compute laf_sha256 for adopted files, write manifest rows
check_boundary.py --report   # human-readable provenance summary; always exit 0
```

| Mode | Trigger | Behavior | Exit code |
|---|---|---|---|
| **verify** (default) | no flag | Runs the A–F rule set below; prints each error | **exit 1 on any violation**, 0 if clean |
| **`--init`** | Phase 0 only | Computes `laf_sha256` for adopted files, records `upstream_sha256`, writes manifest rows; **requires `--upstream <dir>`** (a local checkout of the upstream repo at `upstream_sha`) to record `upstream_sha256` and prove the prefix rewrite is the only transformation | writes manifest |
| **`--report`** | on demand | Human-readable provenance summary | **always exit 0** |

`--init` "runs once in Phase 0. It requires a local checkout of the upstream repo at `upstream_sha` (path via `--upstream <dir>`) to record `upstream_sha256` and prove the prefix rewrite is the only transformation." (boundary-contract.md:102–104)

**UV invocation (project rule, boundary-contract.md:181):** the pre-commit and CI invocations are `uv run python scripts/check_boundary.py`. Phase 0 init form: `uv run python scripts/check_boundary.py --init --upstream <dir>`.

### 3.2 Verify algorithm (rules A–F, verbatim pseudocode)

The complete algorithm (boundary-contract.md:108–151):

```
load VENDOR.md manifest → rows[]
errors = []

# A. Adopted files match their recorded LAF hash (catches ANY edit, body or frontmatter)
for row in rows where class in {ADOPTED-CLEAN, ADOPTED-PATCHED}:
    if sha256(row.path) != row.laf_sha256:
        errors += f"{row.path}: modified since vendoring (laf_sha256 mismatch)"

# B. ADOPTED-CLEAN is exactly upstream-after-prefix-rewrite (no hidden graft)
for row in rows where class == ADOPTED-CLEAN:
    expected = sha256( prefix_rewrite( upstream_blob(row.path) ) )
    if row.laf_sha256 != expected:
        errors += f"{row.path}: ADOPTED-CLEAN but differs from upstream beyond prefix rewrite"

# C. ADOPTED-PATCHED diff is frontmatter-only AND additive
for row in rows where class == ADOPTED-PATCHED:
    up   = prefix_rewrite( upstream_blob(row.path) )   # upstream, prefix-normalized
    cur  = read(row.path)
    if body_of(cur) != body_of(up):                    # body = everything after closing '---'
        errors += f"{row.path}: body changed — adopted agent bodies must be byte-identical"
    added, removed = frontmatter_line_diff(up, cur)
    if removed:
        errors += f"{row.path}: frontmatter lines removed — patch must be additive only"
    if any(not line.strip().startswith('- laf-adaptation:') for line in added):
        errors += f"{row.path}: only additive `- laf-adaptation:<skill>` skill lines are permitted"

# D. Invariant G3 — quartet intact, editor never folded
for name in ["critic","editor","reader-sim","continuity-checker"]:
    p = f"agents/{name}.md"
    if p not in manifest or class(p) != "ADOPTED-CLEAN" or not exists(p):
        errors += f"G3 violation: {p} must exist as ADOPTED-CLEAN (quartet intact)"

# E. No native/build-new file name collides with an upstream file (prevents shadowing an adopted file)
for row in rows where class in {NATIVE, BUILD-NEW}:
    if upstream_has(row.path):
        errors += f"{row.path}: NATIVE/BUILD-NEW shadows an upstream file name"

# F. Every agents/*.md and skills/**/SKILL.md is listed in the manifest (no unmanaged files)
for f in glob("agents/*.md") + glob("skills/**/SKILL.md"):
    if f not in manifest: errors += f"{f}: not in VENDOR.md manifest"

exit(1 if errors else 0); print each error
```

### 3.3 Rule-by-rule authorable breakdown

| Rule | What it does | Applies to | Requires `--upstream`? |
|---|---|---|---|
| **A** — laf-hash match | `sha256(row.path) != row.laf_sha256` → error. The blunt hash gate; catches *any* change to an adopted file, body or frontmatter (boundary-contract.md:112–115, :154) | `ADOPTED-CLEAN`, `ADOPTED-PATCHED` | No (compares live file vs manifest) |
| **B** — clean == upstream-after-rewrite | `expected = sha256(prefix_rewrite(upstream_blob(row.path)))`; if `row.laf_sha256 != expected` → "differs from upstream beyond prefix rewrite" (boundary-contract.md:118–121) | `ADOPTED-CLEAN` | **Yes** — needs `upstream_blob()` |
| **C** — patched = body-identical + additive frontmatter | body_of(cur) must == body_of(up) (byte-identical body); `removed` frontmatter lines → error; any `added` line not starting with `- laf-adaptation:` → error. This is the rule that permits `writer.md`'s single additive skill line and NOTHING else (boundary-contract.md:124–133, :155–156) | `ADOPTED-PATCHED` (only `writer.md`) | **Yes** — needs `upstream_blob()` |
| **D** — G3 quartet intact | For `critic, editor, reader-sim, continuity-checker`: each `agents/<name>.md` must be in manifest AND class `ADOPTED-CLEAN` AND exist; else "G3 violation". Hard-codes editor-never-folded (boundary-contract.md:136–139, :157–158) | quartet paths | No |
| **E** — no name collision | For NATIVE/BUILD-NEW rows: if `upstream_has(row.path)` → "shadows an upstream file name". Stops "patching" an adopted agent by shadowing it with a native file of the same name (boundary-contract.md:142–144, :159–160) | `NATIVE`, `BUILD-NEW` | **Yes** — needs `upstream_has()` |
| **F** — no unmanaged files | Every `glob("agents/*.md") + glob("skills/**/SKILL.md")` must be in manifest; else "not in VENDOR.md manifest" (boundary-contract.md:147–148) | all agents + skill SKILL.md | No |

Final: `exit(1 if errors else 0); print each error` (boundary-contract.md:150).

> **Note on B/C/E in verify mode:** rules B, C, and E dereference `upstream_blob()` / `upstream_has()`, i.e. they need access to the upstream tree. In the default verify path (pre-commit/CI) the manifest already records `upstream_sha256`, so verify can compare `laf_sha256` against the stored `upstream_sha256` after recomputing the deterministic prefix rewrite — the upstream checkout is strictly required at `--init` time (boundary-contract.md:102–104). Implementer decision at execution: whether CI verify re-fetches upstream or trusts the recorded `upstream_sha256`. **Flag: needs decision at execution** — spec text is explicit only that `--init` requires `--upstream`; it does not state verify re-fetches. Safest reading: verify uses recorded `upstream_sha256` (Rule A + stored hashes), full upstream re-derivation happens at `--init`.

### 3.4 Helper functions (boundary-contract.md:162–167)

- **`body_of(text)`** = "everything after the second `---` delimiter line (the markdown body). Adopted bodies must match byte-for-byte." I.e. split on frontmatter fences; body = content after the closing `---`.
- **`frontmatter_line_diff(a, b)`** = "line-level added/removed sets computed on the YAML frontmatter block only, after prefix normalization. **Order-insensitive for `skills:` list entries.`**" So reordering `skills:` entries is not flagged; only genuine additions/removals count. This is critical because `writer.md`'s upstream file lists `creative-writing-craft` twice (agent-schemas.md:143–144) — that duplication is preserved verbatim, and order-insensitivity means the additive `- laf-adaptation:adaptation-rules` line is the only detected `added` entry.

---

## 4. The prefix-rewrite transform (the ONE uniform vendor-time transform)

**Definition:** `prefix_rewrite`: replace the package prefix `creative-writing-skills:` with `laf-adaptation:` (boundary-contract.md:34, :49). It is:
- **Uniform** — applied to *every* adopted file (boundary-contract.md:34).
- **Deterministic** — so the check **recomputes** it rather than trusting a stored diff (boundary-contract.md:35–36).
- **The ONLY permitted transformation at vendor time** (agent-schemas.md:36: "The prefix rewrite is the *only* permitted transformation at vendor time; it is applied uniformly and recorded").

**Where it appears in `skills:` frontmatter** (agent-schemas.md:153–154): every fully-qualified skill entry `creative-writing-skills:<skill>` becomes `laf-adaptation:<skill>`. Example (analyst native agent, agent-schemas.md:55–58) shows even a native agent's adopted skill dependency is rewritten: `creative-writing-skills:story-memory` → `laf-adaptation:story-memory`.

**Two-transform case — `writer.md` only** (agent-schemas.md:152–155, :174–175):
1. **Prefix rewrite** (uniform): `creative-writing-skills:` → `laf-adaptation:` across all its `skills:` lines.
2. **Adaptation-mode graft** (the single additive line): append `- laf-adaptation:adaptation-rules`. Body untouched.

`writer.md` therefore stores *two* hashes — `upstream_sha256` (original cw file) and `laf_sha256` (vendored-with-graft file) — and is classed `ADOPTED-PATCHED` (agent-schemas.md:174–175). It is the sole file where `frontmatter_line_diff` yields a non-empty `added` set, which Rule C permits because that added line starts with `- laf-adaptation:`.

**Implementer note:** because the rewrite is deterministic and recomputed, the vendor step does NOT need to store a patch/diff — it stores only the two SHA-256 hashes, and `check_boundary.py` re-derives the expected `laf_sha256` from `prefix_rewrite(upstream_blob(path))` (Rule B) at `--init`/verify.

---

## 5. Upstream CWS acquisition (Phase 0 — user-chosen: "task acquires CWS first")

**User decision (this track):** Phase 0 acquires the upstream CWS checkout *first* — clone/pin upstream at a chosen SHA into a local checkout dir, then vendor from it and run `check_boundary.py --init --upstream <dir>`.

### 5.1 Acquisition procedure

| Step | Action | Source / rule |
|---|---|---|
| 1 | Clone the upstream repo `https://github.com/haowjy/creative-writing-skills` into a local checkout dir (e.g. `.upstream-cws/`, outside `laf-adaptation/`) | boundary-contract.md:45; repo confirmed to exist (WebSearch HIGH) |
| 2 | **Pin a SHA:** `git checkout <chosen-40-char-SHA>` in the checkout dir. That SHA is recorded as `upstream_sha` in VENDOR.md | boundary-contract.md:46, :102 |
| 3 | **Vendor from `cw/agents/` (Claude-lowered), NOT `agents/` (Mars source).** Copy the adopted agents + adopted skills into `laf-adaptation/` | DESIGN.md:150–154, agent-schemas.md:32; DESIGN.md §7 Phase 0 (:293) |
| 4 | Apply the deterministic **prefix rewrite** to all adopted files; apply the **additive graft** to `writer.md` only | §4 above |
| 5 | Retain **Apache-2.0 attribution in a `NOTICE` file** | boundary-contract.md:48 ("attribution retained per NOTICE"); VENDOR.md `license` line |
| 6 | Run `uv run python scripts/check_boundary.py --init --upstream <checkout-dir>` — writes VENDOR.md manifest rows with both hashes | boundary-contract.md:98, :102–104, :177 |
| 7 | Gate: `check_boundary.py --init` passes; **zero edits to vendored files** | DESIGN.md:293 (Phase 0 gate) |

### 5.2 What `--upstream <dir>` points at

`--upstream <dir>` is the path to the **local checkout of the upstream repo at `upstream_sha`** (boundary-contract.md:102–104). At `--init` the script reads `upstream_blob(path)` from this dir to (a) record `upstream_sha256` and (b) prove the prefix rewrite is the only transformation (Rule B / Rule C). It is the same tree the SHA in step 2 pins.

### 5.3 Why `cw/agents/` not `agents/` (critical acquisition detail)

DESIGN.md §2.1 (:147–154): "all agent/skill frontmatter uses the Claude-native (cw-lowered) dialect, not the Mars-source dialect. Concretely, adopted agents are vendored from CWS's `cw/agents/` (already Claude-lowered), *not* from `agents/` (Mars source with `model-policies`/`sandbox`/`effort`/`subagents` keys that Claude Code does not read)." Vendoring from the wrong subtree would import Mars-only keys and break the permitted-keys dialect (agent-schemas.md §1) — and would change hashes. **The acquisition MUST source from `cw/agents/` and the cw-lowered skills.**

DESIGN.md §1.1 provenance note (:80–82): `chronicler` is **unshipped vapor in BOTH** `cw/agents/` and `agents/` — it carries zero fork premium and must be BUILD-NEW on any path (Phase 2, not vendored). The CWS 11th agent is `web-researcher` (retained but dormant on the core adapt path). So the acquisition vendors 11 CWS agents including `web-researcher`, but `chronicler` is NOT among what is copied.

### 5.4 Unknowns to resolve at execution

- **The exact `upstream_sha`** — an **execution-time choice** (which upstream commit to pin). VENDOR.md holds it as `<full 40-char commit SHA>` placeholder (boundary-contract.md:46). **Flag: needs decision at execution.**
- **`vendored_on`** date — set at execution (spec example shows `2026-07-03`, boundary-contract.md:47).
- **The exact checkout dir path** for `--upstream` — implementer's choice; not spec-pinned. Recommend a repo-external or gitignored dir so it is not itself scanned by Rule F.
- **CI verify upstream access** — see §3.3 note (whether verify re-fetches upstream or trusts recorded `upstream_sha256`). **Flag: needs decision at execution.**

---

## 6. Enforcement points (where the script runs)

Verbatim table (boundary-contract.md:173–179):

| Point | Command | Blocking? |
|---|---|---|
| Pre-commit hook (`.githooks/pre-commit`, opt-in per clone) | `python3 scripts/check_boundary.py` | **Yes** — blocks the commit |
| CI (PR gate) | `python3 scripts/check_boundary.py` | **Yes** — fails the PR |
| Phase 0 vendor | `python3 scripts/check_boundary.py --init --upstream <dir>` | Writes manifest |
| Phase 3 hard gate | `check_boundary.py` green is one of the 5 gate conditions (DESIGN.md §7) | **Yes** |
| Phase 4 upstream-sync | re-run `--init` after re-pinning `upstream_sha`; diff adopted only | Re-pins manifest |

**UV wrapping (boundary-contract.md:181):** "Per project rules, LAF uses UV: the pre-commit and CI invocations are `uv run python scripts/check_boundary.py`." (The table shows bare `python3`; the operative invocation is UV-wrapped.)

**Phase 3 hard gate context (DESIGN.md:296):** `check_boundary.py` green is one of 5 gate conditions: v2.0 tags present · safety PASS · per-tier canon written · all four quartet agents ran · `check_boundary.py` green. Also listed as a residual-risk mitigation (DESIGN.md:281) and constraint #6 enforcement (DESIGN.md:273).

**Deliverables the script depends on (Phase-0 artifacts):** `.githooks/pre-commit` (opt-in hook wrapper) and a CI workflow step — both simply invoke the UV-wrapped command. These are lightweight wrappers, not additional scripts (ADR-006: `check_boundary.py` is the ONLY script).

---

## 7. Upstream-sync protocol (Phase 4, §5) — 6 steps

Verbatim (boundary-contract.md:187–198):

```
1. Fetch upstream; pick new target SHA.
2. For each ADOPTED-CLEAN file: 3-way reconcile
     base = upstream@old_sha (prefix-rewritten)
     ours = laf file (== base, by contract)
     theirs = upstream@new_sha (prefix-rewritten)
   Since ours == base, apply theirs cleanly (fast-forward). Conflicts ⇒ manual cherry-pick.
3. For writer.md (ADOPTED-PATCHED): reapply the single additive skill line on top of theirs' body.
4. NEVER touch NATIVE / BUILD-NEW files during sync.
5. Re-run check_boundary.py --init to recompute hashes; update upstream_sha + vendored_on in VENDOR.md.
6. Re-run the Phase 3 hard gate before shipping the synced version.
```

**Payoff (boundary-contract.md:200–202):** "Because adopted files are provably unmodified (ours == base), upstream patches apply without merge pain — that is the entire payoff of the boundary contract. The moment an adopted file drifts, this fast-forward degrades to manual cherry-pick, which is exactly the cost the contract is designed to prevent."

Phase 4 gate (DESIGN.md:297): "Native files never touched by sync; SHA re-pinned in `VENDOR.md`." Step 5's `--init` re-run is the **Phase-4 re-init** referenced in the enforcement table (§6).

---

## 8. Phase-by-phase implementer checklist (this track's boundary-contract deliverables)

| Phase | Boundary-contract deliverable | Command / gate |
|---|---|---|
| **0. Vendor** | Acquire upstream CWS checkout (clone + pin SHA); vendor from `cw/agents/`; apply prefix rewrite + writer graft; write `NOTICE` (Apache-2.0); author `scripts/check_boundary.py`; run `--init` to generate `VENDOR.md` | `uv run python scripts/check_boundary.py --init --upstream <dir>` passes; zero edits to vendored files (DESIGN.md:293) |
| **1. Native spine** | (No new boundary artifacts) — but Rule F now requires native `agents/{analyst,safety-verifier}.md` + native skills to be manifest-listed as NATIVE; `writer.md` graft must satisfy Rule C | `uv run python scripts/check_boundary.py` green; writer diff frontmatter-only (DESIGN.md:294) |
| **2. Greenfield** | Manifest-list `chronicler.md`, `tier-coordinator.md`, `/adaptation-safety` as BUILD-NEW; Rule E ensures no name collision with upstream | verify green |
| **3. Compose (HARD GATE)** | `check_boundary.py` green is 1 of 5 gate conditions | `uv run python scripts/check_boundary.py` exit 0 (DESIGN.md:296) |
| **4. Upstream-sync** | Document + execute the 6-step §5 protocol; re-run `--init`; re-pin `upstream_sha` + `vendored_on` | Native files untouched; SHA re-pinned (DESIGN.md:297) |

---

## 9. Risks / open items flagged for execution

1. **Exact `upstream_sha`** — execution-time choice (§5.4). HIGH importance: pins the entire manifest.
2. **CI verify's upstream access model** — spec pins `--upstream` only to `--init`; verify-time upstream re-derivation is unstated (§3.3 note). MED.
3. **`upstream_blob()` / `upstream_has()` implementation** — needs the checkout dir OR a stored upstream tree; spec pseudocode assumes an `upstream_*` accessor. MED — resolved by keeping the checkout dir available or caching upstream files.
4. **Checkout dir must be excluded from Rule F's `glob("agents/*.md")`** — keep it outside `laf-adaptation/` (§5.4). LOW.
5. **`writer.md` upstream duplicate `creative-writing-craft` line** — preserved verbatim; `frontmatter_line_diff` order-insensitivity on `skills:` handles it (agent-schemas.md:143–144, boundary-contract.md:167). Confirmed handled, not a risk if helper is implemented per spec.

