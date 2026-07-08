# UPSTREAM-SYNC.md — how the boundary contract survives upstream updates

This is the reconcile procedure for pulling new upstream `creative-writing-skills` changes into the
vendored ADOPTED subset **without merge pain**. It is faithful to `boundary-contract.md §5`.

The whole payoff of the boundary contract lives here: **because adopted files are provably unmodified
(ours == base), upstream patches apply as a clean fast-forward.** The moment an adopted file drifts, this
fast-forward degrades to manual cherry-pick — which is exactly the cost the contract is designed to
prevent. `check_boundary.py` is what guarantees `ours == base`.

## The 6-step procedure

```
1. Fetch upstream; pick new target SHA.
     git clone https://github.com/haowjy/creative-writing-skills <checkout>
     # (or, if already cloned:  git -C <checkout> fetch origin)
     # <checkout> is the dir you pass as `--upstream <checkout>` in Steps 2 and 5.

2. For each ADOPTED-CLEAN file: 3-way reconcile
     base   = upstream@old_sha  (prefix-rewritten)
     ours   = laf file          (== base, by contract)
     theirs = upstream@new_sha  (prefix-rewritten)
   Since ours == base, apply theirs cleanly (fast-forward).
   Conflicts ⇒ manual cherry-pick (only possible if an adopted file drifted — the contract prevents this).

3. For writer.md (ADOPTED-PATCHED): reapply the single additive skill line
   (`- laf-adaptation:adaptation-rules`) on top of theirs' body.

4. NEVER touch NATIVE / BUILD-NEW files during sync.

5. Re-run check_boundary.py --init to recompute hashes; update upstream_sha + vendored_on in VENDOR.md.

6. Re-run the Phase-3 hard gate before shipping the synced version.
```

## Notes on each step

- **Step 2 — the 3-way merge for ADOPTED-CLEAN.** The `base` is the *old* upstream file after the uniform
  prefix rewrite (`creative-writing-skills:` → `laf-adaptation:`). By the boundary contract, `ours` (the
  vendored file) equals `base` exactly — `check_boundary.py` Rule B/A proves it. So applying `theirs` (the
  *new* upstream after the same rewrite) is a fast-forward: there is nothing local to conflict with. If a
  merge conflict *does* occur, it means an adopted file drifted from upstream — stop and investigate; the
  contract was violated somewhere.

- **Step 3 — the writer re-graft (ADOPTED-PATCHED).** `writer.md` is the only patched adopted file. Take
  the new upstream `cw/agents/writer.md` body verbatim (prefix-rewritten), then re-append the single
  additive line `- laf-adaptation:adaptation-rules` to its `skills:` list. Preserve any upstream quirks
  (e.g. the duplicate `creative-writing-craft` line) — do not "fix" them. The result must still satisfy
  Rule C (body byte-identical to upstream-after-rewrite; the only frontmatter delta additive
  `- laf-adaptation:` lines).

- **Step 4 — NEVER touch NATIVE / BUILD-NEW.** The adaptation spine (`analyst`, `safety-verifier`, the
  `adaptation-*` skills) and the greenfield components (`chronicler`, `tier-coordinator`,
  `adaptation-safety`) are LAF-authored and stand entirely outside the upstream relationship. The sync flow
  reads and rewrites ONLY the ADOPTED files (step 2) and re-grafts ONLY `writer.md` (step 3). NATIVE and
  BUILD-NEW files are never read, diffed, or written by the sync.

- **Step 5 — re-pin the manifest.** After the adopted files are updated, run:
  ```
  uv run python scripts/check_boundary.py --init --upstream <new-checkout-dir>
  ```
  This recomputes `upstream_sha256` + `laf_sha256` for every adopted file and rewrites the `VENDOR.md`
  manifest rows. Update the `upstream_sha` and `vendored_on` header fields to the new SHA and date. NATIVE
  and BUILD-NEW rows stay `—` (not hash-pinned).

- **Step 6 — re-prove before shipping.** Re-run the **Phase-3 hard gate** to confirm the synced adopted
  subset still executes the workflow end-to-end. Concretely:

  1. Re-run the boundary check first (fast fail): `uv run python scripts/check_boundary.py` — MUST exit 0.
  2. Run the full **11-step adaptation workflow** on one chapter at Tier 1, then fan the same chapter out
     across Tiers 1/3/5 via `tier-coordinator`. The 11-step order is:
     **analyst → muse → writer → critic → editor → writer → continuity-checker → safety-verifier →
     reader-sim → tier-coordinator → chronicler.**
  3. Confirm **all 5 gate conditions** re-pass:
     1. v2.0 CERTAIN/PROBABLE/UNCERTAIN tags present in analyst output ·
     2. safety PASS (blocking-mode verdict) ·
     3. per-tier canon written (continuity.md + canon-delta.md per tier) ·
     4. all four quartet agents ran (critic/editor/reader-sim/continuity-checker; editor never folded) ·
     5. `check_boundary.py` green.

  A synced version does not ship until the hard gate is GREEN on the new adopted subset.

## Why this is the entire payoff

Because the adopted subset is provably patch-clean (never edited beyond the deterministic prefix rewrite +
the one additive writer line), LAF can absorb upstream improvements to the review/orchestration/kb
machinery as clean fast-forwards, while its domain-specific adaptation spine (NATIVE) and greenfield
components (BUILD-NEW) stay untouched. That is the two-provenance design working as intended: keep the
adopted subset boundary-clean, and upstream sync stays cheap forever.
