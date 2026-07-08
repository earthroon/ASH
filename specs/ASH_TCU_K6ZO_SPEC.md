# ASH TCU K6ZO

Limited expanded canary runtime monitor after K6ZN.

Required prior PASS: ASH-TCU-K6ZN with explicit operator expansion approval accepted, limited canary expansion executed, canary scope changed, expansion ledger written, previous scope candidate_lane_only, new scope limited_candidate_lane_expanded, valid expansion identity, valid expansion ledger, valid scope transition, valid expansion scope guard, valid production replacement guard, valid rollback plan bind, valid post expansion probe, and no production replacement, production route change, global default route change, broad rollout, rollback execution, or performance claim.

K6ZO monitors the limited_candidate_lane_expanded canary after K6ZN expansion. It executes the expanded canary runtime health window, post-expansion replay probe, diff stability probe, timing stability probe, expanded canary scope isolation probe, fallback readiness probe, rollback rehearsal, production replacement block, and runtime monitor verdict.

K6ZO does not expand the canary again. It does not replace production GEMM, change the global default route, broaden rollout, execute rollback, or make performance claims.

PASS marker: PASS_ASH_TCU_K6ZO_LIMITED_EXPANDED_CANARY_RUNTIME_MONITOR_NO_PRODUCTION_REPLACEMENT_SEAL.
