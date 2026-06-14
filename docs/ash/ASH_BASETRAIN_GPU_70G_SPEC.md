# ASH-BASETRAIN-GPU-70G SPEC

## Patch ID
ASH-BASETRAIN-GPU-70G

## Title
Attention Contract Audit / Readonly Block Candidate To Attention Requirement Seal

## Seal
No Attention Dispatch / No Logits / No Loss / No Backward / No Optimizer

## Bake Status
BAKED_CODE_AND_SPECS_RUNTIME_NOT_EXECUTED_IN_CONTAINER

Output ZIP: `ash_pass3_ASH-BASETRAIN-GPU-70G_attention_contract_audit_baked.zip`

## Purpose
GPU-70G audits whether the readonly block candidate produced by GPU-70F can be safely staged toward an attention requirement contract.

This patch does not execute attention dispatch, QKV projection, attention score computation, softmax, value aggregation, residual, norm, LM-head, logits, decode, sampling, generation, loss, backward, optimizer, weight mutation, runtime attach, production attach, or checkpoint mutation.

## Input SSOT
- artifacts/ASH_BASETRAIN_GPU_70F_READONLY_BLOCK_CANDIDATE_ENVELOPE.json
- artifacts/ASH_BASETRAIN_GPU_70F_READONLY_BLOCK_PROBE_STAGING_RECEIPT.json
- artifacts/ASH_BASETRAIN_GPU_70E_HIDDEN_FFN_COMPATIBILITY_AUDIT.json
- artifacts/ASH_BASETRAIN_GPU_70E_HIDDEN_FFN_COMPATIBILITY_AUDIT_RECEIPT.json
- artifacts/ASH_BASETRAIN_GPU_70D_NATIVE_ATLAS_FFN_OUTPUT_PROBE.json
- artifacts/ASH_BASETRAIN_GPU_70C_ASFT_HIDDEN_PROVIDER_PROBE.json
- artifacts/ASH_BASETRAIN_GPU_70B_NATIVE_FORWARD_PATH_SELECTION.json
- artifacts/ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_ENVELOPE.json

## Output SSOT
- artifacts/ASH_BASETRAIN_GPU_70G_ATTENTION_REQUIREMENT_CONTRACT_AUDIT.json
- artifacts/ASH_BASETRAIN_GPU_70G_ATTENTION_CONTRACT_AUDIT_RECEIPT.json

## Required Checks
- 70F pass is true.
- 70F readonly block candidate was created.
- 70F candidate hidden size is 2048.
- 70F selected token position index is 51.
- 70F attention contract state is contract_only_not_executed.
- 70F full block forward was not claimed.
- 70F logits were not materialized.
- 70E provenance remains consistent.
- All forbidden runtime path flags remain false.

## Attention Requirement Contract
The contract records source digests, batch size requirement, sequence length requirement, hidden size requirement, selected token position index, QKV requirement state, attention score requirement state, softmax requirement state, value aggregation requirement state, `attention_dispatch_allowed=false`, and `attention_dispatch_executed=false`.

## Implementation Surface
- crates/base_train/src/ash_basetrain_gpu_70g_attention_contract_audit.rs
- crates/base_train/src/bin/ash_basetrain_gpu_70g_attention_contract_audit.rs
- crates/base_train/src/lib.rs
- crates/base_train/Cargo.toml

## Rust / WGPU Rule
GPU-70G is audit-only and introduces no tensor arithmetic kernel. The Rust implementation should be match-oriented and lookup-table-oriented. No WGSL file is required for 70G. Future tensor computation must route through WGPU/WGSL shader paths.

## Static Summary
- New module `if` count: 0
- New module `json!` count: 0
- `.sha256` sidecars: 0
- WGSL files added: none
- Cargo check: deferred because cargo executable is unavailable in this container

## Next Stage
ASH-BASETRAIN-GPU-70H — QKV Requirement Shape Audit / Attention Contract To QKV Projection Boundary Seal / No QKV Dispatch No Attention Score No Softmax No Logits No Loss No Backward No Optimizer
