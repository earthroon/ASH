# ASH-TCU-K6D

Timed shadow candidate probe after K6C.

Required: K6C PASS.

Shape: M64, N64, K32.

Warmup iterations: 8.

Measured iterations: 32.

Baseline route: existing burn gemm or current runtime path.

Candidate route: K6C K6B native grid candidate.

Output: timing receipts only.

Guards: runtime splice closed, production replacement closed, performance claim closed, promotion closed.

PASS marker: PASS_ASH_TCU_K6D_TIMED_SHADOW_CANDIDATE_PROBE_NO_PROMOTION_SEAL.
