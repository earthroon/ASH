# ASH-BASETRAIN-GPU-70F SPEC

## Patch ID
ASH-BASETRAIN-GPU-70F

## Title
Readonly Block Probe Staging / Hidden FFN Provenance To Block Candidate Seal

## Seal
No Logits / No Decode / No Sampling / No Generation / No Loss / No Backward / No Optimizer

## Bake Status
BAKED_CODE_AND_SPECS_RUNTIME_NOT_EXECUTED_IN_CONTAINER

Output ZIP: `ash_pass3_ASH-BASETRAIN-GPU-70F_readonly_block_probe_staging_baked.zip`

## Purpose
GPU-70F stages a readonly transformer block candidate envelope from the GPU-70E hidden and FFN provenance audit.

This patch does not execute full block forward, attention, residual, norm, LM-head, logits, decode, sampling, generation, loss, backward, optimizer, weight mutation, runtime attach, production attach, or checkpoint mutation.

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
The readonly block candidate envelope records block candidate ID, source digests, hidden input shape, FFN output shape, candidate hidden size, selected token position index, contract-only attention/residual/norm states, `full_block_forward_claimed=false`, and `logits_materialized=false`.

## Implementation Surface
- crates/base_train/src/ash_basetrain_gpu_70f_readonly_block_probe_staging.rs
- crates/base_train/src/bin/ash_basetrain_gpu_70f_readonly_block_probe_staging.rs
- crates/base_train/src/lib.rs
- crates/base_train/Cargo.toml

## Rust / WGPU Rule
GPU-70F is staging-only and introduces no tensor arithmetic kernel. The Rust implementation should be match-oriented and lookup-table-oriented. No WGSL file is required for 70F. Future tensor computation must route through WGPU/WGSL shader paths.

## Static Summary
- New module `if` count: 0
- New module `json!` count: 0
- `.sha256` sidecars: 0
- WGSL files added: none
- Cargo check: deferred because cargo executable is unavailable in this container

## Next Stage
ASH-BASETRAIN-GPU-70G — Attention Contract Audit / Readonly Block Candidate To Attention Requirement Seal / No Attention Dispatch No Logits No Loss No Backward No Optimizer
