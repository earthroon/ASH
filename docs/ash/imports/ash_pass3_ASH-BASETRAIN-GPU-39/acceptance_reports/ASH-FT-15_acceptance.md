# ASH-FT-15 Acceptance

Acceptance requires:

1. FT-14 compare plan, source numeric, shadow numeric, delta compare, and no-token-selection guard are read.
2. Source and shadow candidates are read-only hash checked.
3. Model vocab size equals tokenizer vocab size.
4. Valid token id range is `[0, vocab_size - 1]`.
5. Selector policy candidates are defined.
6. Token selection, argmax, top-k, top-p, temperature sampling, decode, decoded text, generation, runtime default apply, alias rebind, promotion, and train are all false.
7. The next-stage approval candidate is emitted for ASH-FT-16.
