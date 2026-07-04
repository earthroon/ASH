# QW-55A-0-R2
## Logical VTC16 Single-Dispatch SoftMatrix Kernel / Four 8x8 SoftCore Workgroup Seal

## Scope

This patch replaces the R1 logical VTC16 eight-step smoke-wrapper claim with a real single-dispatch software matrix kernel contract.

It adds a portable WGSL software TensorCore-mimic kernel:

```text
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_16x16_from8x8_softgroup.wgsl
```

The kernel computes one logical 16x16 macro tile in one 64-lane workgroup. The output remains four physical 8x8 Vec4F32 atlas tiles: C00, C01, C10, C11.

## Required invariants

```text
physical_tile_shape = [8,8]
logical_tile_shape = [16,16]
workgroup_size = [64,1,1]
k_panels = 2
creates_contiguous_16x16_tile = false
persistent_tile16_storage_created = false
cpu_reference_used_for_runtime_selection = false
runtime_inference_replacement_allowed = false
sft_pass1_replacement_allowed = false
backend_policy_connection_allowed = false
subgroup_fast_path_enabled = false
cooperative_matrix_claimed = false
hardware_tensorcore_claimed = false
```

## Local artifact policy

No docs acceptance report is committed for this patch. Generated manifest and runtime artifacts are produced locally by Rust:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin qw55a0_r2_logical16_softmatrix_audit
```

Expected local outputs:

```text
workspace/runtime/tensorcube/ash_tensorcube_logical16_softmatrix_fixture_latest.json
workspace/runtime/tensorcube/ash_tensorcube_logical16_softmatrix_cpu_reference_latest.json
workspace/runtime/tensorcube/ash_tensorcube_logical16_softmatrix_kernel_hit_ledger_latest.json
workspace/runtime/tensorcube/ash_tensorcube_logical16_softmatrix_report_latest.json
artifacts/qw55a0_r2_logical16_softmatrix_local_manifest.json
```

Those generated files are not committed.

## Acceptance

```text
PASS: new logical16 WGSL shader exists
PASS: shader uses @workgroup_size(64, 1, 1)
PASS: one workgroup computes one logical 16x16 macro tile
PASS: output remains four existing physical 8x8 atlas tiles
PASS: CPU reference matches the software lane mapping mirror
PASS: shader SHA-256 is computed by Rust
PASS: kernel hit ledger forbids inline naive candidate
PASS: kernel hit ledger forbids treating the old 8-step wrapper as the single-dispatch candidate
PASS: runtime splice remains closed
PASS: generated manifest/artifacts are local Rust outputs only
```
