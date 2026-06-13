# 16AI-6J-R2-R1 Acceptance

Status: PENDING_RUNTIME

## Fixed

- `--gpu-default false` is now accepted by `af16ai6j_r2_gpu_shadow_replay8.rs`.
- `--gpu-default true` is explicitly blocked.

## Preserved Safety Contract

```txt
gpu_default=false
cpu_fallback=true
global_default_commit=false
branch_local_commit=true
token_ids_mutated=false
vocab_augmented=false
new_token_ids_created=false
```

## Runtime Acceptance Target

```txt
No unknown argument: --gpu-default
```

Then continue to one of:

```txt
PASS_GPU_SHADOW_REPLAY8
PASS_GPU_SHADOW_REPLAY8_WITH_WARNINGS
PARTIAL_GPU_SHADOW_REPLAY8
FAIL_GPU_SHADOW_REPLAY8
```
