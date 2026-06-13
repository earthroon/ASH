# 16AI-QW-38G-R2 — Live Heartbeat & Hook Reachability / Fail-Closed Receipt Seal

## Status
PENDING_RUNTIME / PASS_HEARTBEAT / FAIL_LAYERWISE_HOOK_NOT_REACHED

## SSOT
- Base patch: 16AI-QW-38G-R1
- Previous failure: generation completed, but no `[16AI-QW-38G]` prefix logs, no layerwise trace JSONL, no summary, no receipt.
- R2 target: runtime infer entry must emit heartbeat and write receipt regardless of layerwise hook success.

## Runtime Contract
- `ASH_LAYERWISE_RESERVED_TRACE=1` or `ASH_QW38G_R2_HEARTBEAT=1` enables R2 heartbeat.
- Runtime writes `workspace/qw38g_runtime_receipt.json` during start/env/model/prompt/generation/final stages.
- Final receipt is written even when layerwise trace hook is not reached.
- PowerShell runner uses release exe and live console output instead of silent stdout/stderr-only redirect.

## Acceptance
| criterion | expected |
|---|---|
| console heartbeat visible | true |
| `[16AI-QW-38G-R2][start]` visible | true |
| `[16AI-QW-38G-R2][env]` visible | true |
| `[16AI-QW-38G-R2][generation_start]` visible | true |
| `qw38g_runtime_receipt.json` written | true |
| missing layer trace still produces receipt | true |
| python postprocess required | false |
| weight mutation | false |
| tokenizer mutation | false |
| safetensors mutation | false |
| banlist mutation | false |

## Decision Matrix
- `PASS_RUNTIME_TRACE`: layerwise trace and summary exist.
- `FAIL_SUMMARY_NOT_WRITTEN`: layerwise trace exists, summary missing.
- `FAIL_LAYERWISE_HOOK_NOT_REACHED`: inference completed but layer trace missing.
- If no R2 prefix appears, the running binary is stale or R2 patch did not compile into the executed exe.
