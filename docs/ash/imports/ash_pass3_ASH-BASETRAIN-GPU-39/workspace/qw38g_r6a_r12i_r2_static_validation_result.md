# 16AI-QW-38G-R6A-R12A-R12I-R2 Static Validation

- Status: PASS_STATIC_VALIDATION
- Script: scripts/run_16AI_QW_38G_R6A_R12A_R12I_R2_capture_input_row_wiring.ps1
- SHA256: cb15083c5e21e846d57641b8714233b4b72a259719d0b107d4133f847f2366fd
- Capture input output: workspace/qw38g_r6a_r12i_metric_capture_input.json
- Partial rows: supported via -AllowPartialRows
- Fixture mode: opt-in only via -AllowFixtureRows; not production/effect evidence
- Mock positive: forbidden by default
- Mutation safety flags: checkpoint/tokenizer/safetensors/lm_head/final_norm/ban_mask remain false

## Recommended local execution

```powershell
.\scripts\run_16AI_QW_38G_R6A_R12A_R12I_R2_capture_input_row_wiring.ps1 -Build -Strict -TargetLikeCount 3 -NegativeControlCount 3 -AllowPartialRows
```
