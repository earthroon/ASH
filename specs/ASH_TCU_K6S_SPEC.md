# ASH TCU K6S

Apply monitor, rollback probe, bound route health, and CLI echo consistency after K6R bound apply.

Required K6R PASS_BOUND with apply_gate_executed true, route_binding_performed true, candidate_default_enabled true, runtime_splice_open true, and production_replacement_open false.

Monitors the explicitly bound K6P GPU row-major emit TensorCube candidate route, rechecks correctness and timing across monitor rounds, probes rollback readiness without executing rollback, checks fallback route readiness, records CLI echo consistency, and confirms post-probe route state.

Does not silently rollback, silently adopt, overwrite production GEMM, or claim external performance.

PASS PASS_ASH_TCU_K6S_APPLY_MONITOR_ROLLBACK_PROBE_NO_PRODUCTION_REPLACEMENT_SEAL.
