# ASH-TCU-K5C — Shape Sweep Rectangle 2x3 Plan / Transposed Non-Square Orientation Policy Seal

## Status

`SPEC_COMMITTED_ASH_TCU_K5C_RECTANGLE_2X3_PLAN_TRANSPOSED_NON_SQUARE_ORIENTATION_POLICY_SEAL`

## Scope

ASH-TCU-K5C is a plan-only TensorCube patch. It consumes the K5B native 3x2 rectangle grid PASS receipt and seals the transposed non-square 2x3 rectangle plan before K5D may execute native 2x3 dispatch.

K5C does not execute native 2x3 dispatch. K5C does not write readback bytes. K5C does not reuse K5B native readback bytes as evidence. K5C does not open production multi-macro dispatch. K5C does not make performance claims.

## Patch ID

```text
ASH-TCU-K5C
Shape Sweep Rectangle 2x3 Plan
Transposed Non-Square Orientation Policy Seal
No Native 2x3 Dispatch
No New Readback Bytes
No Production Multi-Macro Dispatch
No Runtime Splice
No Performance Claim
```

## Prior gates

K5C requires:

```text
K0: TensorCube kernel SSOT identity PASS
K1: CI software adapter / static PASS separation PASS
K2: CPU oracle + mapped readback digest harness PASS
K2-R1: native single-macro dispatch readback producer PASS
K3A: Macro Descriptor Array / Single Macro Compatibility PASS
K3B: WGSL Multi-Macro Descriptor Indexing / Descriptor Array Read Path PASS
K3C: Host Macro Grid Builder / Descriptor Count To Dispatch Grid PASS
K3D: Native 2x1 Multi-Macro Dispatch Readback Correctness PASS
K4A: Shape Sweep 2x1 To 1x2 / Grid Orientation Parity PASS
K4B: Shape Sweep 2x1 / 1x2 Dual Receipt Aggregation / Orientation Matrix PASS
K4C: Native 2x2 Square Grid Dispatch Readback / Four-Macro Coverage Correctness PASS
K5A: Shape Sweep Rectangle 3x2 Plan / Non-Square Macro Grid Policy PASS
K5B: Native 3x2 Rectangle Grid Dispatch Readback / Six-Macro Coverage Correctness PASS
```

K5B must prove:

```text
status = PASS_ASH_TCU_K5B_NATIVE_3X2_RECTANGLE_GRID_DISPATCH_READBACK_SIX_MACRO_COVERAGE_SEAL
descriptor_count = 6
macro_grid_width = 3
macro_grid_height = 2
dispatch_workgroups = [3,2,1]
readback_total_bytes = 6144
logical_output_bytes = 6144
element_count = 1536
failed_count = 0
per_macro_failed_counts = [0,0,0,0,0,0]
nan_count = 0
inf_count = 0
six_macro_coverage.pass = true
oracle_comparison.pass = true
primary_gpu_evidence = true
prior_readback_reused = false
plan_receipt_used_as_runtime_evidence = false
materialized_tensor_fallback_used = false
ragged_grid_used = false
tail_policy_used = false
production_multi_macro_dispatch_allowed = false
runtime_splice_open = false
performance_claim_allowed = false
```

## Artifact ownership rule

```text
Code bake target: uploaded ASH ZIP tree
Spec ownership: GitHub repository docs
Runtime receipt ownership: local Rust execution output
Runtime artifact ownership: local Rust execution output
```

K5C code bake must not include runtime evidence. These files must be produced locally:

```text
workspace/runtime/tensorcube/ash_tensorcube_k5c_rectangle_2x3_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5c_transposed_non_square_policy_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5c_six_macro_coverage_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5c_gate_latest.json
```

K5C must not generate or bake:

```text
workspace/runtime/tensorcube/ash_tensorcube_k5c_readback_bytes_latest.bin
workspace/runtime/tensorcube/ash_tensorcube_k5c_native_2x3_dispatch_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5c_oracle_comparison_latest.json
```

## Plan-only rule

Allowed:

```text
Read K5B gate receipt
Validate K5B 3x2 native PASS
Build RectangleGridPlan 2x3
Build SixMacroCoveragePlan for transposed orientation
Validate transposed non-square orientation policy
Write K5C plan receipts
```

Forbidden:

```text
adapter request
device request
compute pipeline creation
bind group creation
dispatch encoding
queue submit
map_async
new readback bytes
new CPU oracle GPU comparison
native 2x3 dispatch
production dispatch
performance claim
```

## K5C adoption plan

```text
descriptor_count = 6
macro_grid_width = 2
macro_grid_height = 3
planned_dispatch_workgroups = [2,3,1]
```

Logical output:

```text
total_logical_m = 48
total_logical_n = 32
macro_tile_m = 16
macro_tile_n = 16
k = 32
k_panel_count = 4
macro_output_scalar_count = 256
macro_output_byte_len = 1024
total_output_scalar_count = 1536
total_output_byte_len = 6144
```

Input matrix plan:

```text
A shape = 48 x 32
B shape = 32 x 32
C shape = 48 x 32
```

## Transposed orientation policy

K5C must prove that it is the transposed orientation of K5B:

```text
source_orientation = 3x2
target_orientation = 2x3
source_macro_grid_width = 3
source_macro_grid_height = 2
target_macro_grid_width = 2
target_macro_grid_height = 3
descriptor_count_preserved = true
total_output_byte_len_preserved = true
orientation_transposed = true
```

Required distinction:

```text
K5B dispatch = [3,2,1]
K5C planned_dispatch = [2,3,1]
K5B logical_m = 32
K5B logical_n = 48
K5C logical_m = 48
K5C logical_n = 32
```

## Macro index contract

K5C keeps the existing descriptor indexing formula:

```text
macro_index = workgroup_id.y * macro_grid_width + workgroup_id.x
```

For 2x3:

```text
workgroup_id [0,0,0] -> macro_index 0
workgroup_id [1,0,0] -> macro_index 1
workgroup_id [0,1,0] -> macro_index 2
workgroup_id [1,1,0] -> macro_index 3
workgroup_id [0,2,0] -> macro_index 4
workgroup_id [1,2,0] -> macro_index 5
```

## Descriptor plan contract

```text
descriptor_count = 6
descriptors.len() = 6
```

Required descriptor summary:

```text
descriptor[0]: macro_id=0, workgroup_id=[0,0,0], row_offset=0,  col_offset=0,  a_base_element=0,    b_base_element=0,  c_base_element=0
descriptor[1]: macro_id=1, workgroup_id=[1,0,0], row_offset=0,  col_offset=16, a_base_element=0,    b_base_element=16, c_base_element=256
descriptor[2]: macro_id=2, workgroup_id=[0,1,0], row_offset=16, col_offset=0,  a_base_element=512,  b_base_element=0,  c_base_element=512
descriptor[3]: macro_id=3, workgroup_id=[1,1,0], row_offset=16, col_offset=16, a_base_element=512,  b_base_element=16, c_base_element=768
descriptor[4]: macro_id=4, workgroup_id=[0,2,0], row_offset=32, col_offset=0,  a_base_element=1024, b_base_element=0,  c_base_element=1024
descriptor[5]: macro_id=5, workgroup_id=[1,2,0], row_offset=32, col_offset=16, a_base_element=1024, b_base_element=16, c_base_element=1280
```

Per descriptor:

```text
a_row_stride = 32
a_k_stride = 1
b_k_stride = 32
b_col_stride = 1
c_row_stride = 16
c_col_stride = 1
output_scalar_count = 256
output_byte_len = 1024
valid_m = 16
valid_n = 16
valid_k = 32
planned_dispatch_workgroups = [2,3,1]
```

K5C keeps the K4C/K5A/K5B base indexing rule:

```text
A index = desc.a_base_element + local_y * desc.a_row_stride + kk * desc.a_k_stride
B index = desc.b_base_element + kk * desc.b_k_stride + local_x * desc.b_col_stride
C index = desc.c_base_element + local_y * desc.c_row_stride + local_x * desc.c_col_stride
```

`row_offset` is metadata for coverage and logical placement. `a_base_element` already carries the row macro base, so row offset must not be double-applied in A indexing.

## Six-macro coverage plan

```text
macro0 = [0..256]
macro1 = [256..512]
macro2 = [512..768]
macro3 = [768..1024]
macro4 = [1024..1280]
macro5 = [1280..1536]
coverage_non_overlapping = true
coverage_contiguous = true
coverage_covers_total_output = true
```

Required macro coordinates:

```text
macro0: row_offset=0,  col_offset=0
macro1: row_offset=0,  col_offset=16
macro2: row_offset=16, col_offset=0
macro3: row_offset=16, col_offset=16
macro4: row_offset=32, col_offset=0
macro5: row_offset=32, col_offset=16
```

## Policy receipt expectations

```text
grid_kind = Rectangle
orientation_kind = TransposedRectangle
source_orientation = 3x2
target_orientation = 2x3
square_grid = false
non_square_grid_allowed = true
transposed_orientation_allowed = true
ragged_grid_allowed = false
tail_m_allowed = false
tail_n_allowed = false
tail_k_allowed = false
partial_macro_allowed = false
descriptor_count_matches_grid_product = true
dispatch_z_is_one = true
native_2x3_dispatch_allowed = false
```

## Expected code files in bake

```text
crates/burn_webgpu_backend/src/tensorcube_k5c_rectangle_2x3_plan.rs
crates/burn_webgpu_backend/src/tensorcube_k5c_transposed_non_square_policy.rs
crates/burn_webgpu_backend/src/tensorcube_k5c_six_macro_coverage_plan.rs
crates/burn_webgpu_backend/src/tensorcube_k5c_scope_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k5c_gate.rs

crates/burn_webgpu_backend/tests/ash_tcu_k5c_rectangle_2x3_plan_schema.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5c_transposed_non_square_policy.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5c_descriptor_count_matches_grid_product.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5c_macro_index_linearization_2x3.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5c_six_macro_coverage_plan.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5c_transposed_from_k5b.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5c_no_ragged_grid.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5c_no_tail_policy.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5c_no_native_2x3_dispatch.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5c_no_new_readback_bytes.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5c_no_k5b_readback_reuse.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5c_no_production_multi_macro_dispatch.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5c_no_runtime_splice_open.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5c_no_performance_claim.rs

crates/orchestrator_local/src/ash_tcu_k5c_rectangle_2x3_plan_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k5c_rectangle_2x3_plan_audit.rs
```

## Runtime output paths

```text
workspace/runtime/tensorcube/ash_tensorcube_k5c_rectangle_2x3_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5c_transposed_non_square_policy_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5c_six_macro_coverage_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5c_gate_latest.json
```

No K5C `.bin` output is allowed.

## Local Rust command

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k5c_rectangle_2x3_plan_audit `
  -- --repo-root .
```

Strict mode:

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k5c_rectangle_2x3_plan_audit `
  -- --repo-root . --require-k5b-pass
```

Summary check:

```powershell
Get-Content ".\workspace\runtime\tensorcube\ash_tensorcube_k5c_gate_latest.json" -Raw |
  ConvertFrom-Json |
  Select-Object `
    status,
    @{Name="k5b";Expression={$_.prior_gate.k5b_passed}},
    @{Name="grid";Expression={
      "$($_.rectangle_2x3_plan.grid_plan.macro_grid_width)x$($_.rectangle_2x3_plan.grid_plan.macro_grid_height)"
    }},
    @{Name="desc_count";Expression={$_.rectangle_2x3_plan.grid_plan.descriptor_count}},
    @{Name="dispatch";Expression={$_.rectangle_2x3_plan.grid_plan.planned_dispatch_workgroups -join ","}},
    @{Name="bytes";Expression={$_.rectangle_2x3_plan.grid_plan.total_output_byte_len}},
    @{Name="coverage";Expression={$_.six_macro_coverage_plan.pass}},
    @{Name="transposed";Expression={$_.rectangle_2x3_plan.grid_plan.transposed_from_k5b_3x2}},
    @{Name="non_square";Expression={$_.transposed_non_square_policy.policy.non_square_grid_allowed}},
    @{Name="ragged";Expression={$_.transposed_non_square_policy.policy.ragged_grid_allowed}},
    @{Name="tail_m";Expression={$_.transposed_non_square_policy.policy.tail_m_allowed}},
    @{Name="native";Expression={$_.scope_guard.native_2x3_dispatch_executed}},
    @{Name="new_bin";Expression={$_.scope_guard.new_readback_bytes_written}},
    @{Name="reuse";Expression={$_.scope_guard.k5b_native_readback_reused}},
    @{Name="prod";Expression={$_.scope_guard.production_multi_macro_dispatch_allowed}} |
  Format-List
```

Expected PASS:

```text
status     : PASS_ASH_TCU_K5C_RECTANGLE_2X3_PLAN_TRANSPOSED_NON_SQUARE_ORIENTATION_POLICY_SEAL
k5b        : True
grid       : 2x3
desc_count : 6
dispatch   : 2,3,1
bytes      : 6144
coverage   : True
transposed : True
non_square : True
ragged     : False
tail_m     : False
native     : False
new_bin    : False
reuse      : False
prod       : False
```

## Acceptance criteria

```text
1. K5B PASS present.
2. K5B native 3x2 correctness receipt present.
3. K5B six_macro_coverage.pass = true.
4. descriptor_count = 6.
5. macro_grid_width = 2.
6. macro_grid_height = 3.
7. planned_dispatch_workgroups = [2,3,1].
8. descriptor_count = macro_grid_width * macro_grid_height.
9. total_output_scalar_count = 1536.
10. total_output_byte_len = 6144.
11. total_logical_m = 48.
12. total_logical_n = 32.
13. macro_indices = [0,1,2,3,4,5].
14. macro_indices_unique = true.
15. macro_indices_in_bounds = true.
16. host_linearization_matches_wgsl = true.
17. descriptor_macro_id_matches_linear_index = true.
18. six macro coverage ranges are non-overlapping.
19. six macro coverage ranges are contiguous.
20. six macro coverage covers total output.
21. tile offsets are aligned.
22. transposed_from_k5b_3x2 = true.
23. source_orientation = 3x2.
24. target_orientation = 2x3.
25. non_square_grid_allowed = true.
26. transposed_orientation_allowed = true.
27. ragged_grid_allowed = false.
28. tail_m_allowed = false.
29. tail_n_allowed = false.
30. tail_k_allowed = false.
31. partial_macro_allowed = false.
32. native_2x3_dispatch_executed = false.
33. new_readback_bytes_written = false.
34. k5b_native_readback_reused = false.
35. production multi-macro dispatch is closed.
36. runtime splice is closed.
37. no performance claim is made.
```

## PASS marker

```text
PASS_ASH_TCU_K5C_RECTANGLE_2X3_PLAN_TRANSPOSED_NON_SQUARE_ORIENTATION_POLICY_SEAL
```

## Failure markers

```text
FAIL_ASH_TCU_K5C_MISSING_K5B_PASS
FAIL_ASH_TCU_K5C_MISSING_K5B_NATIVE_3X2_CORRECTNESS
FAIL_ASH_TCU_K5C_MISSING_K5B_SIX_MACRO_COVERAGE
FAIL_ASH_TCU_K5C_DESCRIPTOR_COUNT_NOT_SIX
FAIL_ASH_TCU_K5C_GRID_SHAPE_NOT_2X3
FAIL_ASH_TCU_K5C_DISPATCH_GRID_NOT_2X3
FAIL_ASH_TCU_K5C_DESCRIPTOR_COUNT_GRID_PRODUCT_MISMATCH
FAIL_ASH_TCU_K5C_TOTAL_OUTPUT_SCALAR_COUNT_MISMATCH
FAIL_ASH_TCU_K5C_TOTAL_OUTPUT_BYTE_LEN_MISMATCH
FAIL_ASH_TCU_K5C_LOGICAL_SHAPE_NOT_TRANSPOSED
FAIL_ASH_TCU_K5C_NOT_TRANSPOSED_FROM_K5B
FAIL_ASH_TCU_K5C_MACRO_INDEX_LINEARIZATION_MISMATCH
FAIL_ASH_TCU_K5C_DESCRIPTOR_MACRO_ID_MISMATCH
FAIL_ASH_TCU_K5C_C_OUTPUT_RANGE_OVERLAP
FAIL_ASH_TCU_K5C_C_OUTPUT_COVERAGE_MISMATCH
FAIL_ASH_TCU_K5C_TILE_OFFSET_ALIGNMENT_MISMATCH
FAIL_ASH_TCU_K5C_RAGGED_GRID_ALLOWED
FAIL_ASH_TCU_K5C_TAIL_M_POLICY_OPEN
FAIL_ASH_TCU_K5C_TAIL_N_POLICY_OPEN
FAIL_ASH_TCU_K5C_TAIL_K_POLICY_OPEN
FAIL_ASH_TCU_K5C_PARTIAL_MACRO_ALLOWED
FAIL_ASH_TCU_K5C_NATIVE_2X3_DISPATCH_EXECUTED
FAIL_ASH_TCU_K5C_NEW_READBACK_BYTES_WRITTEN
FAIL_ASH_TCU_K5C_K5B_NATIVE_READBACK_REUSED
FAIL_ASH_TCU_K5C_PRIOR_READBACK_REPACKAGED
FAIL_ASH_TCU_K5C_PRODUCTION_MULTI_MACRO_DISPATCH_OPEN
FAIL_ASH_TCU_K5C_RUNTIME_SPLICE_OPEN
FAIL_ASH_TCU_K5C_PERFORMANCE_CLAIM_FOUND
```

## Next allowed patch

```text
ASH-TCU-K5D — Native 2x3 Rectangle Grid Dispatch Readback / Transposed Six-Macro Coverage Correctness Seal
```

K5D is the first patch allowed to execute:

```text
descriptor_count = 6
macro_grid_width = 2
macro_grid_height = 3
dispatch_workgroups = [2,3,1]
total_output_scalar_count = 1536
total_output_byte_len = 6144
```
