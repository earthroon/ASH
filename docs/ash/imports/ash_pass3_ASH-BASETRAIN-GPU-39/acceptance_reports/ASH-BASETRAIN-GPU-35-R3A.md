# ASH-BASETRAIN-GPU-35-R3A Acceptance Report

## Patch

`ASH-BASETRAIN-GPU-35-R3A`

**Atlas Group Plan Receipt Schema Narrowing And Explicit Source Path Rebind / Candidate Flood To Canonical Atlas Plan Receipt No Manifest Invent Seal**

## 확정

This patch adds a read-only canonical source binding runner for the base_train crate.

Implemented files:

- `crates/base_train/src/ash_basetrain_gpu_35_r3a_atlas_group_plan_schema_narrowing.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_35_r3a_atlas_group_plan_schema_narrowing.rs`
- `artifacts/ASH_BASETRAIN_GPU_35_R3A_ATLAS_GROUP_PLAN_SCHEMA_NARROWING.json`
- `artifacts/ASH_BASETRAIN_GPU_35_R3A_STATIC_CHECKS.txt`

The runner accepts an explicit canonical atlas group plan receipt source by priority:

1. CLI: `--atlas-plan-receipt <path>`
2. ENV: `ASH_BASETRAIN_GPU_ATLAS_PLAN_RECEIPT`
3. Pointer receipt: `artifacts/ASH_BASETRAIN_GPU_CANONICAL_ATLAS_PLAN_POINTER.json`

Wildcard candidate flood selection is not used for selection.

## Baked static verdict

```txt
BLOCKED_NO_EXPLICIT_ATLAS_PLAN_RECEIPT_SOURCE
```

This is the expected static sealed result because the bake container did not provide a canonical atlas group plan receipt path. Runtime use can pass an explicit path.

## SSOT

The only source of truth for selected group manifest derivation is the explicit canonical atlas group plan receipt path.

Rejected SSOT sources:

- wildcard artifact scans
- acceptance report floods
- file name inference
- tensor name pattern guessing
- default shape/dtype/byte range filling

## Guard status

```txt
invented_shape=false
invented_dtype=false
invented_byte_range=false
invented_tensor_name=false
invented_source_shard_path=false
selected_group_weights_loaded=false
runtime_gpu_buffer_created=false
selected_group_gradient_buffer_allocated=false
selected_group_backward_executed=false
optimizer_step_executed=false
safetensors_mutation_present=false
runtime_1p1b_training_claimed=false
```

## Runtime commands

Build:

```powershell
cargo build -p base_train --bin ash_basetrain_gpu_35_r3a_atlas_group_plan_schema_narrowing
```

Run without explicit source path, expected BLOCK:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_35_r3a_atlas_group_plan_schema_narrowing
```

Run with explicit source path:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_35_r3a_atlas_group_plan_schema_narrowing -- --atlas-plan-receipt .\artifacts\ash_ft\ash_ft00_atlas_group_plan.json --selected-group-index 0
```

Alternative ENV source path:

```powershell
$env:ASH_BASETRAIN_GPU_ATLAS_PLAN_RECEIPT=".\artifacts\ash_ft\ash_ft00_atlas_group_plan.json"
cargo run -p base_train --bin ash_basetrain_gpu_35_r3a_atlas_group_plan_schema_narrowing -- --selected-group-index 0
```

## PASS target

```txt
PASS_ASH_BASETRAIN_GPU_35_R3A_ATLAS_GROUP_PLAN_RECEIPT_SCHEMA_NARROWING_AND_EXPLICIT_SOURCE_PATH_REBIND_CANDIDATE_FLOOD_TO_CANONICAL_ATLAS_PLAN_RECEIPT_NO_MANIFEST_INVENT
```

## BLOCK follow-up routing

- No source path: `ASH-BASETRAIN-GPU-35-R3A-R1 Canonical Atlas Plan Pointer Receipt Writer`
- Unsupported schema: `ASH-BASETRAIN-GPU-35-R3B Atlas Group Plan Schema Adapter`
- Selected group missing: `ASH-BASETRAIN-GPU-35-R3C Selected Group Request Rebind`
- PASS: `ASH-BASETRAIN-GPU-36 Selected Group Weight Slice Load Preflight`

## 판단불가

The bake container does not include Cargo/Rust, so `cargo build` and `cargo run` were not executed here. Local operator validation is required.
