# ASH-FT-14 — Shadow Candidate Logit Compare Probe / No Token Selection No Generation Seal

## SSOT

ASH-FT-14 compares source and shadow candidate numeric forward/logit proxy outputs using the same bounded synthetic input inherited from ASH-FT-13.

## State ownership

- `artifacts/ash_ft/ash_ft14_logit_compare_plan.json`
- `artifacts/ash_ft/ash_ft14_source_forward_numeric_receipt.json`
- `artifacts/ash_ft/ash_ft14_shadow_forward_numeric_receipt.json`
- `artifacts/ash_ft/ash_ft14_logit_delta_compare_receipt.json`
- `artifacts/ash_ft/ash_ft14_no_token_selection_guard.json`
- `artifacts/ash_ft/ASH-FT-14_receipt.json`

## Allowed

- Read FT-13 receipts.
- Read source and shadow candidates read-only.
- Reuse FT-13 synthetic input.
- Produce source/shadow numeric forward proxy receipts.
- Compute checksum, finite stats, delta norm, relative L2 drift, mean shift.

## Forbidden

- Token selection.
- Argmax.
- Top-k/top-p/temperature sampling.
- Token decode.
- Decoded text creation.
- Generation.
- User prompt inference.
- Runtime default apply.
- Checkpoint alias rebind.
- Promotion.
- Train.

## Expected verdict

`PASS_ASH_FT14_SHADOW_CANDIDATE_LOGIT_COMPARE_PROBE_NO_TOKEN_SELECTION_NO_GENERATION`
