# ASH-BASETRAIN-GPU-13 Bake Report

## Fixed

- Added `crates/base_train/src/ash_basetrain_gpu_13_chunk_window_logits_value_stability_audit.rs`
- Added direct-rebind bin `crates/base_train/src/bin/ash_basetrain_gpu_13_chunk_window_logits_value_stability_audit.rs`
- Did not require `lib.rs` export for the bin path.
- Source 12 module is direct-included by the bin, with an 11 PASS const shim required by the 12 source.

## Boundary

- Repeats ASH-BASETRAIN-GPU-12 output audit path 3 times.
- Compares observable readback evidence digest and sample deltas.
- Does not claim semantic correctness, full logits, generation, loss, backward, optimizer, or mutation.

## Runtime

Local Rust/WGPU compile and run must be executed by the operator.
