# SFT-GPU-PERF-02 — LM Head Vocab Tile Parallel Output Handoff / No Serial Fallback Seal

## SSOT

- `lm_head_vocab_atlas.projection = gpu_parallel_vocab_atlas`
- `lm_head_vocab_atlas.forbid_cpu_serial_tile_loop = true`
- GPU parallel branch owns bridge → pass1 → reduce → pass2 grad → update → export → runtime delta → output handoff.

## Applied changes

- Added GPU parallel output handoff from `GpuLmHeadVocabAtlasBridge` back into `GpuLmHeadLoraSmokeOutput`.
- Removed staged `bail!` stop after runtime delta / multistep / promotion milestones when the GPU parallel route has already produced a valid adapter.
- Added hard guard so `gpu_parallel_vocab_atlas` cannot fall through into the legacy CPU serial tile loop when `forbid_cpu_serial_tile_loop=true`.
- Enabled `gpu_parallel_vocab_atlas` in `configs/ash_ko_short_sft_lm_head_lora_v1_smoke.json` with smoke-safe `multi_step_train.enabled=false` and `quality_eval.enabled=false`.
- Added regression test `gpu_parallel_vocab_atlas_no_serial_fallback.rs` to lock the output handoff and no-serial-fallback contract.

## Expected runtime signature

```text
[lora_train][runtime_delta_verify] PASS_RUNTIME_DELTA_VERIFY
[lora_train][lm_head_vocab_atlas_gpu_parallel] PASS_NO_SERIAL_FALLBACK_OUTPUT_HANDOFF ...
```

If the GPU parallel branch fails to return a handoff and attempts to enter the serial fallback path, the run must fail with:

```text
SFT-GPU-PERF-02 gpu_parallel_vocab_atlas exited without GPU output handoff; CPU serial tile loop fallback is forbidden
```

## Validation commands

```powershell
cargo test -p lora_train --test gpu_parallel_vocab_atlas_no_serial_fallback -- --nocapture
cargo run -p lora_train -- .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.json 1
```

## Judgment

This patch does not claim final throughput victory. It closes the unfinished structural gap first: GPU vocab tile parallel work must either return a proper train artifact handoff or fail loudly, never silently fall back to the host serial tile loop.
