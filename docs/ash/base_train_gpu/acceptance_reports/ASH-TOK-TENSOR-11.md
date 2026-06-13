# ASH-TOK-TENSOR-11 Acceptance Report

## PASS

`PASS_ASH_TOK_TENSOR_11_TOKENIZER_TENSOR_ADAPTER_BASETRAIN_BIND_CANDIDATE_ADAPTER_INPUT_ROUTE_NO_FULL_MODEL_APPLY`

## Scope

BaseTrain now has a tokenizer tensor adapter input-route candidate seal. The route transports `[B,T,F]` tokenizer tensor features plus feature masks as a candidate only. Adapter output is not applied to model hidden state in this patch.

## Closed

- full model apply
- AshModel / transformer / generation forward
- optimizer step
- base or adapter weight commit
- safetensors mutation
- silent feature zero-fill
- silent position shift correction
- side-channel metadata fallback
