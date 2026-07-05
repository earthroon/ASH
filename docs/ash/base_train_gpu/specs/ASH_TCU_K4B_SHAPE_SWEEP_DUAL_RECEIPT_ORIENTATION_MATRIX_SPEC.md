# ASH-TCU-K4B — Shape Sweep 2x1 / 1x2 Dual Receipt Aggregation / Orientation Matrix Seal

## Status

`SPEC_COMMITTED_ASH_TCU_K4B_SHAPE_SWEEP_DUAL_RECEIPT_ORIENTATION_MATRIX_SEAL`

## Scope

ASH-TCU-K4B aggregates the native multi-macro correctness receipts from K3D and K4A into a single orientation matrix receipt.

K3D proved horizontal `2x1` native correctness with `dispatch_workgroups=[2,1,1]`, 2048-byte `ReadbackBufferBytes`, and a 512-element CPU oracle comparison.

K4A proved vertical `1x2` native correctness with `dispatch_workgroups=[1,2,1]`, 2048-byte `ReadbackBufferBytes`, and a 512-element CPU oracle comparison.

K4B performs receipt aggregation only. It does not execute a new GPU dispatch. It does not write a new readback `.bin`. It does not open production multi-macro dispatch.

## Patch ID

```text
ASH-TCU-K4B
Shape Sweep 2x1 / 1x2 Dual Receipt Aggregation
Orientation Matrix Seal
No New Native Dispatch
No New Readback Bytes
No Production Multi-Macro Dispatch
No Runtime Splice
No Performance Claim
```

## Prior gates

K4B requires:

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
```

K3D must prove:

```text
status = PASS_ASH_TCU_K3D_NATIVE_2X1_MULTI_MACRO_DISPATCH_READBACK_CORRECTNESS_SEAL
dispatch_workgroups = [2, 1, 1]
readback_total_bytes = 2048
logical_output_bytes = 2048
scalar_count = 512
element_count = 512
failed_count = 0
nan_count = 0
inf_count = 0
primary_gpu_evidence = true
single_macro_readback_reused = false
materialized_tensor_fallback_used = false
production_multi_macro_dispatch_allowed = false
```

K4A must prove:

```text
status = PASS_ASH_TCU_K4A_SHAPE_SWEEP_2X1_TO_1X2_GRID_ORIENTATION_PARITY_SEAL
dispatch_workgroups = [1, 2, 1]
readback_total_bytes = 2048
logical_output_bytes = 2048
scalar_count = 512
element_count = 512
failed_count = 0
nan_count = 0
inf_count = 0
primary_gpu_evidence = true
single_macro_readback_reused = false
materialized_tensor_fallback_used = false
production_multi_macro_dispatch_allowed = false
```

## Artifact ownership rule

```text
Code bake target: uploaded ASH ZIP tree
Spec ownership: GitHub repository docs
Runtime receipt ownership: local Rust execution output
Runtime artifact ownership: local Rust execution output
```

K4B runtime receipts are generated locally.

K4B code bake must not include these generated files:

```text
workspace/runtime/tensorcube/ash_tensorcube_k4b_dual_receipt_aggregation_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k4b_orientation_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k4b_gate_latest.json
```

K4B must not generate or bake:

```text
workspace/runtime/tensorcube/ash_tensorcube_k4b_readback_bytes_latest.bin
```

## Evidence rule

K4B does not create new primary GPU evidence.

K4B consumes K3D and K4A as prior evidence:

```text
k3d.readback_digest.primary_gpu_evidence = true
k4a.readback_digest.primary_gpu_evidence = true
```

Forbidden:

```text
K3D readback bytes copied as K4B evidence
K4A readback bytes copied as K4B evidence
K3D/K4A readback bytes concatenated into a new .bin
K3D/K4A digest renamed as a K4B digest
new native dispatch
new map_async
new GPU adapter/device request
new readback buffer
production dispatch
performance claim
```

K4B primary output is the orientation matrix receipt.

## Orientation matrix v1

Expected matrix:

```text
horizontal_2x1:
  source_patch_id = ASH-TCU-K3D
  dispatch_workgroups = [2, 1, 1]
  macro_grid_width = 2
  macro_grid_height = 1
  m = 16
  n = 32
  readback_total_bytes = 2048
  element_count = 512
  failed_count = 0
  pass = true

vertical_1x2:
  source_patch_id = ASH-TCU-K4A
  dispatch_workgroups = [1, 2, 1]
  macro_grid_width = 1
  macro_grid_height = 2
  m = 32
  n = 16
  readback_total_bytes = 2048
  element_count = 512
  failed_count = 0
  pass = true
```

Required matrix checks:

```text
both_orientations_present = true
both_orientations_passed = true
dispatch_axes_are_distinct = true
byte_len_parity = true
element_count_parity = true
tolerance_parity = true
no_new_gpu_dispatch = true
no_new_readback_bytes = true
pass = true
```

## Axis distinction contract

K4B must prove the two receipts are not duplicate orientations.

Required:

```text
K3D dispatch = [2,1,1]
K4A dispatch = [1,2,1]
K3D macro_grid_width = 2
K3D macro_grid_height = 1
K4A macro_grid_width = 1
K4A macro_grid_height = 2
```

Forbidden:

```text
K4A dispatch = [2,1,1]
K3D dispatch = [1,2,1]
K3D and K4A dispatch grids are identical
K4A gate copied from K3D gate
readback digest equality used as orientation proof
```

K3D and K4A readback hashes are not expected to match.

## Expected code files in bake

```text
crates/burn_webgpu_backend/src/tensorcube_k4b_dual_receipt_aggregation.rs
crates/burn_webgpu_backend/src/tensorcube_k4b_orientation_matrix.rs
crates/burn_webgpu_backend/src/tensorcube_k4b_receipt_reader.rs
crates/burn_webgpu_backend/src/tensorcube_k4b_scope_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k4b_gate.rs

crates/burn_webgpu_backend/tests/ash_tcu_k4b_dual_receipt_aggregation_schema.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4b_orientation_matrix_schema.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4b_requires_k3d_and_k4a.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4b_axis_distinction.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4b_no_new_native_dispatch.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4b_no_new_readback_bytes.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4b_no_prior_readback_repackage.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4b_no_production_multi_macro_dispatch.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4b_no_runtime_splice_open.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4b_no_performance_claim.rs

crates/orchestrator_local/src/ash_tcu_k4b_orientation_matrix_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k4b_orientation_matrix_audit.rs
```

## Runtime output paths

```text
workspace/runtime/tensorcube/ash_tensorcube_k4b_dual_receipt_aggregation_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k4b_orientation_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k4b_gate_latest.json
```

No K4B `.bin` output is allowed.

## Local Rust command

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k4b_orientation_matrix_audit `
  -- --repo-root .
```

Strict mode:

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k4b_orientation_matrix_audit `
  -- --repo-root . --require-k3d-pass --require-k4a-pass
```

Summary check:

```powershell
Get-Content ".\workspace\runtime\tensorcube\ash_tensorcube_k4b_gate_latest.json" -Raw |
  ConvertFrom-Json |
  Select-Object `
    status,
    @{Name="k3d";Expression={$_.prior_gate.k3d_passed}},
    @{Name="k4a";Expression={$_.prior_gate.k4a_passed}},
    @{Name="h_dispatch";Expression={$_.orientation_matrix.orientations.horizontal_2x1.dispatch_workgroups -join ","}},
    @{Name="v_dispatch";Expression={$_.orientation_matrix.orientations.vertical_1x2.dispatch_workgroups -join ","}},
    @{Name="h_pass";Expression={$_.orientation_matrix.orientations.horizontal_2x1.pass}},
    @{Name="v_pass";Expression={$_.orientation_matrix.orientations.vertical_1x2.pass}},
    @{Name="axes";Expression={$_.orientation_matrix.matrix_checks.dispatch_axes_are_distinct}},
    @{Name="bytes";Expression={$_.orientation_matrix.matrix_checks.byte_len_parity}},
    @{Name="elements";Expression={$_.orientation_matrix.matrix_checks.element_count_parity}},
    @{Name="new_gpu";Expression={$_.scope_guard.new_native_dispatch_executed}},
    @{Name="new_bin";Expression={$_.scope_guard.new_readback_bytes_written}},
    @{Name="prod";Expression={$_.scope_guard.production_multi_macro_dispatch_allowed}} |
  Format-List
```

Expected PASS:

```text
status     : PASS_ASH_TCU_K4B_SHAPE_SWEEP_DUAL_RECEIPT_ORIENTATION_MATRIX_SEAL
k3d        : True
k4a        : True
h_dispatch : 2,1,1
v_dispatch : 1,2,1
h_pass     : True
v_pass     : True
axes       : True
bytes      : True
elements   : True
new_gpu    : False
new_bin    : False
prod       : False
```

## Acceptance criteria

```text
1. K0 identity receipt present.
2. K1 execution-state receipt present.
3. K2 correctness PASS present.
4. K2-R1 readback evidence present as prior gate only.
5. K3A PASS present.
6. K3B PASS present.
7. K3C PASS present.
8. K3D PASS present.
9. K4A PASS present.
10. K3D dispatch_workgroups = [2,1,1].
11. K4A dispatch_workgroups = [1,2,1].
12. K3D and K4A dispatch axes are distinct.
13. K3D readback_total_bytes = 2048.
14. K4A readback_total_bytes = 2048.
15. K3D element_count = 512.
16. K4A element_count = 512.
17. K3D failed_count = 0.
18. K4A failed_count = 0.
19. K3D nan_count = 0.
20. K4A nan_count = 0.
21. K3D inf_count = 0.
22. K4A inf_count = 0.
23. K3D primary_gpu_evidence = true.
24. K4A primary_gpu_evidence = true.
25. K3D materialized fallback = false.
26. K4A materialized fallback = false.
27. K3D/K4A production dispatch = false.
28. K4B new_native_dispatch_executed = false.
29. K4B new_readback_bytes_written = false.
30. K4B prior_readback_bytes_repackaged = false.
31. K4B runtime splice = false.
32. K4B performance claim = false.
```

## PASS marker

```text
PASS_ASH_TCU_K4B_SHAPE_SWEEP_DUAL_RECEIPT_ORIENTATION_MATRIX_SEAL
```

## Failure markers

```text
FAIL_ASH_TCU_K4B_MISSING_K0_RECEIPT
FAIL_ASH_TCU_K4B_MISSING_K1_RECEIPT
FAIL_ASH_TCU_K4B_MISSING_K2_PASS
FAIL_ASH_TCU_K4B_MISSING_K2_R1_READBACK
FAIL_ASH_TCU_K4B_MISSING_K3A_PASS
FAIL_ASH_TCU_K4B_MISSING_K3B_PASS
FAIL_ASH_TCU_K4B_MISSING_K3C_PASS
FAIL_ASH_TCU_K4B_MISSING_K3D_PASS
FAIL_ASH_TCU_K4B_MISSING_K4A_PASS
FAIL_ASH_TCU_K4B_K3D_DISPATCH_NOT_2X1
FAIL_ASH_TCU_K4B_K4A_DISPATCH_NOT_1X2
FAIL_ASH_TCU_K4B_ORIENTATION_AXIS_NOT_DISTINCT
FAIL_ASH_TCU_K4B_K3D_READBACK_BYTE_LEN_MISMATCH
FAIL_ASH_TCU_K4B_K4A_READBACK_BYTE_LEN_MISMATCH
FAIL_ASH_TCU_K4B_ELEMENT_COUNT_MISMATCH
FAIL_ASH_TCU_K4B_FAILED_COUNT_NONZERO
FAIL_ASH_TCU_K4B_NAN_FOUND
FAIL_ASH_TCU_K4B_INF_FOUND
FAIL_ASH_TCU_K4B_PRIMARY_GPU_EVIDENCE_MISSING
FAIL_ASH_TCU_K4B_MATERIALIZED_FALLBACK_USED
FAIL_ASH_TCU_K4B_NEW_NATIVE_DISPATCH_EXECUTED
FAIL_ASH_TCU_K4B_NEW_READBACK_BYTES_WRITTEN
FAIL_ASH_TCU_K4B_PRIOR_READBACK_REPACKAGED
FAIL_ASH_TCU_K4B_PRODUCTION_MULTI_MACRO_DISPATCH_OPEN
FAIL_ASH_TCU_K4B_RUNTIME_SPLICE_OPEN
FAIL_ASH_TCU_K4B_PERFORMANCE_CLAIM_FOUND
```

## Next allowed patch

```text
ASH-TCU-K4C — Native 2x2 Square Grid Dispatch Readback / Four-Macro Coverage Correctness Seal
```

K4C is the first patch allowed to execute:

```text
descriptor_count = 4
macro_grid_width = 2
macro_grid_height = 2
dispatch_workgroups = [2,2,1]
total_output_scalar_count = 1024
total_output_byte_len = 4096
```
