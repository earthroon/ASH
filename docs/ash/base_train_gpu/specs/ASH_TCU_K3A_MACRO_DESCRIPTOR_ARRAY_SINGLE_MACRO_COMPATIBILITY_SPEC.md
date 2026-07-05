# ASH-TCU-K3A — Macro Descriptor Array / Single Macro Compatibility Seal

## Status

`SPEC_COMMITTED_ASH_TCU_K3A_MACRO_DESCRIPTOR_ARRAY_SINGLE_MACRO_COMPATIBILITY_SEAL`

## Scope

ASH-TCU-K3A introduces an explicit Macro Descriptor Array SSOT for TensorCube while preserving the already-proven single-macro behavior from ASH-TCU-K2 and ASH-TCU-K2-R1.

K3A does not open multi-macro dispatch. It does not widen WGSL indexing. It does not change kernel behavior. It only names and validates the single macro as `MacroDesc[0]`.

## Patch ID

```text
ASH-TCU-K3A
Macro Descriptor Array
Single Macro Compatibility Seal
No Multi-Macro Dispatch
No WGSL Multi-Index Widening
No Kernel Behavior Change
No Performance Claim
No Runtime Splice
```

## Prior gates

K3A requires the following chain before adoption:

```text
K0: TensorCube kernel SSOT identity PASS
K1: CI software adapter / static PASS separation PASS
K2: CPU oracle + mapped readback digest harness PASS
K2-R1: native single-macro dispatch readback producer PASS
```

K2 must have `ReadbackBufferBytes` as primary GPU evidence and `comparison.pass=true` before K3A can be treated as adoption-ready.

## Artifact ownership rule

```text
Code bake target: uploaded ASH ZIP tree
Spec ownership: GitHub repository docs
Runtime receipt ownership: local Rust execution output
Runtime artifact ownership: local Rust execution output
```

K3A code bake may include Rust modules, tests, and an audit binary. Runtime receipts are not committed by this spec and must be produced locally.

The following files must not be pre-baked as evidence:

```text
workspace/runtime/tensorcube/ash_tensorcube_k3a_macro_descriptor_array_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3a_single_macro_compat_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3a_descriptor_schema_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3a_gate_latest.json
```

## SSOT transition

Before K3A:

```text
single macro shape/config is implicit in code constants and call paths
```

After K3A:

```text
single macro shape/config is explicitly owned by MacroDesc[0]
MacroDesc array is the TensorCube macro execution unit SSOT
```

K3A descriptor array is still singleton-only:

```text
descriptor_count = 1
descriptors.len() = 1
descriptors[0].macro_id = 0
```

## Included changes

```text
- MacroDesc v1 struct
- MacroDescArray v1 struct
- K2 fixture based single MacroDesc builder
- K2/K2-R1 single macro compatibility checker
- descriptor schema receipt
- descriptor array receipt
- singleton descriptor count guard
- dispatch_workgroups guard
- control_base guard
- runtime splice closed guard
- performance claim forbidden guard
```

## Explicit non-scope

```text
- No multi-macro dispatch
- No descriptor_count > 1
- No WGSL macro index loop
- No WGSL descriptor array indexing
- No dispatch_workgroups greater than (1, 1, 1)
- No host grid builder
- No M/N tail mask
- No K tail policy
- No f16 path
- No int8/dot4 path
- No benchmark
- No runtime inference splice
- No production dispatch
- No SFT pass1 replacement
- No backend policy mutation
```

## MacroDesc v1 minimum fields

```rust
pub struct AshTcuK3aMacroDesc {
    pub descriptor_version: u32,
    pub macro_id: u32,
    pub fixture_id: String,
    pub m: u32,
    pub n: u32,
    pub k: u32,
    pub k_panel_count: u32,
    pub row_offset: u32,
    pub col_offset: u32,
    pub k_offset: u32,
    pub a_base_element: u32,
    pub b_base_element: u32,
    pub c_base_element: u32,
    pub a_row_stride: u32,
    pub a_k_stride: u32,
    pub b_k_stride: u32,
    pub b_col_stride: u32,
    pub c_row_stride: u32,
    pub c_col_stride: u32,
    pub a_tile_table_offset: u32,
    pub b_tile_table_offset: u32,
    pub c_tiles: [u32; 4],
    pub output_scalar_count: u32,
    pub output_byte_len: u32,
    pub valid_m: u32,
    pub valid_n: u32,
    pub valid_k: u32,
    pub control_base: u32,
    pub dispatch_workgroups: [u32; 3],
    pub flags: u32,
}
```

Expected singleton values:

```text
descriptor_version = 1
macro_id = 0
fixture_id = deterministic_pseudo_random_kpanel_4
m = 16
n = 16
k = 32
k_panel_count = 4
row_offset = 0
col_offset = 0
k_offset = 0
a_base_element = 0
b_base_element = 0
c_base_element = 0
a_row_stride = 32
a_k_stride = 1
b_k_stride = 16
b_col_stride = 1
c_row_stride = 16
c_col_stride = 1
a_tile_table_offset = 0
b_tile_table_offset = 8
c_tiles = [0, 1, 2, 3]
output_scalar_count = 256
output_byte_len = 1024
valid_m = 16
valid_n = 16
valid_k = 32
control_base = 0
dispatch_workgroups = [1, 1, 1]
flags = 0
```

## Expected code files in bake

```text
crates/burn_webgpu_backend/src/tensorcube_k3a_macro_descriptor.rs
crates/burn_webgpu_backend/src/tensorcube_k3a_descriptor_array.rs
crates/burn_webgpu_backend/src/tensorcube_k3a_single_macro_compat.rs
crates/burn_webgpu_backend/src/tensorcube_k3a_gate.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3a_macro_descriptor_schema.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3a_descriptor_array_singleton.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3a_single_macro_compat.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3a_no_multi_macro_dispatch.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3a_no_wgsl_multi_indexing.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3a_no_runtime_splice_open.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3a_no_performance_claim.rs
crates/orchestrator_local/src/ash_tcu_k3a_macro_descriptor_array_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k3a_macro_descriptor_array_audit.rs
```

## Runtime output paths

```text
workspace/runtime/tensorcube/ash_tensorcube_k3a_macro_descriptor_array_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3a_single_macro_compat_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3a_descriptor_schema_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3a_gate_latest.json
```

## Local Rust command

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k3a_macro_descriptor_array_audit `
  -- --repo-root .
```

Strict mode:

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k3a_macro_descriptor_array_audit `
  -- --repo-root . --require-k2-pass --require-k2-r1-readback
```

## Acceptance criteria

```text
1. K0 identity receipt present.
2. K1 execution-state receipt present.
3. K2 correctness harness PASS present.
4. K2-R1 readback evidence present.
5. MacroDesc struct exists.
6. MacroDescArray struct exists.
7. descriptor_count = 1.
8. descriptors.len() = 1.
9. descriptors[0].macro_id = 0.
10. descriptors[0] matches K2 fixture dimensions.
11. descriptors[0].output_byte_len = 1024.
12. descriptors[0].output_scalar_count = 256.
13. descriptors[0].control_base = 0.
14. dispatch_workgroups remains (1, 1, 1).
15. No descriptor_count > 1.
16. No WGSL multi-indexing.
17. No host grid builder.
18. No runtime splice.
19. No production dispatch.
20. No performance claim.
```

## PASS marker

```text
PASS_ASH_TCU_K3A_MACRO_DESCRIPTOR_ARRAY_SINGLE_MACRO_COMPATIBILITY_SEAL
```

## Failure markers

```text
FAIL_ASH_TCU_K3A_MISSING_K0_RECEIPT
FAIL_ASH_TCU_K3A_MISSING_K1_RECEIPT
FAIL_ASH_TCU_K3A_MISSING_K2_PASS
FAIL_ASH_TCU_K3A_MISSING_K2_R1_READBACK
FAIL_ASH_TCU_K3A_MISSING_MACRO_DESC
FAIL_ASH_TCU_K3A_MISSING_DESCRIPTOR_ARRAY
FAIL_ASH_TCU_K3A_DESCRIPTOR_COUNT_NOT_ONE
FAIL_ASH_TCU_K3A_DESCRIPTOR_MACRO_ID_NOT_ZERO
FAIL_ASH_TCU_K3A_DESCRIPTOR_SHAPE_MISMATCH
FAIL_ASH_TCU_K3A_DESCRIPTOR_STRIDE_MISMATCH
FAIL_ASH_TCU_K3A_DESCRIPTOR_OUTPUT_BYTE_LEN_MISMATCH
FAIL_ASH_TCU_K3A_CONTROL_BASE_NOT_ZERO
FAIL_ASH_TCU_K3A_MULTI_MACRO_ENABLED
FAIL_ASH_TCU_K3A_WGSL_MULTI_INDEXING_FOUND
FAIL_ASH_TCU_K3A_HOST_GRID_BUILDER_OPEN
FAIL_ASH_TCU_K3A_RUNTIME_SPLICE_OPEN
FAIL_ASH_TCU_K3A_PRODUCTION_DISPATCH_OPEN
FAIL_ASH_TCU_K3A_PERFORMANCE_CLAIM_FOUND
```

## Next allowed patch

```text
ASH-TCU-K3B — WGSL Multi-Macro Descriptor Indexing / Descriptor Array Read Path Seal
```

K3B is the first patch allowed to make WGSL read descriptor array entries by macro index. K3A must not open that path.
