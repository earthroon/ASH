# SAME DEVICE RAW LOGITS BRIDGE PRIORITY5 PATCH

## Scope
Priority-5 folds roadmap stage 1 and stage 2 into the current tree:

1. Reduce eager `cpu_row` materialization on native sampled hot paths.
2. Upgrade the GPU select shader to perform exact `top_k` filtering before noisy selection.

## Changes

### `crates/model_core/src/lib.rs`
- Added `prefer_same_device_sampling_fast_path()`.
- Added `should_materialize_cpu_last_row(...)`.
- Added `ensure_cpu_row_materialized(...)` for lazy fallback-only host rows.
- `apply_logit_postprocessors(...)` now skips CPU mutation when `cpu_row` is empty.
- `forward_last_logits_only(...)` now defers host row creation when the same-device sampling fast path is available and the full vocab row is present.
- `project_last_hidden_last_row(...)` mirrors the same lazy materialization behavior.
- `select_next_token_with_sampling(...)` now:
  - prefers the raw same-device lease path first,
  - only materializes `cpu_row` lazily for CPU upload fallback,
  - uses the lazily materialized row for final greedy fallback.

### `crates/burn_webgpu_backend/src/shaders/gpu_sampling_select.wgsl`
- Replaced the pure temperature-scaled argmax scaffold with:
  - deterministic Gumbel noise generation from shader-side seeds,
  - exact scalar `top_k` thresholding for `top_k > 0 && top_p >= 1.0`,
  - noisy max selection over the filtered set.

## Status
- Same-device sampled hot path no longer requires eager `cpu_row` creation when a raw bridge is available.
- CPU row fallback still exists, but is now lazy and fallback-only.
- `top_k` is exact inside the current single-invocation shader path.
- `top_p` remains placeholder / non-exact and should be treated as next-stage work.

## Follow-up
- Exact GPU-native `top_p`.
- Replace `score -> logprob` placeholder in selection output.
- Remove legacy CPU upload fallback once same-device raw path is proven stable.
