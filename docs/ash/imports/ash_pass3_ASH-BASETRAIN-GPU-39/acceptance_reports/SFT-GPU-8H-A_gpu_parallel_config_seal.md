# SFT-GPU-8H-A GPU parallel config seal

## Status
PASS_STATIC

## Sealed config
- `projection = gpu_parallel_vocab_atlas`
- `gpu_parallel.enabled = true`
- `gpu_parallel.required = true`
- `dispatch_mode = tile_group_parallel`
- `ce_reduce_mode = gpu_partial_logsumexp`
- `grad_reduce_mode = gpu_partial_grad_reduce`
- `update_mode = gpu_reduce_update`
- `forbid_cpu_serial_tile_loop = true`
- `forbid_cpu_token_vocab_loop = true`
- `forbid_logits_readback = true`
- `readback_policy = loss_and_report_only`

## Memory guard
- `forbid_full_vocab_buffer = true`
- `forbid_full_logits_buffer = true`
- `max_group_weight_bytes = 33554432`

## Runtime policy
This commit seals config and validation only. If `gpu_parallel.required=true`, the old 8G CPU-serial/tiled trainer must not run as a quiet fallback. Until SFT-GPU-8H-B introduces the GPU buffer bridge/runner, `projection=gpu_parallel_vocab_atlas` intentionally bails after the config-sealed log.

## Scope
- No WGSL/CubeCL custom kernel is implemented in this commit.
- No sampled CE fallback is introduced.
- No full vocab weight or full logits buffer is allowed.
