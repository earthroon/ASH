# ASH TCU K6ZD

Operator matrix apply decision gate after K6ZC.

Required K6ZC PASS with device_matrix_promotion_review_ready true, operator decision queue valid, cross-window evidence valid, matrix correctness evidence valid, diff drift evidence valid, timing drift evidence valid, route scope stability valid, rollback readiness valid, risk boundary valid, and no broad rollout.

Validates an explicit operator matrix apply decision or defaults to hold. Maps the decision to the next patch route without executing apply, promotion, rollout, rollback, production replacement, or the selected next patch.

Allowed decisions are approve_matrix_apply_gate_review, request_longer_matrix_soak, request_more_matrix_windows, request_device_identity_recheck, reject_candidate, and hold.

PASS PASS_ASH_TCU_K6ZD_OPERATOR_MATRIX_APPLY_DECISION_GATE_NO_BROAD_ROLLOUT_SEAL.
