# SFT-GPU-2 Acceptance

## Status

STATIC-PASS / CARGO-CHECK-NOT-RUN

## Scope

`lm_head module_lora target resolver seal`

## Checked Files

- `crates/lora_train/src/targets.rs`
- `crates/lora_train/src/scaffold.rs`
- `crates/lora_train/src/bin/lora_train.rs`
- `crates/lora_train/src/lib.rs`
- `docs/A_SFT_GPU_DIRECT_LINE.md`

## Required Contract

- `lm_head` is accepted as a `module_lora` train target.
- `lm_head` has global target scope.
- `lm_head` resolves to target_key `lm_head`.
- `lm_head` produces exactly one attachment.
- `lm_head` does not produce `layers.0.lm_head`.
- `lm_head` does not produce duplicate target keys.
- A-SFT direct line does not fall back to `shared_hidden_classifier`.

## Gates

- [x] `LM_HEAD_TARGET` constant exists.
- [x] `ModuleLoraTargetScope::{Global, PerLayer}` exists.
- [x] `module_lora_target_scope("lm_head") == Some(Global)` by code path.
- [x] `module_lora_target_scope("attn.q_proj") == Some(PerLayer)` by code path.
- [x] Unsupported `module_lora` target returns an explicit error instead of being silently filtered.
- [x] `resolve_module_targets()` returns scoped targets.
- [x] Global targets bypass the layer loop.
- [x] Per-layer targets retain the existing layer loop.
- [x] `target_key_base(0, "lm_head")` returns `lm_head`.
- [x] A-SFT direct line requires exactly one `lm_head` attachment.
- [x] Duplicate target_key guard exists.
- [x] CLI emits `[lora_train][module_lora_resolver] target=... scope=... target_key=...` logs.

## Non-goals

- Response-only loss mask execution is not implemented here.
- GPU LoRA A/B update is not implemented here.
- Runtime logits delta verification is not implemented here.
- Generation quality smoke is not implemented here.

## Expected Next Boundary

After SFT-GPU-2, the direct line should pass config validation and target resolution. The next legitimate boundary is response-token label masking and direct SFT batch construction, which belongs to SFT-GPU-3.
