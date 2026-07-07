# ASH TCU K6ZH

Explicit matrix apply gate after K6ZG.

Required K6ZG PASS with operator_decision approve_matrix_apply_gate_review, operator_apply_approval_accepted true, apply_gate_route_ready true, selected_next_patch ASH-TCU-K6ZH_EXPLICIT_MATRIX_APPLY_GATE_BOUND_NO_SILENT_ADOPTION, longer soak evidence accepted, explicit apply gate boundary valid, silent adoption blocked, production replacement blocked, rollback readiness forwarded, and no apply/promotion/selected-next-patch execution inside K6ZG.

Executes a receipt-bound candidate matrix apply for ash_tcu_k6p_row_major_emit_candidate_v1. Writes an append-only apply ledger, records candidate apply lane state transition, probes post-conditions, binds rollback readiness, and verifies no silent adoption, no production route replacement, no global default route change, no broad rollout, no rollback execution, and no external performance claim.

This patch changes only the receipt-bound candidate apply lane, not the production/global/default route.

PASS PASS_ASH_TCU_K6ZH_EXPLICIT_MATRIX_APPLY_GATE_BOUND_NO_SILENT_ADOPTION_SEAL.
