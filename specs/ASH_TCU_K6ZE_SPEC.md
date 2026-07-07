# ASH TCU K6ZE

Longer matrix soak after K6ZD.

Required K6ZD PASS with operator_decision request_longer_matrix_soak, selected_next_patch ASH-TCU-K6ZE_LONGER_MATRIX_SOAK_NO_BROAD_ROLLOUT, longer matrix soak allowed as next patch, and no apply, promotion, broad rollout, production replacement, rollback execution, or performance claim.

Executes longer audit-only matrix soak across extended soak windows. Validates soak window manifest, soak seed set manifest, fixture distribution, device replay results, cross-device correctness, diff distribution, timing, extended diff drift persistence, extended timing drift persistence, route scope, and rollback readiness.

Does not execute apply, promotion, the selected next patch, broad rollout, production GEMM replacement, rollback, or external performance claim.

PASS PASS_ASH_TCU_K6ZE_LONGER_MATRIX_SOAK_NO_BROAD_ROLLOUT_SEAL.
