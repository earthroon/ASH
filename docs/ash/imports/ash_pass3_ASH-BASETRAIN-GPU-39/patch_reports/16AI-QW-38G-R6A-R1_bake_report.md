# 16AI-QW-38G-R6A-R1 Bake Report

## Patch
16AI-QW-38G-R6A-R1 — Pipeline Layout Registry Exposure / Bind Group Audit Seal

## Base
`ash_pass3_16AI-QW-38G-R6A-R1_runner_stability_baked.zip`

## Changed Files
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38G_R6A_R1_pipeline_layout_audit.ps1`
- `acceptance_reports/16AI-QW-38G-R6A-R1_pipeline_layout_registry_exposure.md`
- `target/16AI-QW-38G-R6A-R1_static_validation.json`

## Implementation Summary
- Added `ASH_PIPELINE_LAYOUT_AUDIT` gated audit path.
- Added fail-closed audit/receipt writers.
- Added owner discovery events for shader module, compute pipeline, pipeline layout, bind group layout, bind group, cache key, and dead-path layer-loop candidate.
- Added invocation from the active vocab-atlas projection hot path.
- Added dedicated PowerShell runner with Start-Process build stability and direct live infer logging.

## Safety
- No weight mutation.
- No tokenizer mutation.
- No safetensors mutation.
- No banlist mutation.
- No shader write.
- No pipeline layout or bind group mutation.
- Audit is dry-run only.

## Runtime Files
- `workspace/qw38g_r6a_r1_pipeline_layout_audit.json`
- `workspace/qw38g_r6a_r1_runtime_receipt.json`
- `workspace/infer_qw38g_r6a_r1_pipeline_layout_live.log`
