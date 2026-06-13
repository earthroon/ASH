# ASH-FT-18 Acceptance

Expected verdict:

```txt
PASS_ASH_FT18_SHADOW_CANDIDATE_CONTROLLED_TOKEN_DECODE_SMOKE_NO_GENERATION_NO_SEQUENCE_COMMIT
```

Acceptance requires:

- FT-16 selector execution, token id range, and reserved-token receipts are present and clean.
- FT-17 decode gate, tokenizer lookup, decode policy, special-token guard, and no-text-output guard are present and clean.
- `selected_token_id` equals `34196`.
- Tokenizer manifest and vocab files exist.
- Controlled single-token decode executes once.
- Token string lookup executes once.
- Decoded token exists, is UTF-8 valid, non-empty, and has a SHA256 checksum.
- Decoded text output remains false.
- Sequence commit remains false.
- Generation and sampling remain false.
- Runtime default apply, checkpoint alias rebind, promotion, tokenizer mutation, and train remain false.
