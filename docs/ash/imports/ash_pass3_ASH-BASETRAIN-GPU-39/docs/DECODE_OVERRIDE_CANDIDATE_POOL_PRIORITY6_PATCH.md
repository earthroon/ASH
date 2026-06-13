# Decode Override Candidate Pool Priority 6 Patch

## Goal
Push `stop_sequences` and `min_new_tokens` down from runtime-only postprocessing into `model_core` generation telemetry for native cached generation paths.

## What changed
- `GenerationSamplingConfig` now carries:
  - `stop_sequences: Vec<String>`
  - `min_new_tokens: usize`
- `runtime/src/infer.rs::build_generation_sampling_config(...)` now populates those fields from `StandardInferDecodeOverride`.
- `model_core::generate_with_sampling_cached_with_telemetry(...)` now:
  - accepts `Option<&TokenizerManifest>`
  - reconstructs emitted text incrementally from generated token pieces
  - detects `stop_sequences` after `min_new_tokens` has been satisfied
  - seals `GenerationTelemetry.stop_hit`
  - finalizes `GenerationFinishReason::StopSequence` when a stop sequence is hit
- `model_core::greedy_generate_cached_with_telemetry(...)` now:
  - accepts optional `GenerationSamplingConfig`
  - accepts optional `TokenizerManifest`
  - applies the same `stop_sequences` / `min_new_tokens` telemetry logic on the greedy cached path
- `runtime/src/infer.rs` now passes `Some(&manifest)` into both sampled and greedy telemetry calls.

## Current truth boundary
- `min_new_tokens` is now enforced in `model_core` stop detection logic.
- `stop_hit` is now produced by `model_core` telemetry for native cached generation.
- runtime still trims surface text using `apply_decode_stop_sequences(...)`, but this is now primarily output cleanup rather than the primary finish-reason source.

## Known limits
- This patch only upgrades the native cached path.
- Reference / CPU fallback generation still does not emit the same stop-sequence telemetry truth.
- Model-core stop detection still reconstructs text through tokenizer-manifest pieces and is not yet a token-id-native stop matcher.
- Compile verification was not executed in this environment.
