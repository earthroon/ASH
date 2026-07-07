# ASH TCU K6ZA

Device matrix random f32 replay after K6Z.

Required K6Z PASS with matrix_replay_preflight_ready true, secondary_device_replay_ready true, fallback route identity valid, random f32 matrix fixture policy valid, zero-diff matrix guard policy valid, and recommended_next_patch ASH-TCU-K6ZA_DEVICE_MATRIX_RANDOM_F32_REPLAY_NO_BROAD_ROLLOUT.

Executes audit-only device matrix random f32 replay across current, secondary, and fallback_burn paths. Validates seed manifest, fixture distribution, current and secondary replay results, fallback reference, cross-device correctness, cross-device small non-zero diff distribution, timing, route scope, and rollback readiness.

Does not broaden rollout, replace production GEMM, execute promotion, execute rollback, or claim external performance.

PASS PASS_ASH_TCU_K6ZA_DEVICE_MATRIX_RANDOM_F32_REPLAY_NO_BROAD_ROLLOUT_SEAL.
