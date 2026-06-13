# ASH-FT-16 Acceptance

Expected PASS:

```txt
PASS_ASH_FT16_SHADOW_CANDIDATE_TOKEN_ID_SELECTION_SMOKE_NO_DECODE_NO_GENERATION
```

Acceptance checks:

1. FT-15 receipts are read and verified.
2. Source and shadow candidate files are read-only hash checked.
3. Model/tokenizer vocab sizes match.
4. Deterministic selector creates a receipt-only token id.
5. Token id is within `[0, vocab_size - 1]`.
6. Token id is not committed.
7. Token decode/string lookup/text generation remain false.
8. Runtime default apply, alias rebind, promotion, and train remain false.
