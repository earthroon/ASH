# SFT-ATLAS-01 — Atlas Checkpoint Safetensors Writer / Tensor Index Seal

## Status
PASS_ATLAS_CHECKPOINT_SAFETENSORS_WRITER_TENSOR_INDEX_SEAL

## Scope
- Treats `.safetensors` as Atlas checkpoint SSOT.
- Writes a prebuilt safetensors payload atomically, or binds an existing safetensors file.
- Creates deterministic tensor index seal.
- Creates deterministic checkpoint fingerprint.
- Creates deterministic checkpoint lock hash.
- Creates deterministic checkpoint receipt.
- Reuses the existing SFT-DATA-02 `AshSftAtlasCheckpointKind` contract.
- Treats manifest as metadata only.
- Does not treat manifest as checkpoint SSOT.
- Does not execute native dump.
- Does not execute SFT training.
- Does not write gradients.
- Does not run optimizer step.
- Does not write LoRA runtime artifacts.
- Does not mark SFT slot ready.
- Does not create ASH synapse binding.
- Does not attach runtime LoRA.

## Files
- `crates/ash_core/src/sft_atlas_checkpoint_safetensors_writer.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/sft_atlas_01_checkpoint_safetensors_writer.rs`

## Seal Flags
- `tensor_index_sealed = true`
- `ssot_file_is_safetensors = true`
- `manifest_is_metadata_only = true`
- `safetensors_written = true or false depending on mode`
- `existing_safetensors_bound = true or false depending on mode`
- `manifest_as_checkpoint_ssot_allowed = false`
- `native_dump_execution_allowed = false`
- `sft_training_execution_allowed = false`
- `gradient_write_allowed = false`
- `optimizer_step_allowed = false`
- `lora_artifact_write_allowed = false`
- `sft_slot_ready_allowed = false`
- `synapse_binding_allowed = false`
- `runtime_attach_allowed = false`

## Safetensors SSOT Contract
- Atlas checkpoint SSOT must be `.safetensors`.
- `tensor_format` must equal `safetensors`.
- `expected_sha256` must be present.
- `expected_size_bytes` must be greater than zero.
- Tensor index entries must be present and sealed.
- Manifest must remain metadata only.
- `.json`, `.bin`, `.pt`, and `.ckpt` checkpoint paths are rejected.

## Modes
- `WritePrebuiltSafetensorsPayload` copies an already-built safetensors payload into staging, verifies hash/size, then atomically promotes it to final path.
- `BindExistingSafetensorsFile` verifies and seals an existing safetensors file without rewriting it.

## Reproducibility
- `tensor_index_hash` is deterministically derived from:
  - sorted tensor names
  - dtype
  - shape
  - logical role
  - shard index
  - optional tensor hash

- `checkpoint_fingerprint` is deterministically derived from:
  - safetensors sha256
  - safetensors size
  - tensor format
  - tensor index hash
  - checkpoint kind

- `checkpoint_lock_hash` is deterministically derived from:
  - checkpoint id
  - checkpoint fingerprint
  - safetensors path
  - safetensors sha256
  - safetensors size
  - source dataset lock hash
  - created timestamp

## Result
SFT-ATLAS-01 establishes safetensors as the Atlas checkpoint SSOT and seals tensor index evidence. Native dump execution, SFT training, LoRA artifact write, SFT slot readiness, ASH synapse binding, and runtime attachment remain sealed.
