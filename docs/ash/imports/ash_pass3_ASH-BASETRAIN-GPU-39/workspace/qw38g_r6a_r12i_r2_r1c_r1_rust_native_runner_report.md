# 16AI-QW-38G-R6A-R12A-R12I-R2-R1C-R1 Rust-Native Snapshot Runner / No PowerShell Wrapper Seal

## Status

BAKED_RUST_NATIVE_SNAPSHOT_RUNNER_PENDING_LOCAL_CARGO_RUN

## Applied

- Rewrote `crates/runtime/src/bin/inference_logit_snapshot.rs` as the Rust-native execution owner.
- Removed `scripts/run_inference_logit_snapshot.ps1` from the baked artifact.
- Added direct `--receipt-output-path` and `--log-output-path` support.
- Added `--no-model-write` guard.
- Missing `runtime_forward_logit_rows.json` now writes a PARTIAL runner receipt and exits 0.
- Snapshot output is only written from real runtime forward rows. No mock logits are generated.

## Direct run

```powershell
cargo run -p runtime --bin inference_logit_snapshot -- `
  --target-token-id 13 `
  --masked-top1-token-id 373 `
  --target-layer 21 `
  --target-head 2 `
  --direction-basis LM_HEAD_13_MINUS_373 `
  --profile HEAD2_TARGET_DIRECTION_ORTHOGONAL_ONLY `
  --overlay-mode REVERSIBLE_RUNTIME_ONLY `
  --runtime-forward-source-path .\workspaceuntime_forward_logit_rows.json `
  --snapshot-output-path .\workspaceuntime_logit_snapshot_source.json `
  --receipt-output-path .\workspace\qw38g_r6a_r12i_r2_r1c_runner_receipt.json `
  --log-output-path .\workspace\qw38g_r6a_r12i_r2_r1c_runner.log `
  --runtime-default-apply false `
  --no-model-write `
  --strict
```

## Local expected partial

If `workspace/runtime_forward_logit_rows.json` is missing, Rust should write:

- `workspace/qw38g_r6a_r12i_r2_r1c_runner_receipt.json`
- `workspace/qw38g_r6a_r12i_r2_r1c_runner.log`

with:

```text
status = PARTIAL_INFERENCE_SNAPSHOT_COMMAND_IMPLEMENTATION
adjudication = RUST_RUNNER_PRESENT_BUT_RUNTIME_FORWARD_HOOK_NOT_CONNECTED
exit_code = 0
```
