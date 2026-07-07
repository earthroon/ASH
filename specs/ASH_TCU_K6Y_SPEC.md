# ASH TCU K6Y

Operator canary decision gate after K6X.

Required K6X PASS with promotion review ready, operator decision queue valid, current-device canary scope, and no broad rollout.

Validates an explicit operator decision or defaults to hold. Maps the decision to the next patch route without executing promotion, rollout, rollback, production replacement, or the selected next patch.

Allowed decisions are approve_current_device_canary_promotion_review, request_more_seeds, request_longer_canary_soak, request_device_matrix_replay, reject_candidate, and hold.

PASS PASS_ASH_TCU_K6Y_OPERATOR_CANARY_DECISION_GATE_NO_AUTO_PROMOTION_SEAL.
