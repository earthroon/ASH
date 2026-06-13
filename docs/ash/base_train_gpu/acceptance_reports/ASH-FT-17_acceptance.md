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
