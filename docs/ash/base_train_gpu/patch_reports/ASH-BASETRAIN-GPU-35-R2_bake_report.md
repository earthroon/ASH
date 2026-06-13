# ASH-BASETRAIN-GPU-35-R2 Bake Report

- Added Rust source and bin for selected group manifest template materialization.
- Added operator manifest input probe, placeholder guard, schema validation, digest receipts, target manifest materialization receipt.
- Default baked status: `BLOCKED_MISSING_OPERATOR_MANIFEST_ENV`.
- No runtime GPU allocation, no selected group weight load, no backward, no optimizer.
