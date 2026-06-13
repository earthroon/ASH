# Decode Override Candidate Pool Priority 2 Patch

## Scope
Apply `StandardInferDecodeOverride` to the actual decode path in `crates/runtime/src/infer.rs`.

## What changed
- Added `run_standard_infer_with_decode(req, decode)` as the actual infer entry for per-candidate decode overrides.
- `run_standard_infer(req)` now delegates to `run_standard_infer_with_decode(req, None)`.
- Native WGPU path now builds a `GenerationSamplingConfig` from the override and calls `generate_with_sampling_cached_with_telemetry(...)` when sampled decode is requested.
- Effective `max_new_tokens` is now taken from the override when present.
- Candidate pool generation now calls `run_standard_infer_with_decode(..., Some(decode))` instead of mutating only seed/max token fields.
- Stop sequences / min_new_tokens are applied as post-decode trimming + finish-reason override in runtime output materialization.

## Actual override fields consumed now
- `temperature`
- `top_p`
- `top_k`
- `seed_override`
- `max_new_tokens`
- `stop_sequences` (postprocess trim)
- `min_new_tokens` (gate for stop-sequence trim)

## Still not fully native
- CPU/reference fallback still uses greedy generation.
- Stop sequences are not yet a model-core generation stop source; they are runtime postprocess trim in this patch.
- `min_new_tokens` only gates stop-trim, not model-core stopping.

## Intent
Turn decode override from metadata-only snapshot into a real runtime contract for native candidate generation.
