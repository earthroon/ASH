# ASH TCU K6W

Canary random f32 stability repeat after K6V.

Required K6V PASS with random f32 fixture distribution valid, zero-diff diagnostic class healthy_small_non_zero_diff, timing valid, canary scope current_device_only, and broad rollout blocked.

Repeats the current-device canary random f32 dynamic-range replay across multiple deterministic seeds. Requires non-trivial fixture distribution per seed, small non-zero diff across all seeds, diff diversity, timing variance guard, canary scope repeat guard, and rollback readiness repeat guard.

Does not broaden rollout, replace production GEMM, execute rollback, or claim external performance.

PASS PASS_ASH_TCU_K6W_CANARY_RANDOM_F32_STABILITY_REPEAT_NO_BROAD_ROLLOUT_SEAL.
