# ASH TCU K6ZI

Apply monitor rollback probe after K6ZH.

Required K6ZH PASS with matrix_candidate_apply_executed true, route_state_changed_to_candidate_apply_lane true, apply_ledger_written true, receipt-bound candidate apply lane scope, candidate route identity valid, no silent adoption, no production replacement, no production route change, no global default route change, no broad rollout state change, rollback readiness bound, and no rollback execution.

Monitors the receipt-bound candidate apply lane after explicit matrix apply. Executes candidate lane health window, post-apply replay probe, post-apply diff stability, post-apply timing stability, rollback dry rehearsal, fallback route switch probe, production route isolation guard, and candidate lane revert plan packet.

Does not replace production GEMM, change global default route, broaden rollout, execute rollback, or claim external performance.

PASS PASS_ASH_TCU_K6ZI_APPLY_MONITOR_ROLLBACK_PROBE_NO_PRODUCTION_REPLACEMENT_SEAL.
