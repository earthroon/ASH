# Bake Report — ASH-BASETRAIN-GPU-33

## Files added
- `crates/base_train/src/ash_basetrain_gpu_33_loss_scalar_to_logits_gradient_binding_audit.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_33_loss_scalar_to_logits_gradient_binding_audit.rs`
- ASH_BASETRAIN_GPU_33_* receipts

## Runtime note
Container cargo was not available, so local runtime validation is delegated to operator commands. This patch is a static binding audit and does not require GPU runtime.
