# 16AI-QW-38G-R6A-R12A-R1 — Final Hidden Trace Capture Expansion / Forward Path Hook Coverage Seal

## Status
STATIC_BAKE_DONE_COMPILE_NOT_EXECUTED_IN_CONTAINER

## SSOT
- source_patch: 16AI-QW-38G-R6A-R12A
- source_status: FAIL_FINAL_HIDDEN_DIRECTION_CAPTURE_INCOMPLETE
- target_id: 13
- masked_top1_id: 373
- root_cause_confirmed: false
- mutation_performed: false

## Acceptance Surface
- Added R12A-R1 env gate: `ASH_QW38G_R6A_R12A_R1_TRACE_CAPTURE_EXPANSION`.
- Extended R12A capture enablement so R12A-R1 can drive the existing hidden-direction probe without requiring the old R12A env name.
- Installed direct pre/post hooks in `NativeWgpuModel::final_norm_for_decode()`.
- Preserved existing hooks in `forward_hidden_for_generation_input()`.
- Added R12A-R1 route coverage wrapper and dedicated artifacts.
- Added PowerShell runner for local compile/run.

## Guard
- No lm_head mutation.
- No final_norm weight mutation.
- No tokenizer mutation.
- No safetensors mutation.
- No ban mask mutation.
- Missing capture is reported as route miss, not silently filled.
