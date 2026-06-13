# QW-TOK-FORGE-01-S2 Acceptance

## Status
`PENDING_LOCAL_CORPUS_REQUIRED_IN_CONTAINER_BAKE`

## Confirmed in bake
- [x] `--encode-corpus-pack` CLI dispatch added.
- [x] `--out-corpus-pack` option added.
- [x] Native tokenizer path uses `tokenizer_core::NativeTokenizer` + `TokenizerEngine::encode()`.
- [x] S2 does not introduce whitespace split fallback.
- [x] S2 does not introduce char-code fallback.
- [x] S2 does not force unknown token to zero.
- [x] QWCPK01 pack writer implemented.
- [x] token range receipt implemented.
- [x] encode error receipt implemented.
- [x] no-training receipt implemented.
- [x] checkpoint tensor read/write/training/gpu/decode remain blocked.

## Pending local verification
- [ ] `tokenizer_v5/corpus_v2/train/tokenizer_train_v5_dedup.txt` exists in local project root.
- [ ] pack generation completes.
- [ ] all token ids are within `0..48258`.
- [ ] pack sha256 is generated.
- [ ] `cargo check -p model_core --bin qw_tok_forge01_embed_lmhead_bootstrap` passes in a Rust-enabled environment.

## Container limitation
This container did not include `cargo`, and the baked archive did not include the large local corpus file. No fake PASS runtime receipt was generated.
