# QW-TOK-FORGE-01-S3 Acceptance

## PASS

1. `ash_v5_native_genesis.forge00.safetensors` is the input checkpoint.
2. `qw_tok_forge01_s2_encoded_corpus_pack.bin` is the input corpus pack.
3. CPU/F32 sampled context training executes.
4. `model.embed_tokens.weight` is updated.
5. `lm_head.weight` is updated.
6. Transformer block update is false.
7. Attention update is false.
8. FFN update is false.
9. Norm update is false.
10. Rotary mutation is false.
11. Loss curve receipt is generated.
12. Row norm receipt is generated.
13. Mutation scope receipt is generated.
14. No-transformer-update receipt is generated.
15. Candidate checkpoint is written only with approval.
16. Forge00 input checkpoint is not overwritten.

## PARTIAL

1. Dry-run training plan only.
2. Local forge00 checkpoint is missing in the bake environment.
3. Local S2 corpus pack is missing in the bake environment.
4. Training executes but checkpoint write approval is absent.
5. Loss receipt exists but candidate checkpoint is not produced.

## FAIL

1. Any legacy TRAIN/resized/rebound checkpoint path is used.
2. S2 corpus pack is bypassed by raw corpus re-encoding.
3. Transformer/attention/FFN/norm/rotary bytes are intentionally mutated.
4. Loss becomes NaN/Inf.
5. Forge00 input checkpoint is overwritten.
6. Candidate checkpoint is written without approval.
7. GPU kernel or decode generation is executed.
