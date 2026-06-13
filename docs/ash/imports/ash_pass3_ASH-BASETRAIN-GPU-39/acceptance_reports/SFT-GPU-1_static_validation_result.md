# SFT-GPU-1 Static Validation Result

## Status

STATIC-PASS / CARGO-CHECK-NOT-RUN

## Reason

The bake environment does not have `cargo` installed, so Rust compilation could not be executed in this sandbox.

## Static Checks Run

- Parsed all four A-SFT JSON configs with Python JSON parser.
- Verified direct-line contract fields:
  - `family=sft_lora`
  - `mode=train`
  - `dataset.loss_on=response_only`
  - `training.plan_kind=module_lora`
  - `hyper.target_modules=["lm_head"]`
  - `lora.targets=["lm_head"]`
  - `lora.artifact_family=module_lora`
  - `lora.merge_mode=runtime_attach`
  - `guards.expect_target_key=lm_head`
  - `guards.forbid_prompt_loss=true`
  - `guards.require_response_loss_tokens=true`
- Verified `config.rs` contains strict schema markers for sealed config structs.
- Verified `scaffold.rs` contains `validate_a_sft_direct_line_contract` and calls it from `validate_training_config`.
- Verified `lora_train.rs` emits `[lora_train][contract]` log before plan construction.

## Expected Next Runtime Boundary

SFT-GPU-1 intentionally does not seal `lm_head` into the module target resolver. If runtime now fails with:

```txt
no module targets resolved for module_lora training plan
```

that is the expected boundary for SFT-GPU-2.
