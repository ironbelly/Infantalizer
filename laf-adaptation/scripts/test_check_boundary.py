#!/usr/bin/env python3
"""test_check_boundary.py — stdlib unittest suite for check_boundary.py.

Covers the PR-1 remediation acceptance criteria (spec §5): clean-corpus
regression, CH-1 trust-root, CH-2 resources/** coverage, CH-3 writer-only
patch, CH-4 path safety, CH-5 Mode-U HEAD pin, CH-6 parser hardening, and
CH-7 prefix-rewrite positive path.

Every test builds an isolated fixture tree under tempfile.mkdtemp() and
points the module globals `check_boundary.REPO` / `check_boundary.VENDOR_MD`
at it, so the REAL laf-adaptation/ tree is never mutated (file-scope
invariant). Run via:

    uv run python scripts/test_check_boundary.py
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Make the sibling check_boundary.py importable regardless of cwd.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import check_boundary  # noqa: E402


# --- Fixture content helpers ---------------------------------------------------
# Adopted-fixture bodies intentionally contain NO "creative-writing-skills:"
# literal, so prefix_rewrite() is a no-op and the raw-upstream hash equals
# the on-disk hash. (The prefix-rewrite positive path is exercised separately
# by test_prefix_rewrite_positive with a synthetic literal-bearing blob.)

_QUARTET = ["critic", "editor", "reader-sim", "continuity-checker"]


def _agent_body(name):
    return f"---\nname: {name}\ndescription: adopted agent fixture\n---\n# {name}\nAdopted body.\n"


def _writer_body():
    # ADOPTED-PATCHED: additive laf-adaptation skills line in frontmatter.
    return ("---\nname: writer\ndescription: writer\n"
            "skills:\n  - laf-adaptation:adaptation-rules\n"
            "---\n# writer\nAdopted body.\n")


def _skill_md(name):
    return f"---\nname: {name}\ndescription: skill\n---\n# {name}\nSkill body.\n"


# --- Shared base: tmp REPO + VENDOR.md builder --------------------------------
class BoundaryTestBase(unittest.TestCase):
    """Patches check_boundary.REPO / VENDOR_MD at a tmp dir; restores on tear-down."""

    def setUp(self):
        self._orig_repo = check_boundary.REPO
        self._orig_vendor = check_boundary.VENDOR_MD
        self.tmp = Path(tempfile.mkdtemp(prefix="boundary_test_"))
        check_boundary.REPO = self.tmp
        check_boundary.VENDOR_MD = self.tmp / "VENDOR.md"

    def tearDown(self):
        check_boundary.REPO = self._orig_repo
        check_boundary.VENDOR_MD = self._orig_vendor
        shutil.rmtree(self.tmp, ignore_errors=True)

    # -- low-level fixture writers --
    def write_file(self, rel, content):
        p = self.tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return p

    def write_manifest(self, rows):
        """rows: list of (path, cls, upstream_sha256, laf_sha256) ready to emit."""
        header = (
            "# VENDOR.md fixture\n\n"
            "upstream_repo: https://example/upstream\n"
            f"upstream_sha:  {check_boundary.NO_HASH}\n"
            "prefix_rewrite: \"creative-writing-skills:\" -> \"laf-adaptation:\"\n\n"
            "## Manifest\n\n"
            "| path | class | upstream_sha256 | laf_sha256 |\n"
            "|------|-------|-----------------|------------|\n"
        )
        body = "\n".join(f"| {p} | {c} | {u} | {l} |" for (p, c, u, l) in rows)
        check_boundary.VENDOR_MD.write_text(header + body + "\n", encoding="utf-8")

    # -- hash helpers (delegate to the module under test) --
    def laf_sha(self, rel):
        return check_boundary.sha256_text(check_boundary.read_text(self.tmp / rel))

    def upstream_sha_clean(self, rel):
        """Raw-upstream hash for a no-literal ADOPTED-CLEAN body.

        Matches `--init` line 249 semantics (`sha256_text(up_raw)`): the disk IS the
        prefix-rewritten upstream, so the raw upstream = prefix_unrewrite(disk). For
        fixture bodies with no `creative-writing-skills:` literal the inverse is a
        no-op, so upstream_sha == laf_sha == sha256(disk) — consistent with the real
        corpus's no-literal rows."""
        return check_boundary.sha256_text(
            check_boundary.prefix_unrewrite(check_boundary.read_text(self.tmp / rel)))

    def upstream_sha_patched(self, rel):
        """Raw-upstream hash for ADOPTED-PATCHED == sha256(prefix_rewrite(body_of(disk)))."""
        return check_boundary.sha256_text(
            check_boundary.prefix_rewrite(check_boundary.body_of(check_boundary.read_text(self.tmp / rel))))

    # -- canonical clean-fixture builder --
    def build_clean_fixture(self):
        """Build a minimal self-consistent tree + manifest that satisfies Rules A-F
        (and the remediated A' / extended F). Returns the manifest rows written."""
        NH = check_boundary.NO_HASH
        rows = []
        # Quartet (Rule D requires these as ADOPTED-CLEAN).
        for name in _QUARTET:
            rel = f"agents/{name}.md"
            self.write_file(rel, _agent_body(name))
            rows.append((rel, "ADOPTED-CLEAN", self.upstream_sha_clean(rel), self.laf_sha(rel)))
        # writer.md (ADOPTED-PATCHED).
        wrel = "agents/writer.md"
        self.write_file(wrel, _writer_body())
        rows.append((wrel, "ADOPTED-PATCHED", self.upstream_sha_patched(wrel), self.laf_sha(wrel)))
        # A NATIVE agent.
        nrel = "agents/analyst.md"
        self.write_file(nrel, _agent_body("analyst"))
        rows.append((nrel, "NATIVE", NH, NH))
        # An adopted skill with a SKILL.md + a resources/** file.
        sm = "skills/sample/SKILL.md"
        self.write_file(sm, _skill_md("sample"))
        rows.append((sm, "ADOPTED-CLEAN", self.upstream_sha_clean(sm), self.laf_sha(sm)))
        sr = "skills/sample/resources/note.md"
        self.write_file(sr, "# note\nresource body\n")
        rows.append((sr, "ADOPTED-CLEAN", self.upstream_sha_clean(sr), self.laf_sha(sr)))
        # A native skill (glob row).
        self.write_file("skills/native1/SKILL.md", _skill_md("native1"))
        rows.append(("skills/native1/**", "NATIVE", NH, NH))
        self.write_manifest(rows)
        return rows


# --- Phase-1: clean-corpus regression ------------------------------------------
class CleanCorpusTests(BoundaryTestBase):
    def test_clean_corpus_passes(self):
        self.build_clean_fixture()
        self.assertEqual(check_boundary.verify(), 0,
                         "self-consistent fixture must PASS Mode V verify")


# --- Phase-2: CH-6 parser hardening + CH-4 path safety -------------------------
class ParserHardeningTests(BoundaryTestBase):
    """CH-6 (M4): malformed / duplicate / bad-hash / native-with-hash rows fail loud."""

    def _manifest_with_row(self, raw_row_line):
        """Stamp a clean fixture, then append ONE extra raw row line to the manifest."""
        self.build_clean_fixture()
        txt = check_boundary.VENDOR_MD.read_text(encoding="utf-8")
        check_boundary.VENDOR_MD.write_text(txt.rstrip() + "\n" + raw_row_line + "\n",
                                            encoding="utf-8")

    def test_malformed_row_fails(self):
        for bad in ("| agents/x.md | ADOPTED-CLEAN | short |",          # 3 cells
                    "| agents/y.md | ADOPTED-CLEAN | a | b | c |"):     # 5 cells
            with self.subTest(row=bad):
                self._manifest_with_row(bad)
                _, errors = check_boundary.parse_manifest(
                    check_boundary.read_text(check_boundary.VENDOR_MD))
                self.assertTrue(any("expected 4 cells" in e for e in errors),
                                f"malformed row should fail loud: {bad!r} -> {errors}")

    def test_duplicate_path_fails(self):
        # Re-add a path already in the clean fixture (agents/critic.md).
        dup = ("| agents/critic.md | ADOPTED-CLEAN | "
               "0000000000000000000000000000000000000000000000000000000000000000 | "
               "0000000000000000000000000000000000000000000000000000000000000000 |")
        self._manifest_with_row(dup)
        _, errors = check_boundary.parse_manifest(
            check_boundary.read_text(check_boundary.VENDOR_MD))
        self.assertTrue(any("duplicate path" in e for e in errors), errors)

    def test_bad_hash_fails(self):
        # 63-char hash (one short) on an adopted row.
        bad = ("| agents/zzz.md | ADOPTED-CLEAN | "
               "000000000000000000000000000000000000000000000000000000000000000 | "   # 63 hex
               "0000000000000000000000000000000000000000000000000000000000000000 |")
        self._manifest_with_row(bad)
        _, errors = check_boundary.parse_manifest(
            check_boundary.read_text(check_boundary.VENDOR_MD))
        self.assertTrue(any("64-hex" in e for e in errors), errors)

    def test_native_with_hash_fails(self):
        bad = ("| agents/nnn.md | NATIVE | "
               "0000000000000000000000000000000000000000000000000000000000000000 | — |")
        self._manifest_with_row(bad)
        _, errors = check_boundary.parse_manifest(
            check_boundary.read_text(check_boundary.VENDOR_MD))
        self.assertTrue(any("must have" in e for e in errors), errors)

    def test_well_formed_manifest_has_zero_errors(self):
        self.build_clean_fixture()
        _, errors = check_boundary.parse_manifest(
            check_boundary.read_text(check_boundary.VENDOR_MD))
        self.assertEqual(errors, [], f"clean fixture must parse with zero errors: {errors}")


class PathSafetyTests(BoundaryTestBase):
    """CH-4 (M2): path-traversal and absolute manifest paths rejected."""

    def test_path_traversal_rejected(self):
        self.build_clean_fixture()
        bad = ("| ../../etc/passwd | ADOPTED-CLEAN | "
               "0000000000000000000000000000000000000000000000000000000000000000 | "
               "0000000000000000000000000000000000000000000000000000000000000000 |")
        txt = check_boundary.VENDOR_MD.read_text(encoding="utf-8")
        check_boundary.VENDOR_MD.write_text(txt.rstrip() + "\n" + bad + "\n", encoding="utf-8")
        _, errors = check_boundary.parse_manifest(
            check_boundary.read_text(check_boundary.VENDOR_MD))
        self.assertTrue(any("escapes" in e or "absolute" in e for e in errors), errors)
        # And the verify gate fails on it.
        self.assertNotEqual(check_boundary.verify(), 0)

    def test_absolute_path_rejected(self):
        self.build_clean_fixture()
        bad = ("| /etc/passwd | ADOPTED-CLEAN | "
               "0000000000000000000000000000000000000000000000000000000000000000 | "
               "0000000000000000000000000000000000000000000000000000000000000000 |")
        txt = check_boundary.VENDOR_MD.read_text(encoding="utf-8")
        check_boundary.VENDOR_MD.write_text(txt.rstrip() + "\n" + bad + "\n", encoding="utf-8")
        _, errors = check_boundary.parse_manifest(
            check_boundary.read_text(check_boundary.VENDOR_MD))
        self.assertTrue(any("absolute" in e for e in errors), errors)

    def test_dot_or_empty_path_rejected(self):
        """A manifest path of '.' or '' would resolve to REPO itself and crash
        read_text on the directory mid-rule (Rules A/C). _safe_repo_path must
        reject it loud at the parser boundary, not crash with IsADirectoryError."""
        H = "0" * 64
        for bad_path in (".", ""):
            with self.subTest(path=bad_path):
                self.build_clean_fixture()
                bad = f"| {bad_path} | ADOPTED-CLEAN | {H} | {H} |"
                txt = check_boundary.VENDOR_MD.read_text(encoding="utf-8")
                check_boundary.VENDOR_MD.write_text(txt.rstrip() + "\n" + bad + "\n",
                                                    encoding="utf-8")
                _, errors = check_boundary.parse_manifest(
                    check_boundary.read_text(check_boundary.VENDOR_MD))
                self.assertTrue(errors,
                                f"manifest path {bad_path!r} must fail loud, not crash")
                # And verify mode must FAIL (not raise) on it.
                self.assertNotEqual(check_boundary.verify(), 0,
                                    f"verify must FAIL on path {bad_path!r}, not crash")


class ReportContractTests(BoundaryTestBase):
    """CH-6 caller contract: --report prints manifest errors as warnings but
    STILL exits 0 (preserve L1 contract; the report is a non-blocking summary)."""

    def test_report_exits_0_on_malformed(self):
        self.build_clean_fixture()
        # Append a malformed (3-cell) row.
        txt = check_boundary.VENDOR_MD.read_text(encoding="utf-8")
        check_boundary.VENDOR_MD.write_text(
            txt.rstrip() + "\n| agents/bad.md | ADOPTED-CLEAN | short |\n",
            encoding="utf-8")
        # --report must NOT fail the gate on malformed rows.
        self.assertEqual(check_boundary.do_report(), 0,
                         "--report must exit 0 even when manifest has errors")


# --- Phase-3: CH-1 trust-root, CH-3 writer-only, CH-2 resources/** -------------
class TrustRootTests(BoundaryTestBase):
    """CH-1 (H1): re-anchor ADOPTED-CLEAN integrity to PR-rewrite-resistant
    upstream_sha256 via the INVERSE prefix rewrite (disk is already rewritten)."""

    def _rewrite_manifest_field(self, path, field, new_val):
        """Rewrite ONE row's field in the stamped VENDOR.md fixture."""
        cb = check_boundary
        lines = cb.VENDOR_MD.read_text(encoding="utf-8").splitlines()
        out = []
        for ln in lines:
            s = ln.strip()
            if s.startswith("|") and f"| {path} |" in ln:
                cells = [c.strip() for c in s.strip("|").split("|")]
                if len(cells) == 4 and cells[0] == path:
                    idx = {"upstream_sha256": 2, "laf_sha256": 3}[field]
                    cells[idx] = new_val
                    ln = "| " + " | ".join(cells) + " |"
            out.append(ln)
        cb.VENDOR_MD.write_text("\n".join(out) + "\n", encoding="utf-8")

    def test_clean_corpus_still_passes_under_Aprime(self):
        # Sanity: the corrected inverse formula does not false-positive on a clean tree.
        self.build_clean_fixture()
        self.assertEqual(check_boundary.verify(), 0)

    def test_adopted_body_edit_plus_laf_hash_rewrite_fails(self):
        """H1 attack: mutate an adopted body AND rewrite only its laf_sha256 row
        to match. Rule A would pass (hash matches the new body); Rule A′ must FAIL
        because the body no longer inverts to the pinned upstream_sha256."""
        self.build_clean_fixture()
        # Mutate critic.md body + rewrite its laf_sha256 to the new (mutated) hash.
        crel = "agents/critic.md"
        p = self.tmp / crel
        p.write_text(p.read_text() + "\nMALICIOUS EDIT\n", encoding="utf-8")
        new_laf = check_boundary.sha256_text(check_boundary.read_text(p))
        self._rewrite_manifest_field(crel, "laf_sha256", new_laf)
        self.assertNotEqual(check_boundary.verify(), 0,
                            "CH-1: laf_sha256-only rewrite of an edited body MUST fail")

    def test_upstream_sha256_rewrite_of_clean_body_fails(self):
        """A forged upstream_sha256 (with an unmodified body) is caught: the body
        inverts to the real raw-upstream hash, which no longer matches the forge."""
        self.build_clean_fixture()
        self._rewrite_manifest_field("agents/critic.md", "upstream_sha256", "0" * 64)
        self.assertNotEqual(check_boundary.verify(), 0,
                            "CH-1: a forged upstream_sha256 must fail against the clean body")

    def test_writer_is_not_reanchored_in_mode_v(self):
        """ADOPTED-PATCHED writer.md does NOT get a Mode-V A′ re-anchor (its
        upstream_sha256 is the whole-raw-file hash, not reconstructible from the
        patched disk). A clean writer.md must still PASS (no false positive)."""
        self.build_clean_fixture()
        # writer.md is the only PATCHED row; verify() must still be green for it.
        self.assertEqual(check_boundary.verify(), 0)

    # ------------------------------------------------------------------
    # F2 (CH-1 doc gap, spec §4.1 acceptance bullet 2): the TWO-FIELD forgery is
    # the documented residual that Mode V CANNOT close. This test ASSERTS verify()
    # == 0 for that attack — that is CORRECT, not a bug: it documents a known,
    # accepted limitation of option (a) (re-anchoring to upstream_sha256 without
    # an upstream tree). Asserting != 0 here would be wrong — it would promise a
    # property Mode V structurally cannot deliver (the PR controls BOTH manifest
    # fields, so any manifest-only re-hash is self-consistent by construction).
    # ------------------------------------------------------------------
    def test_adopted_body_edit_plus_both_hashes_forged_PASSES_mode_v(self):
        """DOCUMENTED-RESIDUAL (F2 / spec §4.1 bullet 2): mutate an ADOPTED-CLEAN
        body AND rewrite BOTH upstream_sha256 and laf_sha256 to be self-consistent
        with the mutated body. Under option (a) this PASSES Mode V — inherent,
        because the PR controls both manifest fields.

        This is NOT a desired property; it is a known, accepted limitation. The
        backstops that catch this attack are:
          - Mode U (Rules B/C against a pinned-SHA upstream checkout): the
            mutated body diverges from the real upstream blob at the pinned SHA,
            so Rule B fails loud.
          - Branch protection: the upstream_sha256 diff is review-visible.
          - Mandatory human review of ANY upstream_sha256 diff in a PR: a field
            documented as upstream-derived must not change silently, and a
            reviewer is expected to reject a body+both-hashes change unless it
            arrives via the documented --init re-vendor flow (VENDOR.md §32-35).

        Asserting verify() == 0 here LOCKS the residual into the test suite so a
        future change cannot accidentally under-claim closure (and a future Mode-U
        CI rollout cannot silently regress without this test's comment being
        revisited)."""
        cb = check_boundary
        self.build_clean_fixture()
        crel = "agents/critic.md"
        p = self.tmp / crel
        # Mutate the adopted body.
        mutated = cb.read_text(p) + "\nMALICIOUS TWO-FIELD EDIT\n"
        p.write_text(mutated, encoding="utf-8")
        # Forge BOTH manifest fields to be self-consistent with the mutated body.
        new_upstream = cb.sha256_text(cb.prefix_unrewrite(mutated))
        new_laf = cb.sha256_text(mutated)
        self._rewrite_manifest_field(crel, "upstream_sha256", new_upstream)
        self._rewrite_manifest_field(crel, "laf_sha256", new_laf)
        # DOCUMENTED GAP: Mode V cannot detect a self-consistent two-field forge.
        rc = cb.verify()
        self.assertEqual(rc, 0,
                         "F2 documented-residual: a self-consistent two-field forge PASSES "
                         "Mode V by construction; backstops are Mode U + branch protection + "
                         "human review of upstream_sha256 diffs (see docstring).")


class WriterOnlyPatchTests(BoundaryTestBase):
    """CH-3 (M1): ADOPTED-PATCHED is reserved for agents/writer.md only — in BOTH modes."""

    def test_patched_class_off_writer_fails_mode_v(self):
        self.build_clean_fixture()
        # Reclass critic.md (an ADOPTED-CLEAN row) as ADOPTED-PATCHED.
        cb = check_boundary
        txt = cb.VENDOR_MD.read_text(encoding="utf-8")
        txt2 = txt.replace("| agents/critic.md | ADOPTED-CLEAN |",
                           "| agents/critic.md | ADOPTED-PATCHED |")
        cb.VENDOR_MD.write_text(txt2, encoding="utf-8")
        self.assertNotEqual(check_boundary.verify(), 0,
                            "CH-3 Mode V: non-writer ADOPTED-PATCHED must fail")

    def test_patched_class_off_writer_fails_mode_u(self):
        # Same check under Mode U (with a fixture upstream dir) — must still fail
        # because the C′ constraint runs outside the `if upstream_dir:` block.
        self.build_clean_fixture()
        cb = check_boundary
        txt = cb.VENDOR_MD.read_text(encoding="utf-8")
        txt2 = txt.replace("| agents/critic.md | ADOPTED-CLEAN |",
                           "| agents/critic.md | ADOPTED-PATCHED |")
        cb.VENDOR_MD.write_text(txt2, encoding="utf-8")
        # Build a minimal upstream tree mirroring the fixture's adopted paths.
        up = self.tmp / "_upstream" / "cw"
        up.mkdir(parents=True)
        for rel in ("agents/critic.md", "agents/editor.md", "agents/reader-sim.md",
                    "agents/continuity-checker.md"):
            body = check_boundary.prefix_unrewrite(check_boundary.read_text(self.tmp / rel))
            (up / rel).parent.mkdir(parents=True, exist_ok=True)
            (up / rel).write_text(body, encoding="utf-8")
        rc = check_boundary.verify(str(self.tmp / "_upstream"))
        self.assertNotEqual(rc, 0, "CH-3 Mode U: non-writer ADOPTED-PATCHED must fail")


class ResourcesCoverageTests(BoundaryTestBase):
    """CH-2 (H2): adopted skills' resources/** must be manifest-covered."""

    def test_adopted_resource_row_deleted_fails(self):
        # Build clean fixture, then DELETE the adopted skill's resources row.
        self.build_clean_fixture()
        cb = check_boundary
        txt = cb.VENDOR_MD.read_text(encoding="utf-8")
        # Remove the line for skills/sample/resources/note.md (an adopted resource).
        kept = [ln for ln in txt.splitlines()
                if "| skills/sample/resources/note.md |" not in ln]
        cb.VENDOR_MD.write_text("\n".join(kept) + "\n", encoding="utf-8")
        # The file still exists on disk but is no longer manifested → must FAIL.
        self.assertNotEqual(check_boundary.verify(), 0,
                            "CH-2: deleted adopted-resource row must fail")
        # Confirm the specific error is the Rule F′ message.
        rc_err = self._capture_verify_stderr()
        self.assertIn("adopted-skill file not in VENDOR.md manifest", rc_err)

    def test_untracked_adopted_resource_fails(self):
        # Drop a NEW untracked .md into the adopted skill's resources/ tree.
        self.build_clean_fixture()
        self.write_file("skills/sample/resources/sneaky.md", "# untracked\n")
        self.assertNotEqual(check_boundary.verify(), 0,
                            "CH-2: untracked file under an adopted skill must fail")

    def _capture_verify_stderr(self):
        import io, contextlib
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            check_boundary.verify()
        return err.getvalue()


# --- Phase-4: CH-5 Mode-U HEAD pin + CH-7 prefix-rewrite positive --------------
class PrefixRewritePositiveTest(unittest.TestCase):
    """CH-7 (M5), Option M5-A: exercise Rule B's prefix-rewrite path with a
    positive test. Every real ADOPTED-CLEAN skill row is a no-op rewrite (no
    `creative-writing-skills:` literal), so the rewrite machinery has no positive
    coverage. This constructs a synthetic literal-bearing upstream blob and proves
    sha256(prefix_rewrite(upstream)) is the hash that satisfies Rule B."""

    def test_prefix_rewrite_positive(self):
        cb = check_boundary
        raw_upstream = ("---\nname: synth\n---\n# synth\n"
                        "invoke creative-writing-skills:craft for prose.\n")
        self.assertIn("creative-writing-skills:", raw_upstream)
        rewritten = cb.prefix_rewrite(raw_upstream)
        self.assertNotEqual(raw_upstream, rewritten,
                            "prefix_rewrite must transform a literal-bearing blob")
        self.assertNotIn("creative-writing-skills:", rewritten)
        self.assertIn("laf-adaptation:", rewritten)
        # Rule B equality: laf_sha256 of the vendored file == sha256(prefix_rewrite(raw)).
        laf_sha = cb.sha256_text(rewritten)
        self.assertEqual(cb.sha256_text(cb.prefix_rewrite(raw_upstream)), laf_sha)
        # And it FAILS if the rewrite is skipped (the whole point of M5).
        self.assertNotEqual(cb.sha256_text(raw_upstream), laf_sha,
                            "skipping the rewrite must NOT satisfy Rule B")


class ModeUHeadPinTests(BoundaryTestBase):
    """CH-5 (M3): Mode U asserts the --upstream checkout's HEAD == pinned upstream_sha."""

    def _make_git_checkout(self, pinned_sha):
        """Create a real tmp git repo at _upstream/cw mirroring the fixture's adopted
        paths, with HEAD at pinned_sha. Returns the upstream_dir path."""
        import subprocess
        up_root = self.tmp / "_upstream"
        cw = up_root / "cw"
        cw.mkdir(parents=True)
        # Populate cw/ with inverse-rewritten (raw-upstream) bodies for adopted paths.
        for rel in ("agents/critic.md", "agents/editor.md", "agents/reader-sim.md",
                    "agents/continuity-checker.md", "agents/writer.md"):
            body = check_boundary.prefix_unrewrite(check_boundary.read_text(self.tmp / rel))
            (cw / rel).parent.mkdir(parents=True, exist_ok=True)
            (cw / rel).write_text(body, encoding="utf-8")
        # git init + commit + record HEAD.
        subprocess.run(["git", "init", "-q"], cwd=str(up_root), check=True)
        subprocess.run(["git", "config", "user.email", "t@t"], cwd=str(up_root), check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=str(up_root), check=True)
        subprocess.run(["git", "add", "-A"], cwd=str(up_root), check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=str(up_root), check=True)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(up_root),
                              capture_output=True, text=True, check=True).stdout.strip()
        if pinned_sha == "MATCH":
            pinned_sha = head
        return str(up_root), head, pinned_sha

    def test_upstream_wrong_sha_fails(self):
        self.build_clean_fixture()
        upstream_dir, head, _ = self._make_git_checkout("MATCH")
        # Pin to a WRONG sha (not HEAD).
        rc = check_boundary.verify(upstream_dir, upstream_sha="0" * 40)
        self.assertNotEqual(rc, 0, "Mode U at the wrong SHA must FAIL")
        err = self._capture_verify_stderr_for(lambda: check_boundary.verify(upstream_dir, upstream_sha="0" * 40))
        self.assertIn("HEAD", err)

    def test_upstream_matching_sha_passes_head_check(self):
        # Build fixture whose manifest upstream_sha pins to the checkout HEAD.
        self.build_clean_fixture()
        upstream_dir, head, pinned = self._make_git_checkout("MATCH")
        # Rewrite VENDOR.md upstream_sha: header to the real HEAD.
        cb = check_boundary
        lines = cb.VENDOR_MD.read_text(encoding="utf-8").splitlines()
        out = [("upstream_sha:  " + head) if ln.strip().lower().startswith("upstream_sha:")
               else ln for ln in lines]
        cb.VENDOR_MD.write_text("\n".join(out) + "\n", encoding="utf-8")
        # The HEAD-pin check must pass (Rules B/C may still surface fixture issues,
        # but the CH-5 HEAD-mismatch error must NOT be among them). Assert "HEAD" is
        # absent from the ENTIRE stderr stream, not just the preamble before the
        # "BOUNDARY CONTRACT" banner — a HEAD-mismatch violation would appear in the
        # post-banner violation list, so limiting the check to split("BOUNDARY")[0]
        # (the always-empty preamble) would false-pass on a regression.
        err = self._capture_verify_stderr_for(lambda: check_boundary.verify(upstream_dir))
        self.assertNotIn("HEAD", err,
                         "CH-5 HEAD-mismatch error must NOT fire when HEAD == pinned SHA; "
                         f"full stderr was:\n{err}")

    def _capture_verify_stderr_for(self, fn):
        import io, contextlib
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            fn()
        return err.getvalue()


# --- Phase-6 (F1/F3): re-vendor header rewrite + tarball/no-git fallback --------
class InitReVendorTests(BoundaryTestBase):
    """F1 (CRITICAL): the documented `--init --upstream <checkout>` re-vendor flow
    (VENDOR.md lines 32-35) MUST succeed. Pre-fix bug: do_init() wrote manifest
    rows but not the upstream_sha: header, so CH-5's post-write HEAD-pin compared
    the NEW checkout HEAD against the STALE OLD pin → exit 1 on a legitimate
    re-vendor. Fix: do_init() now rewrites the header to _checkout_head(upstream)
    (falling back to --upstream-sha) BEFORE the verify() call."""

    def _make_upstream_git_checkout(self):
        """Create a tmp git repo at _upstream/cw mirroring the fixture's adopted
        paths (raw-upstream bodies), commit, and return (upstream_dir, head_sha)."""
        import subprocess
        up_root = self.tmp / "_upstream"
        cw = up_root / "cw"
        cw.mkdir(parents=True)
        # Quartet (ADOPTED-CLEAN) raw-upstream bodies.
        for name in _QUARTET:
            rel = f"agents/{name}.md"
            body = check_boundary.prefix_unrewrite(check_boundary.read_text(self.tmp / rel))
            (cw / rel).parent.mkdir(parents=True, exist_ok=True)
            (cw / rel).write_text(body, encoding="utf-8")
        # writer.md raw-upstream body (ADOPTED-PATCHED).
        wrel = "agents/writer.md"
        body = check_boundary.prefix_unrewrite(check_boundary.read_text(self.tmp / wrel))
        (cw / wrel).parent.mkdir(parents=True, exist_ok=True)
        (cw / wrel).write_text(body, encoding="utf-8")
        # Adopted skill raw-upstream bodies.
        for rel in ("skills/sample/SKILL.md", "skills/sample/resources/note.md"):
            body = check_boundary.prefix_unrewrite(check_boundary.read_text(self.tmp / rel))
            (cw / rel).parent.mkdir(parents=True, exist_ok=True)
            (cw / rel).write_text(body, encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=str(up_root), check=True)
        subprocess.run(["git", "config", "user.email", "t@t"], cwd=str(up_root), check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=str(up_root), check=True)
        subprocess.run(["git", "add", "-A"], cwd=str(up_root), check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=str(up_root), check=True)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(up_root),
                              capture_output=True, text=True, check=True).stdout.strip()
        return str(up_root), head

    def test_init_revendor_updates_upstream_sha_header(self):
        """Regression: --init against a git checkout MUST (a) exit 0 and (b) rewrite
        the VENDOR.md `upstream_sha:` header to the checkout's HEAD. Pre-fix this
        exited 1 with a spurious HEAD-mismatch."""
        cb = check_boundary
        self.build_clean_fixture()
        # Stamp a STALE header pin (simulate the prior upstream_sha from an older
        # vendor) — the re-vendor must overwrite it with the new HEAD.
        stale = "0" * 40
        lines = cb.VENDOR_MD.read_text(encoding="utf-8").splitlines()
        out = [("upstream_sha:  " + stale) if ln.strip().lower().startswith("upstream_sha:")
               else ln for ln in lines]
        cb.VENDOR_MD.write_text("\n".join(out) + "\n", encoding="utf-8")
        upstream_dir, head = self._make_upstream_git_checkout()
        self.assertNotEqual(stale, head, "fixture sanity: HEAD must differ from stale pin")
        # Run the documented re-vendor flow.
        rc = cb.do_init(upstream_dir)
        self.assertEqual(rc, 0,
                         "F1: legitimate re-vendor MUST exit 0; pre-fix it spuriously "
                         "failed at CH-5 HEAD-pin against the stale prior pin")
        # Assert the header was rewritten to the checkout HEAD.
        header_now = cb.parse_upstream_sha(cb.read_text(cb.VENDOR_MD))
        self.assertEqual(header_now, head,
                         "F1: do_init must rewrite upstream_sha: header to the checkout HEAD")

    def test_init_revendor_with_explicit_sha_flag(self):
        """Tarball/no-git variant: --init with --upstream-sha (no git HEAD) MUST
        still rewrite the header to the explicit pin and exit 0 (F1 + F3
        composition: F3 skips the HEAD-unreadable error, F1 still updates the
        header from the explicit pin)."""
        cb = check_boundary
        self.build_clean_fixture()
        # Non-git upstream checkout (no .git) — _checkout_head returns None.
        up_root = self.tmp / "_tarball_upstream"
        cw = up_root / "cw"
        cw.mkdir(parents=True)
        for name in _QUARTET:
            rel = f"agents/{name}.md"
            body = cb.prefix_unrewrite(cb.read_text(self.tmp / rel))
            (cw / rel).parent.mkdir(parents=True, exist_ok=True)
            (cw / rel).write_text(body, encoding="utf-8")
        wrel = "agents/writer.md"
        body = cb.prefix_unrewrite(cb.read_text(self.tmp / wrel))
        (cw / wrel).parent.mkdir(parents=True, exist_ok=True)
        (cw / wrel).write_text(body, encoding="utf-8")
        for rel in ("skills/sample/SKILL.md", "skills/sample/resources/note.md"):
            body = cb.prefix_unrewrite(cb.read_text(self.tmp / rel))
            (cw / rel).parent.mkdir(parents=True, exist_ok=True)
            (cw / rel).write_text(body, encoding="utf-8")
        explicit = "1" * 40
        rc = cb.do_init(str(up_root), upstream_sha=explicit)
        self.assertEqual(rc, 0,
                         "F1+F3: --init on a tarball checkout with explicit --upstream-sha "
                         "MUST exit 0")
        header_now = cb.parse_upstream_sha(cb.read_text(cb.VENDOR_MD))
        self.assertEqual(header_now, explicit,
                         "F1: do_init must rewrite upstream_sha: header to the explicit pin "
                         "when the checkout has no readable HEAD")


class TarballModeUTests(BoundaryTestBase):
    """F3 (MINOR): when _checkout_head returns None (no git) BUT an explicit
    --upstream-sha was supplied, verify() must SKIP the HEAD-unreadable error
    (operator has asserted the pin explicitly); only fail-loud when there's no
    explicit pin AND no readable HEAD. Security stance preserved: the pin is an
    operator assertion, and Rules B/C still run against the supplied tree."""

    def test_mode_u_tarball_with_explicit_sha_skips_head_check(self):
        cb = check_boundary
        self.build_clean_fixture()
        # Non-git upstream checkout (no .git).
        up_root = self.tmp / "_tarball_upstream"
        cw = up_root / "cw"
        cw.mkdir(parents=True)
        for name in _QUARTET + ["writer"]:
            rel = f"agents/{name}.md"
            body = cb.prefix_unrewrite(cb.read_text(self.tmp / rel))
            (cw / rel).parent.mkdir(parents=True, exist_ok=True)
            (cw / rel).write_text(body, encoding="utf-8")
        for rel in ("skills/sample/SKILL.md", "skills/sample/resources/note.md"):
            body = cb.prefix_unrewrite(cb.read_text(self.tmp / rel))
            (cw / rel).parent.mkdir(parents=True, exist_ok=True)
            (cw / rel).write_text(body, encoding="utf-8")
        explicit = "deadbeef" * 5  # 40 hex
        # verify() with --upstream-sha on a non-git tree: the HEAD-unreadable error
        # must NOT fire. (Rules B/C still run; any blob mismatch would surface
        # independently, which is exactly the design.)
        import io, contextlib
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = cb.verify(str(up_root), upstream_sha=explicit)
        err_text = err.getvalue()
        self.assertNotIn("could not read HEAD", err_text,
                         "F3: explicit --upstream-sha must skip the HEAD-unreadable error; "
                         f"stderr was:\n{err_text}")
        # Confirm _checkout_head genuinely returns None here (fixture sanity).
        self.assertIsNone(cb._checkout_head(str(up_root)),
                          "fixture sanity: the tarball upstream must NOT be a git repo")


class GlobSafetyTests(BoundaryTestBase):
    """H1: glob rows are restricted to NATIVE/BUILD-NEW skill roots of the exact
    form 'skills/<name>/**'. A hand-edited 'agents/**' or adopted-path glob would
    let an adopted file be "manifest-covered" by a non-hash row, silently dropping
    its hash protection (Rule A only hash-checks is_adopted rows; Rule D protects
    only the quartet). The parse-time gate (parse_manifest) is the real guard;
    manifest_covers() is belt-and-suspenders (Item 1.2)."""

    H64 = "0" * 64  # 64-hex placeholder for adopted-row hash cells

    def _append_row(self, raw_row_line):
        """Stamp a clean fixture, then append ONE raw row line to the manifest."""
        self.build_clean_fixture()
        txt = check_boundary.VENDOR_MD.read_text(encoding="utf-8")
        check_boundary.VENDOR_MD.write_text(txt.rstrip() + "\n" + raw_row_line + "\n",
                                            encoding="utf-8")

    def _capture_verify_stderr(self):
        import io, contextlib
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            check_boundary.verify()
        return err.getvalue()

    def test_agents_glob_rejected(self):
        # A glob row under agents/ (not skills/) must fail loud at parse time.
        self._append_row("| agents/** | NATIVE | — | — |")
        _, errors = check_boundary.parse_manifest(
            check_boundary.read_text(check_boundary.VENDOR_MD))
        self.assertTrue(
            any(("glob" in e and "skills" in e) or "under skills" in e for e in errors),
            f"agents/** glob must be rejected (must be under skills/): {errors}")
        # And the verify gate fails on it (not a silent PASS).
        self.assertNotEqual(check_boundary.verify(), 0,
                            "verify must FAIL on an agents/** glob row")

    def test_adopted_glob_rejected(self):
        # An ADOPTED-class glob row must fail loud (adopted files need exact hash rows).
        self._append_row(f"| agents/writer.md/** | ADOPTED-CLEAN | {self.H64} | {self.H64} |")
        _, errors = check_boundary.parse_manifest(
            check_boundary.read_text(check_boundary.VENDOR_MD))
        self.assertTrue(any("cannot be ADOPTED" in e for e in errors),
                        f"ADOPTED-class glob must be rejected: {errors}")
        self.assertNotEqual(check_boundary.verify(), 0,
                            "verify must FAIL on an ADOPTED-class glob row")

    def test_bare_skills_glob_rejected(self):
        """Regression (QA Phase-1 finding): 'skills/**' (no <name> segment) starts
        with 'skills/' so the prefix-only check accepted it — but it covers EVERY
        skill dir including adopted ones, re-opening the exact H1 silent-coverage
        hole that the gate exists to close. The gate must require a single-level
        '<name>' segment ('skills/<name>/**')."""
        self._append_row("| skills/** | NATIVE | — | — |")
        _, errors = check_boundary.parse_manifest(
            check_boundary.read_text(check_boundary.VENDOR_MD))
        self.assertTrue(
            any("skills/<name>/**" in e for e in errors),
            f"skills/** (no name segment) must be rejected — covers adopted skills: {errors}")
        self.assertNotEqual(check_boundary.verify(), 0,
                            "verify must FAIL on a bare skills/** glob row")

    def test_broad_glob_does_not_cover_adopted(self):
        """An adopted agent whose exact row is dropped in favor of an (illegal)
        agents/** glob must NOT silently PASS. Either the parse-time glob error or
        the Rule F 'not in manifest' error fires — either way verify() != 0."""
        self.build_clean_fixture()
        cb = check_boundary
        txt = cb.VENDOR_MD.read_text(encoding="utf-8")
        # Remove the exact adopted row for agents/critic.md, then add an illegal
        # agents/** glob in its place (the shape a confused editor might produce).
        kept = [ln for ln in txt.splitlines()
                if "| agents/critic.md |" not in ln]
        kept.append("| agents/** | NATIVE | — | — |")
        cb.VENDOR_MD.write_text("\n".join(kept) + "\n", encoding="utf-8")
        rc = check_boundary.verify()
        self.assertNotEqual(rc, 0,
                            "H1: an adopted agent 'covered' only by an illegal agents/** "
                            "glob must FAIL, not silently PASS")
        # Confirm the failure names either the glob violation or the not-manifested agent.
        err = self._capture_verify_stderr()
        self.assertTrue(
            "agents/**" in err or "agents/critic.md" in err,
            f"failure must reference the illegal glob or the unprotected agent: {err}")


class CRLFNormalizationTests(unittest.TestCase):
    """M2 (Option B): the boundary contract is TEXT-NORMALIZED (LF), not byte-accurate.
    Path.read_text (newline=None) normalizes CRLF->LF before hashing, so CRLF and LF
    versions of the same content produce identical laf_sha256. This is INTENDED —
    the contract hashes the LF-normalized form. This test PINS that behavior so a
    future change to byte-level hashing (Option A) is a deliberate, manifest-wide
    rehash, not an accident. See VENDOR.md 'Hash semantics'."""

    def test_crlf_and_lf_hash_identically_under_text_pipeline(self):
        tmp = Path(tempfile.mkdtemp(prefix="crlf_test_"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        content = b"---\nname: x\n---\nbody line 1\nbody line 2\n"
        (tmp / "lf.md").write_bytes(content)
        (tmp / "crlf.md").write_bytes(content.replace(b"\n", b"\r\n"))
        self.assertEqual(
            check_boundary.sha256_text(check_boundary.read_text(tmp / "lf.md")),
            check_boundary.sha256_text(check_boundary.read_text(tmp / "crlf.md")),
            "text pipeline must LF-normalize (M2 Option B contract)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
