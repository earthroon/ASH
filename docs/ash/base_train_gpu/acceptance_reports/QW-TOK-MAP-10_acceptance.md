# QW-TOK-MAP-10 Acceptance Report

## Patch

QW-TOK-MAP-10  
First Transformer Block Input Contract / No Attention Kernel Execution Seal

## Result

PARTIAL_QW_TOK_MAP10_SHAPE_ONLY_BLOCK_INPUT_CONTRACT

## Confirmed

- MAP-09 transformer input bridge was accepted as dependency: true
- MAP-09 dependency status: `PARTIAL_QW_TOK_MAP09_SHAPE_ONLY_BRIDGE`
- hidden_states descriptor was loaded
- hidden_states shape matched `[3, 32, 2048]`
- hidden_states layout was `batch_seq_hidden`
- hidden_states materialized: false
- attention_mask shape matched `[3, 32]`
- attention_mask broadcast candidate shape matched `[3, 1, 1, 32]`
- position_ids shape matched `[3, 32]`
- rotary input contract descriptor was recorded
- block_index was fixed to `0`
- block 0 input contract packet was created
- dtype/backend route receipt was created as `cpu_contract_probe`
- attention kernel was not executed
- Q/K/V projection was not executed
- attention score tensor was not created
- hidden_states were not mutated
- transformer forward was not executed
- lm_head projection was not executed
- sampler was not executed
- token generation was not executed
- checkpoint write was not used
- model weight mutation was not used

## Notes

- This is a shape-only block input contract because MAP-09 is partial.
- Actual embedding-backed block input PASS requires MAP-08 PASS and MAP-09 PASS on the local checkpoint path.
- Cargo/rustc were not available in this container, so local cargo test remains required.

## Next

QW-TOK-MAP-11  
Attention Kernel Dry-run Shape Contract / No Value Mutation Seal
