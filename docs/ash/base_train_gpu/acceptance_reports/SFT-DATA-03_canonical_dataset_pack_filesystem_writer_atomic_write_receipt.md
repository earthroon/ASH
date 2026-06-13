# SFT-DATA-03 — Canonical Dataset Pack Filesystem Writer / Atomic Write Receipt

## Status
PASS_CANONICAL_DATASET_PACK_FILESYSTEM_WRITER_ATOMIC_WRITE_RECEIPT

## Scope
- Reads SFT-DATA-01 canonical dataset pack evidence.
- Reads SFT-DATA-02 dataset pack writer plan.
- Writes canonical dataset pack files into a staging layout.
- Verifies post-write file hashes and sizes.
- Atomically promotes staging dataset root to final dataset root.
- Creates deterministic atomic write receipt.
- Writes dataset manifest, dataset lock, canonical JSONL splits, and validation report.
- May write atlas checkpoint lock and metadata-only manifest.
- Does not write atlas checkpoint safetensors.
- Does not execute native dump.
- Does not execute SFT training.
- Does not write gradients.
- Does not run optimizer step.
- Does not write LoRA artifacts.
- Does not mark SFT slot ready.
- Does not create ASH synapse binding.
- Does not attach runtime LoRA.

## Files
- `crates/ash_core/src/sft_dataset_pack_atomic_writer.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/sft_data_03_dataset_pack_atomic_writer.rs`

## Seal Flags
- `atomic_write_receipt_created = true`
- `staging_write_completed = true`
- `post_write_hash_verified = true`
- `atomic_promote_completed = true`
- `dataset_pack_filesystem_write_allowed = true`
- `atomic_promote_allowed = true`
- `atlas_checkpoint_safetensors_written = false`
- `atlas_checkpoint_safetensors_write_allowed = false`
- `atlas_checkpoint_manifest_as_ssot_allowed = false`
- `sft_training_execution_allowed = false`
- `native_dump_execution_allowed = false`
- `gradient_write_allowed = false`
- `optimizer_step_allowed = false`
- `lora_artifact_write_allowed = false`
- `sft_slot_ready_allowed = false`
- `synapse_binding_allowed = false`
- `runtime_attach_allowed = false`

## Safetensors SSOT Contract
- Atlas checkpoint SSOT remains `.safetensors`.
- SFT-DATA-03 may write atlas checkpoint lock and metadata-only manifest.
- SFT-DATA-03 must not write or mutate `.safetensors`.
- Atlas checkpoint manifest remains metadata only.

## Atomic Write Contract
- Writes are staged first.
- Every staged file receives expected/actual SHA-256 and size verification.
- Final root is not overwritten by default.
- Staging root and final root must be distinct.
- Path traversal via `..` is rejected.
- Atomic promote is performed only after post-write verification passes.

## Reproducibility
- File receipt id is deterministically derived from:
  - atomic write request id
  - source write plan id
  - file kind
  - final path
  - expected hash
  - expected size

- Write receipt id is deterministically derived from:
  - atomic write request id
  - source write plan id
  - dataset id
  - dataset fingerprint
  - dataset lock hash
  - staging root
  - final dataset root
  - file receipt ids
  - created timestamp

## Result
SFT-DATA-03 performs atomic dataset pack filesystem write and creates write receipt only. Safetensors write, native dump execution, SFT training, LoRA artifact write, SFT slot readiness, ASH synapse binding, and runtime attachment remain sealed.
