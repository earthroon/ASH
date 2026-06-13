# SFT-GPU-6 Static Validation Result

## Status

PASS_STATIC 22 / 22

## Validated Scope

- `runtime_delta_verify.rs` exists
- `runtime_delta_verify` module exported from `lib.rs`
- `training.rs` imports and calls `verify_runtime_lm_head_lora_delta`
- `adapter_runtime.json` RuntimeLoraAttachment sidecar is generated
- `model_core::load_runtime_lora_attachments` is used for the runtime sidecar
- `validate_runtime_lora_attachment_for_module` is used before delta verification
- `target_key=lm_head` contract is enforced
- `delta_max_abs > 0` gate exists
- `delta_mean_abs > 0` gate exists
- `delta_nonzero_count > 0` gate exists
- reload reproducibility gate exists
- `runtime_delta_report.json` and `runtime_delta_report.md` are written
- checkpoint manifest records runtime delta report paths
- target stats resume source is updated to `direct_jsonl_sft_gpu6_runtime_delta`

## Notes

This is a static validation result only. The current sandbox does not include `cargo` / `rustc` / WGPU device access, so compile and runtime execution must be validated in the user's local environment.
