# P3 Dual-Form Promotion Summary

**All four assertions PASS** (every command exit 0).

| # | Assertion | Result |
|---|---|---|
| (a) | derived `30-mapping.yaml` is 6-key with `meaning:` | ✅ PASS |
| (b) | kb hyphen copy `tolkien-mapping.yaml` is 6-key with `meaning:` KEPT | ✅ PASS |
| (c) | root underscore copy `tolkien_mapping.yaml` is 5-key with `meaning:` STRIPPED | ✅ PASS |
| (d) | write-provenance: both targets CHANGED since pre-run (non-vacuous) | ✅ PASS |

The dual-form promotion contract (`package-schemas.md` §4.1) is satisfied: the 0.1 hyphen copy keeps `meaning:` so the rewrite `muse` reads it as data; the root underscore copy strips `meaning:` (and `_confidence`) to validate against the frozen 5-key schema (R14). Both targets were genuinely re-written by the runtime promotion (post-run sha256 ≠ pre-run snapshot), so assertion (c) is not a vacuous pass against stale pre-existing content.

See `p3-dualform.txt` for raw output.
