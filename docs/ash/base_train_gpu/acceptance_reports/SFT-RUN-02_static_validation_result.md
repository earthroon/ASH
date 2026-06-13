# SFT-RUN-02 Static Validation Result

## Status
STATIC_REVIEW_ONLY

## Environment
- `cargo` was not available in this execution environment.
- `rustc` was not available in this execution environment.
- Full Rust compilation could not be executed here.

## Static Checks Performed
- Confirmed module file exists: `crates/ash_core/src/sft_run_execution_receipt_intake.rs`.
- Confirmed test file exists: `crates/ash_core/tests/sft_run_02_execution_receipt_intake.rs`.
- Confirmed `crates/ash_core/src/lib.rs` exports `sft_run_execution_receipt_intake`.
- Confirmed SFT-RUN-02 status constants are present.
- Confirmed artifact capture remains sealed by explicit fields:
  - `artifact_capture_performed = false`
  - `trained_artifact_capture_allowed = false`
  - `output_adapter_digest_recorded = false`
  - `output_manifest_digest_recorded = false`
- Confirmed core execution fields remain sealed:
  - `sft_training_execution_performed_in_core = false`
  - `native_dump_execution_performed_in_core = false`
  - `gradient_write_performed_in_core = false`
  - `optimizer_step_performed_in_core = false`
- Confirmed tests cover success receipt, failed run receipt, runner mismatch, nonzero success exit rejection, invalid timestamp rejection, log path mismatch, artifact capture flag rejection, and deterministic receipt ids.

## Local Verification Command
```bash
cargo test -p ash_core sft_run_02 -- --nocapture
```

## Result
SFT-RUN-02 was baked with static validation only in this environment. Compile/runtime validation must be run locally with Cargo.
