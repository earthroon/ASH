# 16AI-QW-38G-R6A-R12A-R12I-R2-R1 Static Validation

- Status: PASS_STATIC_VALIDATION
- Script: scripts/run_16AI_QW_38G_R6A_R12A_R12I_R2_R1_runtime_capture_raw_hook.ps1
- SHA256: b590c8c8d61e31020dd457c0ab02c86d17f21bcb25438d1fcae6879efd7d8006
- Source required status: PARTIAL_CAPTURE_INPUT_ROW_WIRING
- Runtime raw output: workspace/qw38g_r6a_r12i_r2_runtime_capture_raw.json
- Partial raw: supported via -AllowPartialRaw
- Fixture mode: false by default
- Mock positive: forbidden
- Mutation safety flags: checkpoint/tokenizer/safetensors/lm_head/final_norm/ban_mask remain false

## Recommended local execution

PowerShell:

.\scripts\run_16AI_QW_38G_R6A_R12A_R12I_R2_R1_runtime_capture_raw_hook.ps1 -Build -Strict -TargetLikeCount 3 -NegativeControlCount 3 -AllowPartialRaw
