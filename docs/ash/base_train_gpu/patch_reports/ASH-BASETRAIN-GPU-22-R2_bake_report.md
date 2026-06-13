# ASH-BASETRAIN-GPU-22-R2 Bake Report

## Changed

- Converted remaining ASH-BASETRAIN-GPU-22 section-level object `json!({ ... })` builders into atlas-map tile builders.
- Added `serde_json::Map` import.
- Preserved root atlas `serde_json::Map` assembly.
- Added R2 acceptance, receipts, static checks, and handoff files.

## Not Changed

- No local NLL/loss scalar values changed.
- No formula epsilon changed.
- No payload digest changed.
- No verdict or route LUT changed.
- No new loss computation, backward, optimizer, or mutation opened.
- No recursion limit attribute added.

## Container Limitation

`cargo` was unavailable in the current container, so compile PASS must be confirmed by the operator local log.
