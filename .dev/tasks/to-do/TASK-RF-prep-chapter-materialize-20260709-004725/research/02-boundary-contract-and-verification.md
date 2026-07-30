# Research 02 — Boundary Contract Mechanics & Verification Approach

**Status: Complete**
**Topic:** How to add ONE new NATIVE skill (`chapter-materialize`) + edit NATIVE agent/skill/command/doc
bodies WITHOUT tripping `check_boundary.py`. Owns: check_boundary mechanics, VENDOR.md row format,
verification commands. (Researchers 01/03/04 cover file inventory / manifest-schema authoring / MDTM.)

All citations against files as read this turn. Repo root: `/config/workspace/Infantalizer`.

---

## Q1 — Does adding `chapter-materialize` require ANY edit to `check_boundary.py`? → **NO.**

**`classify()` default is NATIVE.** `check_boundary.py:349-368`:

```
363   if parts[0] == "skills" and len(parts) >= 2:
364       sk = parts[1]
365       if sk in BUILD_NEW_SKILLS:
366           return "BUILD-NEW"
367       return "NATIVE"        # <-- DEFAULT for any non-upstream skill
368   return "NATIVE"
```

A non-upstream skill whose name is NOT in `BUILD_NEW_SKILLS` classifies as **NATIVE** by default
(line 367). `BUILD_NEW_SKILLS = {"adaptation-safety"}` (line 47), so `chapter-materialize` (not in that
set) → NATIVE.

**`NATIVE_SKILLS` is NOT an allowlist.** Line 46: `NATIVE_SKILLS = {"adaptation-tiers",
"adaptation-rules", "source-fidelity"}`. This set is **never read anywhere** in the classification or
verify paths — `classify()` only tests `BUILD_NEW_SKILLS` (line 365) and falls through to NATIVE. Proof
that it is not an allowlist: existing NATIVE manifest rows `skills/prep/**` (VENDOR.md:122) and
`skills/thematic-fidelity/**` (VENDOR.md:123) are NATIVE yet are NOT members of `NATIVE_SKILLS`. So a new
NATIVE skill does not need to be added to `NATIVE_SKILLS` either.

Additional confirmation: `classify()` is only invoked by `do_init()` (lines 402, 429). In plain
**verify mode** (the AC6 command, no `--init`), classification is not even run — verify reads the class
straight from the VENDOR.md manifest row (`parse_manifest`, line 512). So the manifest row is the source
of truth; the classifier only matters if/when someone re-runs `--init`, and even then it defaults NATIVE.

> **CONCLUSION (matches spec claim):** Adding `chapter-materialize` requires **zero** edits to
> `check_boundary.py`. Do NOT touch the `NATIVE_SKILLS` / `BUILD_NEW_SKILLS` / `classify()` code.

---

## Q2 — Rule F / F′ manifestation mechanics; one `/**` glob row; `resources/` coverage

**What must be true for the new SKILL.md to be "manifested" (Rule F).** `verify()` Rule F, lines
656-659:

```
656   # F. Every agents/*.md and skills/**/SKILL.md is listed (or glob-covered) in manifest
657   for rel in disk_agents() + disk_skill_skillmds():
658       if not manifest_covers(rows, rel):
659           errors.append(f"{rel}: not in VENDOR.md manifest")
```

`disk_skill_skillmds()` (lines 343-345) globs `skills/**/SKILL.md`. So the on-disk file
`skills/chapter-materialize/SKILL.md` MUST be covered by some manifest row.

**Coverage is satisfied by the single `/**` glob row.** `manifest_covers()`, lines 318-325:

```
318   def manifest_covers(rows, rel):
319       for r in rows:
320           if r.path == rel: return True
322           if r.is_glob and rel.startswith(r.path[:-2]) and not r.is_adopted:
324               return True   # 'skills/x/**' covers 'skills/x/...'
```

`is_glob` = path endswith `/**` (line 177-178). Row `skills/chapter-materialize/**` (NATIVE, not adopted)
covers `skills/chapter-materialize/SKILL.md` because `"skills/chapter-materialize/SKILL.md".startswith(
"skills/chapter-materialize/")` (`r.path[:-2]` strips the trailing `**`, leaving the trailing `/`). ✅

**NATIVE skills get EXACTLY ONE `/**` row — never per-file rows.** `do_init()` skill loop, lines 411-430:

```
411   # Skills — adopted: per-file rows; native/build-new: one /** row
412   for skdir in disk_skill_dirs():
...
416       if adopted:
417           for rel in disk_skill_files(skdir):   # per-file rows
...
428       else:
429           cls = classify(f"{skill_rel}/SKILL.md", declared, upstream_dir)
430           rows.append((f"{skill_rel}/**", cls, NO_HASH, NO_HASH))   # ONE glob row
```

So for a NATIVE skill `--init` emits exactly one row `skills/chapter-materialize/** | NATIVE | — | —`.
This matches every existing NATIVE/BUILD-NEW skill row in VENDOR.md (lines 118-120, 122-123, 126), all of
which are single `/**` rows.

**Glob-shape gate (must be satisfied by the row's shape).** `parse_manifest`, lines 285-295:

```
285   if path.endswith("/**"):
286       if cls.upper() in ("ADOPTED-CLEAN", "ADOPTED-PATCHED"):
287           errors.append(...glob row cannot be ADOPTED...)
290       glob_prefix = path[:-3]            # strip trailing '/**'
291       if not glob_prefix.startswith("skills/") or glob_prefix.count("/") != 1:
292           errors.append(...must be exactly 'skills/<name>/**'...)
```

`skills/chapter-materialize/**` → `glob_prefix = "skills/chapter-materialize"` → starts with `skills/`
AND has exactly one `/` → **passes** the gate. (Note: a hyphen in the skill name is fine; the gate only
counts `/` separators, not hyphens.)

**Does `resources/boundary-rules.yaml` (or any resources/ file) need its own row? → NO.**
Rule F′ (lines 661-675) enforces per-file coverage ONLY for **adopted** skill dirs:

```
667   adopted_skill_dirs = {
668       r.path.split("/")[1] for r in rows
669       if r.path.startswith("skills/") and r.is_adopted   # ADOPTED only
670   }
671   for skdir in disk_skill_dirs():
672       if skdir.name in adopted_skill_dirs:                # NATIVE dirs skipped
673           for rel in disk_skill_files(skdir):
674               if not manifest_covers(rows, rel): errors.append(...)
```

`chapter-materialize` is NATIVE, so it is NOT in `adopted_skill_dirs` → F′ never iterates its files. And
Rule F only checks `SKILL.md` (via `disk_skill_skillmds`), which the `/**` glob already covers. Comment
at lines 665-666 confirms: "NATIVE/BUILD-NEW skill dirs are already covered by their `/**` glob rows."

> **CONCLUSION:** ANY file under `skills/chapter-materialize/` (SKILL.md, `resources/*.yaml`,
> `resources/*.md`, templates, etc.) is covered by the single `skills/chapter-materialize/**` glob row.
> No per-file rows, no separate row for `resources/boundary-rules.yaml`.

---

## Q3 — Rule E (name collision): does `chapter-materialize` collide with any upstream CWS skill?

**How it is checked.** `verify()` Rule E, lines 638-654. In **Mode V (no `--upstream`, the CI path)**
the collision check is manifest-only (lines 650-654):

```
650   else:  # manifest-only best-effort
651       adopted_paths = {x.path for x in rows if x.is_adopted}
652       if r.path in adopted_paths:
653           errors.append(f"{r.path}: NATIVE/BUILD-NEW collides with an ADOPTED row")
```

So in Mode V, a NATIVE skill FAILS Rule E only if its `/**` path also appears as an ADOPTED row. Since
ADOPTED skills are recorded as per-file rows (`skills/<name>/SKILL.md`, never `skills/<name>/**`), a
NATIVE `/**` row can never string-equal an adopted row → no Mode-V collision by construction.

In **Mode U (`--upstream <checkout>`)** the stronger check runs (lines 642-647):

```
643   if r.is_glob:
644       sk = r.path[len("skills/"):-len("/**")]   # "chapter-materialize"
645       if upstream_root(upstream_dir).joinpath("skills", sk).exists():
646           errors.append(f"{r.path}: NATIVE/BUILD-NEW skill shadows upstream skills/{sk}")
```

**What would make it FAIL:** a directory `cw/skills/chapter-materialize/` existing in the pinned upstream
checkout. The adopted upstream skill set is enumerable from VENDOR.md's ADOPTED SKILL.md rows (lines
71-115): `creative-research, creative-writing-craft, creative-writing-modes, grill-with-docs,
intent-modeling, kb-management, llm-writing, shared-dao, story-memory, story-review, writing-principles,
writing-staffing`. `chapter-materialize` is **not** among them → no collision (Unverified against the raw
upstream tree, which is not checked out here; verified against the adopted manifest, which is the CWS
subset LAF vendored). CI runs Mode V, so the manifest-only check applies and passes trivially.

> **CONCLUSION:** `chapter-materialize` does not collide. It is a novel name absent from the 12 adopted
> CWS skills and from all NATIVE/BUILD-NEW skills (VENDOR.md:116-126). Pick any name NOT in that combined
> list and Rule E passes.

---

## Q4 — Exact VENDOR.md row format for a NATIVE skill

**Exact format (copy this shape):**

```
| skills/chapter-materialize/** | NATIVE | — | — |
```

**Em-dash character = U+2014 (EM DASH), verified.** `NO_HASH = "—"` at `check_boundary.py:50`. Confirmed
by inspecting the live NATIVE row `skills/adaptation-rules/**` in VENDOR.md: the two hash cells use
**U+2014** (`—`), NOT U+2013 en-dash and NOT ASCII hyphen-minus U+002D. (The `-` inside the path
`adaptation-rules` is ASCII U+002D; the two placeholder hash cells are U+2014.) The parser accepts
`_norm_hash` values in `("", "-", "--", NO_HASH, "<hash>")` (line 183) and normalizes them to `NO_HASH`,
BUT the NATIVE-row check at lines 270-272 requires both cells `== NO_HASH` after normalization —
`""`/`-`/`--`/`<hash>` all normalize to `NO_HASH`, so any of those literals would technically pass. **Use
the em-dash `—` (U+2014)** to match every existing NATIVE/BUILD-NEW row byte-for-byte.

**Placement / ordering.** The manifest is machine-generated by `do_init` and sorted (lines 432-434):

```
432   order = {"ADOPTED-CLEAN":0, "ADOPTED-PATCHED":0, "NATIVE":1, "BUILD-NEW":2}
434   rows.sort(key=lambda r: (order.get(r[1],3), r[0]))   # group, then path
```

So the canonical order is: all ADOPTED first, then NATIVE (alpha by path), then BUILD-NEW (alpha by path).
**However** the current VENDOR.md NATIVE block is NOT strictly path-sorted (agents interleaved with skills;
`prep`/`thematic-fidelity` appended after the original three — VENDOR.md:116-123), because rows were
hand-appended, not regenerated via `--init`. Since **verify does not check row ordering** (only
`manifest_covers` set-membership and per-row validity), placement is cosmetically-but-not-functionally
constrained.

> **Recommended placement:** insert the new row into the **NATIVE group** (between line 123
> `skills/thematic-fidelity/**` and line 124 `agents/chronicler.md`, i.e. at the end of the NATIVE block,
> before the first BUILD-NEW row). Existing NATIVE skill rows to mirror exactly:
> - `| skills/adaptation-rules/** | NATIVE | — | — |` (VENDOR.md:118)
> - `| skills/prep/** | NATIVE | — | — |` (VENDOR.md:122)
> - `| skills/thematic-fidelity/** | NATIVE | — | — |` (VENDOR.md:123)
>
> Do NOT hand-edit via `--init` (the re-vendor comment at VENDOR.md:51-54 says the table is
> machine-generated, but `--init` requires an `--upstream` checkout which is unavailable in CI/dev; a
> manual single-row append matching the existing hand-appended NATIVE rows is the pragmatic, verify-clean
> path, consistent with how `prep`/`thematic-fidelity` rows were added).

---

## Q5 — AC6 verification command + captured PASSING baseline

**Exact invocation** (matches CLAUDE.md §2 "Enforcement" and the CI `working-directory: laf-adaptation`
note at CLAUDE.md §2 "CI location"):

```
cd laf-adaptation && uv run python scripts/check_boundary.py
```

Success = **exit 0** with `BOUNDARY CONTRACT: PASS`. This is Mode V (no `--upstream`), which is exactly
what CI (`.github/workflows/boundary.yml`) and the opt-in pre-commit hook run. `main()` returns
`verify()`'s int, propagated to the process via `sys.exit(main())` (line 737).

**RAN IT NOW (read-only baseline), from `/config/workspace/Infantalizer/laf-adaptation`:**

```
$ uv run python scripts/check_boundary.py
NOTE: verify running without --upstream — Rules B and C (upstream-diff checks) skipped; Rule A
      hash-match covers adopted-file integrity against the recorded manifest, plus Rules D/E/F.
BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.
EXIT_CODE=0
```

uv + deps available; the check passes cleanly on the current tree. **This is the passing baseline** the
task's AC6 verification item must reproduce after all edits: same command, exit 0, `PASS` line.

> **Precise verification item for the task:** run `cd laf-adaptation && uv run python
> scripts/check_boundary.py`; assert exit code 0 and stdout contains
> `BOUNDARY CONTRACT: PASS`. (The `--report` mode — `... check_boundary.py --report` — can be used as a
> non-gating sanity print of the provenance summary; it always exits 0 and will list the new
> `[NATIVE          ] skills/chapter-materialize/**  (not pinned)` row once added.)

---

## Q6 — `rewrite_phase_reads` byte-stability (path-contract.md §4, the 3-file read-set)

**The read-set, verbatim** (`skills/prep/resources/path-contract.md:62-73`):

```
## 4. `rewrite_phase_reads` (the hardcoded read-set)

`/laf:rewrite --work <slug>` reads **exactly** these three files, by hardcoded path, no other arguments:

    work/prep/<slug>/30-mapping.yaml
    work/prep/<slug>/40-prep-brief.md
    work/prep/<slug>/10-challenges.yaml
```

(Lines 67-69 are the three paths inside a fenced block; line 72 adds the `50-greenlight.md
status: CONFIRMED` precondition; line 73 excludes `70-traceability.md`.)

**Why it matters here:** Stage-0 chapter materialization is a `/laf:prep` change. The rewrite phase's
read-set is a *downstream* contract that this task must NOT perturb. `check_boundary.py` does NOT hash
`path-contract.md` (it is under a NATIVE skill's `resources/`, covered only by the `skills/prep/**` glob
for *existence*, not content — Rule F′ skips NATIVE dirs, Q2). So byte-stability of §4 is **not**
machine-enforced by the boundary check; it must be asserted by the task's own verification.

**Concrete verification suggestions (pick one; both are cheap and deterministic):**

1. **Grep-assert the three exact paths are present and unchanged** (order-independent, robust to
   surrounding edits):
   ```
   f=laf-adaptation/skills/prep/resources/path-contract.md
   grep -qF 'work/prep/<slug>/30-mapping.yaml'   "$f" \
     && grep -qF 'work/prep/<slug>/40-prep-brief.md' "$f" \
     && grep -qF 'work/prep/<slug>/10-challenges.yaml' "$f" \
     && echo "read-set OK"
   ```

2. **git-diff the §4 region (strictest — proves byte-unchanged).** Assert the diff touches no lines in the
   §4 span. Since §4 currently spans lines ~62-73 (heading at line 62, `## 5.` heading at line 75):
   ```
   git diff -- laf-adaptation/skills/prep/resources/path-contract.md \
     | grep -E '^[+-].*(30-mapping|40-prep-brief|10-challenges|rewrite_phase_reads)' \
     && echo "WARNING: §4 read-set touched" || echo "§4 read-set byte-unchanged"
   ```

> **Recommendation:** put suggestion 1 (grep-assert of the 3 exact `work/prep/<slug>/…` paths) in the
> task's verification checklist — it is the highest-signal, lowest-flake check that the 3-file read-set
> survived the edits byte-intact.

---

## Q7 — `.claude/` mirror lockstep: hash-checked or manual convention? Risk if it drifts.

**NOT hash-checked by `check_boundary.py`.** The checker's `REPO` is `Path(__file__).resolve().parents[1]`
= the `laf-adaptation/` dir (line 31). Every discovery/rule path (`disk_agents`, `disk_skill_dirs`,
`_safe_repo_path`, VENDOR.md) is rooted at `laf-adaptation/` and `_safe_repo_path` (lines 193-217)
**refuses any path that escapes** the `laf-adaptation/` tree. The repo-root `.claude/` mirror lives
OUTSIDE `laf-adaptation/`, so the boundary checker never reads it, hashes it, or compares it. There is no
code in `check_boundary.py` referencing `.claude/`. **The `laf-adaptation/ ↔ .claude/` mirror is a manual
convention, not a machine-enforced invariant of the boundary check.**

(Note: the SuperClaude framework's own `.claude/` mirror is governed by `make sync-dev` / `make
verify-sync` per the global CLAUDE.md, but that is the *framework* mirror and is unrelated to the
`laf-adaptation/` boundary contract; neither pipeline hashes the other.)

**Risk if the mirror drifts:** the boundary check will still PASS (exit 0) because it only sees
`laf-adaptation/`. So a new `laf-adaptation/skills/chapter-materialize/` that is NOT copied into the
`.claude/` mirror would be **invisible to the boundary check yet silently non-functional at runtime**
(Claude Code loads skills/agents from the mirror the harness actually reads). The failure mode is a
**green boundary check + a runtime "skill not found"** — the check cannot catch mirror drift.

> **MITIGATION for the task:** add an explicit verification/checklist item that copies the new skill dir
> into the `.claude/` mirror in lockstep and diffs the two trees (e.g. `diff -r
> laf-adaptation/skills/chapter-materialize .claude/skills/chapter-materialize`), since
> `check_boundary.py` provides zero protection here. Researcher 01 owns the concrete mirror-map / edit
> loci; this task must NOT rely on the boundary check to enforce the mirror.

---

## Bottom-line for the task author

- **check_boundary.py: DO NOT EDIT.** New NATIVE skill auto-classifies NATIVE (Q1).
- **VENDOR.md: add EXACTLY ONE row**, em-dash U+2014, NATIVE group:
  `| skills/chapter-materialize/** | NATIVE | — | — |` (Q4). No per-file / no `resources/` rows (Q2).
- **Verification gate (AC6):** `cd laf-adaptation && uv run python scripts/check_boundary.py` → exit 0 +
  `BOUNDARY CONTRACT: PASS`. Baseline PASSES today (Q5).
- **Extra task-owned asserts** (boundary check will NOT catch these): (a) grep-assert the 3
  `rewrite_phase_reads` paths in `path-contract.md` §4 are byte-unchanged (Q6); (b) diff the `.claude/`
  mirror against `laf-adaptation/` for the new skill (Q7).
- Rule E collision: `chapter-materialize` is a free name (Q3).
