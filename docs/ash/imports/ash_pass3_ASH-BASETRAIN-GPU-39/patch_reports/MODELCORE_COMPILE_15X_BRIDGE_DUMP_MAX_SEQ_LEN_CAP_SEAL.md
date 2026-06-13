# MODELCORE-COMPILE-15X — Bridge Dump Max Seq Len / Medium Profile Cap Seal

## Purpose

Apply an effective max sequence length cap to bridge dump token rows before compact teacher hidden generation.

## Changed Files

- crates/lora_train/src/config.rs
- crates/lora_train/src/bin/lora_train.rs
- configs/lora_v5_guarded_dump_smoke.json
- configs/lora_v5_guarded_dump_full.json
- configs/lora_v5_guarded_dump_medium.json

## Changes

- Added `bridge.max_seq_len` as an optional bridge dump cap.
- Resolved effective cap from `bridge.max_seq_len`, falling back to `dataset.max_seq_len`.
- Applied truncation before compact teacher forward and staging append.
- Preserved next-token target alignment by capping input tokens to `max_seq_len + 1`.
- Preserved EOS at the truncated end when EOS was enabled and present.
- Clamped prompt length after truncation.
- Added `max_seq_len_cap` and `[bridge-cap]` diagnostics.
- Added medium profile config with 128 rows and bridge max seq len 192.

## Non-Goals

- No compact GPU kernel changes.
- No feature shard schema changes.
- No full checkpoint GPU loading.
- No tokenizer path changes.

## Validation

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_15X_lora_train_check.log"
$env:ASH_LORA_COMPACT_GPU_TEACHER="1"
cargo run --manifest-path ".\crates\lora_train\Cargo.toml" --bin lora_train -- ".\configs\lora_v5_guarded_dump_medium.json" 6 2>&1 | Tee-Object ".\target\LORA_DUMP_MEDIUM_15X_seq_cap.log"
```

Expected patterns:

```text
max_seq_len_cap=192
[bridge-cap]
feature store dumped
max_seq_len=192
```
