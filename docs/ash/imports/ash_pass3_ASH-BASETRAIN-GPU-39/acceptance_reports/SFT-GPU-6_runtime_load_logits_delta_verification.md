# SFT-GPU-6 Acceptance

## Status

PENDING until cargo/WGPU runtime smoke is executed in the user environment.

## Scope

runtime load / logits delta verification

## Required Contract

- `artifact_family = module_lora`
- `target_key = lm_head`
- tensor keys are `lm_head.lora_A` and `lm_head.lora_B`
- `adapter_runtime.json` is generated as a `RuntimeLoraAttachment` sidecar
- the sidecar is loaded through `model_core::load_runtime_lora_attachments`
- runtime module validation accepts the attachment
- LoRA OFF/ON lm_head logits shapes match
- `delta_max_abs > 0`
- `delta_mean_abs > 0`
- `delta_nonzero_count > 0`
- reload is reproducible within tolerance

## Gates

- [ ] `adapter_manifest.json` exists
- [ ] `adapter_model.safetensors` exists
- [ ] `adapter_runtime.json` is written
- [ ] manifest loads successfully
- [ ] `artifact_family == module_lora`
- [ ] `target_key == lm_head`
- [ ] runtime sidecar loads successfully
- [ ] runtime module attachment validation passes
- [ ] LoRA OFF logits shape is `[checked_positions, vocab_size]`
- [ ] LoRA ON logits shape is `[checked_positions, vocab_size]`
- [ ] all checked logits are finite
- [ ] `delta_max_abs > 0`
- [ ] `delta_mean_abs > 0`
- [ ] `delta_nonzero_count > 0`
- [ ] reload sidecar delta is reproducible
- [ ] `runtime_delta_report.json` is written
- [ ] `runtime_delta_report.md` is written

## Non-goals

- generated text quality is not evaluated here
- adapter merge is not implemented here
- multi-adapter stacking is not implemented here
- q/v/o LoRA runtime expansion is not implemented here

## Notes

SFT-GPU-6 uses the existing runtime loader for the generated `RuntimeLoraAttachment` sidecar, then performs a deterministic lm_head logits-delta equivalence check over response-token hidden states. This avoids treating `adapter_manifest.json` as runtime-loaded unless it has actually been converted into the runtime sidecar format accepted by the current loader.
