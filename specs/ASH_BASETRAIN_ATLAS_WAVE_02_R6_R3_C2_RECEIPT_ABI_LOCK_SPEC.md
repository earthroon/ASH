# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R3-C2

## Stage11 Atlas Parallel Streaming Wave Receipt ABI Lock

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R3-C1`  
> Receipt schema revision: `2`  
> Production admission: blocked  
> Proof ledger: HOLD

## SSOT

The atlas-parallel Stage11 implementation, its authority seal, and its executable gate must compile against one backend-owned receipt ABI. No caller-side alias, inferred counter, or pre-C1 metadata artifact may substitute for the backend type.

## Required contract

```text
backend pipeline identity receipt_schema_revision = 2
backend execution receipt receipt_schema_revision = 2
base_train authority required revision = 2
orchestrator gate required revision = 2
```

The following atlas fields remain mandatory and backend-owned:

```text
statistics_atlas_abi
atlas_wave_count
atlas_wave_capacity_records
atlas_wave_capacity_bytes
atlas_pack_dispatch_count
atlas_merge_dispatch_count
atlas_buffer_reuse_count
atlas_payload_readback_count
atlas_full_source_materialization_count
```

## Incremental compilation boundary

ZIP extraction may preserve source timestamps older than existing Cargo metadata. Applying C2 therefore requires either:

1. touching the three changed Rust files and running targeted `cargo clean -p`, or
2. deleting the affected `burn_webgpu_backend`, `base_train`, and `orchestrator_local` target artifacts.

A full repository clean is not required.

## Forbidden substitutions

- replacing atlas counters with old receipt fields
- mapping `atlas_payload_readback_count` to `statistics_payload_readback_count`
- deriving wave count from unrelated dispatch counters
- increasing recursion limit as a substitute
- accepting a receipt without schema revision 2
- silently trusting stale `.rmeta`

## Admission

Compilation is admitted only if the gate, authority, and backend resolve the same revision-2 receipt and pipeline identity definitions.
