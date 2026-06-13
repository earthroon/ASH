# ASH-BASETRAIN-GPU-36B-R1 Acceptance

## Patch
ASH-BASETRAIN-GPU-36B-R1

## Title
Local Hex Encoder Buildfix / Remove Unlinked Hex Crate Dependency No Logic Change Seal

## Scope
- Replace the unlinked `hex::encode` call in the ASH-BASETRAIN-GPU-36B Rust source.
- Add a local lower-hex encoder backed by a fixed 16-symbol lookup table.
- Do not change the 36B bounded window read, F32 sample stats, digest input, receipt schema, or runtime guard contract.
- Do not add a new Cargo dependency.

## SSOT
- Existing ASH-BASETRAIN-GPU-36B source and receipt contract.
- The original blocker was E0433 for `hex::encode`.

## Expected buildfix effect
The 36B binary should no longer require an external `hex` crate.

## Static acceptance
- `hex::encode` absent from 36B Rust source.
- `use hex` absent from 36B Rust source.
- `extern crate hex` absent from 36B Rust source.
- Local lookup table encoder present.
- Previous live input receipts are not included at their live artifact paths.

## Runtime boundary
No read logic change. 36B still only re-reads the bounded first/middle/last windows from the 36A receipt and generates F32 window stats. Full tensor load, safetensors header parse, GPU upload, forward/backward, optimizer, and mutation remain sealed.

## Local commands
```powershell
cargo build -p base_train --bin ash_basetrain_gpu_36b_bounded_weight_slice_f32_window_sanity
cargo run -p base_train --bin ash_basetrain_gpu_36b_bounded_weight_slice_f32_window_sanity -- --window-read-receipt .\artifacts\ASH_BASETRAIN_GPU_36A_BOUNDED_WEIGHT_SLICE_READ_SMOKE.json
```
