# 16AI-QW-38G-R6A-R1 — Pipeline Layout Registry Exposure / Bind Group Audit Seal

## Status
PENDING_RUNTIME

## SSOT
- Base patch: 16AI-QW-38G-R6A-R1 runner stability baked state
- Runtime target: base-only / no LoRA / ash_dialogue_ko
- Purpose: audit-only discovery of WebGPU pipeline/layout/bind-group ownership

## Acceptance Targets
- `ASH_PIPELINE_LAYOUT_AUDIT=1` env gate exists.
- Audit is default-off and dry-run only.
- Runtime writes `workspace/qw38g_r6a_r1_pipeline_layout_audit.json`.
- Runtime writes `workspace/qw38g_r6a_r1_runtime_receipt.json`.
- Shader write, debug buffer binding mutation, pipeline layout mutation, and bind group mutation are not performed.
- Owner discovery explicitly reports whether shader module, compute pipeline, pipeline layout, bind group layout, bind group, and cache key owners are visible.
- Recommended next patch is recorded.

## Expected Initial Runtime Decision
Current hot path is expected to report backend abstraction boundary, because R6A already showed no direct bind group layout surface from `NativeWgpuModel::project_last_hidden_to_logits_vocab_atlas`.

Expected status:
`PASS_PIPELINE_LAYOUT_AUDIT_BACKEND_PATCH_REQUIRED`

Expected recommended next patch:
`16AI-QW-38G-R6A-R2_BURN_WGPU_PIPELINE_LAYOUT_OWNER_AUDIT`
