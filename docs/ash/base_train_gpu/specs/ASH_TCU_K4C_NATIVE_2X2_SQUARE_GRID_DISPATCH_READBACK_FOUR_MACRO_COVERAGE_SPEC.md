# ASH-TCU-K4C — Native 2x2 Square Grid Dispatch Readback / Four-Macro Coverage Correctness Seal

## Status

`SPEC_COMMITTED_ASH_TCU_K4C_NATIVE_2X2_SQUARE_GRID_DISPATCH_READBACK_FOUR_MACRO_COVERAGE_SEAL`

## Scope

ASH-TCU-K4C is the first TensorCube patch allowed to execute a native 2x2 square grid dispatch. It consumes the K4B orientation matrix, uploads four macro descriptors, executes `dispatch_workgroups=[2,2,1]`, writes a fresh 4096-byte `ReadbackBufferBytes` artifact, and compares 1024 f32 values against a CPU oracle.

K4C does not open production multi-macro inference. K4C does not make performance claims. K4C does not reuse K3D or K4A readback bytes as primary evidence.

## Patch ID

```text
ASH-TCU-K4C
Native 2x2 Square Grid Dispatch Readback
Four-Macro Coverage Correctness Seal
ReadbackBufferBytes Primary Evidence
No Prior 2x1 Or 1x2 Readback Reuse
No Production Multi-Macro Dispatch
No Runtime Splice
No Performance Claim
```

## Prior gates

K4C requires:

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
```

K4B must prove both orientation receipts:

```text
horizontal_2x1.pass = true
vertical_1x2.pass = true
dispatch_axes_are_distinct = true
byte_len_parity = true
element_count_parity = true
no_new_gpu_dispatch = true
no_new_readback_bytes = true
```

## Artifact ownership rule

```text
Code bake target: uploaded ASH ZIP tree
Spec ownership: GitHub repository docs
Runtime receipt ownership: local Rust execution output
Runtime artifact ownership: local Rust execution output
```

K4C code bake must not include runtime evidence. These files must be produced locally:

```text
workspace/runtime/tensorcube/ash_tensorcube_k4c_2x2_cpu_oracle_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k4c_native_2x2_dispatch_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k4c_readback_bytes_latest.bin
workspace/runtime/tensorcube/ash_tensorcube_k4c_readback_digest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k4c_oracle_comparison_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k4c_four_macro_coverage_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k4c_gate_latest.json
```

## Primary evidence rule

K4C primary GPU evidence must be new K4C readback bytes:

```text
source = ReadbackBufferBytes
byte_len = 4096
scalar_count = 1024
format = raw f32 little-endian
```

Forbidden as K4C primary evidence:

```text
K2-R1 single-macro readback bytes
K3D 2x1 readback bytes
K4A 1x2 readback bytes
K3D/K4A readback concatenated into 4096 bytes
CPU oracle bytes
MaterializedTensorBytes fallback
JSON debug arrays
base64 wrappers
empty bytes
padding bytes as logical output
```

## K4C adoption grid

```text
descriptor_count = 4
macro_grid_width = 2
macro_grid_height = 2
dispatch_workgroups = [2, 2, 1]
```

Logical output:

```text
m = 32
n = 32
k = 32
k_panel_count = 4
macro_output_scalar_count = 256
macro_output_byte_len = 1024
total_output_scalar_count = 1024
total_output_byte_len = 4096
```

## Fixture contract

```text
fixture_id = deterministic_pseudo_random_kpanel_4_2x2
base_fixture_id = deterministic_pseudo_random_kpanel_4
A shape = 32 x 32
B shape = 32 x 32
C shape = 4 macro-contiguous tiles x 256 f32
```

Macro meaning:

```text
descriptor[0] computes C[0..16, 0..16]
descriptor[1] computes C[0..16, 16..32]
descriptor[2] computes C[16..32, 0..16]
descriptor[3] computes C[16..32, 16..32]
```

Output ordering:

```text
readback[0..256] = descriptor[0] output
readback[256..512] = descriptor[1] output
readback[512..768] = descriptor[2] output
readback[768..1024] = descriptor[3] output
```

The CPU oracle must serialize the same macro-contiguous ordering before comparison.

## Macro index contract

K4C must keep the K3B/K4A-proven formula:

```text
macro_index = workgroup_id.y * macro_grid_width + workgroup_id.x
```

For 2x2:

```text
workgroup_id [0,0,0] -> macro_index 0
workgroup_id [1,0,0] -> macro_index 1
workgroup_id [0,1,0] -> macro_index 2
workgroup_id [1,1,0] -> macro_index 3
```

## Descriptor contract

```text
descriptor_count = 4
descriptors.len() = 4
```

Required descriptor summary:

```text
descriptor[0]: macro_id=0, row_offset=0,  col_offset=0,  c_base_element=0
descriptor[1]: macro_id=1, row_offset=0,  col_offset=16, c_base_element=256
descriptor[2]: macro_id=2, row_offset=16, col_offset=0,  c_base_element=512
descriptor[3]: macro_id=3, row_offset=16, col_offset=16, c_base_element=768
```

For macro-contiguous output, each descriptor writes 256 f32 values with:

```text
output_scalar_count = 256
output_byte_len = 1024
valid_m = 16
valid_n = 16
valid_k = 32
c_row_stride = 16
c_col_stride = 1
dispatch_workgroups = [2,2,1]
```

K4C uses `a_base_element` for the macro row base and must not double-apply row offset in the shader's A-indexing path.

## Native dispatch contract

K4C must prove:

```text
adapter_requested = true
device_requested = true
descriptor_buffer_created = true
descriptor_control_buffer_created = true
input_a_buffer_created = true
input_b_buffer_created = true
output_buffer_created = true
readback_buffer_created = true
compute_pipeline_created = true
bind_group_created = true
dispatch_encoded = true
copy_to_readback_encoded = true
queue_submitted = true
map_async_requested = true
map_async_completed = true
device_poll_completed = true
mapped_range_acquired = true
readback_buffer_unmapped_after_digest = true
```

Required dispatch:

```text
dispatch_workgroups = [2,2,1]
```

## Buffer contract

```text
Input A:
  shape = 32 x 32
  element_count = 1024
  byte_len = 4096
  usage = STORAGE | COPY_DST

Input B:
  shape = 32 x 32
  element_count = 1024
  byte_len = 4096
  usage = STORAGE | COPY_DST

Output C:
  element_count = 1024
  byte_len = 4096
  usage = STORAGE | COPY_SRC

Readback:
  byte_len = 4096
  usage = MAP_READ | COPY_DST
```

## Four-macro coverage contract

K4C must prove complete non-overlapping coverage:

```text
macro0 = [0..256]
macro1 = [256..512]
macro2 = [512..768]
macro3 = [768..1024]
coverage_non_overlapping = true
coverage_contiguous = true
coverage_covers_total_output = true
```

## Comparison contract

```text
abs_tol = 0.0001
rel_tol = 0.0001
element_count = 1024
passed_count = 1024
failed_count = 0
per_macro_failed_counts = [0,0,0,0]
nan_count = 0
inf_count = 0
pass = true
```

Digest equality is not required. Correctness is value comparison under tolerance.

## Expected code files in bake

```text
crates/burn_webgpu_backend/src/tensorcube_k4c_2x2_fixture.rs
crates/burn_webgpu_backend/src/tensorcube_k4c_2x2_cpu_oracle.rs
crates/burn_webgpu_backend/src/tensorcube_k4c_native_2x2_dispatch.rs
crates/burn_webgpu_backend/src/tensorcube_k4c_readback_bytes.rs
crates/burn_webgpu_backend/src/tensorcube_k4c_oracle_comparison.rs
crates/burn_webgpu_backend/src/tensorcube_k4c_four_macro_coverage.rs
crates/burn_webgpu_backend/src/tensorcube_k4c_gate.rs

crates/burn_webgpu_backend/tests/ash_tcu_k4c_2x2_fixture_schema.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4c_cpu_oracle_1024.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4c_descriptor_2x2_contract.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4c_macro_index_linearization.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4c_four_macro_coverage.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4c_dispatch_grid_required.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4c_readback_byte_len_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4c_oracle_comparison_tolerance.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4c_no_prior_orientation_readback_reuse.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4c_no_materialized_fallback.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4c_no_production_multi_macro_dispatch.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4c_no_runtime_splice_open.rs
crates/burn_webgpu_backend/tests/ash_tcu_k4c_no_performance_claim.rs

crates/orchestrator_local/src/ash_tcu_k4c_native_2x2_dispatch_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k4c_native_2x2_dispatch_audit.rs
```

## Local Rust command

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k4c_native_2x2_dispatch_audit `
  -- --repo-root .
```

Strict mode:

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k4c_native_2x2_dispatch_audit `
  -- --repo-root . --require-k4b-pass --require-native-gpu
```

Low-memory build:

```powershell
$env:CARGO_BUILD_JOBS="1"
$env:CARGO_INCREMENTAL="0"
$env:CARGO_PROFILE_DEV_DEBUG="0"
$env:CARGO_PROFILE_TEST_DEBUG="0"
$env:RUSTFLAGS="-C debuginfo=0"

cargo run -j 1 -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k4c_native_2x2_dispatch_audit `
  -- --repo-root . --require-k4b-pass --require-native-gpu
```

Summary check:

```powershell
Get-Content ".\workspace\runtime\tensorcube\ash_tensorcube_k4c_gate_latest.json" -Raw |
  ConvertFrom-Json |
  Select-Object `
    status,
    @{Name="k4b";Expression={$_.prior_gate.k4b_passed}},
    @{Name="dispatch";Expression={$_.native_dispatch.grid_plan.dispatch_workgroups -join ","}},
    @{Name="gpu";Expression={$_.native_dispatch.gpu_dispatch.queue_submitted}},
    @{Name="map";Expression={$_.native_dispatch.gpu_dispatch.map_async_completed}},
    @{Name="bytes";Expression={$_.readback_digest.readback_total_bytes}},
    @{Name="primary";Expression={$_.readback_digest.primary_gpu_evidence}},
    @{Name="elements";Expression={$_.oracle_comparison.element_count}},
    @{Name="failed";Expression={$_.oracle_comparison.failed_count}},
    @{Name="macro_failed";Expression={$_.oracle_comparison.per_macro_failed_counts -join ","}},
    @{Name="coverage";Expression={$_.four_macro_coverage.pass}},
    @{Name="pass";Expression={$_.oracle_comparison.pass}},
    @{Name="reuse";Expression={$_.scope_guard.prior_orientation_readback_reused}},
    @{Name="prod";Expression={$_.scope_guard.production_multi_macro_dispatch_allowed}} |
  Format-List
```

Expected PASS:

```text
status       : PASS_ASH_TCU_K4C_NATIVE_2X2_SQUARE_GRID_DISPATCH_READBACK_FOUR_MACRO_COVERAGE_SEAL
k4b          : True
dispatch     : 2,2,1
gpu          : True
map          : True
bytes        : 4096
primary      : True
elements     : 1024
failed       : 0
macro_failed : 0,0,0,0
coverage     : True
pass         : True
reuse        : False
prod         : False
```

Readback file size check:

```powershell
(Get-Item ".\workspace\runtime\tensorcube\ash_tensorcube_k4c_readback_bytes_latest.bin").Length
```

Expected:

```text
4096
```

## Acceptance criteria

```text
1. K4B PASS present.
2. K4B orientation matrix has horizontal_2x1 PASS.
3. K4B orientation matrix has vertical_1x2 PASS.
4. descriptor_count = 4.
5. macro_grid_width = 2.
6. macro_grid_height = 2.
7. dispatch_workgroups = [2,2,1].
8. CPU oracle outputs 1024 f32.
9. CPU oracle byte length = 4096.
10. GPU output buffer byte length = 4096.
11. Readback buffer byte length = 4096.
12. Four macro coverage ranges are non-overlapping.
13. Four macro coverage ranges are contiguous.
14. Four macro coverage covers total output.
15. map_async is completed.
16. K4C readback .bin byte length = 4096.
17. primary_gpu_evidence = true.
18. prior_orientation_readback_reused = false.
19. materialized_tensor_fallback_used = false.
20. comparison element_count = 1024.
21. comparison failed_count = 0.
22. per_macro_failed_counts = [0,0,0,0].
23. nan_count = 0.
24. inf_count = 0.
25. production multi-macro dispatch remains closed.
26. runtime splice remains closed.
27. no performance claim is made.
```

## PASS marker

```text
PASS_ASH_TCU_K4C_NATIVE_2X2_SQUARE_GRID_DISPATCH_READBACK_FOUR_MACRO_COVERAGE_SEAL
```

## Failure markers

```text
FAIL_ASH_TCU_K4C_MISSING_K4B_PASS
FAIL_ASH_TCU_K4C_MISSING_ORIENTATION_MATRIX
FAIL_ASH_TCU_K4C_HORIZONTAL_2X1_NOT_PASS
FAIL_ASH_TCU_K4C_VERTICAL_1X2_NOT_PASS
FAIL_ASH_TCU_K4C_DESCRIPTOR_COUNT_NOT_FOUR
FAIL_ASH_TCU_K4C_GRID_SHAPE_NOT_2X2
FAIL_ASH_TCU_K4C_DISPATCH_GRID_NOT_2X2
FAIL_ASH_TCU_K4C_CPU_ORACLE_ELEMENT_COUNT_MISMATCH
FAIL_ASH_TCU_K4C_CPU_ORACLE_BYTE_LEN_MISMATCH
FAIL_ASH_TCU_K4C_MACRO_INDEX_LINEARIZATION_MISMATCH
FAIL_ASH_TCU_K4C_C_OUTPUT_RANGE_OVERLAP
FAIL_ASH_TCU_K4C_C_OUTPUT_COVERAGE_MISMATCH
FAIL_ASH_TCU_K4C_READBACK_BYTE_LEN_MISMATCH
FAIL_ASH_TCU_K4C_PRIOR_ORIENTATION_READBACK_REUSED
FAIL_ASH_TCU_K4C_MATERIALIZED_FALLBACK_USED
FAIL_ASH_TCU_K4C_ORACLE_TOLERANCE_MISMATCH
FAIL_ASH_TCU_K4C_PER_MACRO_FAILURE_FOUND
FAIL_ASH_TCU_K4C_NAN_FOUND
FAIL_ASH_TCU_K4C_INF_FOUND
FAIL_ASH_TCU_K4C_PRODUCTION_MULTI_MACRO_DISPATCH_OPEN
FAIL_ASH_TCU_K4C_RUNTIME_SPLICE_OPEN
FAIL_ASH_TCU_K4C_PERFORMANCE_CLAIM_FOUND
```

## Next allowed patch

```text
ASH-TCU-K5A — Shape Sweep Rectangle 3x2 Plan / Non-Square Macro Grid Policy Seal
```

If K4C fails due mismatch, open:

```text
ASH-TCU-K4C-R1 — 2x2 Failure Diagnostics / Per-Macro Diff Attribution Seal
```
