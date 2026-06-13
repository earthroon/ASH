# ASH-FT-16 Runtime Note

FT-16 is the first stage that may produce a token id number. It still must not translate that id through the tokenizer, render decoded text, append it to a generation sequence, or enter a generation loop.

The implementation uses a deterministic receipt-only selector smoke based on the source/shadow checksums and synthetic boundary metadata. This keeps the stage reproducible while preserving the no-decode/no-generation seal.
