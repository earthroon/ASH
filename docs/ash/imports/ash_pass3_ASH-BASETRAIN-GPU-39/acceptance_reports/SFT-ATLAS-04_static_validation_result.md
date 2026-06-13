# SFT-ATLAS-04 Static Validation Result

## Status
STATIC_VALIDATION_COMPLETED_WITHOUT_RUSTC

## Checked
- `crates/ash_core/src/sft_atlas_dataset_checkpoint_binding_guard.rs` exists.
- `crates/ash_core/tests/sft_atlas_04_dataset_checkpoint_binding_guard.rs` exists.
- `acceptance_reports/SFT-ATLAS-04_dataset_lock_atlas_checkpoint_binding_guard.md` exists.
- `crates/ash_core/src/lib.rs` exports the new module.
- Source/test/lib brace, paren, and bracket balance checked by script.
- Dataset write receipt, checkpoint receipt, and header audit seal are all consumed by the guard.
- Dataset lock hash mismatch rejection path exists.
- Optional missing `source_write_receipt_id` manual-review path exists.
- Header audit failure rejection path exists.
- Safetensors write/mutation, native dump, SFT training, LoRA artifact write, SFT slot ready, ASH synapse binding, and runtime attach flags remain sealed.
- Deterministic `binding_evidence_id` test exists.

## Not Run
`cargo test -p ash_core sft_atlas_04 -- --nocapture` was not run because `cargo` is not installed in this execution environment.

## Local Verification Command
```bash
cargo test -p ash_core sft_atlas_04 -- --nocapture
```
