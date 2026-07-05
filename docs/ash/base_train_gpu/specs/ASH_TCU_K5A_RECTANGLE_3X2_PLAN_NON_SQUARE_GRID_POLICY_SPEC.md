# ASH-TCU-K5A — Shape Sweep Rectangle 3x2 Plan / Non-Square Macro Grid Policy Seal

## Status

`SPEC_COMMITTED_ASH_TCU_K5A_RECTANGLE_3X2_PLAN_NON_SQUARE_GRID_POLICY_SEAL`

## Scope

ASH-TCU-K5A is a plan-only TensorCube patch. It consumes the K4C native 2x2 square grid PASS receipt and seals the next non-square full-tile rectangle plan before K5B may execute native 3x2 dispatch.

K5A does not execute native 3x2 dispatch. K5A does not write readback bytes. K5A does not open production multi-macro dispatch. K5A does not make performance claims.

## Patch ID

```text
ASH-TCU-K5A
Shape Sweep Rectangle 3x2 Plan
Non-Square Macro Grid Policy Seal
No Native 3x2 Dispatch
No New Readback Bytes
No Production Multi-Macro Dispatch
No Runtime Splice
No Performance Claim
```

## Prior gates

K5A requires:

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
```

K4C must prove:

```text
status = PASS_ASH_TCU_K4C_NATIVE_2X2_SQUARE_GRID_DISPATCH_READBACK_FOUR_MACRO_COVERAGE_SEAL
descriptor_count = 4
dispatch_workgroups = [2,2,1]
readback_total_bytes = 4096
element_count = 1024
failed_count = 0
per_macro_failed_counts = [0,0,0,0]
four_macro_coverage.pass = true
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

K5A code bake must not include runtime evidence. These files must be produced locally:

```text
workspace/runtime/tensorcube/ash_tensorcube_k5a_rectangle_3x2_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5a_non_square_grid_policy_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5a_six_macro_coverage_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5a_gate_latest.json
```

K5A must not generate or bake:

```text
workspace/runtime/tensorcube/ash_tensorcube_k5a_readback_bytes_latest.bin
workspace/runtime/tensorcube/ash_tensorcube_k5a_native_3x2_dispatch_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5a_oracle_comparison_latest.json
```

## Plan-only rule

Allowed:

```text
Read K4C gate receipt
Validate K4C 2x2 PASS
Build RectangleGridPlan 3x2
Build SixMacroCoveragePlan
Validate non-square grid policy
Write K5A plan receipts
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
native 3x2 dispatch
production dispatch
performance claim
```

## K5A adoption plan

```text
descriptor_count = 6
macro_grid_width = 3
macro_grid_height = 2
planned_dispatch_workgroups = [3,2,1]
```

Logical output:

```text
total_logical_m = 32
total_logical_n = 48
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
A shape = 32 x 32
B shape = 32 x 48
C shape = 32 x 48
```

## Non-square policy

K5A introduces explicit full-tile rectangle policy:

```text
grid_kind = Rectangle
square_grid = false
non_square_grid_allowed = true
ragged_grid_allowed = false
tail_m_allowed = false
tail_n_allowed = false
tail_k_allowed = false
partial_macro_allowed = false
descriptor_count_matches_grid_product = true
dispatch_z_is_one = true
```

Allowed:

```text
3x2 rectangle plan
macro_grid_width != macro_grid_height
descriptor_count = width * height
full tile coverage
no ragged tiles
no tail tiles
```

Forbidden:

```text
ragged_grid_allowed = true
tail_m_allowed = true
tail_n_allowed = true
tail_k_allowed = true
partial_macro_allowed = true
descriptor_count != width * height
dispatch_z != 1
width = 0
height = 0
descriptor_count = 0
```

## Macro index contract

K5A keeps the existing descriptor indexing formula:

```text
macro_index = workgroup_id.y * macro_grid_width + workgroup_id.x
```

For 3x2:

```text
workgroup_id [0,0,0] -> macro_index 0
workgroup_id [1,0,0] -> macro_index 1
workgroup_id [2,0,0] -> macro_index 2
workgroup_id [0,1,0] -> macro_index 3
workgroup_id [1,1,0] -> macro_index 4
workgroup_id [2,1,0] -> macro_index 5
```

Required checks:

```text
all_macro_indices_unique = true
all_macro_indices_in_bounds = true
host_linearization_matches_wgsl = true
descriptor_macro_id_matches_linear_index = true
```

## Descriptor plan contract

```text
descriptor_count = 6
descriptors.len() = 6
```

Required descriptor summary:

```text
descriptor[0]: macro_id=0, workgroup_id=[0,0,0], row_offset=0,  col_offset=0,  a_base_element=0,   b_base_element=0,  c_base_element=0
descriptor[1]: macro_id=1, workgroup_id=[1,0,0], row_offset=0,  col_offset=16, a_base_element=0,   b_base_element=16, c_base_element=256
descriptor[2]: macro_id=2, workgroup_id=[2,0,0], row_offset=0,  col_offset=32, a_base_element=0,   b_base_element=32, c_base_element=512
descriptor[3]: macro_id=3, workgroup_id=[0,1,0], row_offset=16, col_offset=0,  a_base_element=512, b_base_element=0,  c_base_element=768
descriptor[4]: macro_id=4, workgroup_id=[1,1,0], row_offset=16, col_offset=16, a_base_element=512, b_base_element=16, c_base_element=1024
descriptor[5]: macro_id=5, workgroup_id=[2,1,0], row_offset=16, col_offset=32, a_base_element=512, b_base_element=32, c_base_element=1280
```

Per descriptor:

```text
a_row_stride = 32
a_k_stride = 1
b_k_stride = 48
b_col_stride = 1
c_row_stride = 16
c_col_stride = 1
output_scalar_count = 256
output_byte_len = 1024
valid_m = 16
valid_n = 16
valid_k = 32
planned_dispatch_workgroups = [3,2,1]
```

K5A keeps the K4C base indexing rule:

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
macro2: row_offset=0,  col_offset=32
macro3: row_offset=16, col_offset=0
macro4: row_offset=16, col_offset=16
macro5: row_offset=16, col_offset=32
```

Required alignment:

```text
row_offset % 16 = 0
col_offset % 16 = 0
valid_m = 16
valid_n = 16
valid_k = 32
```

## Expected code files in bake

```text
crates/burn_webgpu_backend/src/tensorcube_k5a_rectangle_3x2_plan.rs
crates/burn_webgpu_backend/src/tensorcube_k5a_non_square_grid_policy.rs
crates/burn_webgpu_backend/src/tensorcube_k5a_six_macro_coverage_plan.rs
crates/burn_webgpu_backend/src/tensorcube_k5a_scope_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k5a_gate.rs

crates/burn_webgpu_backend/tests/ash_tcu_k5a_rectangle_3x2_plan_schema.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5a_non_square_grid_policy.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5a_descriptor_count_matches_grid_product.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5a_macro_index_linearization_3x2.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5a_six_macro_coverage_plan.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5a_no_ragged_grid.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5a_no_tail_policy.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5a_no_native_3x2_dispatch.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5a_no_new_readback_bytes.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5a_no_production_multi_macro_dispatch.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5a_no_runtime_splice_open.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5a_no_performance_claim.rs

crates/orchestrator_local/src/ash_tcu_k5a_rectangle_3x2_plan_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k5a_rectangle_3x2_plan_audit.rs
```

## Runtime output paths

```text
workspace/runtime/tensorcube/ash_tensorcube_k5a_rectangle_3x2_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5a_non_square_grid_policy_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5a_six_macro_coverage_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5a_gate_latest.json
```

No K5A `.bin` output is allowed.

## Local Rust command

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k5a_rectangle_3x2_plan_audit `
  -- --repo-root .
```

Strict mode:

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k5a_rectangle_3x2_plan_audit `
  -- --repo-root . --require-k4c-pass
```

Summary check:

```powershell
Get-Content ".\workspace\runtime\tensorcube\ash_tensorcube_k5a_gate_latest.json" -Raw |
  ConvertFrom-Json |
  Select-Object `
    status,
    @{Name="k4c";Expression={$_.prior_gate.k4c_passed}},
    @{Name="grid";Expression={
      "$($_.rectangle_3x2_plan.grid_plan.macro_grid_width)x$($_.rectangle_3x2_plan.grid_plan.macro_grid_height)"
    }},
    @{Name="desc_count";Expression={$_.rectangle_3x2_plan.grid_plan.descriptor_count}},
    @{Name="dispatch";Expression={$_.rectangle_3x2_plan.grid_plan.planned_dispatch_workgroups -join ","}},
    @{Name="bytes";Expression={$_.rectangle_3x2_plan.grid_plan.total_output_byte_len}},
    @{Name="coverage";Expression={$_.six_macro_coverage_plan.pass}},
    @{Name="non_square";Expression={$_.non_square_grid_policy.policy.non_square_grid_allowed}},
    @{Name="ragged";Expression={$_.non_square_grid_policy.policy.ragged_grid_allowed}},
    @{Name="tail_m";Expression={$_.non_square_grid_policy.policy.tail_m_allowed}},
    @{Name="native";Expression={$_.scope_guard.native_3x2_dispatch_executed}},
    @{Name="new_bin";Expression={$_.scope_guard.new_readback_bytes_written}},
    @{Name="prod";Expression={$_.scope_guard.production_multi_macro_dispatch_allowed}} |
  Format-List
```

Expected PASS:

```text
status     : PASS_ASH_TCU_K5A_RECTANGLE_3X2_PLAN_NON_SQUARE_GRID_POLICY_SEAL
k4c        : True
grid       : 3x2
desc_count : 6
dispatch   : 3,2,1
bytes      : 6144
coverage   : True
non_square : True
ragged     : False
tail_m     : False
native     : False
new_bin    : False
prod       : False
```

## Acceptance criteria

```text
1. K4C PASS present.
2. K4C native 2x2 correctness receipt present.
3. K4C four_macro_coverage.pass = true.
4. descriptor_count = 6.
5. macro_grid_width = 3.
6. macro_grid_height = 2.
7. planned_dispatch_workgroups = [3,2,1].
8. descriptor_count = macro_grid_width * macro_grid_height.
9. total_output_scalar_count = 1536.
10. total_output_byte_len = 6144.
11. macro_indices = [0,1,2,3,4,5].
12. macro_indices_unique = true.
13. macro_indices_in_bounds = true.
14. host_linearization_matches_wgsl = true.
15. descriptor_macro_id_matches_linear_index = true.
16. six macro coverage ranges are non-overlapping.
17. six macro coverage ranges are contiguous.
18. six macro coverage covers total output.
19. tile offsets are aligned.
20. non_square_grid_allowed = true.
21. ragged_grid_allowed = false.
22. tail_m_allowed = false.
23. tail_n_allowed = false.
24. tail_k_allowed = false.
25. partial_macro_allowed = false.
26. native_3x2_dispatch_executed = false.
27. new_readback_bytes_written = false.
28. production multi-macro dispatch is closed.
29. runtime splice is closed.
30. no performance claim is made.
```

## PASS marker

```text
PASS_ASH_TCU_K5A_RECTANGLE_3X2_PLAN_NON_SQUARE_GRID_POLICY_SEAL
```

## Failure markers

```text
FAIL_ASH_TCU_K5A_MISSING_K4C_PASS
FAIL_ASH_TCU_K5A_MISSING_K4C_FOUR_MACRO_COVERAGE
FAIL_ASH_TCU_K5A_DESCRIPTOR_COUNT_NOT_SIX
FAIL_ASH_TCU_K5A_GRID_SHAPE_NOT_3X2
FAIL_ASH_TCU_K5A_DISPATCH_GRID_NOT_3X2
FAIL_ASH_TCU_K5A_DESCRIPTOR_COUNT_GRID_PRODUCT_MISMATCH
FAIL_ASH_TCU_K5A_TOTAL_OUTPUT_SCALAR_COUNT_MISMATCH
FAIL_ASH_TCU_K5A_TOTAL_OUTPUT_BYTE_LEN_MISMATCH
FAIL_ASH_TCU_K5A_MACRO_INDEX_LINEARIZATION_MISMATCH
FAIL_ASH_TCU_K5A_DESCRIPTOR_MACRO_ID_MISMATCH
FAIL_ASH_TCU_K5A_C_OUTPUT_RANGE_OVERLAP
FAIL_ASH_TCU_K5A_C_OUTPUT_COVERAGE_MISMATCH
FAIL_ASH_TCU_K5A_TILE_OFFSET_ALIGNMENT_MISMATCH
FAIL_ASH_TCU_K5A_RAGGED_GRID_ALLOWED
FAIL_ASH_TCU_K5A_TAIL_M_POLICY_OPEN
FAIL_ASH_TCU_K5A_TAIL_N_POLICY_OPEN
FAIL_ASH_TCU_K5A_TAIL_K_POLICY_OPEN
FAIL_ASH_TCU_K5A_PARTIAL_MACRO_ALLOWED
FAIL_ASH_TCU_K5A_NATIVE_3X2_DISPATCH_EXECUTED
FAIL_ASH_TCU_K5A_NEW_READBACK_BYTES_WRITTEN
FAIL_ASH_TCU_K5A_PRIOR_READBACK_REPACKAGED
FAIL_ASH_TCU_K5A_PRODUCTION_MULTI_MACRO_DISPATCH_OPEN
FAIL_ASH_TCU_K5A_RUNTIME_SPLICE_OPEN
FAIL_ASH_TCU_K5A_PERFORMANCE_CLAIM_FOUND
```

## Next allowed patch

```text
ASH-TCU-K5B — Native 3x2 Rectangle Grid Dispatch Readback / Six-Macro Coverage Correctness Seal
```

K5B is the first patch allowed to execute:

```text
descriptor_count = 6
macro_grid_width = 3
macro_grid_height = 2
dispatch_workgroups = [3,2,1]
total_output_scalar_count = 1536
total_output_byte_len = 6144
```
