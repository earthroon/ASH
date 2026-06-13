# Acceptance — 16AI-QW-38G-R6A-R12A-R5

## Required Local Command

```powershell
.\scripts\run_16AI_QW_38G_R6A_R12A_R5_layer21_attention_head_attribution.ps1 -Build
```

## Expected Artifacts
- `workspace/qw38g_r6a_r12a_r5_layer21_attention_head_attribution_trace.jsonl`
- `workspace/qw38g_r6a_r12a_r5_layer21_attention_head_attribution_summary.json`
- `workspace/qw38g_r6a_r12a_r5_layer21_attention_head_attribution_receipt.json`
- `workspace/qw38g_r6a_r12a_r5_layer21_attention_head_attribution_report.md`
- `workspace/qw38g_r6a_r12a_r5_head_scoreboard.json`
- `workspace/qw38g_r6a_r12a_r5_position_scoreboard.json`
- `workspace/qw38g_r6a_r12a_r5_head_position_matrix.json`
- `workspace/qw38g_r6a_r12a_r5_top_head_candidate.json`
- `workspace/qw38g_r6a_r12a_r5_attention_source_token_candidates.json`

## Acceptance Criteria
- R4 source receipt is loaded and must be `PASS_LAYER_COMPONENT_ATTRIBUTION`.
- R4 adjudication must be `LAYER21_ATTENTION_DOMINANT_MARGIN_JUMP`.
- R5 env gate remains default-off and activates only in the runner.
- Layer 21 head events are written.
- Head, position, and head-position matrix scoreboards are written.
- Top head and top source-position candidates are written.
- Root cause remains unconfirmed.
- No tokenizer/safetensors/lm_head/final_norm/ban-mask mutation is performed.
