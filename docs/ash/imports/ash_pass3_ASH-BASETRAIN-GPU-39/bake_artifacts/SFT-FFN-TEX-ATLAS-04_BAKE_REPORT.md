# SFT-FFN-TEX-ATLAS-04 Bake Report

## Commit

SFT-FFN-TEX-ATLAS-04 — Texture Atlas Scratch Budget Guard / Device Limit Preflight

## Base

Built on top of `ash_pass3_SFT-FFN-TEX-ATLAS-03_batched_token_texture_ffn_dispatch_baked.zip`.

## Added

- `crates/ash_core/src/sft_ffn_texture_atlas_budget_guard.rs`
- `crates/ash_core/tests/sft_ffn_tex_atlas_04_budget_guard.rs`
- `acceptance_reports/SFT-FFN-TEX-ATLAS-04_texture_atlas_scratch_budget_guard.md`
- `bake_artifacts/SFT-FFN-TEX-ATLAS-04_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-TEX-ATLAS-04_STATIC_VALIDATION.txt`

## Modified

- `crates/ash_core/src/lib.rs`

## Opened

- Texture atlas budget preflight.
- Device limit profile receipt.
- Scratch estimate receipt.
- Atlas dimension preflight.
- Storage binding limit preflight.
- Dispatch/workgroup limit preflight.
- Safe token group candidate selection.
- Explicit group shrink receipt.

## Kept Closed

- Batched dispatch execution.
- Shader execution for training.
- Shader execution for production.
- Batched dispatch as default.
- SFT training execution in ash_core.
- Gradient write in ash_core.
- Optimizer step in ash_core.
- LoRA trainable texture update.
- Runtime attach.
- Promotion apply.
- Current pointer update.

## Verification Note

This environment does not include `cargo`, `rustc`, or `rustfmt`, so runtime Rust compilation was not executed here. Static file presence, module export wiring, brace balance, and artifact inclusion were checked.
