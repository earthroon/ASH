# SFT-SLOT-02 Static Validation Result

## Status
PASS_STATIC_VALIDATION

## Checks
- crates/ash_core/src/sft_slot_lease_guard.rs: exists, balanced=True
- crates/ash_core/tests/sft_slot_02_lease_exclusive_writer_guard.rs: exists, balanced=True
- crates/ash_core/src/lib.rs: exists, balanced=True
- lib.rs contains `pub mod sft_slot_lease_guard;`: True
- lib.rs contains `pub use sft_slot_lease_guard::*;`: True
- module contains `allow_lease_persistent_write`: True
- module contains `allow_sft_training_execution`: True
- module contains `allow_native_dump_execution`: True
- module contains `allow_lora_artifact_write`: True
- module contains `allow_sft_slot_ready`: True
- module contains `allow_synapse_binding`: True
- module contains `allow_runtime_attach`: True
- module contains `allow_registry_mutation`: True
- module contains `find_active_conflicting_lease`: True
- module contains `LeaseGranted`: True
- module contains `REJECTED_SFT_SLOT_LEASE_CONFLICT`: True
- tests contain `active_lease_conflict_is_rejected`: True
- tests contain `expired_lease_is_not_conflict`: True
- tests contain `deterministic_lease_id`: True
- tests contain `lease_persistent_write_flag_is_rejected`: True

## Failures
- none

## Note
`cargo` is not installed in this execution environment, so Rust compilation was not executed here. Run `cargo test -p ash_core sft_slot_02 -- --nocapture` locally.
