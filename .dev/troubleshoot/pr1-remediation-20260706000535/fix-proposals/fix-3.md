# Fix Proposal 3 — M2: text-normalized hashing (CONTRACT DECISION — needs user input)

## Problem (empirically confirmed)
The boundary contract is described as "byte-identical / byte-faithful vendoring," but `sha256_text` + `read_text` (text mode, default `newline=None`) **normalize CRLF→LF before hashing**. I verified this directly:

```
text equal after read_text: True
sha256_text  LF:   3ff7e6857581edb1
sha256_text  CRLF: 3ff7e6857581edb1   <- identical
sha256_bytes LF:   3ff7e6857581edb1
sha256_bytes CRLF: 049c4fcbde539e6c   <- different
```

So a CRLF and an LF version of the same adopted file produce the **same** `laf_sha256`. The system is internally consistent (the same pipeline feeds prefix rewrite + body comparison), but it is **text-normalized, not byte-accurate**. Today all vendored files are LF, so this is latent — it becomes real if upstream ever ships CRLF.

## Why this is a DECISION, not a unilateral fix
Switching to byte hashing is **not** a localized change:
- **8 hash call sites** use `sha256_text` (lines 382, 383, 396, 397, 403, 506, 526, 573).
- **All 64 manifest rows in VENDOR.md** were computed via `sha256_text`. Switching to `sha256_bytes` invalidates every one.
- `prefix_rewrite` / `prefix_unrewrite` operate on `str`; a byte-level pipeline needs byte-literal replacements.
- The `--init` recompute flow and Rule A′ re-derivation both depend on the text pipeline.

So M2 has two legitimate resolutions, and the choice is yours:

### Option A — Strengthen to byte-accurate (higher fidelity, breaking change)
- Replace `sha256_text(read_text(fp))` → `sha256_bytes(read_bytes(fp))` at all 8 sites.
- Move prefix rewrite to bytes (`PREFIX_FROM.encode()`, `PREFIX_TO.encode()`).
- **Re-run `--init` against the upstream checkout to recompute all 64 manifest hashes** with the new algorithm.
- Update VENDOR.md "Hash semantics" to claim byte-identical.
- Cost: medium (touches 8 sites + full manifest rehash + upstream checkout needed). Risk: rehash must be done at the correct upstream SHA or hashes won't match.

### Option B — Align docs to text-normalized reality (low cost, honest)  ← RECOMMENDED for 0.1
- Keep the text pipeline.
- Soften the prose: change "byte-identical" / "byte-faithful" claims in CLAUDE.md, VENDOR.md, NOTICE, and code comments to "text-normalized (LF) integrity."
- Add a one-line test asserting CRLF and LF produce the same hash (documenting the normalization as *intended*, not accidental).
- Cost: small (docs + 1 test). Risk: none functional. Tradeoff: the contract is honest but can't detect CRLF drift — acceptable for a 0.1 prompt+YAML framework where upstream is LF.

## Recommendation
**Option B for 0.1.** The framework is prompt+YAML (ADR-006), upstream is LF, and a manifest-wide rehash (Option A) is disproportionate to a latent fidelity nit. Make the contract honest now; revisit byte-accuracy if/when upstream ships mixed line endings. **Defer this decision to the user** — do not auto-apply either option.

## Evidence
- `check_boundary.py:68-77` (sha256_text + read_text in text mode)
- Empirical output above (CRLF and LF hash identical under text pipeline)
- `check_boundary.py:382-403, 506, 526, 573` (8 sha256_text call sites)

## Risks
- Option A: rehash at wrong upstream SHA → all hashes mismatch → must redo.
- Option B: none functional; docs-only.
