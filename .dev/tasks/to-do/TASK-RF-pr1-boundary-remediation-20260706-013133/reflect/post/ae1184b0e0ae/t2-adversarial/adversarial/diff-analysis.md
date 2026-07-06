# Diff Analysis: Tier-2 Reflection Audit Comparison

## Metadata
- Generated: 2026-07-06 (session)
- Variants compared: 2 (both `--suspect-source`, `suspect: true`, `tier: T2`)
  - Variant 1: `reflect-review-01-qwen3.6-plus.final.md` (57 lines)
  - Variant 2: `reflect-review-02-glm-5.2.final.md` (40 lines)
- Provenance: swarm t2-swarm; 3rd worker (kimi-k2.7-code) died `proxy_error 400`, leaving 2 survivors.
- Ground-truth basis: this analysis is anchored to the **actual repository files** both reviews cite
  (task file, `check_boundary.py`, `test_check_boundary.py`), not to the reviews' self-report — mandatory
  given both sources are flagged suspect.
- Total differences found: 16 (structural 3, content 6, contradictions 2, unique 6, shared assumptions 3)

## Ground-Truth Verification Digest (anchors every finding below)
| GT | Fact | Source of truth |
|----|------|-----------------|
| GT-1 | Real test total = **30** (25 base + **4** GlobSafety + **1** CRLF) | `grep -c 'def test_' test_check_boundary.py` = 30; GlobSafety block has 4, CRLF has 1 |
| GT-2 | Task **Phase 5.1** literal = "`Ran 29 tests`"; **Phase 3.1** = "total now 29" | task file lines 222, 184 — both STALE |
| GT-3 | `check_boundary.py:291` = `if not glob_prefix.startswith("skills/") or glob_prefix.count("/") != 1` | **code is hardened**; rejects bare `skills/**` and `skills/a/b/**` |
| GT-4 | Task **Phase 1.1 spec block (line 92)** still shows weak `if not path.startswith("skills/"):` | task-file DOC drift only — code (GT-3) is safe |
| GT-5 | `check_boundary.py:540-542` hold the A′ writer.md exclusion; code comment at :626 self-cites `540-542` | corrected citation is ACCURATE |
| GT-6 | Task **Phase 4.1 spec block (line 207)** still cites `check_boundary.py:517` | task-file DOC drift only |
| GT-7 | Frontmatter has `reflect_pre` (l.16-24), **no `reflect_post` key**; `status: "🟠 Doing"` (l.5); 6.1 `[x]`, 6.2 `[ ]` | task file |
| GT-8 | A′ (ADOPTED-CLEAN, :543-) re-anchors integrity to `upstream_sha256` in BOTH modes | `check_boundary.py` — partial upstream_sha drift protection DOES exist |

## Structural Differences
| # | Area | Variant 1 (qwen) | Variant 2 (glm) | Severity |
|---|------|------------------|-----------------|----------|
| S-001 | Top-level sections | 5 (Exec Summary, Findings, Suspect-Source, Pass/Fail Signals, Recommendations) + Audit Status | 3 (Audit Summary, Findings, Suspect-Source) | Medium |
| S-002 | Pass/Fail gate table | Present (6-gate table with ✅/⚠️/❌) | Absent | Medium |
| S-003 | Suspect-source format | Table w/ confidence column, 5 files | Numbered list, 3 files | Low |

## Content Differences
| # | Topic | Variant 1 (qwen) Approach | Variant 2 (glm) Approach | Severity | Ground truth |
|---|-------|---------------------------|--------------------------|----------|--------------|
| C-001 | Overall verdict | `🟠 PENDING VERIFICATION` (conditional) | `FAIL` (definitive) | Medium | Both defensible; see A-001 — neither questions whether "Doing" is the *expected* mid-gate state |
| C-002 | H1 glob-gate drift | Concrete finding **F-01, 🔴 HIGH**, hedged "if source matches spec block" | Only a suspect-file to verify predicate; **no finding** | Medium | GT-3/GT-4: code hardened; drift is doc-only → V1's HIGH overstated, but V1 has the coverage V2 lacks |
| C-003 | Test-count 29→30 | F-03; decomposition "25 + **4** GlobSafety + 1 CRLF" | #3; decomposition "25 + **3** GlobSafety + 1" then notes 4th | Low | GT-1: 30, with **4** GlobSafety → **V1 arithmetic exact** |
| C-004 | reflect_post / finalization | F-02 bundles; exec-summary says "marked `[x]` for completion" | #1 (missing evidence) + #2 (incomplete finalization) — cites `status: Doing`, 6.2 `[ ]` | Medium | GT-7: **V2 more precise**; V1's "marked for completion" is imprecise (status is Doing) |
| C-005 | Phase 4.1 line citation | F-05 (🟢 LOW): 517→540-542 doc drift | #4: same | Low | GT-5/GT-6: both TRUE |
| C-006 | upstream_sha integrity gate | Unique **F-04 (🟡 MEDIUM)**: Phase 5.2 lacks explicit gate; "silent hash drift not caught" | Absent | Medium | GT-8: A′ **does** catch ADOPTED-CLEAN upstream_sha drift → V1's claim is **over-broad / partially inaccurate**; gate is a nicety not a hole |

## Contradictions
| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact | Ground-truth resolution |
|---|-------------------|--------------------|--------------------|--------|-------------------------|
| X-001 | Does the task claim completion? | Exec summary: "task file is **marked `[x]` for completion**" | "`status: 🟠 Doing`... 6.2 unchecked" (does NOT claim completion) | Medium | GT-7: **V2 correct** — status is Doing, 6.2 `[ ]`. V1's phrasing is contradicted by the artifact. |
| X-002 | GlobSafety test count | "**4** GlobSafety" (F-03) | "**3** GlobSafety" (evidence in #3) | Low | GT-1: **V1 correct** (4). |

## Unique Contributions
| # | Variant | Contribution | Value | Ground-truth note |
|---|---------|--------------|-------|-------------------|
| U-001 | V1 (qwen) | 6-gate Pass/Fail Signals table | Medium | Actionable gate-level verdicts; H1/M2 marked CONDITIONAL PASS is well-calibrated |
| U-002 | V1 (qwen) | Actionable Recommendations w/ concrete shell command for upstream_sha gate | Medium | Useful even if F-04 over-broad — the `git diff --quiet ... upstream_sha` gate is a valid belt-and-suspenders |
| U-003 | V1 (qwen) | F-01 H1 spec-block drift as explicit finding | Medium | Real doc drift (GT-4); severity must be recalibrated HIGH→LOW/MED |
| U-004 | V1 (qwen) | F-04 upstream_sha gap + `boundary.yml` suspect file | Low | Partially inaccurate (GT-8); keep only as qualified nicety |
| U-005 | V2 (glm) | Split of finalization into "missing evidence" vs "incomplete finalization" w/ `status: Doing` citation | Medium | Higher precision on the strongest real finding (GT-7) |
| U-006 | V2 (glm) | Test-cleanup verification directive (`addCleanup`/`shutil.rmtree` `/tmp/crlf_test_*` leak) | Low-Med | Concrete, verifiable; the task log (l.274) confirms this exact leak was fixed |

## Shared Assumptions (AD-2 — the "agreement = no scrutiny" surface)
Only UNSTATED preconditions are promoted to `[SHARED-ASSUMPTION]` diff points.

| A-NNN | Assumption | Source Agreement | Classification | Promoted |
|-------|------------|------------------|----------------|----------|
| A-001 | The missing `reflect_post` + open 6.2 + `status: Doing` constitutes **executor failure / false completion** — i.e., the POST gate was *due* to have completed before this audit | Both verdicts (C-001) converge on FAIL/PENDING without asking whether "Doing" is the expected state | **UNSTATED** | **YES** |
| A-002 | The on-disk source code matches the execution log's hardened logic | Both flag `check_boundary.py` as suspect-to-verify | STATED | No (verified TRUE, GT-3/GT-5) |
| A-003 | The task file's spec-block literals authoritatively describe the implementation | Both mine the spec blocks (Phase 1.1, 4.1, 5.1) for "drift" | **CONTRADICTED** | Flagged for debate |

### Promoted `[SHARED-ASSUMPTION]` points
| A-NNN | Assumption | Impact | Status |
|-------|------------|--------|--------|
| A-001 | "Absent `reflect_post` ⇒ executor failure" — but this audit sits at `reflect/post/…/t2-swarm`, i.e. it **is** the POST reflect ensemble. If 6.1's wrapper POST gate is *in-flight* (this run), then absent `reflect_post` and open 6.2 are the **expected pre-gate sequencing**, not a defect. Neither review enumerated the reflect-gate ordering before declaring FAIL. | HIGH — could flip the headline verdict from "executor failed to finalize" to "finalization correctly pending POST gate" | UNRESOLVED → routed to Round 2.5 sufficiency probe |

## Summary
- Total structural differences: 3 (S-001..S-003)
- Total content differences: 6 (C-001..C-006)
- Total contradictions: 2 (X-001, X-002)
- Total unique contributions: 6 (U-001..U-006)
- Total shared assumptions surfaced: 3 (UNSTATED: 1 [A-001, promoted], STATED: 1 [A-002], CONTRADICTED: 1 [A-003])
- Highest-severity items: A-001 (HIGH, headline-verdict risk); C-002/F-01 (HIGH-claimed but severity-overstated per GT-3); C-004/C-006 (Medium precision/accuracy deltas)
- Convergence note: the two reviews AGREE on 4 real findings (reflect_post, finalization, 29→30, 4.1 citation). Agreement between two suspect sources is not verification — A-001 and A-003 are where the shared blind spot lives.
