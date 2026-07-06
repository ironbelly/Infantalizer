# QA Report — Lens: Actionability / Operability (Partition: single-instance)

**Topic:** Remediated `laf-adaptation/scripts/check_boundary.py` (PR-1 remediation, CH-1..CH-8)
**Date:** 2026-07-04
**Phase:** doc-qualitative (actionability lens of the 6-lens QA gate, item 6.3)
**Fix cycle:** N/A (fix_authorization: false — REPORT ONLY)
**Lens:** Actionability / operability — error messages actionable? Mode-U workflow usable? Inverse-rewrite logic maintainable? Tests maintainable? Docs honest? Operational gaps?

---

## Overall Verdict: FAIL

One CRITICAL operational regression (documented re-vendor flow broken by CH-5), two IMPORTANT operator-UX issues, three MINOR actionability gaps. The code itself is operationally sound for its SECURITY purpose; the failure is in OPERATOR EXPERIENCE for the legitimate re-vendor workflow, which the remediation did not account for and the docs do not mention.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Error messages actionable? (`upstream_sha256` mismatch, path escape, HEAD mismatch) | PARTIAL | `check_boundary.py:489-491` (body-mismatch msg), `:216` (escape msg), `:514-519` (HEAD msg). Read in full. Most actionable; path-escape msg omits the resolved path (Finding 4). |
| 2 | `--upstream-sha` + CH-5 give a usable Mode-U workflow? | FAIL | Empirically tested: Mode U verify at wrong SHA fails cleanly with actionable msg. BUT `--init` post-write verify now fails on legitimate re-vendor (Finding 1). `check_boundary.py:425, 507-519`. |
| 3 | "FAIL LOUD if no pin / unreadable HEAD" — good UX or footgun? | FAIL | Right behavior for security use case, but footgun for re-vendor use case (same root cause as Finding 1). `check_boundary.py:507-519`. |
| 4 | Inverse-rewrite (CH-1) logic understandable to future maintainer? Comments adequate? Could someone "simplify" it back to broken forward formula? | PASS | `prefix_unrewrite` docstring `:87-95` + Rule A′ block comment `:470-480` are exemplary: they explain WHY the inverse, warn the on-disk file is already rewritten, and explicitly note the empirical correction. A maintainer would NOT simplify it back. |
| 5 | New tests maintainable (clear fixtures, not brittle)? | PASS | `test_check_boundary.py:56-142` `BoundaryTestBase` is well-factored: tmp-dir monkeypatch in setUp/tearDown, `build_clean_fixture()` is the single source of fixture truth, hash helpers delegate to module-under-test. Mode-U tests use real tmp git checkouts (slower but more honest than mocking). |
| 6 | Doc alignment (CLAUDE.md §2, boundary.yml, VENDOR.md header) gives honest picture of CI catches vs doesn't? | PARTIAL | CLAUDE.md §2 + boundary.yml header are exemplary on Mode-V scope and ADOPTED-PATCHED residual gap. BUT VENDOR.md re-vendor comment (`:32-35`) and CLAUDE.md §2 were NOT updated for the `--init`-now-requires-`--upstream-sha` operational change (Finding 1 + Finding 7). |
| 7 | Does `--init` still work end-to-end with the new signature? (do_init threads upstream_sha now.) | FAIL | Empirically: `do_init` threads `upstream_sha` (`:349, :425`) and writes rows correctly, BUT the post-write `verify()` call (`:425`) fails exit 1 on legitimate re-vendor because CH-5 compares checkout HEAD against the STALE VENDOR.md pin. Rows ARE written; exit code lies (Finding 1). |
| 8 | Does `--report` still work after parser/signature changes? | PASS | Empirically: `--report` exits 0 on real tree and prints warnings-as-non-blocking on malformed input. `do_report` `:612-633`. |
| 9 | Are error-recovery actions discoverable from the error messages alone? | PARTIAL | HEAD-mismatch msg `:518-519` says "(re-checkout at the pinned SHA)" — good for verify mode, but WRONG advice for `--init` mode where the operator WANTS to move the pin (Finding 2). |
| 10 | Gate stays green on real corpus? (operator-trust invariant) | PASS | Empirically: `check_boundary.py` exit 0, `BOUNDARY CONTRACT: PASS`; `--report` exit 0. 21/21 tests pass. |

---

## Summary
- Checks passed: 4 / 10 (1 more PARTIAL)
- Checks failed: 3 (1 CRITICAL, 2 IMPORTANT)
- Partial: 3 (rolled up into findings below)
- Critical issues: 1
- Important issues: 2
- Minor issues: 3
- Issues fixed in-place: 0 (fix_authorization: false)
- Tool engagement: Read 5 (TASK, check_boundary.py, test_check_boundary.py, boundary.yml, VENDOR.md header) | Bash 4 (test suite, real-tree gate+report, re-vendor simulation x3)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | `check_boundary.py:425, 507-519` + VENDOR.md `:32-35` re-vendor comment | **Documented re-vendor flow is broken by CH-5.** The VENDOR.md header comment (lines 32-35) instructs maintainers: "to re-vendor at a new upstream_sha, run `uv run python scripts/check_boundary.py --init --upstream <checkout>` then commit the manifest diff." But CH-5 added a HEAD-pin assertion to `verify()`, and `do_init` calls `verify()` (line 425) as a post-write self-check. When a maintainer legitimately re-vendors at a NEW upstream SHA: the checkout HEAD is the new SHA, but VENDOR.md still pins the OLD SHA (the pin is what `--init` is supposed to UPDATE) → CH-5 fires "checkout HEAD != pinned upstream_sha" → `verify` returns 1 → `do_init` returns 1. **Empirically verified:** `--init --upstream ../cwroot` exits 1 and prints `BOUNDARY CONTRACT: FAIL` on a clean legitimate re-vendor. The manifest rows ARE written correctly, but the exit code and FAIL banner tell the operator the operation failed. A maintainer following the documented flow will either (a) believe re-vendor failed and discard correct work, or (b) commit a "failed" manifest and lose trust in the gate. | Three options, in order of preference: **(a)** Make `do_init` update the VENDOR.md `upstream_sha:` header to the checkout HEAD BEFORE the post-write verify (since `--init` is semantically "I am moving the pin"); **(b)** Make `do_init` skip the CH-5 HEAD-pin check (pass a flag or call a verify-subset), since `--init` is the trusted re-vendor path; **(c)** Document that re-vendor requires `--upstream-sha $(git -C <checkout> rev-parse HEAD)` and update the VENDOR.md header comment to include it. Verified that workaround (c) makes `--init` exit 0. Whichever fix, the VENDOR.md re-vendor comment MUST be updated. |
| 2 | IMPORTANT | `check_boundary.py:425` (`do_init` writes-then-reports-FAIL ordering) | **`--init` writes the manifest, THEN reports `BOUNDARY CONTRACT: FAIL` on its own output.** Operator UX: the FAIL banner and violation list appear in stderr, and only AFTER does "--init: wrote N manifest rows" print. A maintainer reading top-to-bottom sees "FAIL" first and reasonably concludes the manifest was NOT written. Compounds Finding 1. Even when `--init` legitimately succeeds (Finding 1 fixed), the message ordering is misleading: violation lines from the post-write verify stream BEFORE the success summary. | Reorder `do_init` so the "wrote N rows" summary prints BEFORE invoking `verify()`, and clearly label the verify output as a post-write self-check (e.g. prefix with "--init post-write self-check:"). Or capture verify's output and print it after the summary with clear framing. |
| 3 | IMPORTANT | `check_boundary.py:518-519` (HEAD-mismatch message) | **HEAD-mismatch error message gives wrong recovery advice for `--init` mode.** Message: "Mode U: --upstream checkout HEAD {head} != pinned upstream_sha {pinned} (re-checkout at the pinned SHA)". Correct for verify mode. WRONG for `--init` mode, where the operator's intent is to MOVE the pin to a new SHA — telling them to "re-checkout at the pinned SHA" undoes the very re-vendor they're attempting. (This is the message that surfaces in the Finding 1 failure.) | Either suppress the HEAD-pin check in `--init` mode (per Finding 1 fix (b)), or emit a mode-aware message in `--init` context: "you are re-vendoring at a new SHA; pass --upstream-sha <new HEAD> or update VENDOR.md upstream_sha: first." |
| 4 | MINOR | `check_boundary.py:216` (`_safe_repo_path` escape message) | **Path-escape error message doesn't show the resolved target.** "manifest path escapes laf-adaptation/ tree" — doesn't tell the maintainer WHERE it escaped to. Compare the absolute-path message (`:209`) which at least names the input. For a path like `../../etc/passwd` the operator benefits from seeing the resolved absolute path to distinguish a real attack from a benign `../scripts/foo.md` typo. | Include the resolved path in the message: `f"{rel!r}: manifest path escapes laf-adaptation/ tree (resolves to {resolved})"`. |
| 5 | MINOR | `check_boundary.py:489-491` (Rule A′ body-mismatch message) | **Body-mismatch message is clear on WHAT but silent on recovery.** "body no longer matches pinned upstream_sha256 — raw-upstream hash mismatch (CH-1; laf_sha256 rewrite detected)" — a maintainer who didn't author CH-1 may not know whether to (a) restore the body from upstream, (b) re-vendor, or (c) update upstream_sha256. Acceptable for a security gate (the answer is "investigate, this is suspicious"), but a one-line "(restore the adopted body or re-vendor if the change is intentional)" suffix would shorten time-to-resolution. | Append "(restore the adopted body, or re-vendor via --init if the upstream itself changed)" to the message. |
| 6 | MINOR | `VENDOR.md:32-35` (re-vendor comment) + CLAUDE.md §2 | **Re-vendor doc comment predates CH-5 and is now incomplete.** The VENDOR.md HTML comment tells maintainers to run `--init --upstream <checkout>` with no mention of `--upstream-sha`, contradicting the actual post-CH-5 requirement (Finding 1). CLAUDE.md §2 documents Mode V/U enforcement accurately but is silent on the re-vendor operational path. | Update VENDOR.md re-vendor comment to reflect whatever Finding 1 fix is chosen; add a one-line "Re-vendoring" note to CLAUDE.md §2 pointing at UPSTREAM-SYNC.md (which the task log notes is the canonical re-vendor procedure). |
| 7 | MINOR | `test_check_boundary.py:425-451` (`ModeUHeadPinTests._make_git_checkout`) | **Mode-U test shells out to git 6× per test.** Slower than mocking `subprocess.run`, and couples test pass/fail to git being installed and configurable on the runner. Acceptable (more honest than mocking; CI runs on ubuntu-latest which has git), but if a future runner lacks git the failure mode is "subprocess.CalledProcessError" not "git missing — skipped". | Optional: add a `setUp` guard that detects missing git and `self.skipTest("git not available")`. Low priority — current behavior is correct on all realistic runners. |

---

## Operational Simulation Notes (beyond the checklist)

**The CH-1 inverse-rewrite logic is the strongest part of this remediation from a maintainability standpoint.** The OQ-1 resolution recorded in the task log (lines 240-246) shows the implementer CAUGHT AND CORRECTED a wrong formula empirically — the spec was ambiguous, the first recorded answer was wrong, and the corrected inverse formula was verified against the real `brainstormer.md`. The code comments at `prefix_unrewrite` (`:87-95`) and the Rule A′ block (`:470-480`) document this so thoroughly that a future maintainer cannot accidentally "simplify" `prefix_unrewrite(read_text(fp))` back to the broken `prefix_rewrite(...)` without reading an explicit warning that the on-disk file is ALREADY rewritten. This is exactly the kind of comment that prevents regression. (AX-1 drift axis: would-fire on a comment-stripping simplification — currently defended.)

**The fail-loud CH-5 behavior is correct for the security threat model but has a blind spot for the operator workflow.** "Don't silently trust a stale checkout" is the right security default. The problem is that `--init` is the one Mode-U invocation where the operator's INTENT is to move the pin — and CH-5 fires anyway because the pin-update hasn't happened yet when `verify()` runs. This is an architectural seam, not a bug in CH-5 itself: CH-5 is correctly checking the manifest's stated pin against the checkout, but `do_init` is the workflow that's supposed to UPDATE that pin, and it doesn't do so before self-verifying.

**Tests are maintainable.** `BoundaryTestBase.build_clean_fixture()` is the canonical fixture; every negative test stamps it then mutates one thing. The fixture bodies intentionally contain no `creative-writing-skills:` literal (documented at `test_check_boundary.py:32-35`) so the inverse rewrite is a no-op — mirroring the real corpus — and the literal-bearing path is exercised separately by `test_prefix_rewrite_positive`. This is clean separation. The one brittleness is the git-shell-out in Mode-U tests (Finding 7), which is a deliberate honesty-vs-speed trade-off.

---

## Recommendations

Before this remediation can ship:

1. **Fix Finding 1 (CRITICAL).** Pick option (a), (b), or (c) and update both `do_init` and the VENDOR.md re-vendor comment. Option (a) — `do_init` writes the new `upstream_sha:` header from checkout HEAD before post-write verify — is the cleanest because it makes the documented flow (`--init --upstream <checkout>`) work as documented, with no new operator-side knowledge required.

2. **Fix Finding 2 + Finding 3 together** by reordering `do_init` output and (if Finding 1 is fixed via (a) or (b)) suppressing or rewording the HEAD-pin message in `--init` context.

3. **Address Findings 4-6 (MINOR)** in the same doc pass; they are one-line message and comment improvements.

4. Finding 7 is optional and can ship as-is.

After Finding 1 is fixed, re-run the empirical re-vendor simulation in this report to confirm `--init` exits 0 on a legitimate re-vendor with no `--upstream-sha` flag.

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
This is a single-lens qualitative review spawned without an `## Inherited Structural Verdict` block. No rf-qa PASS items were relied upon; all checks above were performed with independent tool engagement.

**(b) Independent semantic checks (≥1 required, INV-019):**
- **Re-vendor flow operational simulation** — built a real tmp git checkout at SHA-1, advanced it to SHA-2, ran the documented `--init --upstream <checkout>` flow, observed exit 1 + `BOUNDARY CONTRACT: FAIL` on a legitimate re-vendor. Evidence: Bash output captured above (3 separate simulation runs to isolate the `cw/` vs `cwroot/` rooting issue). This is the basis for Finding 1 (CRITICAL).
- **Real-tree gate + test suite** — ran `check_boundary.py` (exit 0, PASS), `--report` (exit 0), and `test_check_boundary.py` (21/21 pass) on the actual repo. Evidence: Bash outputs above.
- **Message-actionability read** — read every error path in `check_boundary.py` (`:207-216` path-safety, `:489-491` Rule A′, `:507-519` CH-5 HEAD-pin, `:237` malformed-row, `:253` unknown-class, `:256` duplicate, `:268` bad-hash, `:272` native-with-hash) and assessed each for operator recoverability. Evidence: cited line ranges in the table above.
- **Test-maintainability read** — read `test_check_boundary.py` end-to-end (493 lines), traced fixture construction and the monkeypatch lifecycle, verified the no-literal invariant is documented and the literal-bearing path is separately covered.

1. **Factual claims independently verified against source:** 14 (every line citation above was read from the actual file; the re-vendor breakage was reproduced empirically, not inferred).
2. **Specific files read:** TASK file, `check_boundary.py` (full), `test_check_boundary.py` (full), `boundary.yml` (full), `VENDOR.md` (header), `CLAUDE.md` §2 (via system context).
3. **If 0 issues found, would the user trust this?** N/A — 7 issues found, 1 CRITICAL reproduced empirically.
4. **Web research:** none performed (all verification was local-file-bound: reading the document, reading the code, running the gate and tests, simulating the operator workflow). Tavily MCP not engaged because no external lookup was required.

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## QA Complete
