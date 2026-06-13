# ASH-33 Runtime Composite Latency / Memory Guard

## Status
PASS_RUNTIME_COMPOSITE_LATENCY_MEMORY_GUARD

## Sealed
- AshRuntimeCompositePerfGuardMode
- AshRuntimeCompositePerfDecision
- AshRuntimeCompositePerfSeverity
- AshRuntimeCompositePerfObservedMetrics
- AshRuntimeCompositePerfThresholds
- AshRuntimeCompositePerfGuardConfig
- AshRuntimeCompositePerfMetricCheck
- AshRuntimeCompositeCompressionRecommendation
- AshRuntimeCompositePerfGateEvidence
- AshRuntimeCompositePerfGuardReport
- latency threshold evaluation
- memory threshold evaluation
- compression recommendation
- rollback review recommendation
- runtime perf observer contract

## Policy
- ASH-33 does not change current pointer.
- ASH-33 does not mutate artifact registry.
- ASH-33 does not run ASH-31 compression.
- ASH-33 does not run runtime inference from ash_core.
- Missing metrics are represented as None and are not zero-filled.
- Latency hard limit can block promotion.
- Memory hard limit can block promotion.
- Critical current pressure recommends rollback review only.
- Compression recommendation does not execute ASH-31.
- No Python validator.

## Boundary
ash_core computes guard decisions.
runtime emits observed metrics.
orchestrator_local reports guard evidence.
artifact_store preserves perf guard snapshots.
