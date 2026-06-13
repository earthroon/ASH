# QW-TOK-MAP-12 Acceptance Report

## Patch

QW-TOK-MAP-12  
First Attention Compute Probe / No LMHead Seal

## Result

PARTIAL_QW_TOK_MAP12_ATTENTION_COMPUTE_PREFLIGHT_ONLY

## Confirmed

- MAP-11 dependency status was read as `PARTIAL_QW_TOK_MAP11_SHAPE_ONLY_ATTENTION_DRYRUN_CONTRACT`.
- Current bake remains preflight-only because upstream is not value-backed PASS.
- Attention config source remains `specs/model_spec_v5_48259.toml`.
- Q/K/V shape readiness is recorded for `[3, 32, 2048]` with 32 query heads and 4 KV heads.
- Q/K/V projection compute was not executed.
- Attention score compute was not executed.
- Mask application and softmax were not executed.
- Attention context values were not created.
- lm_head projection was not executed.
- Logits, sampler, token selection, and generation were not used.
- Full transformer block forward was not claimed.
- Checkpoint write and model weight mutation were not used.

## Next

QW-TOK-MAP-12-R1 or local rerun: value-backed attention compute after MAP-08/09/10/11 PASS.  
Then QW-TOK-MAP-13: First Block Forward Probe / No Logits Seal.
