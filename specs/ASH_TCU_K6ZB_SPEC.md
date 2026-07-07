# ASH TCU K6ZB

Device matrix stability repeat after K6ZA.

Required K6ZA PASS with audit-only current + secondary + fallback_burn matrix replay executed, cross-device correctness valid, healthy small non-zero diff distribution across devices, timing valid, and no broad rollout.

Repeats audit-only device matrix random f32 replay across stability windows. Validates per-window fixture distribution, device replay results, cross-device correctness, cross-device diff distribution, cross-device timing, cross-window diff drift, cross-window timing drift, matrix scope stability, and rollback readiness repeat.

Does not broaden rollout, replace production GEMM, execute promotion, execute rollback, or claim external performance.

PASS PASS_ASH_TCU_K6ZB_DEVICE_MATRIX_STABILITY_REPEAT_NO_BROAD_ROLLOUT_SEAL.
