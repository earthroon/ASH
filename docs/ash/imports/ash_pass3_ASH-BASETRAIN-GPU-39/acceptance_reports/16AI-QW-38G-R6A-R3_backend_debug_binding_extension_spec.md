# 16AI-QW-38G-R6A-R3 — Backend Debug Binding Extension Spec / No-Apply Design Seal

## Status
PENDING_RUNTIME

## SSOT
- Backend patch is required by 16AI-QW-38G-R6A-R2.
- This patch is no-apply design only.
- It must not mutate shader source, pipeline layout, bind group layout, pipeline cache key, tokenizer, safetensors, banlist, or generation output.

## Expected Runtime Artifacts
- `workspace/qw38g_r6a_r3_backend_debug_binding_extension_spec.json`
- `workspace/qw38g_r6a_r3_backend_debug_binding_design_receipt.json`
- `workspace/infer_qw38g_r6a_r3_backend_debug_binding_spec_live.log`

## Acceptance
| criterion | expected |
|---|---:|
| backend_debug_binding_spec_env_gate_exists | true |
| backend_debug_binding_spec_default_off | true |
| no_apply_required | true |
| debug_shader_variant_policy_written | true |
| pipeline_cache_key_policy_written | true |
| bind_group_layout_policy_written | true |
| debug_buffer_policy_written | true |
| safety_policy_written | true |
| shader_write_performed | false |
| pipeline_layout_mutation_performed | false |
| bind_group_mutation_performed | false |
| generation_output_mutation_performed | false |
| spec_json_written | true |
| receipt_json_written | true |

## Decision
Runtime should close as `PASS_NO_APPLY_DESIGN_SEAL` and recommend `16AI-QW-38G-R6A-R4_BACKEND_EXTENSION_APPLY_DRY_RUN`.
