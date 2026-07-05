# ASH-TCU-K5B — Native 3x2 Rectangle Grid Dispatch Readback / Six-Macro Coverage Correctness Seal

## Status

`SPEC_COMMITTED_ASH_TCU_K5B_NATIVE_3X2_RECTANGLE_GRID_DISPATCH_READBACK_SIX_MACRO_COVERAGE_SEAL`

## Scope

ASH-TCU-K5B is the first TensorCube patch allowed to execute a native non-square 3x2 rectangle grid dispatch. It consumes the K5A rectangle 3x2 plan, uploads six macro descriptors, executes `dispatch_workgroups=[3,2,1]`, writes a fresh 6144-byte `ReadbackBufferBytes` artifact, and compares 1536 f32 values against a CPU oracle.

K5B does not open production multi-macro inference. K5B does not make performance claims. K5B does not reuse K4C/K3D/K4A readback bytes as primary evidence. K5B does not treat the K5A plan receipt as runtime evidence.

## Patch ID

```text
ASH-TCU-K5B
Native 3x2 Rectangle Grid Dispatch Readback
Six-Macro Coverage Correctness Seal
ReadbackBufferBytes Primary Evidence
No Prior 2x2 Readback Reuse
No Plan Receipt As Runtime Evidence
No Production Multi-Macro Dispatch
No Runtime Splice
No Performance Claim
```

## Prior gates

K5B requires:

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
```

K5A must prove:

```text
status = PASS_ASH_TCU_K5A_RECTANGLE_3X2_PLAN_NON_SQUARE_GRID_POLICY_SEAL
descriptor_count = 6
macro_grid_width = 3
macro_grid_height = 2
planned_dispatch_workgroups = [3,2,1]
total_output_scalar_count = 1536
total_output_byte_len = 6144
six_macro_coverage_plan.pass = true
non_square_grid_allowed = true
ragged_grid_allowed = false
tail_m_allowed = false
tail_n_allowed = false
tail_k_allowed = false
partial_macro_allowed = false
native_3x2_dispatch_executed = false
new_readback_bytes_written = false
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

K5B code bake must not include runtime evidence. These files must be produced locally:

```text
workspace/runtime/tensorcube/ash_tensorcube_k5b_3x2_cpu_oracle_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5b_native_3x2_dispatch_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5b_readback_bytes_latest.bin
workspace/runtime/tensorcube/ash_tensorcube_k5b_readback_digest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5b_oracle_comparison_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5b_six_macro_coverage_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5b_gate_latest.json
```

## Primary evidence rule

K5B primary GPU evidence must be new K5B readback bytes:

```text
source = ReadbackBufferBytes
byte_len = 6144
scalar_count = 1536
format = raw f32 little-endian
```

Forbidden as K5B primary evidence:

```text
K2-R1 single-macro readback bytes
K3D 2x1 readback bytes
K4A 1x2 readback bytes
K4C 2x2 readback bytes
K5A plan receipt
K5A coverage plan receipt
CPU oracle bytes
MaterializedTensorBytes fallback
JSON debug arrays
base64 wrappers
empty bytes
padding bytes as logical output
```

## K5B adoption grid

```text
descriptor_count = 6
macro_grid_width = 3
macro_grid_height = 2
dispatch_workgroups = [3,2,1]
```

Logical output:

```text
m = 32
n = 48
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

## Fixture contract

```text
fixture_id = deterministic_pseudo_random_kpanel_4_3x2
base_fixture_id = deterministic_pseudo_random_kpanel_4
A shape = 32 x 32
B shape = 32 x 48
C shape = 6 macro-contiguous tiles x 256 f32
```

Output ordering:

```text
readback[0..256] = descriptor[0] output
readback[256..512] = descriptor[1] output
readback[512..768] = descriptor[2] output
readback[768..1024] = descriptor[3] output
readback[1024..1280] = descriptor[4] output
readback[1280..1536] = descriptor[5] output
```

The CPU oracle must serialize the same macro-contiguous ordering before comparison.

## Macro index contract

K5B must keep the existing formula:

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

## Descriptor contract

```text
descriptor_count = 6
descriptors.len() = 6
```

Required descriptor summary:

```text
descriptor[0]: macro_id=0, row_offset=0,  col_offset=0,  a_base_element=0,   b_base_element=0,  c_base_element=0
descriptor[1]: macro_id=1, row_offset=0,  col_offset=16, a_base_element=0,   b_base_element=16, c_base_element=256
descriptor[2]: macro_id=2, row_offset=0,  col_offset=32, a_base_element=0,   b_base_element=32, c_base_element=512
descriptor[3]: macro_id=3, row_offset=16, col_offset=0,  a_base_element=512, b_base_element=0,  c_base_element=768
descriptor[4]: macro_id=4, row_offset=16, col_offset=16, a_base_element=512, b_base_element=16, c_base_element=1024
descriptor[5]: macro_id=5, row_offset=16, col_offset=32, a_base_element=512, b_base_element=32, c_base_element=1280
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
dispatch_workgroups = [3,2,1]
```

K5B keeps the K4C/K5A base indexing rule:

```text
A index = desc.a_base_element + local_y * desc.a_row_stride + kk * desc.a_k_stride
B index = desc.b_base_element + kk * desc.b_k_stride + local_x * desc.b_col_stride
C index = desc.c_base_element + local_y * desc.c_row_stride + local_x * desc.c_col_stride
```

`row_offset` is metadata for coverage and logical placement. `a_base_element` already carries the row macro base, so row offset must not be double-applied in A indexing.

## Native dispatch contract

K5B must prove:

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
dispatch_workgroups = [3,2,1]
```

## Buffer contract

```text
Input A:
  shape = 32 x 32
  element_count = 1024
  byte_len = 4096
  usage = STORAGE | COPY_DST

Input B:
  shape = 32 x 48
  element_count = 1536
  byte_len = 6144
  usage = STORAGE | COPY_DST

Output C:
  element_count = 1536
  byte_len = 6144
  usage = STORAGE | COPY_SRC

Readback:
  byte_len = 6144
  usage = MAP_READ | COPY_DST
```

## Six-macro coverage contract

K5B must prove complete non-overlapping coverage:

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

## Comparison contract

```text
abs_tol = 0.0001
rel_tol = 0.0001
element_count = 1536
passed_count = 1536
failed_count = 0
per_macro_failed_counts = [0,0,0,0,0,0]
nan_count = 0
inf_count = 0
pass = true
```

Digest equality is not required. Correctness is value comparison under tolerance.

## Expected code files in bake

```text
crates/burn_webgpu_backend/src/tensorcube_k5b_3x2_fixture.rs
crates/burn_webgpu_backend/src/tensorcube_k5b_3x2_cpu_oracle.rs
crates/burn_webgpu_backend/src/tensorcube_k5b_native_3x2_dispatch.rs
crates/burn_webgpu_backend/src/tensorcube_k5b_readback_bytes.rs
crates/burn_webgpu_backend/src/tensorcube_k5b_oracle_comparison.rs
crates/burn_webgpu_backend/src/tensorcube_k5b_six_macro_coverage.rs
crates/burn_webgpu_backend/src/tensorcube_k5b_gate.rs

crates/burn_webgpu_backend/tests/ash_tcu_k5b_3x2_fixture_schema.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5b_cpu_oracle_1536.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5b_descriptor_3x2_contract.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5b_macro_index_linearization.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5b_six_macro_coverage.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5b_dispatch_grid_required.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5b_readback_byte_len_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5b_oracle_comparison_tolerance.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5b_no_prior_readback_reuse.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5b_no_materialized_fallback.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5b_no_ragged_grid.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5b_no_tail_policy.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5b_no_production_multi_macro_dispatch.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5b_no_runtime_splice_open.rs
crates/burn_webgpu_backend/tests/ash_tcu_k5b_no_performance_claim.rs

crates/orchestrator_local/src/ash_tcu_k5b_native_3x2_dispatch_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k5b_native_3x2_dispatch_audit.rs
```

## Runtime output paths

```text
workspace/runtime/tensorcube/ash_tensorcube_k5b_3x2_cpu_oracle_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5b_native_3x2_dispatch_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5b_readback_bytes_latest.bin
workspace/runtime/tensorcube/ash_tensorcube_k5b_readback_digest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5b_oracle_comparison_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5b_six_macro_coverage_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k5b_gate_latest.json
```

These files must not be committed to GitHub and must not be baked into ZIP.

## Local Rust command

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k5b_native_3x2_dispatch_audit `
  -- --repo-root .
```

Strict mode:

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k5b_native_3x2_dispatch_audit `
  -- --repo-root . --require-k5a-pass --require-native-gpu
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
  --bin ash_tcu_k5b_native_3x2_dispatch_audit `
  -- --repo-root . --require-k5a-pass --require-native-gpu
```

Summary check:

```powershell
Get-Content ".\workspace\runtime\tensorcube\ash_tensorcube_k5b_gate_latest.json" -Raw |
  ConvertFrom-Json |
  Select-Object `
    status,
    @{Name="k5a";Expression={$_.prior_gate.k5a_passed}},
    @{Name="dispatch";Expression={$_.native_dispatch.grid_plan.dispatch_workgroups -join ","}},
    @{Name="gpu";Expression={$_.native_dispatch.gpu_dispatch.queue_submitted}},
    @{Name="map";Expression={$_.native_dispatch.gpu_dispatch.map_async_completed}},
    @{Name="bytes";Expression={$_.readback_digest.readback_total_bytes}},
    @{Name="primary";Expression={$_.readback_digest.primary_gpu_evidence}},
    @{Name="elements";Expression={$_.oracle_comparison.element_count}},
    @{Name="failed";Expression={$_.oracle_comparison.failed_count}},
    @{Name="macro_failed";Expression={$_.oracle_comparison.per_macro_failed_counts -join ","}},
    @{Name="coverage";Expression={$_.six_macro_coverage.pass}},
    @{Name="pass";Expression={$_.oracle_comparison.pass}},
    @{Name="reuse";Expression={$_.scope_guard.prior_readback_reused}},
    @{Name="planEvidence";Expression={$_.scope_guard.plan_receipt_used_as_runtime_evidence}},
    @{Name="ragged";Expression={$_.scope_guard.ragged_grid_used}},
    @{Name="tail";Expression={$_.scope_guard.tail_policy_used}},
    @{Name="prod";Expression={$_.scope_guard.production_multi_macro_dispatch_allowed}} |
  Format-List
```

Expected PASS:

```text
status       : PASS_ASH_TCU_K5B_NATIVE_3X2_RECTANGLE_GRID_DISPATCH_READBACK_SIX_MACRO_COVERAGE_SEAL
k5a          : True
dispatch     : 3,2,1
gpu          : True
map          : True
bytes        : 6144
primary      : True
elements     : 1536
failed       : 0
macro_failed : 0,0,0,0,0,0
coverage     : True
pass         : True
reuse        : False
planEvidence : False
ragged       : False
tail         : False
prod         : False
```

Readback file size check:

```powershell
(Get-Item ".\workspace\runtime\tensorcube\ash_tensorcube_k5b_readback_bytes_latest.bin").Length
```

Expected:

```text
6144
```

## Acceptance criteria

```text
1. K5A PASS present.
2. K5A rectangle_3x2_plan.pass = true.
3. K5A six_macro_coverage_plan.pass = true.
4. K5A non_square_grid_policy.pass = true.
5. descriptor_count = 6.
6. macro_grid_width = 3.
7. macro_grid_height = 2.
8. dispatch_workgroups = [3,2,1].
9. CPU oracle outputs 1536 f32.
10. CPU oracle byte length = 6144.
11. GPU output buffer byte length = 6144.
12. Readback buffer byte length = 6144.
13. Six macro coverage ranges are non-overlapping.
14. Six macro coverage ranges are contiguous.
15. Six macro coverage covers total output.
16. map_async is completed.
17. K5B readback .bin byte length = 6144.
18. primary_gpu_evidence = true.
19. prior_readback_reused = false.
20. plan_receipt_used_as_runtime_evidence = false.
21. materialized_tensor_fallback_used = false.
22. ragged_grid_used = false.
23. tail_policy_used = false.
24. comparison element_count = 1536.
25. comparison failed_count = 0.
26. per_macro_failed_counts = [0,0,0,0,0,0].
27. nan_count = 0.
28. inf_count = 0.
29. production multi-macro dispatch remains closed.
30. runtime splice remains closed.
31. no performance claim is made.
```

## PASS marker

```text
PASS_ASH_TCU_K5B_NATIVE_3X2_RECTANGLE_GRID_DISPATCH_READBACK_SIX_MACRO_COVERAGE_SEAL
```

## Failure markers

```text
FAIL_ASH_TCU_K5B_MISSING_K5A_PASS
FAIL_ASH_TCU_K5B_MISSING_K5A_RECTANGLE_PLAN
FAIL_ASH_TCU_K5B_MISSING_K5A_SIX_MACRO_COVERAGE
FAIL_ASH_TCU_K5B_MISSING_K5A_NON_SQUARE_POLICY
FAIL_ASH_TCU_K5B_DESCRIPTOR_COUNT_NOT_SIX
FAIL_ASH_TCU_K5B_GRID_SHAPE_NOT_3X2
FAIL_ASH_TCU_K5B_DISPATCH_GRID_NOT_3X2
FAIL_ASH_TCU_K5B_CPU_ORACLE_ELEMENT_COUNT_MISMATCH
FAIL_ASH_TCU_K5B_CPU_ORACLE_BYTE_LEN_MISMATCH
FAIL_ASH_TCU_K5B_MACRO_INDEX_LINEARIZATION_MISMATCH
FAIL_ASH_TCU_K5B_C_OUTPUT_RANGE_OVERLAP
FAIL_ASH_TCU_K5B_C_OUTPUT_COVERAGE_MISMATCH
FAIL_ASH_TCU_K5B_READBACK_BYTE_LEN_MISMATCH
FAIL_ASH_TCU_K5B_PRIOR_READBACK_REUSED
FAIL_ASH_TCU_K5B_PLAN_RECEIPT_USED_AS_RUNTIME_EVIDENCE
FAIL_ASH_TCU_K5B_MATERIALIZED_FALLBACK_USED
FAIL_ASH_TCU_K5B_ORACLE_TOLERANCE_MISMATCH
FAIL_ASH_TCU_K5B_PER_MACRO_FAILURE_FOUND
FAIL_ASH_TCU_K5B_NAN_FOUND
FAIL_ASH_TCU_K5B_INF_FOUND
FAIL_ASH_TCU_K5B_RAGGED_GRID_USED
FAIL_ASH_TCU_K5B_TAIL_POLICY_USED
FAIL_ASH_TCU_K5B_PRODUCTION_MULTI_MACRO_DISPATCH_OPEN
FAIL_ASH_TCU_K5B_RUNTIME_SPLICE_OPEN
FAIL_ASH_TCU_K5B_PERFORMANCE_CLAIM_FOUND
```

## Next allowed patch

```text
ASH-TCU-K5C — Shape Sweep Rectangle 2x3 Plan / Transposed Non-Square Orientation Policy Seal
```

If K5B fails due mismatch, open:

```text
ASH-TCU-K5B-R1 — 3x2 Failure Diagnostics / Per-Macro Diff Attribution Seal
```
