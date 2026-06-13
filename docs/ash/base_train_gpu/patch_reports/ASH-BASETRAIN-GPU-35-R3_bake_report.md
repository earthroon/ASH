# ASH-BASETRAIN-GPU-35-R3 Bake Report

## Scope

Read-only selected group manifest derivation from existing atlas group plan receipt.

## Implemented

- Added R3 Rust module and bin wrapper.
- Added recursive JSON/JSONL/Markdown JSON-block discovery for existing plan/receipt candidates.
- Added alias-based direct field extraction for selected group identity, tensor name, dtype, shape, byte range, and shard path.
- Added deterministic selected manifest digest generation.
- Added no-invent, no-weight-load, no-GPU-runtime, no-backward, no-optimizer, and no-mutation guards.
- Added static baked receipts for the current ZIP state.

## Static baked verdict

```txt
BLOCKED_NO_SELECTED_GROUP_ENTRY_FOUND
```

## Why blocked

The current ZIP contains prior locator/template/skeleton artifacts but no complete source atlas group plan receipt that directly provides the selected group tensor metadata. R3 therefore refuses to invent a manifest.

## Non-goals preserved

- No safetensors full load.
- No selected weight byte read.
- No WGPU device request.
- No GPU buffer creation.
- No forward/backward.
- No optimizer step.
- No delta candidate materialization.
- No checkpoint/safetensors mutation.

## Validation

See:

- `ASH_BASETRAIN_GPU_35_R3_STATIC_BUNDLE.json`
- `ASH_BASETRAIN_GPU_35_R3_SELECTED_GROUP_MANIFEST_FROM_ATLAS_PLAN_RECEIPT.json`
- `ASH_BASETRAIN_GPU_35_R3_STATIC_CHECKS.txt`
