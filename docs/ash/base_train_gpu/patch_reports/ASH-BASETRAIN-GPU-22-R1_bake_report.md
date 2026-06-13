# ASH-BASETRAIN-GPU-22-R1 Bake Report

## Changed

- Replaced giant top-level `json!({...})` receipt bundle in `ash_basetrain_gpu_22_loss_scalar_audit.rs`.
- Added section builder functions for receipt sections.
- Added shallow `serde_json::Map` top-level assembly.
- Did not add `#![recursion_limit = "256"]`.

## Not Changed

- No loss value changed.
- No formula epsilon changed.
- No verdict string changed.
- No route LUT changed.
- No new loss computation added.
- No backward/optimizer/safetensors mutation opened.

## Container Limitation

`cargo` was unavailable in the current container, so compile PASS must be confirmed by the operator local log.
