# ASH-BASETRAIN-GPU-37N-R1 Bake Report

## Summary

This bake repairs the 37N compile failure caused by a local payload digest alias mismatch.

## Direct Change

```rust
payload_receipt_digest_hex: payload_digest_hex,
```

## Non-Changes

The following behavior is intentionally unchanged:

- multi-word diagnostic WGSL generation
- sample index validation
- bounded payload segment read
- queue upload
- dispatch/readback
- no forward/backward/optimizer/mutation guards

## Static Checks

See:

```txt
artifacts/ASH_BASETRAIN_GPU_37N_R1_STATIC_CHECKS.txt
artifacts/ASH_BASETRAIN_GPU_37N_R1_STATIC_CHECKS.json
```

## Operator Command

```powershell
cargo build -p base_train --bin ash_basetrain_gpu_37n_selected_group_row_block_multi_word_diagnostic_kernel
```
