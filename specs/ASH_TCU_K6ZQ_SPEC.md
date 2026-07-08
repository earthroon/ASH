# ASH TCU K6ZQ

Limited production-shadow canary gate after K6ZP.

Required prior PASS: ASH-TCU-K6ZP with limited expanded canary promotion review executed, limited production-shadow eligible, operator shadow approval required, runtime evidence digest valid, shadow eligibility valid, shadow risk boundary valid, shadow scope valid, operator shadow approval queue valid, production replacement blocked, rollback plan forwarded, and no shadow bind executed inside K6ZP.

K6ZQ accepts explicit operator_shadow_decision approve_limited_production_shadow and binds a limited production-shadow canary in observation-only mode. It writes the shadow config, prior promotion review receipt, operator shadow approval input and validation, shadow identity receipt, append-only shadow bind ledger, shadow scope transition, shadow scope guard, production replacement guard, rollback plan bind packet, post-bind probe, and shadow canary verdict.

K6ZQ changes only the shadow observation scope. It does not commit shadow outputs, use shadow outputs as default, use shadow outputs for user-visible results, replace production GEMM, change the global default route, broaden rollout, execute rollback, or make performance claims.

PASS marker: PASS_ASH_TCU_K6ZQ_LIMITED_PRODUCTION_SHADOW_CANARY_GATE_NO_PRODUCTION_REPLACEMENT_SEAL.

Recommended next patch: ASH-TCU-K6ZR_LIMITED_PRODUCTION_SHADOW_RUNTIME_MONITOR_NO_PRODUCTION_REPLACEMENT.
