# SFT-GPU-8H-D global CE reduce kernel

## Status
PASS_STATIC / PASS_GLOBAL_CE_REDUCE_KERNEL_SMOKE

## Sealed
- `lm_head_vocab_atlas_gpu_reduce.rs`
- `GpuGlobalCeReduceConfig`
- `GpuGlobalCeReduceReport`
- `validate_global_ce_reduce_policy(...)`
- `cpu_reference_global_ce_reduce(...)`
- `dispatch_global_ce_reduce_kernel(...)`
- `write_gpu_reduce_report(...)`

## CE state
- `global_max`: `[active_tokens]`
- `global_sum_exp`: `[active_tokens]`
- `global_logsumexp`: `[active_tokens]`
- `target_logit`: `[active_tokens]`
- `target_seen_count`: `[active_tokens]`
- `loss`: `[active_tokens]`
- `mean_loss`: `[1]`

## Guards
- full logits buffer forbidden
- logits readback forbidden
- readback policy sealed to `loss_and_report_only`
- `target_seen_count` must be exactly `1` per active token
- nonfinite `global_max`, invalid `global_sum_exp`, and nonfinite `loss` are hard failures

## Runtime transition
When every vocab tile group has a pass1 partial buffer, the path now runs:

```txt
all-group pass1 partial buffers
→ global CE reduce smoke
→ vocab_atlas_gpu_reduce_report.json/.md
→ explicit stop for SFT-GPU-8H-E
```

## Next
SFT-GPU-8H-E pass2 GPU gradient kernel.
