# SFT-ATLAS-02 — Safetensors Header Audit / Tensor Index Cross-Verification

## Status
PASS_SAFETENSORS_HEADER_AUDIT_TENSOR_INDEX_CROSS_VERIFICATION

## Scope
- Reads SFT-ATLAS-01 checkpoint receipt.
- Reads externally observed safetensors header evidence.
- Verifies safetensors path, hash, and size.
- Cross-verifies sealed tensor index against observed header tensor map.
- Verifies tensor names, dtype, shape, and tensor count.
- Verifies tensor index hash.
- Creates deterministic header audit seal.
- Detects tensor index mismatch.
- Treats `.safetensors` as Atlas checkpoint SSOT.
- Treats manifest as metadata only.
- Does not write or mutate safetensors.
- Does not execute native dump.
- Does not execute SFT training.
- Does not write gradients.
- Does not run optimizer step.
- Does not write LoRA artifact.
- Does not mark SFT slot ready.
- Does not create ASH synapse binding.
- Does not attach runtime LoRA.

## Files
- `crates/ash_core/src/sft_atlas_safetensors_header_audit.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/sft_atlas_02_safetensors_header_audit.rs`

## Seal Flags
- `tensor_index_cross_verified = true`
- `header_audit_passed = true`
- `ssot_file_is_safetensors = true`
- `manifest_is_metadata_only = true`
- `manifest_as_checkpoint_ssot_allowed = false`
- `safetensors_write_allowed = false`
- `safetensors_mutation_allowed = false`
- `native_dump_execution_allowed = false`
- `sft_training_execution_allowed = false`
- `gradient_write_allowed = false`
- `optimizer_step_allowed = false`
- `lora_artifact_write_allowed = false`
- `sft_slot_ready_allowed = false`
- `synapse_binding_allowed = false`
- `runtime_attach_allowed = false`

## Reproducibility
- `header_audit_seal_id` is deterministically derived from:
  - header audit request id
  - SFT-ATLAS-01 checkpoint receipt id
  - checkpoint id
  - tensor index id
  - safetensors path
  - safetensors sha256
  - safetensors size
  - sealed tensor index hash
  - observed tensor index hash
  - comparison issue ids
  - created timestamp

## Result
SFT-ATLAS-02 cross-verifies safetensors header evidence against the sealed tensor index. Safetensors write/mutation, native dump execution, SFT training, LoRA artifact write, SFT slot readiness, ASH synapse binding, and runtime attachment remain sealed.
