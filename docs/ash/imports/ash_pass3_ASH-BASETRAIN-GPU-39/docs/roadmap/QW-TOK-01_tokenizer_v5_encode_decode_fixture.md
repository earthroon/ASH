# QW-TOK-01 Roadmap

1. Load tokenizer_v5.model with a SentencePiece-compatible loader.
2. Confirm piece_size == 48259.
3. Validate required task/lang/cue/QWave/DeltaK special tokens as atomic pieces.
4. Run encode/decode fixture cases.
5. Check byte fallback tail and rare unicode roundtrip.
6. Keep runtime decode bind and model inference blocked.

Next: `QW-TOK-02 Tokenizer V5 Runtime Input Binding Dry-run / No Model Inference Seal`.
