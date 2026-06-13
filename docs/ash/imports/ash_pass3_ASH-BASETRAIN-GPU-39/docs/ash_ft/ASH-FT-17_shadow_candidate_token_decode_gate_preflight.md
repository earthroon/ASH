# ASH-FT-17 — Shadow Candidate Token Decode Gate Preflight / No Text Output No Generation Seal

## SSOT

ASH-FT-17 starts only after `PASS_ASH_FT16_SHADOW_CANDIDATE_TOKEN_ID_SELECTION_SMOKE_NO_DECODE_NO_GENERATION`.

FT-16 selected `selected_token_id = 34196` as a receipt-only token id. FT-17 does not decode it, does not perform token string lookup, does not create decoded text, and does not enter generation. It only validates tokenizer artifact presence, vocab/range compatibility, selected-token entry presence by metadata/count preflight, special/reserved policy, and no-text-output guards.

## State ownership

- `artifacts/ash_ft/ash_ft17_token_decode_gate_plan.json`
- `artifacts/ash_ft/ash_ft17_tokenizer_lookup_preflight.json`
- `artifacts/ash_ft/ash_ft17_decode_policy_receipt.json`
- `artifacts/ash_ft/ash_ft17_special_token_decode_guard.json`
- `artifacts/ash_ft/ash_ft17_no_text_output_guard.json`
- `artifacts/ash_ft/ASH-FT-17_receipt.json`

## Allowed

- Read FT-16 receipt artifacts.
- Validate tokenizer manifest and tokenizer vocab paths.
- Verify model/tokenizer vocab size agreement.
- Verify selected token id is in range.
- Check tokenizer entry presence without exposing token string content.
- Write FT-17 receipts.

## Forbidden

- Token decode execution.
- Token string lookup execution.
- Decoded text creation or printing.
- Sequence commit.
- Generation loop entry.
- User prompt inference.
- Tokenizer mutation.
- Runtime default apply.
- Checkpoint alias rebind.
- Promotion.
- Train.

## Expected PASS

`PASS_ASH_FT17_SHADOW_CANDIDATE_TOKEN_DECODE_GATE_PREFLIGHT_NO_TEXT_OUTPUT_NO_GENERATION`

# ASH-FT-17 Acceptance

## Required previous receipt

`PASS_ASH_FT16_SHADOW_CANDIDATE_TOKEN_ID_SELECTION_SMOKE_NO_DECODE_NO_GENERATION`

## PASS conditions

1. FT-16 selection plan, selector execution, token range, reserved-token policy, and no-decode guard are read.
2. `selected_token_id = 34196` is confirmed from FT-16.
3. tokenizer manifest and tokenizer vocab paths exist.
4. `model_vocab_size == tokenizer_vocab_size == 48259`.
5. selected token id is inside `[0, 48258]`.
6. tokenizer entry presence is checked without exposing the token string.
7. no token decode executes.
8. no token string lookup executes.
9. no decoded text is created or printed.
10. no generation, runtime default apply, alias rebind, promotion, tokenizer mutation, or train executes.

## FAIL conditions

Any text output, decode, token string lookup, sequence commit, generation, runtime default mutation, or silent special-token pass fails this patch.
