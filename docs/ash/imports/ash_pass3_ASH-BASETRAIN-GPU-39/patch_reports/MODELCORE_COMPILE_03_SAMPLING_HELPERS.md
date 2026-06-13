# MODELCORE-COMPILE-03 — Shared Sampling Helpers Extraction

## Purpose

Move shared token/text sampling helpers into `crates/model_core/src/sampling_helpers.rs`.

This keeps sampling policy helpers out of native-only or generation-only modules and gives `reference_checkpoint.rs`, `generation_sampling.rs`, and `native_wgpu.rs` one crate-local SSOT for shared token masking, repetition checks, stop-sequence holdback, cancellation, and token-piece append behavior.

## Changed Files

- `crates/model_core/src/lib.rs`
- `crates/model_core/src/sampling_helpers.rs`
- `crates/model_core/src/native_wgpu.rs`
- `crates/model_core/src/generation_sampling.rs`
- `crates/model_core/src/reference_checkpoint.rs`

## Extracted Helpers

- `apply_banned_token_mask`
- `apply_repetition_penalty`
- `has_repeating_suffix`
- `has_repeating_ngram`
- `StreamingTextHoldback`
- `max_stop_holdback_chars`
- `check_generation_cancel`
- `append_token_piece_to_text`
- `detect_stop_hit`

Private support helpers moved with the append path:

- `token_piece_from_manifest`
- `detokenize_sentencepiece_like`

## Ownership Notes

- `GenerationPieceSink` remains in `generation_sampling.rs` because it is part of the generation streaming surface, not the shared helper boundary.
- `sampling_helpers.rs` is registered as `mod sampling_helpers;`, not `pub mod sampling_helpers;`.
- Helpers are exposed as `pub(crate)` only where cross-module use is required.
- Helper implementations were moved without behavior changes.

## Non-Goals

- No `NativeWgpuModel` accessor repair.
- No `runtime_lora` schema repair.
- No reference checkpoint math extraction.
- No `model_layers` runtime_lora hook repair.
- No config changes.
- No sampling behavior changes.

## Validation

Run locally:

```powershell
cargo check -p model_core 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_03_check.log"
```

Expected cleared patterns:

```text
apply_banned_token_mask not found
apply_repetition_penalty not found
has_repeating_suffix not found
has_repeating_ngram not found
StreamingTextHoldback inaccessible
max_stop_holdback_chars inaccessible
check_generation_cancel inaccessible
append_token_piece_to_text inaccessible
detect_stop_hit inaccessible
```

Allowed remaining patterns:

```text
reference checkpoint math helper inaccessible
NativeWgpuModel private field/method access
runtime_lora schema drift
model_layers runtime_lora hook access
```

## Local Environment Note

This bake environment does not provide `cargo`, so compile validation must be run on the local Rust environment.
