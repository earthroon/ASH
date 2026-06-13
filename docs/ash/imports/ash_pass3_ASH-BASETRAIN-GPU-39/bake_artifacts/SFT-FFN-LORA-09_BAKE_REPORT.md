# SFT-FFN-LORA-09 Bake Report

## Status

Baked on top of `SFT-FFN-INFRA-PERF-02`.

## Added

- `crates/ash_core/src/sft_ffn_lora_runtime_attach_dry_run.rs`
- `crates/ash_core/tests/sft_ffn_lora_09_runtime_attach_dry_run.rs`
- `crates/burn_webgpu_backend/src/ffn_lora_runtime_attach_dry_run.rs`
- `acceptance_reports/SFT-FFN-LORA-09_runtime_attach_dry_run.md`
- `bake_artifacts/SFT-FFN-LORA-09_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-LORA-09_STATIC_VALIDATION.txt`
- `bake_artifacts/SFT-FFN-LORA-09_FILE_DIGESTS.sha256`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- Approved adapter runtime attach dry-run.
- Artifact read for dry-run.
- Dry-run runtime sandbox evidence.
- Adapter load sanity evidence.
- Dry-run output sanity evidence.
- Rollback requirement evidence.
- Current pointer unchanged guard.

## Still Closed

- Production runtime attach.
- Promotion apply.
- Current pointer update.
- Slot ready mark.
- ASH binding.
- SFT training execution in core.
- Gradient write in core.
- Optimizer step in core.

## Local Verification

```bash
cargo test -p ash_core sft_ffn_lora_09 -- --nocapture
cargo test -p ash_core sft_ffn_lora_08 -- --nocapture
cargo test -p ash_core sft_ffn_lora_07 -- --nocapture
cargo test -p ash_core sft_ffn_lora_06 -- --nocapture
cargo test -p ash_core sft_ffn_lora_05 -- --nocapture
cargo test -p ash_core infra_perf_02 -- --nocapture
cargo test -p ash_core infra_perf_01 -- --nocapture
cargo test -p burn_webgpu_backend ffn_lora_runtime_attach_dry_run -- --nocapture
```

## Note

The current execution environment does not provide `cargo`, `rustc`, or `rustfmt`; runtime compilation remains pending for local validation.
