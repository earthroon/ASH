# QW-TOK-MAP-11 Acceptance Report

## Patch

QW-TOK-MAP-11  
Attention Kernel Dry-run Shape Contract / No Value Mutation Seal

## Result

PARTIAL_QW_TOK_MAP11_SHAPE_ONLY_ATTENTION_DRYRUN_CONTRACT

## Confirmed

- MAP-10 first block input contract was accepted as dependency status: PARTIAL_QW_TOK_MAP10_SHAPE_ONLY_BLOCK_INPUT_CONTRACT
- block_index was fixed to 0
- hidden_states shape was loaded as [3, 32, 2048]
- attention config source was specs/model_spec_v5_48259.toml
- attention head config was resolved as num_attention_heads=32, num_key_value_heads=4, head_dim=64
- Q projection shape candidate was created as q_reshaped_shape=[3, 32, 32, 64]
- K/V projection shape candidates were created as k_shape=[3, 4, 32, 64], v_shape=[3, 4, 32, 64]
- attention score shape candidate was created as [3, 32, 32, 32]
- attention mask broadcast compatibility was checked
- causal mask shape candidate was created as [1, 1, 32, 32]
- rotary shape candidate was recorded without rotary compute
- KV cache shape candidate was created without allocation or mutation
- dispatch dimension dry-run was recorded without WGPU dispatch
- Q/K/V projection compute was not executed
- attention score compute was not executed
- softmax was not executed
- KV cache was not allocated or mutated
- hidden_states were not mutated
- WGPU dispatch was not executed
- transformer forward was not executed
- lm_head projection was not executed
- sampler was not executed
- token generation was not executed
- checkpoint write was not used
- model weight mutation was not used

## Next

QW-TOK-MAP-12  
First Attention Compute Probe / No LMHead Seal
