# SFT-GPU-PERF-03A — LoRA A Delta Warm-Step Gate / Zero-B Init Allowance Seal

## Scope

This seal allows zero LoRA A delta only on the first real redispatch step when B-zero initialization is explicitly detected, while requiring nonzero B gradient and nonzero B delta. From step 2 onward it requires nonzero grad_lora_mid, nonzero A delta, and nonzero B delta.

## Required Evidence

- run id
- target key
- real step index
- optimizer step index
- B-zero init detection result and source
- grad_B norm
- grad_lora_mid norm
- A delta norm
- B delta norm
- pass1/pass2/update dispatch counters
- CPU fallback flag
- logits readback flag
- synthetic step flag

## Guards

- first step B-zero-init may allow zero A delta
- first step still requires nonzero grad_B
- first step still requires nonzero B delta
- step 2+ requires nonzero grad_lora_mid
- step 2+ requires nonzero A delta
- step 2+ requires nonzero B delta
- synthetic warm step rejected
- CPU serial fallback rejected
- logits readback rejected
- full logits buffer rejected
- dispatch counters must advance

## Baked Integration

- Added `crates/lora_train/src/lora_a_delta_warm_step_gate.rs`.
- Added `crates/lora_train/tests/lora_a_delta_warm_step_gate.rs`.
- Exported the module from `crates/lora_train/src/lib.rs`.
- Integrated the warm-step gate into `lm_head_vocab_atlas_gpu_update.rs` before the legacy `require_a_norm_change` failure.
- Wrote warm-step receipts from `write_gradient_reduce_update_report`:
  - `lora_a_delta_warm_step_receipt.json`
  - `lora_a_delta_warm_step_receipts.jsonl`
- Extended adapter export validation so first-step zero A delta can pass only when PERF-03A receipt explicitly allowed it.

## Acceptance Tests

- zero-B init first step allows zero A delta
- first step requires B delta
- first step requires grad B
- step 2 requires A delta and passes
- step 2 rejects zero A delta
- step 2 rejects missing grad_lora_mid / B carryover
- synthetic warm step rejected
- CPU fallback rejected
- logits readback rejected
- deterministic receipt id

## Result

PASS_STATIC for file presence, module export, guard text, receipt output paths, and brace-balance checks in this container.

PENDING_RUNTIME until exercised by real SFT-GPU-PERF-03 multi-step train run on the local Rust/GPU environment.
