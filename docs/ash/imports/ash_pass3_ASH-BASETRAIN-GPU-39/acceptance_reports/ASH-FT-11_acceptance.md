# ASH-FT-11 Acceptance

## PASS criteria

- FT-10 header/tensor map/source unchanged/promotion block receipts are read and PASS.
- Shadow candidate exists and sha256 matches the expected value, or `auto` is explicitly used for read-only observed hash sealing.
- Shadow safetensors header and tensor map parse successfully.
- `model.embed_tokens.weight` and `lm_head.weight` are found.
- Embed and LM head shapes match `[48259, 2048]` under the default contract.
- Metadata-only load remains true.
- Actual model construction, GPU upload, inference, decode/generation, runtime default apply, alias rebind, promotion, and train remain false.

## Artifact rule

Runtime `artifacts/ash_ft/*.json` outputs are not included in this baked zip. They must be generated locally by running the bin target.
