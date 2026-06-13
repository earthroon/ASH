# 16AI-QW-35B — KV Cache Cursor Trace / Decode Step Monotonic Seal

## Status
PASS_STATIC / PENDING_RUNTIME

## SSOT
- Patch scope: WebGPU native cached generation trace only
- Primary files:
  - `crates/model_core/src/decode_state.rs`
  - `crates/model_core/src/generation_sampling.rs`
- No model, safetensors, tokenizer, LoRA, banlist, or prompt default mutation.

## Implemented
- Added `prompt_len` to `KvCache` so decode steps can compare cursor movement against the original prompt boundary.
- Added env-gated trace surface:
  - `ASH_KV_TRACE=1`
  - `ASH_KV_TRACE_MAX_STEPS=8` default
  - `ASH_KV_TRACE_LAYERS=0,1,last` default
  - `ASH_KV_TRACE_STRICT=1` optional fail-closed mode
  - `ASH_KV_TRACE_JSONL=workspace/kv_trace_16AI_QW_35B.jsonl` default
- Added per-layer prefill trace.
- Added per-layer decode trace.
- Added final KV summary emission for cached generation paths.

## Trace fields
- phase: `prefill` or `decode`
- step
- layer
- input_len
- prompt_len
- generated_so_far
- past_len_before
- write_pos
- read_len
- expected_write_pos
- expected_read_len
- monotonic
- reused
- k_shape
- v_shape
- warnings

## Warning Codes
- `KV_SHAPE_MISMATCH`
- `KV_WRITE_POS_NOT_MONOTONIC`
- `KV_READ_LEN_BELOW_EXPECTED`
- `KV_SLOT_REUSED`
- `KV_PAST_LEN_FINAL_MISMATCH`

## Runtime command
```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$env:ASH_PROMPT_TEMPLATE="ash_dialogue_ko"
$env:ASH_KV_TRACE="1"
$env:ASH_KV_TRACE_MAX_STEPS="8"
$env:ASH_KV_TRACE_LAYERS="0,1,last"
$env:ASH_KV_TRACE_JSONL="workspace/kv_trace_16AI_QW_35B.jsonl"

cargo run --manifest-path ".\crates\runtime\Cargo.toml" --example infer_only -- `
  --model-spec ".\specs\model_spec_v5_48259.toml" `
  --tokenizer ".\artifacts\tokenizer_manifest_v5_final.json" `
  --checkpoint ".\tokenizer_v5\artifacts\full_model_vocab_v5_resized.safetensors" `
  --task freeform `
  --max-new-tokens 32 `
  --seed 42 `
  --text "1+1은?" `
  --json `
  1> ".\workspace\infer_qw35b_kv_trace_ash_dialogue_1plus1_stdout.json" `
  2> ".\workspace\infer_qw35b_kv_trace_ash_dialogue_1plus1_stderr.log"
```

## Runtime inspection
```powershell
Select-String -Path ".\workspace\infer_qw35b_kv_trace_ash_dialogue_1plus1_stderr.log" `
  -Pattern "16AI-QW-35B|kv_trace|kv_summary|KV_WRITE_POS|KV_READ_LEN|KV_SLOT|KV_SHAPE|output_text_preview|generated_tail_head" `
  -Context 0,2

Get-Content ".\workspace\kv_trace_16AI_QW_35B.jsonl" -Encoding UTF8 | Select-Object -First 60
```

## Decision matrix
- `monotonic=true`, no warnings: KV cursor is first-pass cleared; proceed to RoPE offset trace.
- `KV_WRITE_POS_NOT_MONOTONIC`: decode write position is not tracking past length; inspect cache append / sequence dim.
- `KV_READ_LEN_BELOW_EXPECTED`: cache grows incorrectly or read span does not include full context.
- `KV_SLOT_REUSED`: cache is likely overwriting a previous slot.
- `KV_SHAPE_MISMATCH`: K/V sequence axis does not match expected read length.

## Container validation
- `target/16AI-QW-35B_static_validation.json`: PASS_STATIC
- `cargo check`: NOT_RUN because cargo is not installed in the bake container.
