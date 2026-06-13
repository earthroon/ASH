# ASH-BASETRAIN-GPU-15 Acceptance

Status: BAKED_STATIC_GATE

Expected verdict:

```text
PASS_ASH_BASETRAIN_GPU_15_CHUNK_WINDOW_LOGITS_EXPANSION_READINESS_GATE_WINDOW_1024_TO_2048_CANDIDATE_NO_DISPATCH_NO_OPTIMIZER
```

## Scope
- 1024 to 2048 logits window expansion readiness candidate
- No dispatch
- No readback
- No optimizer

## SSOT boundary
The 2048 window is a candidate only. Execution must wait for ASH-BASETRAIN-GPU-16.
