# SAME_DEVICE_RAW_LOGITS_BRIDGE_PRIORITY4_PATCH

## Summary
Priority-4 binds the backend GPU sampling runtime into `crates/model_core/src/lib.rs`.

### Added in model_core
- `GenerationSamplingConfig`
- `NextTokenChoice.logprob`
- `NextTokenChoice.sampled`
- `NativeWgpuModel.gpu_sampling_runtime`
- `select_next_token_with_sampling(...)`
- `prefill_with_sampling(...)`
- `decode_step_with_sampling(...)`
- `generate_with_sampling_cached(...)`

## Behavior
When sampled decode is requested:
1. try same-device raw logits bridge (`gpu_last_row` + `RawWgpuBufferLease`)
2. fall back to same runtime with CPU logits upload
3. fall back to greedy selection if runtime path fails

## Notes
- This patch binds the runtime at the model-core seam.
- It does not yet remove `cpu_row` materialization from all paths.
- It does not yet thread sampled generation through every infer caller.
