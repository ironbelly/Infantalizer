#!/usr/bin/env python3
"""check_boundary.py — the ONLY script in laf-adaptation/ (ADR-006: this is a
validation tool, NOT a runtime). It enforces the boundary contract between the
ADOPTED upstream CWS subset and LAF's NATIVE / BUILD-NEW additions.

It never transforms the framework — it only reads files, computes sha256 hashes,
and compares (boundary-contract.md §3, lines 18-19). The one transformation it
*models* (never writes) is the deterministic prefix rewrite
    "creative-writing-skills:" -> "laf-adaptation:"

Modes (boundary-contract.md §3.1):
    check_boundary.py                       # verify (default); exit 1 on any violation
    check_boundary.py --init --upstream DIR # first vendor: compute hashes, write manifest rows
    check_boundary.py --report              # human-readable provenance summary; always exit 0

Path rooting: all relative paths resolve against REPO = Path(__file__).resolve().parents[1]
(the laf-adaptation/ dir), so `glob("agents/*.md")` is correct no matter the caller's cwd —
the task invokes this from the repo root as `uv run python laf-adaptation/scripts/check_boundary.py`
(boundary-contract.md §3.2 uses relative globs; this rooting makes them unambiguous).

Pure standard library only (no third-party deps — ADR-006 forbids a runtime).
"""

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

# --- Path rooting (Step 2.2 cwd-rooting contract) -------------------------------
REPO = Path(__file__).resolve().parents[1]          # the laf-adaptation/ dir
VENDOR_MD = REPO / "VENDOR.md"

# --- The deterministic prefix rewrite -------------------------------------------
PREFIX_FROM = "creative-writing-skills:"
PREFIX_TO = "laf-adaptation:"

# --- Provenance of LAF-authored (non-upstream) files ----------------------------
# Adopted files are auto-detected by presence in the upstream checkout. The files
# below do NOT exist upstream; this closed set (DESIGN reconciled counts,
# constraint #8) lets --init label NATIVE vs BUILD-NEW deterministically. An
# existing manifest row's class is ALWAYS preserved over this map (manifest is the
# source of truth); the map only classifies newly-discovered non-upstream files.
NATIVE_AGENTS = {"analyst.md", "safety-verifier.md"}
BUILD_NEW_AGENTS = {"chronicler.md", "tier-coordinator.md"}
NATIVE_SKILLS = {"adaptation-tiers", "adaptation-rules", "source-fidelity"}
BUILD_NEW_SKILLS = {"adaptation-safety"}

QUARTET = ["critic", "editor", "reader-sim", "continuity-checker"]
NO_HASH = "—"  # em dash marks a non-hash-pinned (NATIVE/BUILD-NEW) row

# Manifest row classes (CH-6): a parser-validated closed set.
CLASSES = {"ADOPTED-CLEAN", "ADOPTED-PATCHED", "NATIVE", "BUILD-NEW"}


class ManifestError(ValueError):
    """Raised when a manifest row is malformed, unsafe, or self-inconsistent.

    The parser collects these into the errors list (verify/do_init treat them as
    boundary-contract FAIL; --report prints them as warnings but still exits 0)."""


# --- Low-level helpers ----------------------------------------------------------
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def read_bytes(p: Path) -> bytes:
    return p.read_bytes()


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def prefix_rewrite(text: str) -> str:
    """The one permitted vendor-time transform, recomputed (never trusted from a
    stored diff): replace every literal 'creative-writing-skills:' with
    'laf-adaptation:'."""
    return text.replace(PREFIX_FROM, PREFIX_TO)


def prefix_unrewrite(text: str) -> str:
    """Inverse of prefix_rewrite: 'laf-adaptation:' -> 'creative-writing-skills:'.

    Used by verify-mode Rule A′ (CH-1) to re-derive the RAW upstream blob from an
    already-prefix-rewritten on-disk adopted body, so its hash can be compared
    against the pinned (PR-rewrite-resistant) `upstream_sha256`. The on-disk file
    IS the prefix-rewritten upstream (disk == prefix_rewrite(raw_upstream)), so
    prefix_unrewrite(disk) == raw_upstream for ADOPTED-CLEAN rows. For files
    containing no prefix literal this is a no-op (disk == raw)."""
    return text.replace(PREFIX_TO, PREFIX_FROM)


def split_frontmatter(text: str):
    """Return (frontmatter_lines, body_text). Frontmatter is between the first two
    '---' delimiter lines; body is everything after the second '---'
    (boundary-contract.md §3.3)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = lines[1:i]
            body = "\n".join(lines[i + 1:])
            return fm, body
    return [], text  # malformed frontmatter → treat as no frontmatter


def body_of(text: str) -> str:
    return split_frontmatter(text)[1]


def frontmatter_line_diff(up_text: str, cur_text: str):
    """Line-level added/removed on the YAML frontmatter only, after prefix
    normalization. ORDER-INSENSITIVE for skills-list entries (set semantics),
    which also correctly handles writer.md's preserved duplicate
    'creative-writing-craft' line (boundary-contract.md §3.3)."""
    up_fm = {ln.rstrip() for ln in split_frontmatter(up_text)[0] if ln.strip()}
    cur_fm = {ln.rstrip() for ln in split_frontmatter(cur_text)[0] if ln.strip()}
    added = sorted(cur_fm - up_fm)
    removed = sorted(up_fm - cur_fm)
    return added, removed


# --- Upstream dereference (only when --upstream DIR is provided) -----------------
def upstream_root(upstream_dir: str) -> Path:
    return Path(upstream_dir).resolve() / "cw"


def upstream_path(upstream_dir: str, rel: str) -> Path:
    return upstream_root(upstream_dir) / rel


def upstream_has(upstream_dir: str, rel: str) -> bool:
    return upstream_path(upstream_dir, rel).exists()


def upstream_blob(upstream_dir: str, rel: str) -> str:
    return read_text(upstream_path(upstream_dir, rel))


def _checkout_head(upstream_dir: str):
    """Read the HEAD commit SHA of the --upstream checkout (CH-5, M3). Returns the
    40-hex SHA, or None if git is unavailable or the dir is not a git repo (e.g. a
    tarball checkout) — caller then FAILs loud rather than trusting the tree.
    `subprocess` is stdlib; only invoked in Mode U."""
    try:
        out = subprocess.run(
            ["git", "-C", str(Path(upstream_dir).resolve()), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True, timeout=10)
        head = out.stdout.strip()
        return head or None
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None


# --- VENDOR.md manifest parsing -------------------------------------------------
class Row:
    __slots__ = ("path", "cls", "upstream_sha256", "laf_sha256")

    def __init__(self, path, cls, up, laf):
        self.path = path
        self.cls = cls
        self.upstream_sha256 = up
        self.laf_sha256 = laf

    @property
    def is_adopted(self):
        return self.cls in ("ADOPTED-CLEAN", "ADOPTED-PATCHED")

    @property
    def is_glob(self):
        return self.path.endswith("/**")


def _norm_hash(cell: str) -> str:
    cell = cell.strip()
    if cell in ("", "-", "--", NO_HASH, "<hash>"):
        return NO_HASH
    return cell


def _is_hex64(c: str) -> bool:
    """True iff c is a 64-char lowercase/uppercase hex string (a sha256 digest)."""
    return len(c) == 64 and all(ch in "0123456789abcdef" for ch in c.lower())


def _safe_repo_path(rel: str) -> Path:
    """Resolve a manifest path relative to REPO and refuse escapes (CH-4, M2).

    A literal `|` inside a path is impossible here (the parser splits on `|`
    and rejects rows that don't yield exactly 4 cells — see parse_manifest), so
    the only escape vectors are absolute paths and `..` traversal. Both resolve
    outside REPO and are rejected as ManifestError. REPO is resolved (absolute)
    so a symlinked work-tree cannot smuggle a path back inside.

    A manifest entry that resolves to REPO itself (`.` or an empty path) is also
    rejected: such a row is never a legitimate file (it would crash read_text on
    the directory in Rules A/C), so we fail loud at the parser boundary rather
    than letting an IsADirectoryError escape mid-rule."""
    if rel.strip() == "" or rel.strip() == ".":
        raise ManifestError(f"{rel!r}: manifest path is empty or REPO itself — must name a file")
    if Path(rel).is_absolute():
        raise ManifestError(f"{rel!r}: manifest path is absolute — must be relative to laf-adaptation/")
    resolved = (REPO / rel).resolve()
    repo_resolved = REPO.resolve()
    # Containment: resolved must be STRICTLY under REPO (a child, not REPO itself).
    # The `resolved == repo_resolved` case is rejected above for non-empty/non-dot
    # inputs too, because a `..` chain that lands exactly on REPO is not a file.
    if resolved == repo_resolved or repo_resolved not in resolved.parents:
        raise ManifestError(f"{rel!r}: manifest path escapes laf-adaptation/ tree")
    return resolved


def parse_manifest(text: str):
    """Parse the 4-column manifest table (path | class | upstream_sha256 |
    laf_sha256). Returns (rows, errors) where errors is a list[str] of
    malformed / duplicate / bad-hash / unsafe-path findings (CH-6, M4 + CH-4, M2).

    A security-boundary parser must FAIL LOUD: a silently-dropped row would
    un-protect its file. Header/separator rows are still skipped silently. A
    literal `|` inside a path/hash shifts columns → the row yields ≠4 cells →
    loud failure (paths/hashes must not contain `|`; documented in VENDOR.md)."""
    rows, errors = [], []
    seen_paths = {}  # path -> first lineno (duplicate detection)
    for lineno, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) != 4:
            errors.append(f"manifest line {lineno}: expected 4 cells, got {len(cells)}: {s!r}")
            continue
        path, cls = cells[0], cells[1]
        # Header / separator-row detection. Must be PRECISE: a silently-dropped
        # data row un-protects its file (CH-6 principle). The only legitimate
        # non-data rows are (a) the exact 'path' header and (b) the all-dashes
        # separator ('---', non-empty, dashes only). Anything else — including
        # an empty path cell, a single space, or ':'-only — is a malformed data
        # row and must fail loud. The previous `set(path) <= set("-: ")` test
        # admitted the empty string (set() is a subset of every set), silently
        # swallowing empty-path rows.
        is_header = path.lower() == "path"
        is_separator = len(path) >= 1 and set(path) <= {"-"}
        if is_header or is_separator:
            continue
        if cls.upper() not in CLASSES:
            errors.append(f"manifest line {lineno}: unknown class {cls!r}")
            continue
        if path in seen_paths:
            errors.append(f"manifest line {lineno}: duplicate path {path!r} (first at line {seen_paths[path]})")
            continue
        seen_paths[path] = lineno
        # Path safety (CH-4): reject absolute / escaping paths loud, not silent.
        try:
            _safe_repo_path(path)
        except ManifestError as e:
            errors.append(f"manifest line {lineno}: {e}")
            continue
        up, laf = _norm_hash(cells[2]), _norm_hash(cells[3])
        if cls.upper() in ("ADOPTED-CLEAN", "ADOPTED-PATCHED"):
            if not _is_hex64(up) or not _is_hex64(laf):
                errors.append(f"manifest line {lineno}: {path!r} adopted row needs 64-hex hashes")
                continue
        else:  # NATIVE / BUILD-NEW
            if up != NO_HASH or laf != NO_HASH:
                errors.append(f"manifest line {lineno}: {path!r} {cls.upper()} row must have {NO_HASH} hashes")
                continue
        # Glob-shape gate (H1): glob rows are reserved for NATIVE/BUILD-NEW skill
        # roots of the EXACT form 'skills/<name>/**' — a single non-empty skill
        # name segment. A hand-edited 'agents/**', root-level '/**', or
        # adopted-path glob would let an adopted file be "manifest-covered" by a
        # non-hash row, silently dropping its hash protection (Rule A only
        # hash-checks is_adopted rows; Rule D protects only the quartet). The
        # prefix check alone ('startswith skills/') is NOT sufficient: 'skills/**'
        # (no name segment) would cover EVERY skill dir including adopted ones,
        # re-opening the same silent-coverage hole as 'agents/**'. The
        # '<name>' segment must be present and single-level (never 'skills/a/b/**',
        # which --init never emits).
        if path.endswith("/**"):
            if cls.upper() in ("ADOPTED-CLEAN", "ADOPTED-PATCHED"):
                errors.append(f"manifest line {lineno}: glob row {path!r} cannot be "
                              f"ADOPTED (adopted files need exact hash rows)")
                continue
            glob_prefix = path[:-3]  # strip the trailing '/**'
            if not glob_prefix.startswith("skills/") or glob_prefix.count("/") != 1:
                errors.append(f"manifest line {lineno}: glob row {path!r} must be exactly "
                              f"'skills/<name>/**' (a single skill name; bare 'skills/**' "
                              f"would cover adopted skills too)")
                continue
        rows.append(Row(path, cls.upper(), up, laf))
    return rows, errors


def parse_upstream_sha(text: str):
    """Read the `upstream_sha:` field from the VENDOR.md header (CH-5, M3).

    Returns the SHA string or None if unset/unparseable. The manifest table
    parser ignores header lines; this re-reads the header prose for the pin.
    The em-dash NO_HASH placeholder and empty/whitespace values are treated as
    'unset' (return None) — otherwise a header `upstream_sha: —` would be
    treated as a truthy pin and produce a misleading HEAD-mismatch error
    instead of the clearer 'no pin' failure."""
    for line in text.splitlines():
        s = line.strip()
        if s.lower().startswith("upstream_sha:") and ":" in s:
            val = s.split(":", 1)[1].strip()
            if val and val != NO_HASH:
                return val
    return None


def manifest_covers(rows, rel: str) -> bool:
    for r in rows:
        if r.path == rel:
            return True
        if r.is_glob and rel.startswith(r.path[:-2]) and not r.is_adopted:
            # 'skills/x/**' covers 'skills/x/...' — adopted files require exact hash rows
            return True
    return False


# --- Discovery of on-disk files -------------------------------------------------
def disk_agents():
    d = REPO / "agents"
    return sorted(f.relative_to(REPO).as_posix() for f in d.glob("*.md")) if d.is_dir() else []


def disk_skill_dirs():
    d = REPO / "skills"
    return sorted([p for p in d.iterdir() if p.is_dir()]) if d.is_dir() else []


def disk_skill_files(skill_dir: Path):
    return sorted(f.relative_to(REPO).as_posix() for f in skill_dir.rglob("*") if f.is_file())


def disk_skill_skillmds():
    d = REPO / "skills"
    return sorted(f.relative_to(REPO).as_posix() for f in d.glob("**/SKILL.md")) if d.is_dir() else []


# --- Classification (for --init) ------------------------------------------------
def classify(rel: str, declared: dict, upstream_dir):
    if rel in declared:
        return declared[rel]
    if upstream_dir and upstream_has(upstream_dir, rel):
        if rel == "agents/writer.md":
            return "ADOPTED-PATCHED"
        return "ADOPTED-CLEAN"  # skills + other agents vendor clean; Rule B validates
    # non-upstream → LAF-authored
    name = rel.split("/")[-1]
    parts = rel.split("/")
    if parts[0] == "agents":
        if name in BUILD_NEW_AGENTS:
            return "BUILD-NEW"
        return "NATIVE"
    if parts[0] == "skills" and len(parts) >= 2:
        sk = parts[1]
        if sk in BUILD_NEW_SKILLS:
            return "BUILD-NEW"
        return "NATIVE"
    return "NATIVE"


# --- --init: compute hashes + (re)write manifest rows ---------------------------
def do_init(upstream_dir: str, upstream_sha=None):
    if not upstream_dir:
        print("ERROR: --init requires --upstream <dir> (a checkout of the upstream repo "
              "at upstream_sha) to record upstream_sha256 and prove the prefix rewrite is "
              "the only transformation.", file=sys.stderr)
        return 2
    if not upstream_root(upstream_dir).is_dir():
        print(f"ERROR: --upstream {upstream_dir!r} has no cw/ subtree at "
              f"{upstream_root(upstream_dir)}", file=sys.stderr)
        return 2
    if not VENDOR_MD.exists():
        print(f"ERROR: {VENDOR_MD} not found — author the VENDOR.md header + Manifest "
              f"table header first (Step 2.12).", file=sys.stderr)
        return 2

    vendor_text = read_text(VENDOR_MD)
    existing_rows, manifest_errors = parse_manifest(vendor_text)
    if manifest_errors:
        print(f"ERROR: VENDOR.md manifest is malformed — refusing to --init:",
              file=sys.stderr)
        for e in manifest_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    declared = {r.path: r.cls for r in existing_rows}

    rows = []          # (path, cls, upstream_sha256, laf_sha256)
    warnings = []

    # Agents — one row per file
    for rel in disk_agents():
        cls = classify(rel, declared, upstream_dir)
        if cls in ("ADOPTED-CLEAN", "ADOPTED-PATCHED"):
            up_raw = upstream_blob(upstream_dir, rel)
            up_sha = sha256_text(up_raw)
            laf_sha = sha256_text(read_text(_safe_repo_path(rel)))
            rows.append((rel, cls, up_sha, laf_sha))
        else:
            rows.append((rel, cls, NO_HASH, NO_HASH))

    # Skills — adopted: per-file rows (SKILL.md + resources/**); native/build-new: one /** row
    for skdir in disk_skill_dirs():
        sk = skdir.name
        skill_rel = f"skills/{sk}"
        adopted = bool(upstream_dir) and upstream_root(upstream_dir).joinpath("skills", sk).is_dir()
        if adopted:
            for rel in disk_skill_files(skdir):
                if upstream_has(upstream_dir, rel):
                    up_sha = sha256_text(upstream_blob(upstream_dir, rel))
                    laf_sha = sha256_text(read_text(_safe_repo_path(rel)))
                    rows.append((rel, "ADOPTED-CLEAN", up_sha, laf_sha))
                else:
                    # a file present in laf's adopted skill but absent upstream → suspicious
                    warnings.append(f"{rel}: in an adopted skill dir but absent upstream — "
                                    f"labeled ADOPTED-CLEAN, Rule B will flag it")
                    laf_sha = sha256_text(read_text(_safe_repo_path(rel)))
                    rows.append((rel, "ADOPTED-CLEAN", NO_HASH, laf_sha))
        else:
            cls = classify(f"{skill_rel}/SKILL.md", declared, upstream_dir)
            rows.append((f"{skill_rel}/**", cls, NO_HASH, NO_HASH))

    # Order: adopted first, then native, then build-new; stable by path within group
    order = {"ADOPTED-CLEAN": 0, "ADOPTED-PATCHED": 0, "NATIVE": 1, "BUILD-NEW": 2}
    rows.sort(key=lambda r: (order.get(r[1], 3), r[0]))

    _write_manifest_rows(vendor_text, rows)

    # F1 (CH-5 re-vendor flow): BEFORE the post-write verify() call, rewrite the
    # VENDOR.md `upstream_sha:` header to the checkout's current HEAD. Without
    # this, CH-5's HEAD-pin compares the NEW checkout HEAD (the sha being vendored)
    # against the stale OLD pinned sha still in the header → a legitimate re-vendor
    # spuriously FAILs at exit. Source precedence for the new pin:
    #   1. _checkout_head(upstream_dir) — the actual HEAD (normal git-checkout path)
    #   2. explicit --upstream-sha flag — tarball/no-git fallback (F3)
    #   3. neither → leave the header as-is and let CH-5 fail loud below (do NOT
    #      silently trust the tree). The normal `--init --upstream <git checkout>`
    #      re-vendor path documented in VENDOR.md lines 32-35 MUST succeed.
    new_pin = _checkout_head(upstream_dir) or upstream_sha
    if new_pin:
        _write_upstream_sha_header(new_pin)
        print(f"--init: pinned upstream_sha: header to {new_pin[:12]}…")

    adopted_n = sum(1 for r in rows if r[1] in ("ADOPTED-CLEAN", "ADOPTED-PATCHED"))
    native_n = sum(1 for r in rows if r[1] == "NATIVE")
    buildnew_n = sum(1 for r in rows if r[1] == "BUILD-NEW")
    print(f"--init: wrote {len(rows)} manifest rows to {VENDOR_MD.name} "
          f"({adopted_n} adopted, {native_n} native, {buildnew_n} build-new).")
    for w in warnings:
        print(f"  WARNING: {w}")

    # Self-check: run verify against the freshly written manifest + upstream.
    print("--init: running post-write verification …")
    return verify(upstream_dir, upstream_sha)


def _write_manifest_rows(vendor_text: str, rows):
    lines = vendor_text.splitlines()
    header_idx = None
    for i, ln in enumerate(lines):
        s = ln.strip().lower()
        if s.startswith("| path") and "class" in s and "sha256" in s:
            header_idx = i
            break
    if header_idx is None:
        raise SystemExit("ERROR: VENDOR.md has no '| path | class | upstream_sha256 | "
                         "laf_sha256 |' manifest header (author it in Step 2.12).")
    sep_idx = header_idx + 1  # the |---|---| separator row
    kept = lines[: sep_idx + 1]
    body = [f"| {p} | {c} | {u} | {l} |" for (p, c, u, l) in rows]
    VENDOR_MD.write_text("\n".join(kept + body) + "\n", encoding="utf-8")


def _write_upstream_sha_header(sha: str):
    """Rewrite the VENDOR.md `upstream_sha:` header line in-place to `sha` (F1).

    The re-vendor flow (do_init) computes manifest rows from a freshly-checked-out
    upstream; this captures the checkout's HEAD into the header so the post-write
    verify()'s CH-5 HEAD-pin sees the NEW sha rather than the stale prior pin.
    Idempotent: re-reads the current file, replaces the first `upstream_sha:` line,
    preserves every other line byte-for-byte. If no header line exists, this is a
    no-op (the VENDOR.md format contract requires one; verify() will report it)."""
    lines = VENDOR_MD.read_text(encoding="utf-8").splitlines()
    out, replaced = [], False
    for ln in lines:
        s = ln.strip().lower()
        if s.startswith("upstream_sha:") and ":" in s:
            # Preserve original indentation + the field's key spelling.
            prefix = ln[: ln.index(":") + 1]
            out.append(f"{prefix} {sha}")
            replaced = True
        else:
            out.append(ln)
    if replaced:
        VENDOR_MD.write_text("\n".join(out) + "\n", encoding="utf-8")


# --- verify (default mode) ------------------------------------------------------
def verify(upstream_dir=None, upstream_sha=None) -> int:
    if not VENDOR_MD.exists():
        print(f"ERROR: {VENDOR_MD} not found", file=sys.stderr)
        return 1
    rows, manifest_errors = parse_manifest(read_text(VENDOR_MD))
    if not rows and not manifest_errors:
        print("ERROR: VENDOR.md manifest has no rows — run --init --upstream <dir> first.",
              file=sys.stderr)
        return 1

    errors = list(manifest_errors)  # malformed/duplicate/bad-hash rows fail the gate (CH-6)
    by_path = {r.path: r for r in rows}

    # A. Adopted files match their recorded LAF hash (catches ANY edit)
    for r in rows:
        if not r.is_adopted:
            continue
        fp = _safe_repo_path(r.path)  # path already parser-validated; safe by construction here
        if not fp.exists():
            errors.append(f"{r.path}: adopted file missing from tree")
            continue
        if sha256_text(read_text(fp)) != r.laf_sha256:
            errors.append(f"{r.path}: modified since vendoring (laf_sha256 mismatch)")

    # A′. (CH-1, H1) Re-anchor ADOPTED-CLEAN integrity to the PR-rewrite-resistant
    # `upstream_sha256` — breaks the self-referential `laf_sha256` loop. The on-disk
    # body is the prefix-rewritten upstream, so inverting the rewrite recovers the
    # raw upstream blob whose hash `upstream_sha256` pins. A commit that edits an
    # adopted body AND rewrites only `laf_sha256` now FAILS here (the body no longer
    # inverts to the pinned raw-upstream hash). Runs in BOTH modes (no upstream tree
    # needed) — zero CI cost. (Adopted rows are CH-6-validated to carry a 64-hex
    # upstream_sha256, so NO_HASH here would itself be a parser error already raised.)
    # ADOPTED-PATCHED (writer.md) is intentionally excluded: its `upstream_sha256` is
    # the whole-raw-upstream-file hash, not reconstructible from the patched disk
    # without the upstream blob; its absolute guarantee is Mode-U Rule C.
    for r in rows:
        if r.cls != "ADOPTED-CLEAN":
            continue
        fp = _safe_repo_path(r.path)
        if not fp.exists():
            continue  # already reported under Rule A
        derived = sha256_text(prefix_unrewrite(read_text(fp)))
        if derived != r.upstream_sha256:
            errors.append(
                f"{r.path}: body no longer matches pinned upstream_sha256 — "
                f"raw-upstream hash mismatch (CH-1; laf_sha256 rewrite detected)")

    # C′. (CH-3, M1) ADOPTED-PATCHED is reserved for agents/writer.md only. Runs in
    # BOTH modes (needs no upstream tree) — placed outside the `if upstream_dir:` block.
    for r in rows:
        if r.cls == "ADOPTED-PATCHED" and r.path != "agents/writer.md":
            errors.append(f"{r.path}: ADOPTED-PATCHED is reserved for agents/writer.md only")

    # B. ADOPTED-CLEAN == upstream-after-prefix-rewrite (needs upstream)
    if upstream_dir:
        # CH-5 (M3): before trusting any upstream blob, assert the checkout's HEAD
        # equals VENDOR.md's pinned `upstream_sha`. A stale/wrong checkout would
        # silently false-green Rules B/C. Pin source precedence: explicit
        # --upstream-sha flag > VENDOR.md header `upstream_sha:`. If neither yields
        # a pin, FAIL LOUD (do not silently trust the tree). Runs only in Mode U —
        # zero cost in Mode V / CI.
        #
        # Tarball/no-git fallback (F3): if HEAD is unreadable (no git / not a repo)
        # BUT an explicit --upstream-sha was supplied, SKIP the HEAD-mismatch check
        # — the operator has asserted the pin explicitly, so we do not need to
        # re-derive it from git. Rules B/C still run against the supplied tree, so
        # the security stance (never silently trust an unverifiable tree) is
        # preserved: the pin is an operator assertion, not an inference. Only fail
        # loud when there is NO explicit pin AND no readable HEAD.
        pinned = upstream_sha or parse_upstream_sha(read_text(VENDOR_MD))
        if not pinned:
            errors.append("Mode U: no pinned upstream_sha (set upstream_sha: in VENDOR.md "
                          "or pass --upstream-sha) — refusing to trust the checkout")
        else:
            head = _checkout_head(upstream_dir)
            if head is None and upstream_sha is None:
                errors.append(f"Mode U: could not read HEAD of --upstream {upstream_dir!r} "
                              f"(not a git repo / git unavailable) — pass --upstream-sha "
                              f"to assert the pin explicitly")
            elif head is not None and head != pinned:
                errors.append(f"Mode U: --upstream checkout HEAD {head[:12]} != pinned "
                              f"upstream_sha {pinned[:12]} (re-checkout at the pinned SHA)")
        for r in rows:
            if r.cls != "ADOPTED-CLEAN":
                continue
            if not upstream_has(upstream_dir, r.path):
                errors.append(f"{r.path}: ADOPTED-CLEAN but absent from upstream checkout")
                continue
            expected = sha256_text(prefix_rewrite(upstream_blob(upstream_dir, r.path)))
            if r.laf_sha256 != expected:
                errors.append(f"{r.path}: ADOPTED-CLEAN but differs from upstream beyond "
                              f"prefix rewrite")

        # C. ADOPTED-PATCHED diff is frontmatter-only AND additive (needs upstream)
        for r in rows:
            if r.cls != "ADOPTED-PATCHED":
                continue
            if not upstream_has(upstream_dir, r.path):
                errors.append(f"{r.path}: ADOPTED-PATCHED but absent from upstream checkout")
                continue
            up = prefix_rewrite(upstream_blob(upstream_dir, r.path))
            cur = read_text(_safe_repo_path(r.path))
            if body_of(cur) != body_of(up):
                errors.append(f"{r.path}: body changed — adopted agent bodies must be "
                              f"byte-identical")
            added, removed = frontmatter_line_diff(up, cur)
            if removed:
                errors.append(f"{r.path}: frontmatter lines removed — patch must be "
                              f"additive only ({removed})")
            bad = [ln for ln in added if not ln.strip().startswith("- laf-adaptation:")]
            if bad:
                errors.append(f"{r.path}: only additive `- laf-adaptation:<skill>` skill "
                              f"lines are permitted (offending: {bad})")
    else:
        # Mode V (no --upstream): Rules B/C skipped. ADOPTED-PATCHED writer.md's
        # additive-body guarantee is a documented residual here — its absolute
        # proof is Mode-U Rule C (OQ-4: Mode U in CI is deferred). Backstopped by
        # branch protection + mandatory human review of any upstream_sha256 diff.
        # See check_boundary.py:540-542 (Rule A′ writer.md exclusion), .github/workflows/boundary.yml:27-33, VENDOR.md.
        print("NOTE: verify running without --upstream — Rules B and C (upstream-diff "
              "checks) skipped; Rule A hash-match covers adopted-file integrity against the "
              "recorded manifest, plus Rules D/E/F.")

    # D. Invariant G3 — quartet intact, editor never folded
    for name in QUARTET:
        p = f"agents/{name}.md"
        r = by_path.get(p)
        if r is None or r.cls != "ADOPTED-CLEAN" or not (REPO / p).exists():
            errors.append(f"G3 violation: {p} must exist as ADOPTED-CLEAN (quartet intact)")

    # E. No NATIVE/BUILD-NEW name collides with an upstream file
    for r in rows:
        if r.cls not in ("NATIVE", "BUILD-NEW"):
            continue
        if upstream_dir:
            if r.is_glob:
                sk = r.path[len("skills/"):-len("/**")]
                if upstream_root(upstream_dir).joinpath("skills", sk).exists():
                    errors.append(f"{r.path}: NATIVE/BUILD-NEW skill shadows upstream "
                                  f"skills/{sk}")
            elif upstream_has(upstream_dir, r.path):
                errors.append(f"{r.path}: NATIVE/BUILD-NEW shadows an upstream file name")
        else:
            # manifest-only best-effort: a native path also listed as adopted = collision
            adopted_paths = {x.path for x in rows if x.is_adopted}
            if r.path in adopted_paths:
                errors.append(f"{r.path}: NATIVE/BUILD-NEW collides with an ADOPTED row")

    # F. Every agents/*.md and skills/**/SKILL.md is listed (or glob-covered) in manifest
    for rel in disk_agents() + disk_skill_skillmds():
        if not manifest_covers(rows, rel):
            errors.append(f"{rel}: not in VENDOR.md manifest")

    # F′. (CH-2, H2) Extend Rule F to adopted skills' resources/** — every file under
    # an adopted skill dir must be manifest-covered. Without this, deleting a manifest
    # row or dropping an untracked file into an adopted skill's resources/ is invisible
    # to every CI-mode rule. This makes the manifest's resources/** superset ENFORCED,
    # not merely descriptive. NATIVE/BUILD-NEW skill dirs are already covered by their
    # `/**` glob rows, so this sub-check targets only adopted skill dirs.
    adopted_skill_dirs = {
        r.path.split("/")[1] for r in rows
        if r.path.startswith("skills/") and r.is_adopted
    }
    for skdir in disk_skill_dirs():
        if skdir.name in adopted_skill_dirs:
            for rel in disk_skill_files(skdir):
                if not manifest_covers(rows, rel):
                    errors.append(f"{rel}: adopted-skill file not in VENDOR.md manifest")

    if errors:
        print(f"BOUNDARY CONTRACT: FAIL — {len(errors)} violation(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.")
    return 0


# --- --report (always exit 0) ---------------------------------------------------
def do_report() -> int:
    if not VENDOR_MD.exists():
        print("No VENDOR.md present yet.")
        return 0
    rows, manifest_errors = parse_manifest(read_text(VENDOR_MD))  # --report: exit 0 always
    counts = {}
    for r in rows:
        counts[r.cls] = counts.get(r.cls, 0) + 1
    print("laf-adaptation/ provenance summary (from VENDOR.md)")
    print("=" * 52)
    for cls in ("ADOPTED-CLEAN", "ADOPTED-PATCHED", "NATIVE", "BUILD-NEW"):
        print(f"  {cls:<16} {counts.get(cls, 0)}")
    print(f"  {'TOTAL rows':<16} {len(rows)}")
    print("-" * 52)
    for r in rows:
        pin = "hash-pinned" if r.is_adopted else "not pinned"
        print(f"  [{r.cls:<15}] {r.path}  ({pin})")
    # Manifest errors are warnings in --report (exit 0 is the contract); verify mode
    # treats them as FAIL, but --report is a human summary and stays non-blocking.
    for e in manifest_errors:
        print(f"  WARNING (manifest): {e}")
    return 0


# --- CLI ------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Boundary-contract checker for laf-adaptation/ (validation tool, not a runtime).")
    ap.add_argument("--init", action="store_true",
                    help="compute hashes and (re)write VENDOR.md manifest rows; requires --upstream")
    ap.add_argument("--report", action="store_true",
                    help="print a human-readable provenance summary; always exit 0")
    ap.add_argument("--upstream", metavar="DIR", default=None,
                    help="path to a checkout of the upstream repo at upstream_sha")
    ap.add_argument("--upstream-sha", metavar="SHA", default=None,
                    help="explicit upstream_sha pin (Mode U); used if the checkout is not a "
                         "git repo or VENDOR.md has no upstream_sha. Asserts HEAD == pin.")
    args = ap.parse_args(argv)

    if args.init and args.report:
        print("ERROR: choose one of --init / --report / (default verify).", file=sys.stderr)
        return 2
    if args.init:
        return do_init(args.upstream, args.upstream_sha)
    if args.report:
        return do_report()
    return verify(args.upstream, args.upstream_sha)


if __name__ == "__main__":
    sys.exit(main())
