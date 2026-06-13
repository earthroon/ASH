# ASH-FT-12 — Shadow Candidate Runtime Bind Dry-run / No Decode No Generation Seal

## SSOT

FT-12 binds the FT-11 approved staged shadow candidate into a temporary metadata-only runtime candidate slot. The slot is receipt-only and does not mutate runtime default or checkpoint aliases.

## Allowed

- Read FT-11 loader/header/tensor lookup/model contract/runtime guard receipts.
- Read-only shadow candidate path/hash validation.
- Create a temporary candidate slot receipt.
- Create metadata descriptor handles for required tensors.
- Create backend compatibility and no-decode guard receipts.

## Forbidden

- Actual model construction.
- GPU upload.
- Full model forward.
- Inference, decode, generation, sampling, KV cache creation.
- Runtime default apply, checkpoint alias rebind, promotion.
- Model/tokenizer mutation, optimizer state persist, training.

## Expected PASS

```txt
PASS_ASH_FT12_SHADOW_CANDIDATE_RUNTIME_BIND_DRYRUN_NO_DECODE_NO_GENERATION
```
