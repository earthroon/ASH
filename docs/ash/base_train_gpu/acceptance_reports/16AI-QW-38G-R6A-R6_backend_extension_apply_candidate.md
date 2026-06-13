# 16AI-QW-38G-R6A-R6 — Backend Extension Apply Candidate / Guarded Variant Construction Seal

## Status
PENDING_RUNTIME

## SSOT
- Source approval: `workspace/qw38g_r6a_r5_operator_review_receipt.json`
- Source review packet: `workspace/qw38g_r6a_r5_operator_review_packet.json`
- Source dry-run: `workspace/qw38g_r6a_r4_backend_extension_dry_run.json`
- Source spec: `workspace/qw38g_r6a_r3_backend_debug_binding_extension_spec.json`
- Output candidate: `workspace/qw38g_r6a_r6_apply_candidate.json`
- Output receipt: `workspace/qw38g_r6a_r6_apply_candidate_receipt.json`

## Guarded construction scope
- Consumes R5 operator approval receipt.
- Validates R3 spec and R4 dry-run sources.
- Constructs debug shader variant, debug cache key, debug bind group layout, and debug buffer binding candidates.
- Does not execute shader write.
- Does not mutate pipeline layout, bind group layout, bind group, pipeline cache, or generation output.

## Acceptance
- `approval_valid_for_r6 = true`
- `spec_loaded = true`
- `dry_run_loaded = true`
- `apply_candidate_ready = true`
- `debug_variant_constructed = true`
- `debug_cache_key_constructed = true`
- `debug_bind_group_layout_constructed = true`
- `debug_buffer_binding_candidate_constructed = true`
- `normal_pipeline_unchanged = true`
- `normal_bind_group_layout_unchanged = true`
- `mutation_guard_passed = true`
- `apply_executed = false`
- `rollback_plan_written = true`

## Next
`16AI-QW-38G-R6A-R7 — Backend Extension Apply Sandbox / Debug Variant Smoke Seal`
