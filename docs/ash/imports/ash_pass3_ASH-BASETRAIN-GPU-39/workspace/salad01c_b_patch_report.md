# 16AI-QW-38G-R6A-SALAD-01C-B Bake Report

## Status
PASS_STATIC_RECEIPT_WIRING_BAKE_PENDING_LOCAL_CARGO_BUILD

## SSOT
`crates/orchestrator_local/src/infer_entry.rs` now writes a SALAD-01C-B pre-infer receipt before `StandardInferRequest` decode execution begins.

## What changed
- Updated SALAD continuation patch id to `16AI-QW-38G-R6A-SALAD-01C-B`.
- Added `salad01c_pre_infer_receipt_json()`.
- Resolves `salad01cReceiptPath` and canonical `workspace/salad01c_generation_receipt.json` before decode.
- Writes a pre-infer receipt before the first infer call.
- Final receipt records `receipt_stage = pre_and_post_infer`, `infer_entry_seen = true`, and `generic_collapse_guard_evaluated = true`.
- Existing output artifact and response JSON embedding of `salad01c_receipt` is preserved.

## Guard behavior
- Generic EOS collapse detection remains based on `generated_tail_len <= 2`, `last_token == EOS`, and `output_text_chars <= 8`.
- `[29899, 2]` variants should be detected because the guard no longer depends on the token before EOS.

## Mutation policy
- checkpoint_modified = false
- tokenizer_modified = false
- safetensors_modified = false
- lm_head_modified = false
- final_norm_modified = false
- ban_mask_modified = false

## Local validation required
Run:

```powershell
cargo build -p orchestrator_local --bin orchestrator_local
```

Then execute the SALAD-01C-B greeting probe and verify both:

- `.\workspace\salad01c_b_greeting_01_receipt.json`
- `.\workspace\salad01c_generation_receipt.json`

exist even if inference collapses or retry fails.
