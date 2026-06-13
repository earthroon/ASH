# ASH-FT-09 Shadow Candidate Write Dry-run

This patch validates the first staged shadow write path for a single atlas group. It does not promote, alias, or apply to runtime default.

Important implementation note: ASH-FT-08 currently emits a manifest-level delta packet, not raw delta payload bytes. Therefore ASH-FT-09 creates the staged shadow candidate and validates packet ranges/checksums. If packet payloads are not materialized, the receipt records `metadata_only_shadow_write_dryrun_no_raw_delta_payload` and writes no raw delta bytes.
