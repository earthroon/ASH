# ASH TCU K6P

GPU row-major emit and layout-native bridge decision after K6O.

Required K6O PASS, K6N-R1 PASS, and K6M PASS.

Adds row-major emit shader path so the candidate can write row-major output on GPU without CPU canonicalization.

Outputs row-major emit config, row-major emit path, row-major emit parity, row-major emit timing, layout bridge probe, layout ownership decision, diagnosis, static checks.

PASS PASS_ASH_TCU_K6P_GPU_ROW_MAJOR_EMIT_LAYOUT_BRIDGE_DECISION_NO_PROMOTION_SEAL.
