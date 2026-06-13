# SFT-ATLAS-02 Static Validation Result

Status: PASS

## Checks
- [x] crates/ash_core/src/sft_atlas_safetensors_header_audit.rs: exists
- [x] crates/ash_core/src/sft_atlas_safetensors_header_audit.rs: paren_balance
- [x] crates/ash_core/src/sft_atlas_safetensors_header_audit.rs: brace_balance
- [x] crates/ash_core/src/sft_atlas_safetensors_header_audit.rs: bracket_balance
- [x] crates/ash_core/tests/sft_atlas_02_safetensors_header_audit.rs: exists
- [x] crates/ash_core/tests/sft_atlas_02_safetensors_header_audit.rs: paren_balance
- [x] crates/ash_core/tests/sft_atlas_02_safetensors_header_audit.rs: brace_balance
- [x] crates/ash_core/tests/sft_atlas_02_safetensors_header_audit.rs: bracket_balance
- [x] crates/ash_core/src/lib.rs: exists
- [x] crates/ash_core/src/lib.rs: paren_balance
- [x] crates/ash_core/src/lib.rs: brace_balance
- [x] crates/ash_core/src/lib.rs: bracket_balance
- [x] source: contains AshSftAtlasHeaderAuditMode
- [x] source: contains AshSftAtlasObservedSafetensorsHeader
- [x] source: contains AshSftAtlasTensorIndexComparisonStatus
- [x] source: contains AshSftAtlasSafetensorsHeaderAuditConfig
- [x] source: contains AshSftAtlasSafetensorsHeaderAuditSeal
- [x] source: contains AshSftAtlasSafetensorsHeaderAuditReport
- [x] source: contains build_sft_atlas_safetensors_header_audit
- [x] source: contains compute_observed_tensor_index_hash
- [x] source: contains allow_safetensors_write: false
- [x] source: contains allow_safetensors_mutation: false
- [x] source: contains allow_native_dump_execution: false
- [x] source: contains allow_sft_training_execution: false
- [x] source: contains allow_lora_artifact_write: false
- [x] source: contains allow_sft_slot_ready: false
- [x] source: contains allow_synapse_binding: false
- [x] source: contains allow_runtime_attach: false
- [x] tests: contains audits_matching_header_successfully
- [x] tests: contains rejects_sha256_mismatch
- [x] tests: contains rejects_unexpected_tensor
- [x] tests: contains rejects_dtype_and_shape_mismatch
- [x] tests: contains rejects_tensor_index_hash_mismatch
- [x] tests: contains rejects_manifest_or_write_or_native_flags_open
- [x] tests: contains deterministic_header_audit_seal_id
- [x] lib: module exported
- [x] lib: pub use exported

## Cargo
- `cargo test -p ash_core sft_atlas_02 -- --nocapture` could not be executed in this environment because `cargo` is not installed.

## Seal
- Safetensors write remains disabled.
- Safetensors mutation remains disabled.
- Native dump execution remains disabled.
- SFT training remains disabled.
- LoRA artifact write remains disabled.
- SFT slot ready remains disabled.
- ASH synapse binding remains disabled.
- Runtime attach remains disabled.
