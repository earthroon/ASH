# ASH-BASETRAIN-GPU-66A-R1 SPEC

## Patch ID

ASH-BASETRAIN-GPU-66A-R1

## Summary

Atlas grouped builder rebind for GPU-66A input packet preflight.

The patch removes large serde_json macro object construction and uses small Map based builder groups plus a forbidden flag lookup table.

## Static Contract

- json_macro_count: 0
- recursion_limit_count: 0
- atlas_merge_present: true
- map_builder_present: true
- forbidden_lookup_table_present: true
- match_validation_present: true
- no_sha256_sidecar_files_created: true

## Next

ASH-BASETRAIN-GPU-67A