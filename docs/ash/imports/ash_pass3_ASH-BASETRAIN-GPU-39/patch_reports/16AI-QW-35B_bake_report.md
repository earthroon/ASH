# 16AI-QW-35B Bake Report

## Baked Target
`16AI-QW-35B — KV Cache Cursor Trace / Decode Step Monotonic Seal`

## Result
PASS_STATIC / PENDING_LOCAL_CARGO_CHECK_AND_RUNTIME

## Files changed
- `crates/model_core/src/decode_state.rs`
- `crates/model_core/src/generation_sampling.rs`

## Files added
- `acceptance_reports/16AI-QW-35B_kv_cache_cursor_trace.md`
- `patch_reports/16AI-QW-35B_decode_state.diff`
- `patch_reports/16AI-QW-35B_generation_sampling.diff`
- `patch_reports/16AI-QW-35B_bake_report.md`
- `target/16AI-QW-35B_static_validation.json`

## Implementation summary
- Added env-gated KV cursor trace helpers.
- Added prefill layer trace after K/V cache creation.
- Added decode layer trace after K/V cache append.
- Added final KV summary in cached generation paths.
- Preserved default behavior when `ASH_KV_TRACE` is unset.

## Guardrails
- No safetensors mutation.
- No tokenizer mutation.
- No banlist mutation.
- No LoRA mutation.
- No prompt default mutation.
- No shader fix applied in this patch.

## Local required checks
```powershell
cargo check -p model_core 2>&1 | Tee-Object ".\target\16AI-QW-35B_model_core_check.log"
cargo check -p runtime 2>&1 | Tee-Object ".\target\16AI-QW-35B_runtime_check.log"
```

## Runtime required check
See `acceptance_reports/16AI-QW-35B_kv_cache_cursor_trace.md`.
