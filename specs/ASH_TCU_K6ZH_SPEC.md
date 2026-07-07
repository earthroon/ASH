# ASH TCU K6ZH

Explicit matrix apply gate after K6ZG.

Required K6ZG PASS with operator_decision approve_matrix_apply_gate_review, operator_apply_approval_accepted true, apply_gate_route_ready true, selected_next_patch ASH-TCU-K6ZH_EXPLICIT_MATRIX_APPLY_GATE_BOUND_NO_SILENT_ADOPTION, longer soak evidence accepted, explicit apply boundary valid, silent adoption blocked, production replacement blocked, rollback readiness forwarded, and no broad rollout or production replacement.

Executes a receipt-bound candidate matrix apply. Writes an append-only apply ledger, records candidate apply state transition, validates candidate route identity, blocks silent adoption, blocks production replacement, probes post-apply state, and binds rollback readiness to the apply ledger.

This patch only changes the receipt-bound candidate apply lane. It does not silently adopt the candidate, broaden rollout, replace production GEMM, change global default route, execute rollback, or claim external performance.

PASS PASS_ASH_TCU_K6ZH_EXPLICIT_MATRIX_APPLY_GATE_BOUND_NO_SILENT_ADOPTION_SEAL.
