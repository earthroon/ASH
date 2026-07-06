# ASH-TCU-K5E — Rectangle Orientation Matrix Aggregation / 3x2 And 2x3 Dual Receipt Seal

## Status

`SPEC_COMMITTED_ASH_TCU_K5E_RECTANGLE_ORIENTATION_MATRIX_AGGREGATION_DUAL_RECEIPT_SEAL`

## Scope

ASH-TCU-K5E is an aggregation-only TensorCube patch. It consumes the K5B native 3x2 rectangle correctness receipt and the K5D native 2x3 transposed rectangle correctness receipt, then seals both as a two-row rectangle orientation matrix.

K5E does not execute a new GPU dispatch. K5E does not write readback bytes. K5E does not generate a new CPU oracle or oracle comparison. K5E does not repackage K5B/K5D readback bytes. K5E does not open production multi-macro dispatch, runtime splice, or performance claims.

## Patch ID

```text
ASH-TCU-K5E
Rectangle Orientation Matrix Aggregation
3x2 And 2x3 Dual Receipt Seal
No New Native Dispatch
No New Readback Bytes
No Prior Readback Repackage
No Production Multi-Macro Dispatch
No Runtime Splice
No Performance Claim
```

## Prior gates

K5E requires:

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
```

K5B must prove:

```text
status = PASS_ASH_TCU_K5B_NATIVE_3X2_RECTANGLE_GRID_DISPATCH_READBACK_SIX_MACRO_COVERAGE_SEAL
descriptor_count = 6
macro_grid_width = 3
macro_grid_height = 2
dispatch_workgroups = [3,2,1]
logical_m = 32
logical_n = 48
readback_total_bytes = 6144
element_count = 1536
failed_count = 0
per_macro_failed_counts = [0,0,0,0,0,0]
coverage_pass = true
oracle_comparison_pass = true
primary_gpu_evidence = true
source = ReadbackBufferBytes
prior_readback_reused = false
plan_receipt_used_as_runtime_evidence = false
materialized_tensor_fallback_used = false
ragged_grid_used = false
tail_policy_used = false
production_multi_macro_dispatch_allowed = false
runtime_splice_open = false
performance_claim_allowed = false
```

K5D must prove:

```text
status = PASS_ASH_TCU_K5D_NATIVE_2X3_RECTANGLE_GRID_DISPATCH_READBACK_TRANSPOSED_SIX_MACRO_COVERAGE_SEAL
descriptor_count = 6
macro_grid_width = 2
macro_grid_height = 3
dispatch_workgroups = [2,3,1]
logical_m = 48
logical_n = 32
readback_total_bytes = 6144
element_count = 1536
failed_count = 0
per_macro_failed_counts = [0,0,0,0,0,0]
transposed_six_macro_coverage_pass = true
oracle_comparison_pass = true
primary_gpu_evidence = true
source = ReadbackBufferBytes
prior_readback_reused = false
k5b_native_readback_reused = false
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

K5E code bake must not include runtime evidence. These files must be produced locally:

```text
workspace/runtime/tensorcube/ash_tensorcube_k5e_dual_receipt_aggregation_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5e_rectangle_orientation_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5e_gate_latest.json
```

K5E must not generate or bake:

```text
workspace/runtime/tensorcube/ash_tensorcube_k5e_readback_bytes_latest.bin
workspace/runtime/tensorcube/ash_tensorcube_k5e_native_dispatch_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5e_oracle_comparison_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5e_cpu_oracle_latest.json
```

## Aggregation identity

```text
orientation_pair = Rectangle3x2And2x3
orientation_count = 2
descriptor_count_per_orientation = 6
total_output_byte_len_per_orientation = 6144
element_count_per_orientation = 1536
```

Required entries:

```text
orientation[0] = rectangle_3x2 from ASH-TCU-K5B
orientation[1] = rectangle_2x3 from ASH-TCU-K5D
```

## Matrix contract

K5E must build exactly two matrix rows:

```text
row[0]:
  orientation_kind = Rectangle3x2
  source_patch_id = ASH-TCU-K5B
  dispatch_workgroups = [3,2,1]
  macro_grid_width = 3
  macro_grid_height = 2
  logical_m = 32
  logical_n = 48
  descriptor_count = 6
  readback_total_bytes = 6144
  element_count = 1536
  failed_count = 0
  nan_count = 0
  inf_count = 0
  per_macro_failed_counts = [0,0,0,0,0,0]
  coverage_pass = true
  oracle_comparison_pass = true
  primary_gpu_evidence = true
  pass = true

row[1]:
  orientation_kind = Rectangle2x3
  source_patch_id = ASH-TCU-K5D
  dispatch_workgroups = [2,3,1]
  macro_grid_width = 2
  macro_grid_height = 3
  logical_m = 48
  logical_n = 32
  descriptor_count = 6
  readback_total_bytes = 6144
  element_count = 1536
  failed_count = 0
  nan_count = 0
  inf_count = 0
  per_macro_failed_counts = [0,0,0,0,0,0]
  coverage_pass = true
  oracle_comparison_pass = true
  primary_gpu_evidence = true
  pass = true
```

## Matrix checks

K5E must validate:

```text
both_receipts_present = true
both_receipts_passed = true
both_primary_gpu_evidence = true
both_sources_are_readback_buffer_bytes = true
both_readback_bytes_6144 = true
both_logical_output_bytes_6144 = true
both_element_count_1536 = true
both_descriptor_count_6 = true
both_failed_count_zero = true
both_nan_inf_zero = true
both_per_macro_failed_counts_zero = true
both_coverage_passed = true
both_oracle_comparison_passed = true
both_scope_guards_closed = true

dispatch_axes_are_distinct = true
orientation_shapes_are_transposed = true
logical_shapes_are_transposed = true
byte_len_parity = true
element_count_parity = true
descriptor_count_parity = true
tolerance_parity = true

no_new_gpu_dispatch = true
no_new_readback_bytes = true
no_prior_readback_repackage = true
no_materialized_fallback = true
no_production_dispatch = true
no_runtime_splice = true
no_performance_claim = true
```

Transposition checks:

```text
K5B macro_grid_width = K5D macro_grid_height
K5B macro_grid_height = K5D macro_grid_width
K5B logical_m = K5D logical_n
K5B logical_n = K5D logical_m
K5B dispatch_workgroups = [3,2,1]
K5D dispatch_workgroups = [2,3,1]
```

## Scope guard

```text
new_native_dispatch_executed = false
new_readback_bytes_written = false
new_cpu_oracle_generated = false
new_oracle_comparison_executed = false
k5b_readback_repackaged = false
k5d_readback_repackaged = false
prior_readback_bytes_repackaged = false
materialized_tensor_fallback_used = false
production_multi_macro_dispatch_allowed = false
runtime_splice_open = false
production_dispatch_allowed = false
performance_claim_allowed = false
```

## Expected code files in bake

```text
crates/burn_webgpu_backend/src/tensorcube_k5e_receipt_reader.rs
crates/burn_webgpu_backend/src/tensorcube_k5e_dual_receipt_aggregation.rs
crates/burn_webgpu_backend/src/tensorcube_k5e_rectangle_orientation_matrix.rs
crates/burn_webgpu_backend/src/tensorcube_k5e_scope_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k5e_gate.rs

crates/burn_webgpu_backend/tests/ash_tcu_k5e_dual_receipt_aggregation_schema.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5e_rectangle_orientation_matrix_schema.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5e_requires_k5b_and_k5d.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5e_orientation_axes_distinct.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5e_logical_shapes_transposed.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5e_both_readback_bytes_6144.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5e_both_element_count_1536.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5e_both_per_macro_failed_zero.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5e_no_new_native_dispatch.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5e_no_new_readback_bytes.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5e_no_prior_readback_repackage.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5e_no_materialized_fallback.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5e_no_production_multi_macro_dispatch.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5e_no_runtime_splice_open.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5e_no_performance_claim.rs

crates/orchestrator_local/src/ash_tcu_k5e_rectangle_orientation_matrix_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k5e_rectangle_orientation_matrix_audit.rs
```

## Runtime output paths

```text
workspace/runtime/tensorcube/ash_tensorcube_k5e_dual_receipt_aggregation_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5e_rectangle_orientation_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5e_gate_latest.json
```

No K5E `.bin`, native dispatch, CPU oracle, or oracle comparison output is allowed.

## Local Rust command

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k5e_rectangle_orientation_matrix_audit `
  -- --repo-root .
```

Strict mode:

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k5e_rectangle_orientation_matrix_audit `
  -- --repo-root . --require-k5b-pass --require-k5d-pass
```

Summary check:

```powershell
Get-Content ".\workspace\runtime\tensorcube\ash_tensorcube_k5e_gate_latest.json" -Raw |
  ConvertFrom-Json |
  Select-Object `
    status,
    @{Name="k5b";Expression={$_.prior_gate.k5b_passed}},
    @{Name="k5d";Expression={$_.prior_gate.k5d_passed}},
    @{Name="orientations";Expression={$_.rectangle_orientation_matrix.matrix.orientation_count}},
    @{Name="dispatch0";Expression={$_.rectangle_orientation_matrix.matrix.orientations[0].dispatch_workgroups -join ","}},
    @{Name="dispatch1";Expression={$_.rectangle_orientation_matrix.matrix.orientations[1].dispatch_workgroups -join ","}},
    @{Name="bytes0";Expression={$_.rectangle_orientation_matrix.matrix.orientations[0].readback_total_bytes}},
    @{Name="bytes1";Expression={$_.rectangle_orientation_matrix.matrix.orientations[1].readback_total_bytes}},
    @{Name="elements0";Expression={$_.rectangle_orientation_matrix.matrix.orientations[0].element_count}},
    @{Name="elements1";Expression={$_.rectangle_orientation_matrix.matrix.orientations[1].element_count}},
    @{Name="axesDistinct";Expression={$_.rectangle_orientation_matrix.matrix_checks.dispatch_axes_are_distinct}},
    @{Name="transposed";Expression={$_.rectangle_orientation_matrix.matrix_checks.logical_shapes_are_transposed}},
    @{Name="matrixPass";Expression={$_.rectangle_orientation_matrix.matrix_checks.pass}},
    @{Name="newDispatch";Expression={$_.scope_guard.new_native_dispatch_executed}},
    @{Name="newBin";Expression={$_.scope_guard.new_readback_bytes_written}},
    @{Name="repackage";Expression={$_.scope_guard.prior_readback_bytes_repackaged}},
    @{Name="prod";Expression={$_.scope_guard.production_multi_macro_dispatch_allowed}} |
  Format-List
```

Expected PASS:

```text
status       : PASS_ASH_TCU_K5E_RECTANGLE_ORIENTATION_MATRIX_AGGREGATION_DUAL_RECEIPT_SEAL
k5b          : True
k5d          : True
orientations : 2
dispatch0    : 3,2,1
dispatch1    : 2,3,1
bytes0       : 6144
bytes1       : 6144
elements0    : 1536
elements1    : 1536
axesDistinct : True
transposed   : True
matrixPass   : True
newDispatch  : False
newBin       : False
repackage    : False
prod         : False
```

## Acceptance criteria

```text
1. K5B PASS present.
2. K5D PASS present.
3. K5B dispatch_workgroups = [3,2,1].
4. K5D dispatch_workgroups = [2,3,1].
5. K5B descriptor_count = 6.
6. K5D descriptor_count = 6.
7. K5B readback_total_bytes = 6144.
8. K5D readback_total_bytes = 6144.
9. K5B element_count = 1536.
10. K5D element_count = 1536.
11. K5B failed_count = 0.
12. K5D failed_count = 0.
13. K5B per_macro_failed_counts = [0,0,0,0,0,0].
14. K5D per_macro_failed_counts = [0,0,0,0,0,0].
15. K5B coverage pass = true.
16. K5D coverage pass = true.
17. K5B oracle comparison pass = true.
18. K5D oracle comparison pass = true.
19. K5B primary_gpu_evidence = true.
20. K5D primary_gpu_evidence = true.
21. K5B source = ReadbackBufferBytes.
22. K5D source = ReadbackBufferBytes.
23. Dispatch axes are distinct.
24. Logical shapes are transposed.
25. Matrix orientation count = 2.
26. No new native dispatch is executed.
27. No new readback bytes are written.
28. No prior readback bytes are repackaged.
29. No materialized fallback is used.
30. Production multi-macro dispatch remains closed.
31. Runtime splice remains closed.
32. No performance claim is made.
```

## PASS marker

```text
PASS_ASH_TCU_K5E_RECTANGLE_ORIENTATION_MATRIX_AGGREGATION_DUAL_RECEIPT_SEAL
```

## Failure markers

```text
FAIL_ASH_TCU_K5E_MISSING_K5B_PASS
FAIL_ASH_TCU_K5E_MISSING_K5D_PASS
FAIL_ASH_TCU_K5E_MISSING_NATIVE_RECEIPT
FAIL_ASH_TCU_K5E_NATIVE_RECEIPT_NOT_PASS
FAIL_ASH_TCU_K5E_K5B_DISPATCH_NOT_3X2
FAIL_ASH_TCU_K5E_K5D_DISPATCH_NOT_2X3
FAIL_ASH_TCU_K5E_DESCRIPTOR_COUNT_MISMATCH
FAIL_ASH_TCU_K5E_READBACK_BYTE_LEN_MISMATCH
FAIL_ASH_TCU_K5E_ELEMENT_COUNT_MISMATCH
FAIL_ASH_TCU_K5E_FAILED_COUNT_NONZERO
FAIL_ASH_TCU_K5E_PER_MACRO_FAILURE_FOUND
FAIL_ASH_TCU_K5E_NAN_OR_INF_FOUND
FAIL_ASH_TCU_K5E_COVERAGE_NOT_PASS
FAIL_ASH_TCU_K5E_ORACLE_COMPARISON_NOT_PASS
FAIL_ASH_TCU_K5E_PRIMARY_GPU_EVIDENCE_MISSING
FAIL_ASH_TCU_K5E_SOURCE_NOT_READBACK_BUFFER_BYTES
FAIL_ASH_TCU_K5E_ORIENTATION_COUNT_NOT_TWO
FAIL_ASH_TCU_K5E_DISPATCH_AXES_NOT_DISTINCT
FAIL_ASH_TCU_K5E_LOGICAL_SHAPES_NOT_TRANSPOSED
FAIL_ASH_TCU_K5E_MATRIX_BYTE_PARITY_MISMATCH
FAIL_ASH_TCU_K5E_MATRIX_ELEMENT_PARITY_MISMATCH
FAIL_ASH_TCU_K5E_MATRIX_DESCRIPTOR_PARITY_MISMATCH
FAIL_ASH_TCU_K5E_NEW_NATIVE_DISPATCH_EXECUTED
FAIL_ASH_TCU_K5E_NEW_READBACK_BYTES_WRITTEN
FAIL_ASH_TCU_K5E_NEW_CPU_ORACLE_GENERATED
FAIL_ASH_TCU_K5E_NEW_ORACLE_COMPARISON_EXECUTED
FAIL_ASH_TCU_K5E_K5B_READBACK_REPACKAGED
FAIL_ASH_TCU_K5E_K5D_READBACK_REPACKAGED
FAIL_ASH_TCU_K5E_PRIOR_READBACK_REPACKAGED
FAIL_ASH_TCU_K5E_MATERIALIZED_FALLBACK_USED
FAIL_ASH_TCU_K5E_PRODUCTION_MULTI_MACRO_DISPATCH_OPEN
FAIL_ASH_TCU_K5E_RUNTIME_SPLICE_OPEN
FAIL_ASH_TCU_K5E_PERFORMANCE_CLAIM_FOUND
```

## Next allowed patch

```text
ASH-TCU-K5F — Rectangle Runtime Candidate Policy / Orientation Matrix To Non-Production Dispatch Registry Seal
```

K5F is not production runtime splice. It may only decide whether the K5E rectangle orientation matrix can be elevated into a non-production runtime candidate registry.
