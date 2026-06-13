# ASH-FT-45 Materialized Delta Payload Integrity Audit

ASH-FT-45 audits the materialized selected-group delta payload created by ASH-FT-44.

The patch does not package an official delta packet. It does not append the delta stack. It does not apply the payload to a checkpoint. The payload remains a candidate artifact until later stages.

## Required evidence

- ASH-FT-44 receipt is PASS.
- Payload file exists and is readable.
- Recomputed payload SHA256 matches FT-44 hash manifest.
- Shape/dtype metadata matches FT-44 manifest.
- Payload scope remains selected-group-only.
- Provenance chain remains present.
- No stack append, no apply, and no shadow replay guards remain PASS.

## CLI

See `README_ASH_FT_45_BAKED.md` for the full command.
