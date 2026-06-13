# ASH-BASETRAIN-GPU-14 Acceptance

Status: BAKED / LOCAL RUNTIME PENDING

Source SSOT: `ASH-BASETRAIN-GPU-13` PASS runtime result and baked source package.

Scope:
- static chunk-window logits stability promotion gate
- no new WGPU execution
- no new readback
- no semantic full forward
- no generation/decode/loss/backward/optimizer/mutation
- direct bin rebind, no lib.rs export requirement for bin

Promotion target:

```txt
fixed_token_chunk_window_logits_path
```

Expected PASS verdict:

```txt
PASS_ASH_BASETRAIN_GPU_14_CHUNK_WINDOW_LOGITS_STABILITY_PROMOTION_GATE_DETERMINISTIC_READBACK_TO_FORWARD_EXPANSION_CANDIDATE_NO_BACKWARD_NO_OPTIMIZER
```
