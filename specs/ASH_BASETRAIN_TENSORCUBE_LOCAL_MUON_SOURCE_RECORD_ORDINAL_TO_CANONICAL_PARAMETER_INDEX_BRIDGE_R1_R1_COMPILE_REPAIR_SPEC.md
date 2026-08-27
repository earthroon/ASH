# ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-SOURCE-RECORD-ORDINAL-TO-CANONICAL-PARAMETER-INDEX-BRIDGE-R1-R1

## Status

Compile-only repair to R1. No semantic change to the bridge contract.

## Trigger

Rust compile failure:

`expected usize, found Option<usize>`

at the gather-side call to `packed_index_for_logical`.

## Root cause

The outer `canonical_parameter_index` is intentionally represented as `Option<usize>` because the TensorCube Local Muon runtime itself is optional.

After `muon_geometry` becomes `Some`, the Muon branch is active and a canonical parameter index is mandatory. R1 originally deferred the fail-closed `Option<usize> -> usize` conversion until after the gather loop, so the first gather-side canonical-index consumer received the Option directly.

## Repair

At the beginning of the `if let Some(geometry) = muon_geometry` branch, convert the optional canonical index using the existing Result-based fail-closed token:

`FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_CANONICAL_PARAMETER_INDEX_MISSING`

The resulting `usize` is then reused by all canonical identity consumers in that branch:

- gather `packed_index_for_logical`
- training provenance projection
- Muon execution
- scatter `packed_index_for_logical`
- route-span lookup

The later duplicate conversion is removed.

## Forbidden repair

Do not use:

- `expect`
- `unwrap`
- default index 0
- source record ordinal fallback
- registry mutation
- source reorder

## Preserved invariants

```text
No Source Record Reorder /
No Packed Offset Rewrite /
No Registry Rewrite /
No Optimizer Routing Rewrite /
No Momentum Offset Rewrite /
No Training Math Change /
No Gradient Math Change /
No Muon Kernel Change /
No AdamW Kernel Change /
```

The R1 SSOT and receipt schema remain unchanged.
