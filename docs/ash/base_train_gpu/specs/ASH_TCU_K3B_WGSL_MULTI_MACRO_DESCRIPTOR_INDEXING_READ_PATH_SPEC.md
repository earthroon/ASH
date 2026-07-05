# ASH-TCU-K3B — WGSL Multi-Macro Descriptor Indexing / Descriptor Array Read Path Seal

## Status

`SPEC_COMMITTED_ASH_TCU_K3B_WGSL_MULTI_MACRO_DESCRIPTOR_INDEXING_READ_PATH_SEAL`

## Scope

ASH-TCU-K3B connects the K3A MacroDescArray SSOT to a WGSL descriptor read path. K3A named the singleton macro as `MacroDesc[0]`; K3B makes WGSL able to calculate a macro index, bounds-check it, and load `macro_descs[macro_index]`.

K3B does not open host grid widening. K3B does not open production multi-macro dispatch. Those remain K3C scope.

## Patch ID

```text
ASH-TCU-K3B
WGSL Multi-Macro Descriptor Indexing
Descriptor Array Read Path Seal
Single Dispatch Compatibility
No Host Grid Builder
No Production Multi-Macro Dispatch
No Performance Claim
No Runtime Splice
```

## Prior gates

K3B requires the following chain before adoption:

```text
K0: TensorCube kernel SSOT identity PASS
K1: CI software adapter / static PASS separation PASS
K2: CPU oracle + mapped readback digest harness PASS
K2-R1: native single-macro dispatch readback producer PASS
K3A: Macro Descriptor Array / Single Macro Compatibility PASS
```

K3A must have `descriptor_count=1`, `compatible=true`, and `multi_macro_enabled=false`.

## Artifact ownership rule

```text
Code bake target: uploaded ASH ZIP tree
Spec ownership: GitHub repository docs
Runtime receipt ownership: local Rust execution output
Runtime artifact ownership: local Rust execution output
```

K3B code bake may include Rust modules, tests, a WGSL read-path source, and an audit binary. Runtime receipts and readback bytes are not committed by this spec and must be produced locally.

The following files must not be pre-baked as evidence:

```text
workspace/runtime/tensorcube/ash_tensorcube_k3b_descriptor_buffer_layout_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3b_wgsl_descriptor_read_path_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3b_single_dispatch_compat_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3b_gate_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3b_readback_bytes_latest.bin
```

## SSOT transition

K3A SSOT:

```text
MacroDescArray.descriptors[0]
```

K3B connection:

```text
WGSL descriptor buffer read path
macro_index calculation
macro_index bounds guard
macro_descs[macro_index] load
```

K3B is therefore a read-path and indexing-seal patch, not a grid-widening patch.

## Included changes

```text
- Host MacroDesc K3B layout
- WGSL MacroDesc K3B layout
- Host/WGSL field-order receipt
- Descriptor pack-to-u32 order receipt
- Descriptor buffer binding token guard
- Descriptor control binding token guard
- WGSL macro_index function
- descriptor_count bounds guard
- macro_descs[macro_index] load token guard
- singleton index guard
- single dispatch compatibility receipt
- no host grid builder guard
- no production multi-macro dispatch guard
- no runtime splice guard
- no performance claim guard
```

## Explicit non-scope

```text
- No host grid builder
- No dispatch_workgroups greater than [1, 1, 1]
- No production multi-macro execution
- No active descriptor_count > 1 dispatch
- No M/N tile grid sweep
- No M/N tail mask
- No K tail policy
- No descriptor compaction
- No dynamic macro scheduling
- No f16 path
- No int8/dot4 path
- No benchmark
- No runtime inference splice
- No backend policy mutation
- No SFT pass1 replacement
```

## K3B descriptor layout

K3B uses an explicit 40-u32 descriptor layout. Host and WGSL field order must match.

```text
field_count = 40 u32
byte_len_per_descriptor = 160
alignment = u32 aligned
host_order == wgsl_order
implicit padding = forbidden
explicit reserved fields = required
```

Minimum host/WGSL field order:

```text
descriptor_version
macro_id
fixture_hash_lo
fixture_hash_hi
m
n
k
k_panel_count
row_offset
col_offset
k_offset
a_base_element
b_base_element
c_base_element
a_row_stride
a_k_stride
b_k_stride
b_col_stride
c_row_stride
c_col_stride
a_tile_table_offset
b_tile_table_offset
c_tile_0
c_tile_1
c_tile_2
c_tile_3
output_scalar_count
output_byte_len
valid_m
valid_n
valid_k
control_base
dispatch_x
dispatch_y
dispatch_z
flags
reserved_0
reserved_1
reserved_2
reserved_3
```

## Descriptor control block

K3B adoption run uses singleton dispatch values:

```text
descriptor_count = 1
macro_grid_width = 1
macro_grid_height = 1
active_dispatch_x = 1
active_dispatch_y = 1
active_dispatch_z = 1
flags = 0
```

`descriptor_count > 1` is not allowed to dispatch in K3B.

## WGSL macro index contract

WGSL must contain a macro index function equivalent to:

```wgsl
fn ash_tcu_k3b_macro_index(workgroup_id: vec3<u32>, macro_grid_width: u32) -> u32 {
    return workgroup_id.y * macro_grid_width + workgroup_id.x;
}
```

K3B adoption values:

```text
workgroup_id = [0, 0, 0]
macro_grid_width = 1
macro_index = 0
descriptor_count = 1
macro_index < descriptor_count = true
```

## WGSL descriptor bounds guard

WGSL must guard descriptor load with `descriptor_count` before the indexed read.

```wgsl
let macro_index = ash_tcu_k3b_macro_index(workgroup_id, descriptor_control.macro_grid_width);
if (macro_index >= descriptor_control.descriptor_count) {
    return;
}
let desc = macro_descs[macro_index];
```

The exact fallback form may vary, but the receipt must prove:

```text
descriptor_count guard exists
macro_descs[macro_index] load exists
workgroup_id participates in macro_index
```

## Binding contract

K3B must expose explicit descriptor and control bindings without colliding with the existing K2/K2-R1 singleton path.

Reference binding plan:

```text
@group(0) @binding(0) A input storage
@group(0) @binding(1) B input storage
@group(0) @binding(2) C output storage
@group(0) @binding(3) legacy tile/control buffer
@group(0) @binding(4) K3B descriptor storage buffer
@group(0) @binding(5) K3B descriptor control buffer
```

## Expected code files in bake

```text
crates/burn_webgpu_backend/src/tensorcube_k3b_descriptor_layout.rs
crates/burn_webgpu_backend/src/tensorcube_k3b_descriptor_pack.rs
crates/burn_webgpu_backend/src/tensorcube_k3b_wgsl_descriptor_read.rs
crates/burn_webgpu_backend/src/tensorcube_k3b_index_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k3b_single_dispatch_compat.rs
crates/burn_webgpu_backend/src/tensorcube_k3b_gate.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3b_descriptor_layout_schema.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3b_descriptor_pack_order.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3b_wgsl_descriptor_read_tokens.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3b_macro_index_bounds_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3b_single_dispatch_compat.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3b_no_host_grid_builder.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3b_no_production_multi_macro.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3b_no_runtime_splice_open.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3b_no_performance_claim.rs
crates/orchestrator_local/src/ash_tcu_k3b_descriptor_read_path_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k3b_descriptor_read_path_audit.rs
```

## Runtime output paths

```text
workspace/runtime/tensorcube/ash_tensorcube_k3b_descriptor_buffer_layout_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3b_wgsl_descriptor_read_path_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3b_single_dispatch_compat_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3b_gate_latest.json
```

Optional future readback bytes path:

```text
workspace/runtime/tensorcube/ash_tensorcube_k3b_readback_bytes_latest.bin
```

K3B adoption may use K2-R1 ReadbackBufferBytes as prior evidence for singleton correctness while proving the new descriptor read path statically and structurally. K3C is responsible for host grid widening.

## Local Rust command

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k3b_descriptor_read_path_audit `
  -- --repo-root .
```

Strict mode:

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k3b_descriptor_read_path_audit `
  -- --repo-root . --require-k3a-pass --require-single-dispatch-readback
```

## Acceptance criteria

```text
1. K0 identity receipt present.
2. K1 execution-state receipt present.
3. K2 correctness PASS present.
4. K2-R1 readback evidence present.
5. K3A PASS present.
6. Host MacroDesc and WGSL MacroDesc field order match.
7. Descriptor byte length is 160.
8. Descriptor buffer binding exists.
9. Descriptor control binding exists.
10. WGSL macro_index function exists.
11. WGSL descriptor_count bounds guard exists.
12. WGSL loads macro_descs[macro_index].
13. workgroup_id participates in macro_index.
14. Adoption dispatch remains [1, 1, 1].
15. Active descriptor_count dispatched remains 1.
16. Singleton descriptor read path remains compatible with K2/K2-R1 correctness evidence.
17. No host grid builder is opened.
18. No production multi-macro dispatch is opened.
19. No runtime splice is opened.
20. No performance claim is made.
```

## PASS marker

```text
PASS_ASH_TCU_K3B_WGSL_MULTI_MACRO_DESCRIPTOR_INDEXING_READ_PATH_SEAL
```

## Failure markers

```text
FAIL_ASH_TCU_K3B_MISSING_K0_RECEIPT
FAIL_ASH_TCU_K3B_MISSING_K1_RECEIPT
FAIL_ASH_TCU_K3B_MISSING_K2_PASS
FAIL_ASH_TCU_K3B_MISSING_K2_R1_READBACK
FAIL_ASH_TCU_K3B_MISSING_K3A_PASS
FAIL_ASH_TCU_K3B_HOST_WGSL_DESCRIPTOR_LAYOUT_MISMATCH
FAIL_ASH_TCU_K3B_DESCRIPTOR_BYTE_LEN_MISMATCH
FAIL_ASH_TCU_K3B_MISSING_DESCRIPTOR_BUFFER_BINDING
FAIL_ASH_TCU_K3B_MISSING_DESCRIPTOR_CONTROL_BINDING
FAIL_ASH_TCU_K3B_MISSING_MACRO_INDEX_FUNCTION
FAIL_ASH_TCU_K3B_MISSING_DESCRIPTOR_COUNT_GUARD
FAIL_ASH_TCU_K3B_MISSING_MACRO_DESC_INDEXED_LOAD
FAIL_ASH_TCU_K3B_WORKGROUP_ID_NOT_USED_FOR_MACRO_INDEX
FAIL_ASH_TCU_K3B_ACTIVE_DESCRIPTOR_COUNT_GT_ONE_DISPATCHED
FAIL_ASH_TCU_K3B_DISPATCH_WIDENING_FOUND
FAIL_ASH_TCU_K3B_READBACK_BYTE_LEN_MISMATCH
FAIL_ASH_TCU_K3B_ORACLE_TOLERANCE_MISMATCH
FAIL_ASH_TCU_K3B_NAN_FOUND
FAIL_ASH_TCU_K3B_INF_FOUND
FAIL_ASH_TCU_K3B_HOST_GRID_BUILDER_OPEN
FAIL_ASH_TCU_K3B_PRODUCTION_MULTI_MACRO_DISPATCH_OPEN
FAIL_ASH_TCU_K3B_RUNTIME_SPLICE_OPEN
FAIL_ASH_TCU_K3B_PERFORMANCE_CLAIM_FOUND
```

## Next allowed patch

```text
ASH-TCU-K3C — Host Macro Grid Builder / Descriptor Count To Dispatch Grid Seal
```

K3C is the first patch allowed to derive dispatch grid from descriptor count and macro grid shape.
