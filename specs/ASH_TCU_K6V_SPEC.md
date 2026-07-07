# ASH TCU K6V

Canary random f32 monitor after K6U.

Required K6U PASS with current-device canary hold and random f32 fixture policy valid.

Replays the K6P row-major emit TensorCube candidate under current-device canary scope with non-trivial mixed-sign f32 fixture values, fixture distribution audit, correctness replay, zero-diff diagnostic guard, timing replay, route state guard, and rollback readiness guard.

Exact zero diff for independent f32 GEMM is classified by the diagnostic guard instead of being accepted as automatic proof of health. The expected healthy class is small non-zero diff within tolerance.

Does not broaden rollout, replace production GEMM, execute rollback, or claim external performance.

PASS PASS_ASH_TCU_K6V_CANARY_HOLD_RANDOM_F32_MONITOR_NO_BROAD_ROLLOUT_SEAL.
