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


def parse_manifest(text: str):
    """Parse the 4-column manifest table (path | class | upstream_sha256 |
    laf_sha256). Returns list[Row]. Skips the header + separator rows."""
    rows = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 4:
            continue
        path, cls = cells[0], cells[1]
        if path.lower() == "path" or set(path) <= set("-: "):  # header / separator
            continue
        if cls.upper() not in ("ADOPTED-CLEAN", "ADOPTED-PATCHED", "NATIVE", "BUILD-NEW"):
            continue
        rows.append(Row(path, cls.upper(), _norm_hash(cells[2]), _norm_hash(cells[3])))
    return rows


def manifest_covers(rows, rel: str) -> bool:
    for r in rows:
        if r.path == rel:
            return True
        if r.is_glob and rel.startswith(r.path[:-2]):  # 'skills/x/**' covers 'skills/x/...'
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
def do_init(upstream_dir: str):
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
    declared = {r.path: r.cls for r in parse_manifest(vendor_text)}

    rows = []          # (path, cls, upstream_sha256, laf_sha256)
    warnings = []

    # Agents — one row per file
    for rel in disk_agents():
        cls = classify(rel, declared, upstream_dir)
        if cls in ("ADOPTED-CLEAN", "ADOPTED-PATCHED"):
            up_raw = upstream_blob(upstream_dir, rel)
            up_sha = sha256_text(up_raw)
            laf_sha = sha256_text(read_text(REPO / rel))
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
                    laf_sha = sha256_text(read_text(REPO / rel))
                    rows.append((rel, "ADOPTED-CLEAN", up_sha, laf_sha))
                else:
                    # a file present in laf's adopted skill but absent upstream → suspicious
                    warnings.append(f"{rel}: in an adopted skill dir but absent upstream — "
                                    f"labeled ADOPTED-CLEAN, Rule B will flag it")
                    laf_sha = sha256_text(read_text(REPO / rel))
                    rows.append((rel, "ADOPTED-CLEAN", NO_HASH, laf_sha))
        else:
            cls = classify(f"{skill_rel}/SKILL.md", declared, upstream_dir)
            rows.append((f"{skill_rel}/**", cls, NO_HASH, NO_HASH))

    # Order: adopted first, then native, then build-new; stable by path within group
    order = {"ADOPTED-CLEAN": 0, "ADOPTED-PATCHED": 0, "NATIVE": 1, "BUILD-NEW": 2}
    rows.sort(key=lambda r: (order.get(r[1], 3), r[0]))

    _write_manifest_rows(vendor_text, rows)

    adopted_n = sum(1 for r in rows if r[1] in ("ADOPTED-CLEAN", "ADOPTED-PATCHED"))
    native_n = sum(1 for r in rows if r[1] == "NATIVE")
    buildnew_n = sum(1 for r in rows if r[1] == "BUILD-NEW")
    print(f"--init: wrote {len(rows)} manifest rows to {VENDOR_MD.name} "
          f"({adopted_n} adopted, {native_n} native, {buildnew_n} build-new).")
    for w in warnings:
        print(f"  WARNING: {w}")

    # Self-check: run verify against the freshly written manifest + upstream.
    print("--init: running post-write verification …")
    return verify(upstream_dir)


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


# --- verify (default mode) ------------------------------------------------------
def verify(upstream_dir=None) -> int:
    if not VENDOR_MD.exists():
        print(f"ERROR: {VENDOR_MD} not found", file=sys.stderr)
        return 1
    rows = parse_manifest(read_text(VENDOR_MD))
    if not rows:
        print("ERROR: VENDOR.md manifest has no rows — run --init --upstream <dir> first.",
              file=sys.stderr)
        return 1

    errors = []
    by_path = {r.path: r for r in rows}

    # A. Adopted files match their recorded LAF hash (catches ANY edit)
    for r in rows:
        if not r.is_adopted:
            continue
        fp = REPO / r.path
        if not fp.exists():
            errors.append(f"{r.path}: adopted file missing from tree")
            continue
        if sha256_text(read_text(fp)) != r.laf_sha256:
            errors.append(f"{r.path}: modified since vendoring (laf_sha256 mismatch)")

    # B. ADOPTED-CLEAN == upstream-after-prefix-rewrite (needs upstream)
    if upstream_dir:
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
            cur = read_text(REPO / r.path)
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
    rows = parse_manifest(read_text(VENDOR_MD))
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
    args = ap.parse_args(argv)

    if args.init and args.report:
        print("ERROR: choose one of --init / --report / (default verify).", file=sys.stderr)
        return 2
    if args.init:
        return do_init(args.upstream)
    if args.report:
        return do_report()
    return verify(args.upstream)


if __name__ == "__main__":
    sys.exit(main())
