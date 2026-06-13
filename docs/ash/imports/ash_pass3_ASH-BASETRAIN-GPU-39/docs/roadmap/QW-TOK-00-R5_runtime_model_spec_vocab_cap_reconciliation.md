# QW-TOK-00-R5 Roadmap Note

R5 is the vocab-cap reconciliation ledger. It does not fix the system; it names the mismatch surface.

## Inputs

1. Tokenizer final manifest vocab size
2. Local tokenizer artifact hash parity
3. Model config vocab size
4. Embedding row count
5. LMHead row count or explicit tied contract
6. Runtime vocab cap
7. Native vocab projection cap
8. Max token id allowed
9. Checkpoint spec vocab
10. Runtime spec vocab

## Next

If values remain unknown, proceed to `QW-TOK-00-R6 Runtime Vocab Cap Evidence Collector / Operator Path Probe Seal`.
If all values are known and match, proceed to `QW-TOK-01 Tokenizer V5 Encode Decode Fixture / Special Token Roundtrip Seal`.
