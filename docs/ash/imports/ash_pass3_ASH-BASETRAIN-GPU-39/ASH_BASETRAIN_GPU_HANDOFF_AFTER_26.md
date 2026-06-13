# ASH-BASETRAIN-GPU Handoff After 26

## Current SSOT

`ASH-BASETRAIN-GPU-26` is the current baked source candidate.

## Source SSOT

`ASH-BASETRAIN-GPU-25` PASS:

```txt
PASS_ASH_BASETRAIN_GPU_25_GPU_LOCAL_LOSS_REPEATABILITY_AUDIT_REPEATED_WINDOW_2048_TARGET_1_GPU_LOSS_CANDIDATE_STABILITY_NO_BACKWARD_NO_OPTIMIZER
```

## 26 Scope

`26` is a static promotion gate from stable GPU local loss candidate to backward readiness candidate.

It does not open:

```txt
new GPU dispatch
new readback
new loss computation
backward
gradient buffer creation
optimizer
weight mutation
safetensors mutation
checkpoint finalization
```

## Key Values

```txt
stable_gpu_local_nll_loss = 7.624625205993652
cpu_reference_loss = 7.624619041439192
max_gpu_repeat_loss_delta_abs = 0.0
gpu_repeat_epsilon = 0.00001
max_cpu_reference_delta_abs = 0.000006164554460674765
gpu_loss_candidate_epsilon = 0.0001
payload_digest_hex = 856552759fc5e7f0b0b7c7b2de78fe0f1e59f82b2ff7c935f819758572878052
```

## Next Patch

```txt
ASH-BASETRAIN-GPU-27
GPU Backward Preflight /
Stable GPU Loss Candidate To Gradient Buffer Contract No Backward No Optimizer Seal
```
