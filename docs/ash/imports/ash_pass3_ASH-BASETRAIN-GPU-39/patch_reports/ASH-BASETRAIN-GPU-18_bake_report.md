# ASH-BASETRAIN-GPU-18 Bake Report

## Included

- `crates/base_train/src/ash_basetrain_gpu_18_window_2048_logits_readback_determinism_audit.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_18_window_2048_logits_readback_determinism_audit.rs`
- Acceptance report and handoff files

## Boundary

This patch repeats the ASH-BASETRAIN-GPU-17 2048 output audit path three times and compares raw readback SHA256 digests, samples, finite scans, and boundary receipts. It does not add loss, backward, optimizer, weight commit, safetensors mutation, generation, or decode.
