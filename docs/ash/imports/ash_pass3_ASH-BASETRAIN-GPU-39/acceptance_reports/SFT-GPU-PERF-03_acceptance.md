# SFT-GPU-PERF-03 — LM Head Vocab Tile Real Multi-Step Redispatch / Sharded AdamW State Seal

## Status

PASS_BAKED_STATIC_CONTRACT

## Applied changes

- `lm_head_vocab_atlas_gpu_multistep.rs`
  - Adds `lm_head_vocab_tile_step_receipts.jsonl` as the per-step redispatch receipt SSOT.
  - Adds `lm_head_vocab_tile_adamw_state_manifest.json` as the sharded AdamW state SSOT.
  - Extends multi-step reports with PERF-03 counters: pass1/reduce/pass2/update dispatch counts, synthetic-step forbidden seal, serial fallback forbidden seal, and sharded AdamW state seal.
  - Validates the final PERF-03 report before writing PASS state.

- `lm_head_vocab_atlas_gpu_adamw.rs`
  - Replaces full B optimizer state materialization with vocab-tile shard storage: `m_b_tiles` / `v_b_tiles`.
  - Adds tile-level checksum roots and state completeness reporting.
  - Adds manifest structure for global A state and B tile-local AdamW shards.

- `lm_head_vocab_atlas.rs`
  - Emits PERF-03 status and dispatch counters after the multi-step loop.

- configs
  - Enables `multi_step_train` for the GPU parallel vocab atlas smoke/train-from-features configs.
  - Keeps `projection=gpu_parallel_vocab_atlas` and `forbid_cpu_serial_tile_loop=true`.

- tests
  - Adds `gpu_parallel_vocab_atlas_real_multistep_redispatch.rs` static contract tests.

## Verification performed in this container

- JSON config validation: PASS
- Source contract grep: PASS
- Cargo build/test: NOT RUN, cargo is unavailable in this container.

## Local verification commands

```powershell
cargo test -p lora_train --test gpu_parallel_vocab_atlas_real_multistep_redispatch -- --nocapture
cargo test -p lora_train --test gpu_parallel_vocab_atlas_no_serial_fallback -- --nocapture
cargo run -p lora_train -- .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.json 1
```

## Expected PERF-03 log line

```txt
[lora_train][lm_head_vocab_atlas_perf03] status=PASS_REAL_GPU_REDISPATCH_SHARDED_ADAMW_STATE real_redispatch=true synthetic_forbidden=true sharded_adamw=true ...
```
