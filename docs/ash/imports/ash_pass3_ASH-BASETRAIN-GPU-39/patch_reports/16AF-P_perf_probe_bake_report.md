# 16AF-P Performance Probe Bake Report

## Status

```txt
16AF-P source bake = DONE
runtime validation = PENDING_LOCAL_RUN
generation_connected = false
```

## SSOT

```txt
Base = ash_pass3_commit16AF-M_multi_layer_parity_bake.zip
Prior runtime seal = 16AF-M3 all layers [0..13] Native Atlas FFN parity PASS
Scope = generation 연결 전 native FFN dispatch/readback/tile loop 병목 계측 + 최소 최적화
```

## Changed Files

```txt
crates/burn_webgpu_backend/src/native_atlas_ffn.rs
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/native_atlas_ffn_probe.rs
crates/model_core/src/bin/af16m_multi_layer_parity.rs
crates/model_core/src/bin/af16p_ffn_perf_probe.rs
scripts/run_16AF_P_ffn_perf_probe.ps1
scripts/run_16AF_P_ffn_perf_probe.sh
```

## Implemented

```txt
- Reusable NativeAtlasFfn16AfDispatcher now caches WGPU shader modules / bind group layout / compute pipelines.
- Multi-layer runners reuse one dispatcher across all layer probes instead of creating a WGPU device/pipeline per layer.
- Added NativeAtlasFfn16AfReadbackMode::OutputOnly.
- 16AF-P probe reads back only final FFN output for parity metrics, not gate/up/swiglu intermediates.
- Added per-layer telemetry:
  - readback_mode
  - readback_buffers
  - readback_elements
  - weight_upload_ms
  - bind_encode_ms
  - submit_readback_ms
  - total_gpu_ms
- Added dedicated af16p_ffn_perf_probe binary and scripts.
```

## Expected Performance Delta

```txt
Before 16AF-P parity readback per layer:
  gate + up + swiglu + out = 4 readback buffers
  elements = 5632 * 3 + 2048 = 18944 f32

After 16AF-P output-only parity readback per layer:
  out = 1 readback buffer
  elements = 2048 f32

Readback element reduction:
  18944 -> 2048
  about 89.19% fewer readback elements
```

## Locked Paths

```txt
generation_connected = false
attention native path = untouched
KV cache = untouched
sampling/hot token cache = untouched
```

## Local Validation Required

This container has no cargo/rustc runtime, so local cargo check and WGPU runtime validation remain pending.

```powershell
$ckpt = ".\tokenizer_v5\artifacts\full_model_vocab_v5_resized.safetensors"

cargo run --manifest-path crates/model_core/Cargo.toml --bin af16p_ffn_perf_probe -- `
  --spec "specs/model_spec_300m_dialogue_continue_gqa8_headwise_atlas.toml" `
  --checkpoint $ckpt `
  --all-layers `
  --threshold 0.001 `
  --top-k 8 `
  --fail-fast false
```
