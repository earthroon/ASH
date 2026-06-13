# QW-54G Acceptance Report

## Status

`PATCH_IMPLEMENTED_PENDING_LOCAL_CARGO_RUNTIME_CHECK`

## Files changed

- `crates/model_core/src/qw54g_closed_attractor_set_breaker.rs`
- `crates/model_core/src/generation_sampling.rs`
- `crates/model_core/src/lib.rs`
- `crates/runtime/examples/infer_only.rs`
- `specs/runtime_profile.toml`
- `specs/QW-54G_closed_attractor_set_breaker_spec.md`
- `docs/roadmap/QW-54G_closed_attractor_set_breaker.md`
- `scripts/run_qw54g_closed_attractor_vulkan.cmd`

## Validation commands

```powershell
cargo check -p model_core --lib
cargo check -p runtime --all-targets
```

## Runtime check

```powershell
$env:WGPU_BACKEND="vulkan"
$env:ASH_QW54F_ENABLE="1"
$env:ASH_QW54F_TRACE="1"
$env:ASH_QW54G_ENABLE="1"
$env:ASH_QW54G_TRACE="1"
.\target\release\examples\infer_only.exe --runtime-profile .\specs\runtime_profile.toml --task subtitle_polish --text "I thought you were going to leave me behind." --max-new-tokens 160 --seed 42 --enable-qw54g --qw54g-trace --json
```

## Expected artifacts

- `workspace/runtime_traces/qw54g_closed_attractor_set_breaker_trace.jsonl`
- `workspace/trace/qw54g_closed_attractor_set_breaker_receipt.json`
- `artifacts/qw54g_closed_attractor_set_breaker_report.json`

## Acceptance notes

The implementation is intentionally runtime-only and finite-delta only. It does not add token bans, token masks, vocabulary removals, model weight mutation, LoRA mutation, or sampler default mutation.
