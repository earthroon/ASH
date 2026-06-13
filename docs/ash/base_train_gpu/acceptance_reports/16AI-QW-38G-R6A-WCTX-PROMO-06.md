# 16AI-QW-38G-R6A-WCTX-PROMO-06

## Title

RT00 Real Forward Receipt Rebind / No Mock20 Receipt Substitution Seal

## SSOT

- Domain: `en_to_ko_translation_subtitle_machine`
- State owner: `ash_core::word_context_promo_06_rt00_real_forward_receipt_rebind`
- Upstream evidence: `PROMO-04` real forward dry probe + `PROMO-05` real top-k trace
- Rebind target: `WCTX-RT-00` forward dry probe receipt

## Acceptance

`PASS_WCTX_PROMO_06_RT00_REAL_FORWARD_RECEIPT_REBIND_NO_MOCK20_RECEIPT_SUBSTITUTION`

## Sealed contract

- `mock20_shape_reference_allowed = true`
- `mock20_substitution_allowed = false`
- `rt00_rebind_allowed = true`
- `rt00_rebind_executed = true`
- `rt00_receipt_key_created = true`
- `rt00_receipt_key_unique_from_mock20 = true`
- `rt00_receipt_digest_matches_rebind_sources = true`
- `selected_token_id_present = false`
- `token_selection_executed = false`
- `decode_executed = false`
- `candidate_text_created = false`
- `rt01_receipt_created = false`
- `runtime_apply_allowed = false`

## Matrix

- Positive cases: 4
- Negative cases: 54
- Total cases: 58

## Static status

`BAKED_STATIC_NO_CARGO`
