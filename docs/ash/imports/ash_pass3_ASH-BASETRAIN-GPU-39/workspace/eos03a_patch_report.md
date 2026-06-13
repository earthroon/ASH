# 16AI-QW-38G-R6A-EOS-03A — Conditional EOS Restore After Min-New-Tokens / Natural Stop Recovery Seal

## Status
PASS_STATIC_CONDITIONAL_EOS_RESTORE_BAKED_PENDING_LOCAL_CARGO_BUILD

## Scope
- Added EOS-03A restore receipt and step trace wiring in `crates/orchestrator_local/src/infer_entry.rs`.
- Added step-local EOS suppression before `min_new_tokens` in `crates/model_core/src/decode_state.rs`.

## Behavior
- `eosRestoreEnabled` / `eos_restore_enabled` enables EOS-03A receipt output.
- `eosRestoreReceiptPath` and `eosRestoreStepTracePath` are supported.
- EOS token is no longer request-wide banned for EOS-03A.
- In model-core decode state, EOS is masked only while `generated_token_count_after_step < sampling.min_new_tokens`.
- Once generated token count reaches `min_new_tokens`, EOS is no longer dynamically masked and can naturally stop generation.

## Non-mutation guarantees
- checkpoint_modified = false
- tokenizer_modified = false
- safetensors_modified = false
- lm_head_modified = false
- final_norm_modified = false
- ban_mask_modified = false
