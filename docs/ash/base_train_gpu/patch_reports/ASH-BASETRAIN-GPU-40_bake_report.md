# ASH-BASETRAIN-GPU-40 Bake Report

## Patch

ASH-BASETRAIN-GPU-40 — Multi Row-Block MatVec Candidate / Segmented Atlas Group Dispatch Matrix Seal / No Logits Adoption No Optimizer

## Source SSOT

- Code/runtime bake base: `ash_pass3_ASH-BASETRAIN-GPU-39_atlas_upload_ring_buffer_slot_lease_release_baked (2) (2).zip`
- Documentation/evidence SSOT: `https://github.com/earthroon/ASH`

## Implemented Files

- `crates/base_train/src/ash_basetrain_gpu_40_multi_row_block_matvec_segmented_dispatch_matrix.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_40_multi_row_block_matvec_segmented_dispatch_matrix.rs`
- `specs/ASH_BASETRAIN_GPU_40_SPEC.md`

## Runtime Contract

40 uses the 39 slot ring receipt as primary gate and processes at least two row-block segments through explicit lease/fill/upload/dispatch/readback/release. Segment outputs are sealed as a segmented dispatch matrix only.

## Guards

- `model_forward_executed = false`
- `forward_output_adopted = false`
- `logits_materialized = false`
- `logits_written = false`
- `loss_computed = false`
- `backward_executed = false`
- `optimizer_step_executed = false`
- `weight_buffer_mutated = false`
- `checkpoint_written = false`
- `safetensors_written = false`

## Verification

- Static checks: PASS
- Cargo build: NOT_RUN_CARGO_UNAVAILABLE_IN_CONTAINER
- Runtime GPU: NOT_RUN_LOCAL_GPU_REQUIRED
