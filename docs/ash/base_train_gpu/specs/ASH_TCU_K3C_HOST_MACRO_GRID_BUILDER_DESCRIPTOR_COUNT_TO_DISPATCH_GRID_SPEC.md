# ASH-TCU-K3C — Host Macro Grid Builder / Descriptor Count To Dispatch Grid Seal

## Status

`SPEC_COMMITTED_ASH_TCU_K3C_HOST_MACRO_GRID_BUILDER_DESCRIPTOR_COUNT_TO_DISPATCH_GRID_SEAL`

## Scope

ASH-TCU-K3C opens the host-side macro grid builder. K3B proved that WGSL can read `macro_descs[macro_index]` with a descriptor-count guard. K3C derives an explicit `MacroGridPlan` from `descriptor_count`, `macro_grid_width`, and `macro_grid_height`, and seals the mapping to `dispatch_workgroups`.

K3C does not execute native multi-macro readback correctness. K3C does not open production multi-macro dispatch. That remains K3D scope.

## Patch ID

```text
ASH-TCU-K3C
Host Macro Grid Builder
Descriptor Count To Dispatch Grid Seal
Explicit Grid Shape Required
No Silent Grid Inference
No Production Multi-Macro Dispatch
No Runtime Splice
No Performance Claim
```

## Prior gates

K3C requires the following chain before adoption:

```text
K0: TensorCube kernel SSOT identity PASS
K1: CI software adapter / static PASS separation PASS
K2: CPU oracle + mapped readback digest harness PASS
K2-R1: native single-macro dispatch readback producer PASS
K3A: Macro Descriptor Array / Single Macro Compatibility PASS
K3B: WGSL Multi-Macro Descriptor Indexing / Descriptor Array Read Path PASS
```

K3B must have `layout=true`, `read_path=true`, `compat=true`, `desc_count=1`, and `host_grid=false` before K3C opens host grid planning.

## Artifact ownership rule

```text
Code bake target: uploaded ASH ZIP tree
Spec ownership: GitHub repository docs
Runtime receipt ownership: local Rust execution output
Runtime artifact ownership: local Rust execution output
```

K3C code bake may include Rust modules, tests, and an audit binary. Runtime receipts are not committed by this spec and must be produced locally.

The following files must not be pre-baked as evidence:

```text
workspace/runtime/tensorcube/ash_tensorcube_k3c_macro_grid_builder_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3c_descriptor_count_to_dispatch_grid_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3c_descriptor_coverage_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3c_gate_latest.json
```

K3C does not generate a readback `.bin` as adoption evidence. Native 2x1 readback belongs to K3D.

## SSOT transition

K3A/K3B SSOT:

```text
MacroDescArray = macro execution unit descriptor SSOT
WGSL descriptor read path = descriptor consumption path
```

K3C adds:

```text
MacroGridPlan = host dispatch grid SSOT
```

Dispatch grid values must be derived from `MacroGridPlan`. Manual dispatch literals are forbidden as adoption evidence.

## K3C adoption grid

```text
descriptor_count = 2
macro_grid_width = 2
macro_grid_height = 1
dispatch_workgroups = [2, 1, 1]
```

This 2x1 plan is a host grid builder smoke target, not production multi-macro inference.

## Included changes

```text
- MacroGridShape v1
- MacroGridPlan v1
- explicit grid shape validation
- descriptor_count == macro_grid_width * macro_grid_height validation
- dispatch_workgroups derivation
- dispatch z == 1 guard
- host macro_index linearization
- host/K3B WGSL macro_index formula equivalence guard
- descriptor macro_id == linear index guard
- C output range non-overlap guard
- C output total coverage guard
- tile offset alignment guard
- no silent grid inference guard
- no native multi-macro correctness claim guard
- no production multi-macro dispatch guard
- no runtime splice guard
- no performance claim guard
```

## Explicit non-scope

```text
- No native multi-macro readback correctness
- No K3D 2x1 GPU output .bin
- No production multi-macro dispatch
- No descriptor_count automatic inference
- No ragged grid
- No tail mask
- No M/N tail policy
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

## MacroGridShape v1

```rust
pub struct AshTcuK3cMacroGridShape {
    pub grid_version: u32,
    pub descriptor_count: u32,
    pub macro_grid_width: u32,
    pub macro_grid_height: u32,
    pub macro_tile_m: u32,
    pub macro_tile_n: u32,
    pub k: u32,
    pub k_panel_count: u32,
}
```

Adoption values:

```text
grid_version = 1
descriptor_count = 2
macro_grid_width = 2
macro_grid_height = 1
macro_tile_m = 16
macro_tile_n = 16
k = 32
k_panel_count = 4
```

## MacroGridPlan v1

```rust
pub struct AshTcuK3cMacroGridPlan {
    pub patch_id: &'static str,
    pub grid_version: u32,
    pub descriptor_count: u32,
    pub macro_grid_width: u32,
    pub macro_grid_height: u32,
    pub dispatch_workgroups: [u32; 3],
    pub total_logical_m: u32,
    pub total_logical_n: u32,
    pub total_output_scalar_count: u32,
    pub total_output_byte_len: u32,
    pub explicit_grid_shape_provided: bool,
    pub silent_grid_inference_used: bool,
    pub descriptor_count_matches_grid_product: bool,
    pub dispatch_grid_matches_macro_grid: bool,
}
```

Expected plan:

```text
descriptor_count = 2
macro_grid_width = 2
macro_grid_height = 1
dispatch_workgroups = [2, 1, 1]
total_logical_m = 16
total_logical_n = 32
total_output_scalar_count = 512
total_output_byte_len = 2048
explicit_grid_shape_provided = true
silent_grid_inference_used = false
descriptor_count_matches_grid_product = true
dispatch_grid_matches_macro_grid = true
```

## Grid validation contract

```text
descriptor_count > 0
macro_grid_width > 0
macro_grid_height > 0
descriptor_count == macro_grid_width * macro_grid_height
dispatch_workgroups[0] == macro_grid_width
dispatch_workgroups[1] == macro_grid_height
dispatch_workgroups[2] == 1
ragged_grid_allowed = false
```

## Host linearization contract

K3C host linearization must match K3B WGSL:

```text
macro_index = y * macro_grid_width + x
```

2x1 mapping:

```text
workgroup_id [0, 0, 0] -> macro_index 0
workgroup_id [1, 0, 0] -> macro_index 1
```

## Descriptor coverage contract

Adoption descriptors:

```text
descriptor[0]:
  macro_id = 0
  row_offset = 0
  col_offset = 0
  c_base_element = 0
  output_scalar_count = 256
  output_byte_len = 1024

descriptor[1]:
  macro_id = 1
  row_offset = 0
  col_offset = 16
  c_base_element = 256
  output_scalar_count = 256
  output_byte_len = 1024
```

Coverage requirements:

```text
descriptor_count = 2
descriptors.len() = 2
descriptor macro_id matches linear index
C output ranges do not overlap
C output ranges cover total logical output
row/col offsets align to 16x16 macro tile
```

## Expected code files in bake

```text
crates/burn_webgpu_backend/src/tensorcube_k3c_macro_grid_shape.rs
crates/burn_webgpu_backend/src/tensorcube_k3c_macro_grid_builder.rs
crates/burn_webgpu_backend/src/tensorcube_k3c_descriptor_grid_plan.rs
crates/burn_webgpu_backend/src/tensorcube_k3c_dispatch_grid_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k3c_descriptor_coverage_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k3c_gate.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3c_macro_grid_shape_schema.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3c_descriptor_count_to_dispatch_grid.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3c_explicit_grid_shape_required.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3c_no_silent_grid_inference.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3c_macro_index_linearization.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3c_descriptor_coverage_non_overlap.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3c_no_production_multi_macro_dispatch.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3c_no_runtime_splice_open.rs
crates/burn_webgpu_backend/tests/ash_tcu_k3c_no_performance_claim.rs
crates/orchestrator_local/src/ash_tcu_k3c_macro_grid_builder_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k3c_macro_grid_builder_audit.rs
```

## Runtime output paths

```text
workspace/runtime/tensorcube/ash_tensorcube_k3c_macro_grid_builder_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3c_descriptor_count_to_dispatch_grid_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3c_descriptor_coverage_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k3c_gate_latest.json
```

## Local Rust command

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k3c_macro_grid_builder_audit `
  -- --repo-root .
```

Strict mode:

```powershell
cargo run -p orchestrator_local `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k3c_macro_grid_builder_audit `
  -- --repo-root . --require-k3b-pass --descriptor-count 2 --grid-width 2 --grid-height 1
```

## Acceptance criteria

```text
1. K0 identity receipt present.
2. K1 execution-state receipt present.
3. K2 correctness PASS present.
4. K2-R1 readback evidence present.
5. K3A PASS present.
6. K3B PASS present.
7. MacroGridShape struct exists.
8. MacroGridPlan struct exists.
9. explicit grid shape is provided.
10. silent grid inference is not used.
11. descriptor_count = 2 in adoption smoke.
12. macro_grid_width = 2.
13. macro_grid_height = 1.
14. descriptor_count == macro_grid_width * macro_grid_height.
15. dispatch_workgroups = [2, 1, 1].
16. dispatch z = 1.
17. host linearization matches K3B WGSL macro_index formula.
18. descriptor macro_id matches linear index.
19. C output ranges are non-overlapping.
20. C output ranges cover total logical output.
21. tile offsets are aligned to 16x16 macro tile.
22. native multi-macro dispatch is not executed as K3C correctness evidence.
23. production multi-macro dispatch is closed.
24. runtime splice is closed.
25. no performance claim is made.
```

## PASS marker

```text
PASS_ASH_TCU_K3C_HOST_MACRO_GRID_BUILDER_DESCRIPTOR_COUNT_TO_DISPATCH_GRID_SEAL
```

## Failure markers

```text
FAIL_ASH_TCU_K3C_MISSING_K0_RECEIPT
FAIL_ASH_TCU_K3C_MISSING_K1_RECEIPT
FAIL_ASH_TCU_K3C_MISSING_K2_PASS
FAIL_ASH_TCU_K3C_MISSING_K2_R1_READBACK
FAIL_ASH_TCU_K3C_MISSING_K3A_PASS
FAIL_ASH_TCU_K3C_MISSING_K3B_PASS
FAIL_ASH_TCU_K3C_MISSING_MACRO_GRID_SHAPE
FAIL_ASH_TCU_K3C_MISSING_MACRO_GRID_PLAN
FAIL_ASH_TCU_K3C_EXPLICIT_GRID_SHAPE_MISSING
FAIL_ASH_TCU_K3C_SILENT_GRID_INFERENCE_USED
FAIL_ASH_TCU_K3C_DESCRIPTOR_COUNT_ZERO
FAIL_ASH_TCU_K3C_GRID_WIDTH_ZERO
FAIL_ASH_TCU_K3C_GRID_HEIGHT_ZERO
FAIL_ASH_TCU_K3C_DESCRIPTOR_COUNT_GRID_PRODUCT_MISMATCH
FAIL_ASH_TCU_K3C_DISPATCH_GRID_MISMATCH
FAIL_ASH_TCU_K3C_DISPATCH_Z_NOT_ONE
FAIL_ASH_TCU_K3C_RAGGED_GRID_FOUND
FAIL_ASH_TCU_K3C_HOST_WGSL_LINEARIZATION_MISMATCH
FAIL_ASH_TCU_K3C_DESCRIPTOR_MACRO_ID_MISMATCH
FAIL_ASH_TCU_K3C_DESCRIPTOR_INDEX_OUT_OF_BOUNDS
FAIL_ASH_TCU_K3C_C_OUTPUT_RANGE_OVERLAP
FAIL_ASH_TCU_K3C_C_OUTPUT_COVERAGE_MISMATCH
FAIL_ASH_TCU_K3C_TILE_OFFSET_ALIGNMENT_MISMATCH
FAIL_ASH_TCU_K3C_NATIVE_MULTI_MACRO_DISPATCH_EXECUTED_AS_CORRECTNESS
FAIL_ASH_TCU_K3C_PRODUCTION_MULTI_MACRO_DISPATCH_OPEN
FAIL_ASH_TCU_K3C_RUNTIME_SPLICE_OPEN
FAIL_ASH_TCU_K3C_PERFORMANCE_CLAIM_FOUND
```

## Next allowed patch

```text
ASH-TCU-K3D — Native 2x1 Multi-Macro Dispatch Readback / Grid Plan To GPU Output Correctness Seal
```

K3D is the first patch allowed to execute the 2x1 native multi-macro dispatch and verify 2048 readback bytes against CPU oracle.
