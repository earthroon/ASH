# 16AI-QW-38G-R6A-R12A-R4 — Layer Component Attribution / Attention-MLP-Residual Origin Split Seal

## Patch Intent
- Split R3 layerwise candidates into attention / MLP / residual before-after component deltas.
- Preserve all model weights, tokenizer, safetensors, lm_head, final_norm, and ban mask.
- Keep root_cause_confirmed=false and route the next patch from measured component attribution.

## Implementation
- Adds R4 env gate and component trace writer in `native_wgpu.rs`.
- Adds layer 0 / layer 21 component-stage captures in `decode_state.rs`.
- Adds R4 runner and report/receipt generation.
