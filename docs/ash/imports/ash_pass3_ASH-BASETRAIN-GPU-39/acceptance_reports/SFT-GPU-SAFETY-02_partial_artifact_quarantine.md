# SFT-GPU-SAFETY-02 Acceptance Report

## Seal

`SFT-GPU-SAFETY-02 — Partial Artifact Quarantine / Failed Train Output Guard`

## Source

- source_gpu_train_fault_recovery_seal_id: required
- source_fault_receipt_id: required
- train_run_id: required
- adapter_slot_id: required
- adapter_candidate_id: required

## Partial Artifact Scan

- failed_train_output_root: required
- partial_artifact_scan_digest: required
- failed_train_output_digest: required
- artifact_entry_count: required and non-zero

## Quarantine

- quarantine_required: derived from artifact entries
- quarantine_applied: true only when quarantine is required and no guard failure exists
- quarantine_namespace: `quarantine/sft-gpu/{train_run_id}/{adapter_candidate_id}/{failed_output_digest}`
- quarantine_ledger_event_id: deterministic append-only event id
- quarantine_receipt_digest: deterministic receipt digest
- partial_artifact_quarantine_seal_id: emitted only for accepted quarantine records

## Blocked Paths

- registry_intake_allowed: false
- promotion_allowed: false
- current_pointer_binding_allowed: false
- lifecycle_action_path_allowed: false

## Silent Correction Guard

- auto_repair_performed: false
- silent_registry_correction_detected: false
- silent_manifest_patch_detected: false
- silent_digest_replacement_detected: false

## Runtime Closure

- runtime_sft_training_performed_after_quarantine: false
- runtime_gradient_write_performed_after_quarantine: false
- runtime_optimizer_step_performed_after_quarantine: false
- textureSample / sampler / normalized UV weight fetch: closed

## Added Files

- `crates/ash_core/src/sft_gpu_partial_artifact_quarantine.rs`
- `crates/ash_core/tests/sft_gpu_safety_02_partial_artifact_quarantine.rs`
- `crates/lora_train/src/partial_artifact_quarantine.rs`
- `crates/lora_train/tests/partial_artifact_quarantine.rs`
- `crates/burn_webgpu_backend/src/gpu_partial_artifact_guard.rs`
- `crates/burn_webgpu_backend/tests/gpu_partial_artifact_guard.rs`

## Verification Commands

```bash
cargo test -p ash_core sft_gpu_safety_02 -- --nocapture
cargo test -p lora_train partial_artifact_quarantine -- --nocapture
cargo test -p burn_webgpu_backend gpu_partial_artifact_guard -- --nocapture
cargo test -p ash_core sft_gpu_safety_01 -- --nocapture
cargo test -p ash_core sft_gpu_run_13 -- --nocapture
cargo test -p ash_core sft_gpu_run_12 -- --nocapture
cargo test -p ash_core sft_gpu_run_11 -- --nocapture
```

## Local Container Note

The current bake container does not expose `cargo`, `rustc`, or `rustfmt`, so Rust compilation was not executed here. Static verification was performed for delimiter balance, export wiring, required file presence, and path inclusion. Run the commands above in the project Rust environment.
