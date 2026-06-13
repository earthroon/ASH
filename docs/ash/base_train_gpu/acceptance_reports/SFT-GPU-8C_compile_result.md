# SFT-GPU-8C Compile Result

## Status

NOT_RUN_IN_SANDBOX

## Reason

The sandbox used for baking does not provide `cargo` or `rustc`, so Rust compile validation could not be executed here.

## Local command

```powershell
cargo check -p lora_train
```

## Runtime smoke command

```powershell
cargo run -p lora_train --bin lora_train -- `
  .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.json 1
```

## Expected safe behavior for current direct_train smoke config

Until `atlas_grouped_native_hidden` is wired into the direct JSONL train loop, or a valid `dataset.feature_store_manifest` is provided, the run should fail before full checkpoint-backed teacher load:

```txt
[A-SFT][hidden_source_guard] A-SFT train phase forbids full checkpoint-backed teacher
```

This is intentional and prevents the OOM-prone fallback path.
