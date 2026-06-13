# SFT-FFN-LORA-01 Bake Report

## Patch

SFT-FFN-LORA-01 — FFN Down Projection LoRA Target / GPU Delta Path Seal

## Baked On Top Of

SFT-FFN-TEX-ATLAS-07 — Hybrid Delta Timing Probe / Base Texture + LoRA Buffer Compare Seal

## Added

- `crates/ash_core/src/sft_ffn_lora_target.rs`
- `crates/ash_core/tests/sft_ffn_lora_01_down_projection_target.rs`
- `crates/burn_webgpu_backend/src/ffn_lora_target.rs`
- `acceptance_reports/SFT-FFN-LORA-01_ffn_down_projection_lora_target.md`
- `bake_artifacts/SFT-FFN-LORA-01_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-LORA-01_STATIC_VALIDATION.txt`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- FFN down projection LoRA target candidate
- Target module contract
- Target module fingerprint
- LoRA shape contract
- LoRA scale policy
- LoRA delta target evidence
- LoRA buffer read

## Still Closed

- FFN gate/up LoRA target
- Target auto-remap
- LoRA target for training
- LoRA target for production
- LoRA target as default
- LoRA buffer write
- LoRA optimizer step
- LoRA texture update
- SFT training in core
- Gradient write in core
- Optimizer step in core
- Runtime attach
- Promotion apply
- Current pointer update

## Local Validation Command

```bash
cargo test -p ash_core sft_ffn_lora_01 -- --nocapture
cargo test -p ash_core sft_ffn_tex_atlas_07 -- --nocapture
cargo test -p burn_webgpu_backend ffn_lora_target -- --nocapture
```

## Environment Note

This bake environment does not include `cargo`, `rustc`, or `rustfmt`, so runtime compilation was not executed here. Static file, module, brace, acceptance, and archive checks were performed.
