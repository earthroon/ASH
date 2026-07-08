# ASH TCU K6ZN

Limited canary expansion gate after K6ZM.

Required prior PASS: ASH-TCU-K6ZM with limited canary promotion review executed, expansion eligible, operator expansion approval required, runtime evidence valid, expansion eligibility valid, expansion scope valid, operator expansion queue valid, production replacement blocked, rollback plan forwarded, and no expansion executed inside K6ZM.

K6ZN accepts explicit operator_expansion_decision approve_limited_canary_expansion and changes the canary scope from candidate_lane_only to limited_candidate_lane_expanded. It writes the expansion config, prior promotion review receipt, operator approval input and validation, expansion identity receipt, append-only expansion ledger, scope transition, expansion scope guard, production replacement guard, rollback plan bind packet, post-expansion probe, and expansion verdict.

K6ZN changes only the limited canary scope. It does not replace production GEMM, change the global default route, broaden rollout, execute rollback, or make performance claims.

PASS marker: PASS_ASH_TCU_K6ZN_LIMITED_CANARY_EXPANSION_GATE_NO_PRODUCTION_REPLACEMENT_SEAL.
