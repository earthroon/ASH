# ASH TCU K6ZM

Limited canary promotion review after K6ZL.

Required prior PASS: ASH-TCU-K6ZL with limited canary runtime monitor valid, health window valid, replay valid, diff and timing stability healthy, scope isolation valid, fallback readiness valid, rollback rehearsal valid, and production replacement blocked.

K6ZM reviews the runtime-monitored limited candidate-lane canary and marks it eligible for the next limited canary expansion gate. It creates the review config, prior monitor receipt, runtime evidence digest, expansion eligibility packet, expansion risk boundary packet, expansion scope packet, operator expansion approval queue, production replacement block, rollback plan forward packet, and promotion review verdict.

K6ZM does not execute expansion. It does not replace production GEMM, change the global default route, broaden rollout, execute rollback, or make performance claims.

PASS marker: PASS_ASH_TCU_K6ZM_LIMITED_CANARY_PROMOTION_REVIEW_NO_PRODUCTION_REPLACEMENT_SEAL.
