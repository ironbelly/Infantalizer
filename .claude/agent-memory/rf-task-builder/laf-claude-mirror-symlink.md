---
name: laf-claude-mirror-symlink
description: The repo-root .claude mirror of laf-adaptation is symlink-based, not copy-based; changes how mirror steps are encoded in task builds
metadata:
  type: project
---

The repo-root `.claude/skills/*` and `.claude/agents/*` entries are relative SYMLINKS into `laf-adaptation/` (e.g. `.claude/skills/prep -> ../../laf-adaptation/skills/prep`, `.claude/agents/prep-cordinator.md -> ../../laf-adaptation/agents/prep-cordinator.md`).

**Why:** editing a NATIVE `laf-adaptation/` source file AUTO-updates its `.claude` view — there is NO copy/sync step for edited files, unlike the SuperClaude framework's own `make sync-dev` mirror (which is unrelated). This was gate finding G-1 on the chapter-materialize build.

**How to apply:** when a LAF task edits an existing mirrored file, encode a single edit to the `laf-adaptation/` source and explicitly note NO copy step. Only two things need explicit `.claude` action:
- A NEW skill dir: after authoring `laf-adaptation/skills/<name>/`, create ONE relative symlink `ln -s ../../laf-adaptation/skills/<name> .claude/skills/<name>`; verify with `readlink` resolving to the source (NOT `diff -r`, which is degenerate for symlinks).
- `.claude/commands/laf/*.md` are REAL canonical files (there is NO `laf-adaptation/commands/` source) — edit them directly.

`laf-adaptation/VENDOR.md` and `laf-adaptation/source/README.md` have NO `.claude` mirror at all — edit source only.

See [[laf-boundary-contract]] for what the boundary check does/doesn't enforce (it does NOT read `.claude/`, so mirror drift = green check + runtime "skill not found").
