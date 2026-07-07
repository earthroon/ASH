# ASH TCU K6ZL

Limited canary runtime monitor after K6ZK.

Required K6ZK PASS with explicit operator canary approval accepted, limited_canary_bind_executed true, canary_lane_state_changed true, canary_bind_ledger_written true, canary_scope candidate_lane_only, valid canary identity, valid bind ledger, valid canary lane state transition, valid scope guard, valid production replacement guard, valid rollback plan bind packet, valid post-bind probe, and no production replacement, global default route change, broad rollout, rollback execution, or external performance claim.

Monitors the limited candidate-lane canary after bind. Executes limited canary runtime health window, post-bind replay probe, diff stability probe, timing stability probe, canary scope isolation probe, fallback readiness probe, rollback rehearsal, production replacement block, and runtime monitor verdict.

Does not expand canary, replace production GEMM, change global default route, broaden rollout, execute rollback, or claim external performance.

PASS PASS_ASH_TCU_K6ZL_LIMITED_CANARY_RUNTIME_MONITOR_NO_PRODUCTION_REPLACEMENT_SEAL.
