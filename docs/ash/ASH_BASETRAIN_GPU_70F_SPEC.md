# ASH-BASETRAIN-GPU-70F SPEC

## Patch ID
ASH-BASETRAIN-GPU-70F

## Title
Readonly Block Probe Staging / Hidden FFN Provenance To Block Candidate Seal

## Seal
No Logits / No Decode / No Sampling / No Generation / No Loss / No Backward / No Optimizer

## Purpose
GPU-70F stages a readonly transformer block candidate envelope from the GPU-70E hidden and FFN provenance audit.

This patch does not execute full block forward, attention, residual, norm, LM-head, logits, decode, sampling, generation, loss, backward, optimizer, weight mutation, runtime attach, production attach, or checkpoint mutation.

GPU-70F proves that the 70E-proven hidden input and native atlas FFN output can be carried into a block-candidate staging envelope without silently claiming a full transformer block result.

## Input SSOT
- artifacts/ASH_BASETRAIN_GPU_70E_HIDDEN_FFN_COMPATIBILITY_AUDIT.json
- artifacts/ASH_BASETRAIN_GPU_70E_HIDDEN_FFN_COMPATIBILITY_AUDIT_RECEIPT.json
- artifacts/ASH_BASETRAIN_GPU_70D_NATIVE_ATLAS_FFN_OUTPUT_PROBE.json
- artifacts/ASH_BASETRAIN_GPU_70D_NATIVE_ATLAS_FFN_SMOKE_RECEIPT.json
- artifacts/ASH_BASETRAIN_GPU_70C_ASFT_HIDDEN_PROVIDER_PROBE.json
- artifacts/ASH_BASETRAIN_GPU_70B_NATIVE_FORWARD_PATH_SELECTION.json
- artifacts/ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_CANDIDATE_ENVELOPE.json
- artifacts/ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_ENVELOPE.json

## Output SSOT
- artifacts/ASH_BASETRAIN_GPU_70F_READONLY_BLOCK_CANDIDATE_ENVELOPE.json
- artifacts/ASH_BASETRAIN_GPU_70F_READONLY_BLOCK_PROBE_STAGING_RECEIPT.json

## State Ownership
GPU-70F owns readonly block candidate staging envelope, block candidate shape metadata, inherited hidden and FFN provenance references, and no-execution forbidden-path confirmation.

GPU-70F does not own attention execution, residual execution, norm execution, LM-head execution, logits, decode, sampling, generation, loss, backward, optimizer, weight mutation, runtime attach, production attach, checkpoint mutation, or full block output state.

## Required Checks
- 70E pass is true.
- 70E provenance_consistent is true.
- 70E hidden_provider_lineage_present is true.
- 70E hidden_probe_metadata_only_respected is true.
- 70E hidden_payload_reconstruction_claimed is false.
- 70E new_hidden_provider_execution_used is false.
- 70E new_ffn_execution_used is false.
- 70E hidden_input_shape is [2048].
- 70E ffn_output_shape is [2048].
- 70E selected_token_position_index is 51.
- 70D FFN output digest exists.
- 70D hidden input digest exists.
- All forbidden runtime path flags remain false.

## Block Candidate Contract
The readonly block candidate envelope records block_candidate_id, source digests, hidden input shape, FFN output shape, candidate hidden size, selected token position index, contract-only attention/residual/norm states, full_block_forward_claimed false, and logits_materialized false.

## Implementation Surface
- crates/base_train/src/ash_basetrain_gpu_70f_readonly_block_probe_staging.rs
- crates/base_train/src/bin/ash_basetrain_gpu_70f_readonly_block_probe_staging.rs
- crates/base_train/src/lib.rs
- crates/base_train/Cargo.toml

## Rust / WGPU Rule
GPU-70F is staging-only and introduces no tensor arithmetic kernel. The Rust implementation should be match-oriented and lookup-table-oriented. No WGSL file is required for 70F. Future patches that execute tensor computation should route compute through WGPU/WGSL shader paths.

## Next Stage
ASH-BASETRAIN-GPU-70G — Attention Contract Audit / Readonly Block Candidate To Attention Requirement Seal / No Attention Dispatch No Logits No Loss No Backward No Optimizer
