# SFT-GPU-8F Static Validation Result

```txt
SFT-GPU-8F static validation
PASS count: 15
[PASS] hot path per-example teacher.forward_hidden_ids loop removed from sft_feature_store.rs
[PASS] A-SFT padded batch builder and seq_len slice helpers present
[PASS] native_dump uses ASftBatchedHiddenProvider::forward_group
[PASS] progress report records compute-level batched seal fields
[PASS] a_sft_batched_hidden_provider module exported
[PASS] batched hidden input/output structs present
[PASS] provider has native and explicit fallback variants
[PASS] native provider calls NativeWgpuModel::forward_hidden_padded_batch
[PASS] NativeWgpuModel::forward_hidden_padded_batch API present
[PASS] ASftDumpBatchingConfig.hidden_provider present
[PASS] ASftDumpBatchingConfig.require_compute_batched_hidden present
[PASS] ASftDumpBatchingConfig.forbid_per_example_forward present
[PASS] native_dump config hidden_provider=native_wgpu_padded_hidden
[PASS] native_dump config require_compute_batched_hidden=true
[PASS] native_dump config forbid_per_example_forward=true
[PASS_STATIC] SFT-GPU-8F compute-level batched hidden provider seal
```

## Status

PASS_STATIC

## Runtime

Not executed in this environment because Rust/WGPU toolchain/runtime is unavailable here. Use the target machine runtime gate from `SFT-GPU-8F_a_sft_compute_level_batched_hidden_provider_seal.md`.
