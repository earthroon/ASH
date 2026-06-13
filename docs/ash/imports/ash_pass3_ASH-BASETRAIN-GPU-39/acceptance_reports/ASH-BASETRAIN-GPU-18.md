# ASH-BASETRAIN-GPU-18 Acceptance

- Patch: ASH-BASETRAIN-GPU-18
- Title: Window 2048 Logits Readback Determinism Audit / Repeated Dispatch Readback Raw Digest Stability No Backward No Optimizer Seal
- Source: ASH-BASETRAIN-GPU-17 PASS output audit
- Scope: repeated 2048 dispatch/readback raw digest determinism only
- Forbidden: full logits, generation, decode, loss, backward, optimizer, mutation
- Expected PASS: PASS_ASH_BASETRAIN_GPU_18_WINDOW_2048_LOGITS_READBACK_DETERMINISM_AUDIT_REPEATED_DISPATCH_READBACK_RAW_DIGEST_STABILITY_NO_BACKWARD_NO_OPTIMIZER
