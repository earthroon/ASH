# ASH TCU K6ZK

Limited canary bind gate after K6ZJ.

Required K6ZJ PASS with candidate_canary_promotion_review_executed true, candidate_canary_eligible true, operator_canary_approval_required true, candidate lane evidence digest valid, limited canary scope packet valid, operator canary approval queue valid, production replacement blocked, rollback plan forwarded, and no limited canary bind execution inside K6ZJ.

Accepts explicit operator_canary_decision approve_limited_canary_bind and binds the candidate route into a limited candidate-lane canary. Writes limited canary bind config, prior canary promotion review receipt, operator canary approval input and validation, candidate canary identity receipt, append-only limited canary bind ledger, canary lane state transition, limited canary scope guard, production replacement guard, rollback plan bind packet, canary post-bind probe, and limited canary bind verdict.

This patch changes only the candidate-lane canary state. It does not replace production GEMM, change global default route, broaden rollout, execute rollback, or claim external performance.

PASS PASS_ASH_TCU_K6ZK_LIMITED_CANARY_BIND_GATE_NO_PRODUCTION_REPLACEMENT_SEAL.
