# SFT-DATA-01 — Dataset Source Manifest / Canonical JSONL Pack Seal

## Status
PASS_DATASET_SOURCE_MANIFEST_CANONICAL_JSONL_PACK_SEAL

## Scope
- Adds `crates/ash_core/src/sft_dataset_pack.rs`.
- Accepts single JSONL / multi JSONL / folder source metadata as dataset source input.
- Normalizes `input/output`, `prompt/completion`, and `messages` rows into canonical SFT examples.
- Creates deterministic row fingerprints.
- Creates dataset manifest evidence.
- Creates validation report evidence.
- Creates dataset fingerprint evidence.
- Creates dataset lock evidence.
- Creates canonical JSONL dataset pack evidence in memory.
- Supports auto-generated manifest for single JSONL input.
- Quarantines duplicate or suspicious rows.
- Rejects invalid or unusable rows.
- Does not write canonical dataset pack files to disk.
- Does not execute SFT training.
- Does not write gradients.
- Does not run optimizer step.
- Does not write LoRA artifacts.
- Does not mark SFT slot ready.
- Does not create ASH synapse binding.
- Does not attach runtime LoRA.

## Files
- `crates/ash_core/src/sft_dataset_pack.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/sft_data_01_dataset_pack_seal.rs`
- `acceptance_reports/SFT-DATA-01_dataset_source_manifest_canonical_jsonl_pack_seal.md`

## Seal Flags
- `canonical_pack_created = true`
- `manifest_created = true`
- `validation_report_created = true`
- `dataset_lock_created = true`
- `canonical_pack_filesystem_write_allowed = false`
- `sft_training_execution_allowed = false`
- `gradient_write_allowed = false`
- `optimizer_step_allowed = false`
- `lora_artifact_write_allowed = false`
- `sft_slot_ready_allowed = false`
- `synapse_binding_allowed = false`
- `runtime_attach_allowed = false`

## Reproducibility
- `row_fingerprint` is deterministically derived from normalized input, normalized output, split, sorted tags, sorted adapter scope, and weight.
- `dataset_id` is deterministically derived from schema version, sorted adapter scope, and row hash root.
- `dataset_fingerprint` is deterministically derived from schema version, sorted adapter scope, accepted row fingerprints, quarantined row fingerprints, and split counts.
- `dataset_lock_hash` is deterministically derived from dataset id, dataset fingerprint, manifest hash, row hashes root, canonical split hashes, and row counts.

## Result
SFT-DATA-01 creates canonical dataset pack evidence only. Filesystem pack write, SFT execution, gradient write, optimizer step, LoRA artifact write, SFT slot readiness, ASH synapse binding, and runtime attachment remain sealed.
