# ASH TCU K6Z

Device matrix replay preflight after K6Y.

Required K6Y PASS with operator_decision request_device_matrix_replay and selected_next_patch ASH-TCU-K6Z_DEVICE_MATRIX_REPLAY_PREFLIGHT_NO_BROAD_ROLLOUT.

Validates device slot declaration, current device identity, secondary device identity probe, fallback route identity, matrix replay requirements, random f32 matrix fixture policy, zero-diff matrix guard policy, and replay plan routing.

Does not execute device matrix replay, enable broad rollout, replace production GEMM, execute rollback, or claim external performance.

PASS PASS_ASH_TCU_K6Z_DEVICE_MATRIX_REPLAY_PREFLIGHT_NO_BROAD_ROLLOUT_SEAL.
