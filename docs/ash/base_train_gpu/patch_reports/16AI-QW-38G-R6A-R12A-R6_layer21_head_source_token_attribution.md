# 16AI-QW-38G-R6A-R12A-R6 — Layer21 Head Source Token Attribution / Head2 Position-Origin Seal

## Status
STATIC_VALIDATION_PASS

## Source
- source_patch: 16AI-QW-38G-R6A-R12A-R5
- source_status_required: PASS_LAYER21_ATTENTION_HEAD_ATTRIBUTION
- source_adjudication_required: LAYER21_ATTENTION_SINGLE_HEAD_CANDIDATE_IDENTIFIED

## Purpose
R6 resolves the `source_token_id` / `source_token_piece` null gap left by R5 for layer 21 head 2 attribution. It maps source positions 20 and 55 back to prompt token ids, enriches those ids with tokenizer manifest vocab pieces, then separates attention-probability dominance from value-direction contribution.

## Implemented Changes
- Added R6 env gate and raw trace path support in `native_wgpu.rs`.
- Extended R5 attention-head capture with optional source token ids.
- Passed `prompt_ids` into prefill layer attention capture from `decode_state.rs`.
- Ensured R6 compare positions `20,55` are included even when they are not in the R5 top attention list.
- Added R6 runner that:
  - validates R5 PASS / single-head candidate source receipt,
  - runs the runtime infer example with R6 env gates,
  - loads tokenizer manifest vocab to restore token pieces,
  - writes position 20 and position 55 probes,
  - writes attention-probability vs value-contribution split,
  - writes source origin candidate and guard receipts.

## Output Artifacts
- `workspace/qw38g_r6a_r12a_r6_layer21_head_source_token_attribution_trace.jsonl`
- `workspace/qw38g_r6a_r12a_r6_layer21_head_source_token_attribution_summary.json`
- `workspace/qw38g_r6a_r12a_r6_layer21_head_source_token_attribution_receipt.json`
- `workspace/qw38g_r6a_r12a_r6_layer21_head_source_token_attribution_report.md`
- `workspace/qw38g_r6a_r12a_r6_head2_source_position_scoreboard.json`
- `workspace/qw38g_r6a_r12a_r6_head2_position20_probe.json`
- `workspace/qw38g_r6a_r12a_r6_head2_position55_probe.json`
- `workspace/qw38g_r6a_r12a_r6_source_token_piece_map.json`
- `workspace/qw38g_r6a_r12a_r6_head2_source_origin_candidate.json`
- `workspace/qw38g_r6a_r12a_r6_attention_prob_vs_value_contribution_split.json`

## Guard
- mutation_performed: false
- tokenizer_modified: false
- safetensors_modified: false
- lm_head_modified: false
- final_norm_modified: false
- ban_mask_modified: false

## Local Execution
```powershell
.\scripts\run_16AI_QW_38G_R6A_R12A_R6_layer21_head_source_token_attribution.ps1 -Build
```

## Container Note
The container used for baking does not provide the Windows runtime/GPU environment required for execution. Static validation was performed only.
