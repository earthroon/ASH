# QW-52A-R3 Bake Report

## Result
Static bake completed.

## Added / modified
- Added Rust projection alignment probe module.
- Added Rust validator binary.
- Exported R3 probe types and helpers from model_core.
- Attached additive `cheonjiin_projection_alignment` field to QW-52A candidate awareness when projection bridge trace is available.
- Added static schema, receipt, validation result, bake report, and file digest manifest.

## Mutation policy
- decode policy mutation: false
- guard policy mutation: false
- lora scale mutation: false
- model weight mutation: false
- token ban added: false
- hidden state fusion: false
- residual stream mutation: false
- logit mutation: false
- sampler mutation: false
- adapter projection applied: false
- webgpu shader added: false
- python trace mutation: false
- python receipt mutation: false

## Validation
- static validation: PASS
- zip integrity: PASS
- cargo check: NOT RUN - cargo unavailable in bake environment
- runtime probe: NOT RUN - cargo unavailable in bake environment

## Next
- QW-52A-R4: Cheonjiin Adapter Gated Fusion Candidate / No Default Apply Seal
- QW-52B: Decode Detector Registry / Word Salad Risk Seal
