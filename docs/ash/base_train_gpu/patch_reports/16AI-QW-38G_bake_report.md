# 16AI-QW-38G Bake Report

## Patch
`16AI-QW-38G — Reserved Direction Hidden Activation Source Trace / Layerwise Residual Seal`

## Base
`ash_pass3_16AI-QW-38D_hidden_projection_baked.zip`

## Changed Files
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38G_layerwise_reserved_direction.ps1`
- `scripts/summarize_16AI_QW_38G_layerwise_reserved_direction.py`
- `acceptance_reports/16AI-QW-38G_layerwise_reserved_direction_trace.md`
- `patch_reports/16AI-QW-38G_bake_report.md`
- `patch_reports/16AI-QW-38G_native_wgpu.diff`
- `target/16AI-QW-38G_static_validation.json`

## Implementation Notes
- Adds env-gated layerwise reserved-direction tracing under `ASH_LAYERWISE_RESERVED_TRACE=1`.
- Traces selected stages: embedding, post-attention residual, post-MLP residual, and post-final-norm by default.
- Compares target token `13` against fixed normal/reference token IDs through dot/cosine projection using the lm_head vocab atlas rows.
- Emits `[16AI-QW-38G][layer_trace]` stderr lines and JSONL records.
- Adds a PowerShell runner with stable `Start-Process` execution and a Python summarizer.

## Non-Mutation Seal
- No checkpoint mutation.
- No safetensors mutation.
- No tokenizer mutation.
- No banlist mutation.
- No prompt default change.
- No LoRA mutation.

## Validation
- Static validation: `PASS_STATIC`
- Cargo check: `NOT_RUN_CONTAINER_CARGO_UNAVAILABLE`
