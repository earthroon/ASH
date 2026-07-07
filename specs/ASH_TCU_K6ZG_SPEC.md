# ASH TCU K6ZG

Operator matrix apply approval gate after K6ZF.

Required K6ZF PASS with longer_soak_promotion_review_ready true, extended longer soak evidence valid, extended correctness valid, extended diff persistence valid, extended timing persistence valid, route scope valid, rollback readiness valid, risk boundary valid, operator decision queue valid, and no apply, promotion, broad rollout, production replacement, rollback execution, or performance claim.

Accepts the K6ZF longer-soak promotion review evidence and records an explicit operator approval to proceed to the matrix apply gate. Routes to ASH-TCU-K6ZH_EXPLICIT_MATRIX_APPLY_GATE_BOUND_NO_SILENT_ADOPTION.

Does not execute apply, promotion, the selected next patch, silent adoption, broad rollout, production GEMM replacement, rollback, or external performance claim.

PASS PASS_ASH_TCU_K6ZG_OPERATOR_MATRIX_APPLY_APPROVAL_GATE_NO_BROAD_ROLLOUT_SEAL.
