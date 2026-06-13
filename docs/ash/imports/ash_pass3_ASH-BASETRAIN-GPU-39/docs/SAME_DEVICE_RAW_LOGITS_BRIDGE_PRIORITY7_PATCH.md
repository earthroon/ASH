# SAME_DEVICE_RAW_LOGITS_BRIDGE_PRIORITY7_PATCH

## Scope
Priority 7 introduces sampled cached path telemetry in `crates/model_core/src/lib.rs`.

## Added
- `GenerationFinishReason`
- `GenerationStepTelemetry`
- `GenerationTelemetry`
- `generate_with_sampling_cached_with_telemetry(...)`
- internal choice-returning helpers:
  - `prefill_with_sampling_choice(...)`
  - `decode_step_with_sampling_choice(...)`

## Behavior
- sampled cached generation now records per-step `token_id / logit / logprob / sampled`
- `mean_logprob / min_logprob / sampled_decode_applied` are finalized from model_core truth
- legacy `generate_with_sampling_cached(...)` remains and now wraps the telemetry variant

## Notes
- finish reason is currently `Eos | MaxNewTokens | Unknown`
- greedy path telemetry remains sparse (`logprob: None`) because non-sampled path step truth is not yet threaded through
- runtime/infer is not yet bound to consume the new telemetry API in this patch
