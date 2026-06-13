# TCU-18 TensorCube Perf Guard Integration / Regression Router

## Status
PASS_TCU_18_TENSORCUBE_PERF_REGRESSION_ROUTED

## Sealed
- AshTensorCubePerfGuardMode
- AshTensorCubePerfMetricKind
- AshTensorCubePerfRegressionKind
- AshTensorCubePerfRegressionSeverity
- AshTensorCubePerfMetricSnapshot
- AshTensorCubePerfRegressionFactor
- AshTensorCubePerfRegressionDecision
- AshTensorCubePerfRegressionRouter
- AshTensorCubePerfGuardIntegrationReport
- AshTensorCubePerfGuardIntegrationConfig
- TensorCube perf metric snapshot
- TensorCube regression factor detection
- latency-only vs TensorCube regression separation
- regression router decision
- TCU-12 bridge integration

## Policy
- TensorCube metrics are first-class PerfGuard inputs
- Raw bridge missing blocks native perf readiness
- Runtime splice missing blocks native perf readiness
- CPU materialize is a blocking TensorCube regression
- Promotion failure is critical regression
- Splice determinism failure blocks apply candidate
- Latency-only regression is not mislabeled as TensorCube pressure
- PerfGuard integration does not mutate runtime state
- runtime pointer is not mutated
- LoRA attach/detach is not executed
- TensorCube/GPU buffer is not mutated
- no SFT/DPO training execution
- no Python validator

## Boundary
TCU-18 only integrates TensorCube metrics into PerfGuard and routes regressions.
TCU-19 handles TensorCube emergency demotion / safe tensor mode.
TCU-20 handles long-horizon TensorCube health ledger.
