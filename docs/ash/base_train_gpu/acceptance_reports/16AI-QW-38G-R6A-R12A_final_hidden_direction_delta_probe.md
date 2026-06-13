# Acceptance Report — 16AI-QW-38G-R6A-R12A

## Status
STATIC_BAKE_DONE_COMPILE_NOT_EXECUTED_IN_CONTAINER

## Acceptance Criteria Mapping

| criterion | static status |
|---|---|
| compile_pass | not executed in container |
| r12a_env_gate_exists | true |
| r12a_default_off | true |
| r12b_source_loaded | runtime checked |
| r12_source_loaded | runtime checked |
| r10_r2_source_loaded | runtime checked |
| target_token_id_confirmed | runtime checked |
| masked_top1_token_id_confirmed | runtime checked |
| pre_final_hidden_captured | runtime checked |
| post_final_hidden_captured | runtime checked |
| projection_input_hidden_captured | runtime checked |
| pre_final_hidden_norm_written | runtime checked |
| post_final_hidden_norm_written | runtime checked |
| projection_input_hidden_norm_written | runtime checked |
| pre_cosine_to_target_written | runtime checked |
| post_cosine_to_target_written | runtime checked |
| projection_cosine_to_target_written | runtime checked |
| pre_cosine_to_masked_written | runtime checked |
| post_cosine_to_masked_written | runtime checked |
| projection_cosine_to_masked_written | runtime checked |
| target_alignment_gain_written | runtime checked |
| masked_alignment_gain_written | runtime checked |
| target_minus_masked_delta_written | runtime checked |
| target_vs_neighbor_alignment_written | runtime checked |
| target_vs_normal_korean_alignment_written | runtime checked |
| adjudication_written | true by implementation |
| recommended_next_patch_written | true by implementation |
| trace_jsonl_written | runtime checked |
| summary_json_written | runtime checked |
| receipt_json_written | runtime checked |
| report_md_written | runtime checked |
| live_log_written | runner checked |
| root_cause_confirmed | false |
| mutation_performed | false |
| safetensors_modified | false |
| tokenizer_modified | false |
| lm_head_modified | false |
| final_norm_modified | false |
| ban_mask_modified | false |

## Run Command

```powershell
.\scripts\run_16AI_QW_38G_R6A_R12A_final_hidden_direction_delta_probe.ps1 -Build
```

## Notes
This acceptance report is static because the current bake container does not include Cargo/Rust. The local workstation run should produce the authoritative receipt:

`workspace/qw38g_r6a_r12a_final_hidden_direction_delta_receipt.json`
