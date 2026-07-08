# ASH TCU K6ZP

Limited expanded canary promotion review after K6ZO.

Required prior PASS: ASH-TCU-K6ZO with limited expanded canary runtime monitor executed, expanded canary health window valid, post-expansion replay valid, diff and timing stability healthy, scope isolation valid, fallback readiness valid, rollback rehearsal valid, production replacement blocked, canary scope limited_candidate_lane_expanded, no additional expansion, no production route change, no global default route change, no broad rollout, no rollback execution, and no performance claim.

K6ZP reviews the K6ZO-monitored limited_candidate_lane_expanded canary and marks it eligible for the next limited production-shadow canary gate. It creates the promotion review config, prior monitor receipt, runtime evidence digest, limited production-shadow eligibility packet, risk boundary packet, scope packet, operator shadow approval queue, production replacement block packet, rollback plan forward packet, and promotion review verdict.

K6ZP does not bind production-shadow inside K6ZP. It does not replace production GEMM, change the global default route, broaden rollout, execute rollback, or make performance claims.

PASS marker: PASS_ASH_TCU_K6ZP_LIMITED_EXPANDED_CANARY_PROMOTION_REVIEW_NO_PRODUCTION_REPLACEMENT_SEAL.

Recommended next patch: ASH-TCU-K6ZQ_LIMITED_PRODUCTION_SHADOW_CANARY_GATE_NO_PRODUCTION_REPLACEMENT.
