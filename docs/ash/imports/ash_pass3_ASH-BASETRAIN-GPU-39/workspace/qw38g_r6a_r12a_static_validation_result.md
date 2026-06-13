# 16AI-QW-38G-R6A-R12A Static Validation

Status: STATIC_BAKE_DONE_COMPILE_NOT_EXECUTED_IN_CONTAINER

```json
{
  "patch_id": "16AI-QW-38G-R6A-R12A",
  "patch_name": "Final Hidden Direction Delta Probe / Target Attractor Vector Alignment Seal",
  "status": "STATIC_BAKE_DONE_COMPILE_NOT_EXECUTED_IN_CONTAINER",
  "compile_pass": "not_executed_cargo_missing_in_container",
  "checks": {
    "r12a_env_gate_exists": true,
    "r12a_default_off": true,
    "pre_final_capture_hook_exists": true,
    "post_final_capture_hook_exists": true,
    "projection_probe_call_exists": true,
    "trace_jsonl_written": true,
    "summary_json_written": true,
    "receipt_json_written": true,
    "report_md_written": true,
    "runner_exists": true,
    "runner_sets_env_gate": true,
    "mutation_forbidden_flags_cleared": true,
    "root_cause_not_confirmed": true,
    "safetensors_not_modified_marker": true,
    "tokenizer_not_modified_marker": true,
    "lm_head_not_modified_marker": true,
    "final_norm_not_modified_marker": true,
    "ban_mask_not_modified_marker": true
  },
  "recommended_local_command": ".\\scripts\\run_16AI_QW_38G_R6A_R12A_final_hidden_direction_delta_probe.ps1 -Build",
  "mutation_performed": false,
  "safetensors_modified": false,
  "tokenizer_modified": false,
  "lm_head_modified": false,
  "final_norm_modified": false,
  "ban_mask_modified": false,
  "root_cause_confirmed": false
}
```
