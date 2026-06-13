# ASH-BASETRAIN-GPU-13 Acceptance

Status: BAKED / LOCAL RUNTIME PENDING

Source SSOT: `ash_pass3_ASH-BASETRAIN-GPU-12_multi_buffer_forward_output_audit_baked (2).zip`

Scope:
- repeated fixed-token chunk-window dispatch readback stability audit
- repeat_count = 3
- no semantic full forward
- no generation/decode/loss/backward/optimizer/mutation

Expected PASS verdict:

```txt
PASS_ASH_BASETRAIN_GPU_13_CHUNK_WINDOW_LOGITS_VALUE_STABILITY_AUDIT_REPEATED_FIXED_TOKEN_DISPATCH_READBACK_DETERMINISM_NO_BACKWARD_NO_OPTIMIZER
```

Note: this implementation uses direct bin rebind to avoid the previously observed lib.rs export overlay mismatch.
