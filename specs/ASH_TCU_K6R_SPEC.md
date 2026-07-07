# ASH TCU K6R

Explicit apply gate with operator decision after K6Q.

Required K6Q PASS with promotion_review_ready true.

Adds an explicit apply gate for the K6P GPU row-major emit TensorCube candidate. Default mode is review-only hold. Explicit binding requires operator decision approve_for_apply_gate plus --allow-explicit-apply, fresh correctness recheck, fresh timing recheck, device allowlist, fallback route, and armed rollback.

Outputs apply gate config, operator decision, fresh correctness recheck, fresh timing recheck, device allowlist, fallback route, rollback arming, route binding plan, route binding receipt, apply gate verdict, diagnosis, static checks.

Does not silently adopt, overwrite production GEMM, or claim external performance.

PASS PASS_ASH_TCU_K6R_EXPLICIT_APPLY_GATE_REVIEW_ONLY_NO_SILENT_ADOPTION_SEAL or PASS_ASH_TCU_K6R_EXPLICIT_APPLY_GATE_BOUND_NO_SILENT_ADOPTION_SEAL.
