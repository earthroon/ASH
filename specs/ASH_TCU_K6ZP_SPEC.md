# ASH TCU K6ZP

Limited expanded canary promotion review after K6ZO.

Required prior PASS: ASH-TCU-K6ZO with limited expanded canary runtime monitor executed, expanded canary health window valid, post-expansion replay valid, diff and timing stability healthy, scope isolation valid, fallback readiness valid, rollback rehearsal valid, production replacement blocked, canary scope limited_candidate_lane_expanded, no additional expansion, no production route change, no global default route change, no broad rollout, no rollback execution, and no performance claim.

K6ZP reviews the runtime-monitored limited_candidate_lane_expanded canary and marks it eligible for a limited production-shadow canary gate. It creates the review config, prior monitor receipt, runtime evidence digest, production-shadow eligibility packet, production-shadow risk boundary packet, production-shadow scope packet, operator shadow approval queue, production replacement block, rollback plan forward packet, and promotion review verdict.

K6ZP does not bind production-shadow. It does not replace production GEMM, change the global default route, broaden rollout, execute rollback, or make performance claims.

PASS marker: PASS_ASH_TCU_K6ZP_LIMITED_EXPANDED_CANARY_PROMOTION_REVIEW_NO_PRODUCTION_REPLACEMENT_SEAL.
