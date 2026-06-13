# 16AI-6W-1 Byte Token Logit Attribution Probe

## Purpose

Trace why `<0x63>` is selected by the decoder by recording selected token id, selected piece, top-k logits, byte-like token rank, and baseline/v6 pair decisions.

## Contract

- Does not suppress byte tokens.
- Does not mutate output text.
- Does not change tokenizer/vocab/checkpoint.
- Uses `16AI-6V-5-R3` and `16AI-6V-5-R1` as source gates.

## Expected status

`PASS_BYTE_TOKEN_LOGIT_ATTRIBUTION` means attribution logs were produced, not that byte leak was fixed.
