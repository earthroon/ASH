# 16AI-QW-35E — Base-only vs LoRA Semantic Split Bake Report

## Status
BAKED_STATIC / PENDING_RUNTIME

## Changed Files
- `crates/runtime/src/infer.rs`
- `scripts/run_16AI_QW_35E_semantic_split.ps1`
- `scripts/compare_16AI_QW_35E_semantic_split.ps1`
- `acceptance_reports/16AI-QW-35E_base_only_vs_lora_semantic_split.md`
- `patch_reports/16AI-QW-35E_bake_report.md`
- `patch_reports/16AI-QW-35E_infer_rs.diff`
- `target/16AI-QW-35E_static_validation.json`

## Implemented Runtime Gate
`ASH_FORCE_NO_LORA=1` now forces base-only inference by:

1. Skipping requested LoRA JSON load.
2. Clearing `decision.selected_lora_ids` if policy selected any.
3. Logging selected/loaded/attached LoRA counts through `[16AI-QW-35E][semantic_split]`.

## Runner
`run_16AI_QW_35E_semantic_split.ps1` runs:

1. Base-only with `ASH_FORCE_NO_LORA=1`.
2. LoRA-attached if `-LoraJson` is supplied.
3. The compare script to write `workspace/compare_qw35e_base_vs_lora_semantic_split.json`.

## Compare Script
`compare_16AI_QW_35E_semantic_split.ps1` extracts:

- `resolved_backend`
- `prompt_template_id`
- `selected_lora_ids`
- `loaded_loras`
- `attached_loras`
- `generated_tail_head`
- `output_text_preview`
- arithmetic pass / word-salad heuristic
- decision and recommended next patch

## Not Changed
- Base checkpoint
- Safetensors
- Tokenizer manifest/vocab
- Banlist
- Prompt template default
- KV cache implementation
- RoPE implementation
- Attention mask implementation
- Output guard policy

## Operator Note Incorporated
The operator identified three deeper runtime probes that remain relevant if base and LoRA both fail:

1. RoPE position ID monotonicity.
2. KV cache sequence dimension growth.
3. Attention softmax weights after causal mask.

35E records this as next-trace guidance only. It does not alter those runtime mechanics.

## Validation
Static validation: see `target/16AI-QW-35E_static_validation.json`.
Cargo validation: not run in the bake container.
