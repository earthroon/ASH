# 16AI-QW-38G-R6A-SALAD-01C-D-A Bake Report

## Status
PASS_STATIC_FINAL_RECEIPT_REBIND_BAKED_PENDING_LOCAL_CARGO_BUILD

## Source patch
16AI-QW-38G-R6A-SALAD-01C-D

## Purpose
Rebind the post-infer final SALAD receipt object as the single SSOT used for primary receipt, canonical receipt, and output artifact embedded receipt.

## Implemented
- Updated `SALAD01C_PATCH_ID` to `16AI-QW-38G-R6A-SALAD-01C-D-A`.
- Updated pre-infer status to `STARTED_SALAD01C_D_A_RECEIPT_WIRING`.
- Added `final_receipt_object_rebound`, `final_receipt_single_ssot`, and `primary_canonical_embedded_receipt_should_match`.
- Added a hard sync block immediately before output artifact write.
- Rewrites primary and canonical receipt paths after final receipt rebind.
- Re-inserts the rebound final receipt into `output_json["salad01c_receipt"]`.

## Non-mutation guarantee
checkpoint/tokenizer/safetensors/lm_head/final_norm/ban_mask are not modified.

## Local validation
Run:

```powershell
cargo build -p orchestrator_local --bin orchestrator_local
```

Then run `salad01c_d_a_greeting_01` and compare primary, canonical, and embedded receipts.
