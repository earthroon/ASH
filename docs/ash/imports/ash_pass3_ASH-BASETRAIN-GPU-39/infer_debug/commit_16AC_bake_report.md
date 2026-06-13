# Commit 16AC Bake Report

## Commit
Commit 16AC — Matmul Autotune / Grouped Attention Safe Path Seal

## SSOT
16AB proved that the headwise/raw/qkv bridge disable gate works, but the run still fails in the standard Burn/CubeCL matmul autotune path:

- `grouped_query_attention`
- `Tensor::matmul`
- `burn_cubecl_fusion::optim::matmul::tune::fused_matmul_autotune`
- `cubecl_runtime::tune::local::LocalTuner::execute`
- `No tile size is available for the problem` / `SHADER_INT64`

## Implemented

### Policy plumbing
Added request/payload fields:

- `disableNativeMatmulAutotune` / `disable_native_matmul_autotune`
- `disableNativeBurnFusion` / `disable_native_burn_fusion`
- `forceNativeSafeAttention` / `force_native_safe_attention`
- `forceNativeReferencePrefill` / `force_native_reference_prefill`

The fields are carried through:

- `orchestrator_local::infer_entry`
- `runtime::infer::StandardInferRequest`
- `runtime::infer::request_resolution::ResolvedStandardInferRequest`
- native aux probe metadata

### Safe-generation gate
After native WebGPU model load succeeds, if any 16AC guard is enabled, runtime skips cached native generation before it can enter `allocate_kv_cache`, `forward_prefill`, `grouped_query_attention`, or Burn/CubeCL matmul autotune.

The fallback uses `ReferenceModel::greedy_generate` / `greedy_generate_streaming` and emits:

```text
[16AC][safe-generation] cached_path_skipped=true reason=matmul_autotune_guard ...
```

The backend label is suffixed with:

```text
+16AC_reference_safe_generation
```

## Expected pass condition
The following stack should disappear when 16AC flags are true:

- `fused_matmul_autotune`
- `LocalTuner::execute`
- `model_core::model_layers::grouped_query_attention`
- `No tile size is available for the problem`
- `SHADER_INT64`

## Caveat
This is a safety seal, not a performance optimization. It intentionally bypasses native cached generation when the matmul autotune guard is enabled. 16Y atlas construction can still happen during native load, but token generation is routed to the CPU/reference path to avoid CubeCL autotune panic.

## Local validation status
Not compiled in bake container because `cargo` is unavailable here. Final SSOT is the user's local `cargo build -p native_host --bin native_host --release` and `run_16AC_stderr.txt`.
