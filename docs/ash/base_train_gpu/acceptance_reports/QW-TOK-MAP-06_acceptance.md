# QW-TOK-MAP-06 Acceptance

- PASS: model input packet batch built.
- PASS: all input ids are in 0..48258.
- PASS: attention mask and position ids contracts pass.
- PASS: no embedding lookup, transformer forward, lm_head logits, sampler, or token generation.
- PASS: no runtime persistent apply or artifact mutation.
