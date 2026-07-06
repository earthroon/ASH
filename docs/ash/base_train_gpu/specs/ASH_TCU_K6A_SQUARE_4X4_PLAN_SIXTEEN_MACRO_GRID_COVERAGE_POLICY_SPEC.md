# ASH-TCU-K6A — Square 4x4 Plan / Sixteen-Macro Grid Coverage Policy Seal

## Status

`SPEC_COMMITTED_ASH_TCU_K6A_SQUARE_4X4_PLAN_SIXTEEN_MACRO_GRID_COVERAGE_POLICY_SEAL`

## Scope

ASH-TCU-K6A is a plan-only TensorCube scale expansion patch. It consumes the K5E rectangle orientation matrix PASS receipt and seals a 4x4 square macro grid plan before K6B may execute native 4x4 dispatch.

K6A does not execute native 4x4 dispatch. K6A does not write readback bytes. K6A does not generate a CPU oracle or oracle comparison. K6A does not open production multi-macro dispatch, runtime splice, or performance claims.

## Patch ID

```text
ASH-TCU-K6A
Square 4x4 Plan
Sixteen-Macro Grid Coverage Policy Seal
No Native 4x4 Dispatch
No New Readback Bytes
No Production Multi-Macro Dispatch
No Runtime Splice
No Performance Claim
```

## Prior gates

K6A requires:

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
K5C: Shape Sweep Rectangle 2x3 Plan / Transposed Non-Square Orientation Policy PASS
K5D: Native 2x3 Rectangle Grid Dispatch Readback / Transposed Six-Macro Coverage Correctness PASS
K5E: Rectangle Orientation Matrix Aggregation / 3x2 And 2x3 Dual Receipt PASS
```

K5E must prove:

```text
status = PASS_ASH_TCU_K5E_RECTANGLE_ORIENTATION_MATRIX_AGGREGATION_DUAL_RECEIPT_SEAL
orientation_count = 2
rectangle_3x2.pass = true
rectangle_2x3.pass = true
K5B dispatch_workgroups = [3,2,1]
K5D dispatch_workgroups = [2,3,1]
K5B readback_total_bytes = 6144
K5D readback_total_bytes = 6144
K5B element_count = 1536
K5D element_count = 1536
K5B failed_count = 0
K5D failed_count = 0
K5B per_macro_failed_counts = [0,0,0,0,0,0]
K5D per_macro_failed_counts = [0,0,0,0,0,0]
dispatch_axes_are_distinct = true
orientation_shapes_are_transposed = true
logical_shapes_are_transposed = true
new_native_dispatch_executed = false
new_readback_bytes_written = false
prior_readback_bytes_repackaged = false
materialized_tensor_fallback_used = false
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

K6A code bake must not include runtime evidence. These files must be produced locally:

```text
workspace/runtime/tensorcube/ash_tensorcube_k6a_square_4x4_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6a_sixteen_macro_coverage_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6a_square_grid_policy_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6a_gate_latest.json
```

K6A must not generate or bake:

```text
workspace/runtime/tensorcube/ash_tensorcube_k6a_readback_bytes_latest.bin
workspace/runtime/tensorcube/ash_tensorcube_k6a_native_4x4_dispatch_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6a_oracle_comparison_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6a_cpu_oracle_latest.json
```

## Plan-only rule

Allowed:

```text
Read K5E gate receipt
Validate K5E rectangle orientation matrix PASS
Build SquareGridPlan 4x4
Build SixteenMacroCoveragePlan
Validate square grid scale policy
Write K6A plan receipts
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
native 4x4 dispatch
production dispatch
performance claim
```

## K6A adoption plan

```text
descriptor_count = 16
macro_grid_width = 4
macro_grid_height = 4
planned_dispatch_workgroups = [4,4,1]
```

Logical output:

```text
total_logical_m = 64
total_logical_n = 64
macro_tile_m = 16
macro_tile_n = 16
k = 32
k_panel_count = 4
macro_output_scalar_count = 256
macro_output_byte_len = 1024
total_output_scalar_count = 4096
total_output_byte_len = 16384
```

Input matrix plan:

```text
A shape = 64 x 32
B shape = 32 x 64
C shape = 64 x 64
```

## Scale expansion policy

K6A expands beyond the K5 six-macro boundary:

```text
source_max_descriptor_count = 6
target_descriptor_count = 16
source_max_readback_total_bytes = 6144
target_planned_total_output_byte_len = 16384
source_max_element_count = 1536
target_planned_element_count = 4096
```

Required checks:

```text
descriptor_count = macro_grid_width * macro_grid_height
planned_dispatch_workgroups = [macro_grid_width, macro_grid_height, 1]
macro_index = workgroup_id.y * macro_grid_width + workgroup_id.x
coverage ranges are contiguous
coverage ranges are non-overlapping
coverage covers total output
square_grid = true
ragged grid is forbidden
tail policy is closed
legacy descriptor_count = 6 is rejected
legacy total_output_byte_len = 6144 is rejected
```

## Macro index contract

```text
macro_index = workgroup_id.y * macro_grid_width + workgroup_id.x
```

For 4x4:

```text
[0,0,0] -> macro0
[1,0,0] -> macro1
[2,0,0] -> macro2
[3,0,0] -> macro3
[0,1,0] -> macro4
[1,1,0] -> macro5
[2,1,0] -> macro6
[3,1,0] -> macro7
[0,2,0] -> macro8
[1,2,0] -> macro9
[2,2,0] -> macro10
[3,2,0] -> macro11
[0,3,0] -> macro12
[1,3,0] -> macro13
[2,3,0] -> macro14
[3,3,0] -> macro15
```

## Descriptor contract

```text
descriptor_count = 16
descriptors.len() = 16
```

Common descriptor fields:

```text
a_row_stride = 32
a_k_stride = 1
b_k_stride = 64
b_col_stride = 1
c_row_stride = 16
c_col_stride = 1
output_scalar_count = 256
output_byte_len = 1024
valid_m = 16
valid_n = 16
valid_k = 32
planned_dispatch_workgroups = [4,4,1]
```

Descriptor summary:

```text
descriptor[0]:  macro_id=0,  workgroup_id=[0,0,0], row_offset=0,  col_offset=0,  a_base_element=0,    b_base_element=0,  c_base_element=0
descriptor[1]:  macro_id=1,  workgroup_id=[1,0,0], row_offset=0,  col_offset=16, a_base_element=0,    b_base_element=16, c_base_element=256
descriptor[2]:  macro_id=2,  workgroup_id=[2,0,0], row_offset=0,  col_offset=32, a_base_element=0,    b_base_element=32, c_base_element=512
descriptor[3]:  macro_id=3,  workgroup_id=[3,0,0], row_offset=0,  col_offset=48, a_base_element=0,    b_base_element=48, c_base_element=768
descriptor[4]:  macro_id=4,  workgroup_id=[0,1,0], row_offset=16, col_offset=0,  a_base_element=512,  b_base_element=0,  c_base_element=1024
descriptor[5]:  macro_id=5,  workgroup_id=[1,1,0], row_offset=16, col_offset=16, a_base_element=512,  b_base_element=16, c_base_element=1280
descriptor[6]:  macro_id=6,  workgroup_id=[2,1,0], row_offset=16, col_offset=32, a_base_element=512,  b_base_element=32, c_base_element=1536
descriptor[7]:  macro_id=7,  workgroup_id=[3,1,0], row_offset=16, col_offset=48, a_base_element=512,  b_base_element=48, c_base_element=1792
descriptor[8]:  macro_id=8,  workgroup_id=[0,2,0], row_offset=32, col_offset=0,  a_base_element=1024, b_base_element=0,  c_base_element=2048
descriptor[9]:  macro_id=9,  workgroup_id=[1,2,0], row_offset=32, col_offset=16, a_base_element=1024, b_base_element=16, c_base_element=2304
descriptor[10]: macro_id=10, workgroup_id=[2,2,0], row_offset=32, col_offset=32, a_base_element=1024, b_base_element=32, c_base_element=2560
descriptor[11]: macro_id=11, workgroup_id=[3,2,0], row_offset=32, col_offset=48, a_base_element=1024, b_base_element=48, c_base_element=2816
descriptor[12]: macro_id=12, workgroup_id=[0,3,0], row_offset=48, col_offset=0,  a_base_element=1536, b_base_element=0,  c_base_element=3072
descriptor[13]: macro_id=13, workgroup_id=[1,3,0], row_offset=48, col_offset=16, a_base_element=1536, b_base_element=16, c_base_element=3328
descriptor[14]: macro_id=14, workgroup_id=[2,3,0], row_offset=48, col_offset=32, a_base_element=1536, b_base_element=32, c_base_element=3584
descriptor[15]: macro_id=15, workgroup_id=[3,3,0], row_offset=48, col_offset=48, a_base_element=1536, b_base_element=48, c_base_element=3840
```

Descriptor base policy:

```text
A index = desc.a_base_element + local_y * desc.a_row_stride + kk * desc.a_k_stride
B index = desc.b_base_element + kk * desc.b_k_stride + local_x * desc.b_col_stride
C index = desc.c_base_element + local_y * desc.c_row_stride + local_x * desc.c_col_stride
```

`row_offset` is metadata for coverage and logical placement. `a_base_element` already carries the row macro base, so row offset must not be double-applied.

## Sixteen-macro coverage plan

```text
macro0  = [0..256]
macro1  = [256..512]
macro2  = [512..768]
macro3  = [768..1024]
macro4  = [1024..1280]
macro5  = [1280..1536]
macro6  = [1536..1792]
macro7  = [1792..2048]
macro8  = [2048..2304]
macro9  = [2304..2560]
macro10 = [2560..2816]
macro11 = [2816..3072]
macro12 = [3072..3328]
macro13 = [3328..3584]
macro14 = [3584..3840]
macro15 = [3840..4096]
coverage_non_overlapping = true
coverage_contiguous = true
coverage_covers_total_output = true
```

## Square grid policy

```text
grid_kind = Square
orientation_kind = Square4x4
square_grid = true
non_square_grid_allowed = false
scale_expansion_allowed = true
ragged_grid_allowed = false
tail_m_allowed = false
tail_n_allowed = false
tail_k_allowed = false
partial_macro_allowed = false
descriptor_count_matches_grid_product = true
dispatch_grid_matches_macro_grid = true
dispatch_z_is_one = true
native_4x4_dispatch_allowed = false
```

## Expected code files in bake

```text
crates/burn_webgpu_backend/src/tensorcube_k6a_square_4x4_plan.rs
crates/burn_webgpu_backend/src/tensorcube_k6a_sixteen_macro_coverage_plan.rs
crates/burn_webgpu_backend/src/tensorcube_k6a_square_grid_policy.rs
crates/burn_webgpu_backend/src/tensorcube_k6a_scope_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6a_gate.rs

crates/burn_webgpu_backend/tests/ash_tcu_k6a_square_4x4_plan_schema.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_square_grid_policy.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_descriptor_count_matches_grid_product.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_macro_index_linearization_4x4.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_sixteen_macro_coverage_plan.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_expanded_from_k5e.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_total_output_byte_len_16384.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_reject_legacy_6144_byte_len.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_reject_legacy_descriptor_count_6.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_no_ragged_grid.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_no_tail_policy.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_no_native_4x4_dispatch.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_no_new_readback_bytes.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_no_production_multi_macro_dispatch.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_no_runtime_splice_open.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6a_no_performance_claim.rs

crates/orchestrator_local/src/ash_tcu_k6a_square_4x4_plan_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k6a_square_4x4_plan_audit.rs
```

## Runtime output paths

```text
workspace/runtime/tensorcube/ash_tensorcube_k6a_square_4x4_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6a_sixteen_macro_coverage_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6a_square_grid_policy_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6a_gate_latest.json
```

No K6A `.bin`, native dispatch, CPU oracle, or oracle comparison output is allowed.

## Local Rust command

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k6a_square_4x4_plan_audit `
  -- --repo-root .
```

Strict mode:

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k6a_square_4x4_plan_audit `
  -- --repo-root . --require-k5e-pass
```

Summary check:

```powershell
Get-Content ".\workspace\runtime\tensorcube\ash_tensorcube_k6a_gate_latest.json" -Raw |
  ConvertFrom-Json |
  Select-Object `
    status,
    @{Name="k5e";Expression={$_.prior_gate.k5e_passed}},
    @{Name="grid";Expression={
      "$($_.square_4x4_plan.grid_plan.macro_grid_width)x$($_.square_4x4_plan.grid_plan.macro_grid_height)"
    }},
    @{Name="desc_count";Expression={$_.square_4x4_plan.grid_plan.descriptor_count}},
    @{Name="dispatch";Expression={$_.square_4x4_plan.grid_plan.planned_dispatch_workgroups -join ","}},
    @{Name="scalars";Expression={$_.square_4x4_plan.grid_plan.total_output_scalar_count}},
    @{Name="bytes";Expression={$_.square_4x4_plan.grid_plan.total_output_byte_len}},
    @{Name="coverage";Expression={$_.sixteen_macro_coverage_plan.pass}},
    @{Name="square";Expression={$_.square_grid_policy.policy.square_grid}},
    @{Name="ragged";Expression={$_.square_grid_policy.policy.ragged_grid_allowed}},
    @{Name="tail_m";Expression={$_.square_grid_policy.policy.tail_m_allowed}},
    @{Name="native";Expression={$_.scope_guard.native_4x4_dispatch_executed}},
    @{Name="new_bin";Expression={$_.scope_guard.new_readback_bytes_written}},
    @{Name="prod";Expression={$_.scope_guard.production_multi_macro_dispatch_allowed}} |
  Format-List
```

Expected PASS:

```text
status     : PASS_ASH_TCU_K6A_SQUARE_4X4_PLAN_SIXTEEN_MACRO_GRID_COVERAGE_POLICY_SEAL
k5e        : True
grid       : 4x4
desc_count : 16
dispatch   : 4,4,1
scalars    : 4096
bytes      : 16384
coverage   : True
square     : True
ragged     : False
tail_m     : False
native     : False
new_bin    : False
prod       : False
```

## Acceptance criteria

```text
1. K5E PASS present.
2. K5E rectangle orientation matrix pass = true.
3. descriptor_count = 16.
4. macro_grid_width = 4.
5. macro_grid_height = 4.
6. planned_dispatch_workgroups = [4,4,1].
7. descriptor_count = macro_grid_width * macro_grid_height.
8. total_output_scalar_count = 4096.
9. total_output_byte_len = 16384.
10. total_logical_m = 64.
11. total_logical_n = 64.
12. macro_indices = [0..15].
13. macro_indices_unique = true.
14. macro_indices_in_bounds = true.
15. host_linearization_matches_wgsl = true.
16. descriptor_macro_id_matches_linear_index = true.
17. sixteen macro coverage ranges are non-overlapping.
18. sixteen macro coverage ranges are contiguous.
19. sixteen macro coverage covers total output.
20. tile offsets are aligned.
21. square_grid = true.
22. scale_expansion_allowed = true.
23. ragged_grid_allowed = false.
24. tail_m_allowed = false.
25. tail_n_allowed = false.
26. tail_k_allowed = false.
27. partial_macro_allowed = false.
28. legacy 6144-byte constant is rejected.
29. legacy descriptor_count 6 is rejected.
30. native_4x4_dispatch_executed = false.
31. new_readback_bytes_written = false.
32. new_cpu_oracle_generated = false.
33. new_oracle_comparison_executed = false.
34. production multi-macro dispatch remains closed.
35. runtime splice remains closed.
36. no performance claim is made.
```

## PASS marker

```text
PASS_ASH_TCU_K6A_SQUARE_4X4_PLAN_SIXTEEN_MACRO_GRID_COVERAGE_POLICY_SEAL
```

## Failure markers

```text
FAIL_ASH_TCU_K6A_MISSING_K5E_PASS
FAIL_ASH_TCU_K6A_MISSING_K5E_ORIENTATION_MATRIX
FAIL_ASH_TCU_K6A_K5E_MATRIX_NOT_PASS
FAIL_ASH_TCU_K6A_DESCRIPTOR_COUNT_NOT_SIXTEEN
FAIL_ASH_TCU_K6A_GRID_SHAPE_NOT_4X4
FAIL_ASH_TCU_K6A_DISPATCH_GRID_NOT_4X4
FAIL_ASH_TCU_K6A_DESCRIPTOR_COUNT_GRID_PRODUCT_MISMATCH
FAIL_ASH_TCU_K6A_TOTAL_OUTPUT_SCALAR_COUNT_MISMATCH
FAIL_ASH_TCU_K6A_TOTAL_OUTPUT_BYTE_LEN_MISMATCH
FAIL_ASH_TCU_K6A_LEGACY_6144_BYTE_LEN_LEAK
FAIL_ASH_TCU_K6A_LEGACY_DESCRIPTOR_COUNT_6_LEAK
FAIL_ASH_TCU_K6A_LOGICAL_SHAPE_NOT_64X64
FAIL_ASH_TCU_K6A_MACRO_INDEX_LINEARIZATION_MISMATCH
FAIL_ASH_TCU_K6A_DESCRIPTOR_MACRO_ID_MISMATCH
FAIL_ASH_TCU_K6A_C_OUTPUT_RANGE_OVERLAP
FAIL_ASH_TCU_K6A_C_OUTPUT_COVERAGE_MISMATCH
FAIL_ASH_TCU_K6A_TILE_OFFSET_ALIGNMENT_MISMATCH
FAIL_ASH_TCU_K6A_SQUARE_POLICY_MISMATCH
FAIL_ASH_TCU_K6A_RAGGED_GRID_ALLOWED
FAIL_ASH_TCU_K6A_TAIL_M_POLICY_OPEN
FAIL_ASH_TCU_K6A_TAIL_N_POLICY_OPEN
FAIL_ASH_TCU_K6A_TAIL_K_POLICY_OPEN
FAIL_ASH_TCU_K6A_PARTIAL_MACRO_ALLOWED
FAIL_ASH_TCU_K6A_NATIVE_4X4_DISPATCH_EXECUTED
FAIL_ASH_TCU_K6A_NEW_READBACK_BYTES_WRITTEN
FAIL_ASH_TCU_K6A_NEW_CPU_ORACLE_GENERATED
FAIL_ASH_TCU_K6A_NEW_ORACLE_COMPARISON_EXECUTED
FAIL_ASH_TCU_K6A_PRODUCTION_MULTI_MACRO_DISPATCH_OPEN
FAIL_ASH_TCU_K6A_RUNTIME_SPLICE_OPEN
FAIL_ASH_TCU_K6A_PERFORMANCE_CLAIM_FOUND
```

## Next allowed patch

```text
ASH-TCU-K6B — Native 4x4 Square Grid Dispatch Readback / Sixteen-Macro Coverage Correctness Seal
```

K6B is the first patch allowed to execute:

```text
descriptor_count = 16
macro_grid_width = 4
macro_grid_height = 4
dispatch_workgroups = [4,4,1]
total_output_scalar_count = 4096
total_output_byte_len = 16384
ReadbackBufferBytes = 16384 bytes
CPU oracle comparison = 4096 elements
per_macro_failed_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
```
