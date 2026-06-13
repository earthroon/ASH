# ASH-BASETRAIN-GPU-12 Acceptance

- Source SSOT: ASH-BASETRAIN-GPU-11-SSOT-R1
- Scope: fixed token chunk-window logits readback audit
- Output window: [1, 1, 1024]
- Expected readback bytes: 4096
- Verdict target: `PASS_ASH_BASETRAIN_GPU_12_MULTI_BUFFER_FORWARD_OUTPUT_AUDIT_FIXED_TOKEN_CHUNK_WINDOW_LOGITS_SMOKE_READBACK_AND_BOUNDARY_VERIFICATION_NO_BACKWARD_NO_OPTIMIZER`
- No backward / no optimizer / no safetensors mutation.
