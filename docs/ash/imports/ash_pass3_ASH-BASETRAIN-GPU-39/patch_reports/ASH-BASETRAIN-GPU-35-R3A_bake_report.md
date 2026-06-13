# ASH-BASETRAIN-GPU-35-R3A Bake Report

## 확정

Patched R3A on top of the R3 baked ZIP.

Added a new base_train binary:

```txt
ash_basetrain_gpu_35_r3a_atlas_group_plan_schema_narrowing
```

Added runtime behavior:

```txt
explicit canonical atlas plan receipt source required
candidate flood selection disabled
schema narrowed to groups / atlas_groups / selected_group / tensor_index_mapping
selected group manifest derived only from direct metadata
missing metadata blocks instead of filling defaults
weight/GPU/backward/optimizer all sealed closed
```

## Static baked result

```txt
BLOCKED_NO_EXPLICIT_ATLAS_PLAN_RECEIPT_SOURCE
```

This result is intentional because no canonical path was supplied during static bake.

## Local verification commands

```powershell
cargo check -p base_train
cargo build -p base_train --bin ash_basetrain_gpu_35_r3a_atlas_group_plan_schema_narrowing
cargo run -p base_train --bin ash_basetrain_gpu_35_r3a_atlas_group_plan_schema_narrowing
```

Expected no-source runtime status:

```txt
BLOCKED_NO_EXPLICIT_ATLAS_PLAN_RECEIPT_SOURCE
```

Explicit path run:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_35_r3a_atlas_group_plan_schema_narrowing -- --atlas-plan-receipt .\artifacts\ash_ft\ash_ft00_atlas_group_plan.json --selected-group-index 0
```

## 추정

If the explicit file exists but does not match a supported canonical schema, the next patch should be `ASH-BASETRAIN-GPU-35-R3B` rather than `ASH-BASETRAIN-GPU-36`.

If the schema matches but selected group id/index is wrong, the next patch should be `ASH-BASETRAIN-GPU-35-R3C`.

## 판단불가

Actual local compile/run status is not known from this container because Cargo/Rust is unavailable.
