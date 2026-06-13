# ASH-45C SFT Outcome Metric Priority Resolver

## Status
PASS_ASH_45C_SFT_OUTCOME_METRIC_PRIORITY_RESOLVER

## Sealed
- AshSftOutcomeMetricPriorityMode
- AshEventTagMetricPriorityRule
- AshResolvedSftOutcomeMetricSignal
- event-tag metric priority table
- deterministic metric resolution
- metric order invariance check
- fallback warning path
- safety-aware conservative metric resolution
- report/profile metric counts

## Policy
- `metric_scores[0]` / implicit first-delta selection is forbidden.
- Event tag priority decides the selected SFT outcome metric.
- Metric array order must not change selected metric or delta.
- TelemetryContractRepair prioritizes TelemetryContract before HoldoutQuality.
- HardNegativeAvoidance prioritizes HardNegativeReplay before HoldoutQuality.
- LatencyPressure prioritizes LatencyPerf before generic quality.
- Manual review / telemetry safety flags force conservative metric resolution context.
- Fallback metric resolution cannot remain strong-confidence.
- Runtime router config is not mutated.
- Current pointer is not changed.
- No LoRA attach/detach.
- No Python validator.

## Boundary
ASH-45C only resolves SFT outcome metric priority and writes metric trace into calibration evidence.
ASH-45D handles LoRA artifact lineage binding.
ASH-45E handles calibration snapshot consistency.
ASH-45F handles deterministic replay seal.
