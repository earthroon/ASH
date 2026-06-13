# Commit 16W Bake Report

SSOT: FFN = down_proj(SiLU(gate_proj(normed)) * up_proj(normed)).

Patched file:
- crates/model_core/src/lib.rs

Applied changes:
- Added silu_tensor<B, const D>(x) = x * sigmoid(x).
- Replaced FFN gate sigmoid paths in AshDecoderBlock::forward.
- Replaced FFN gate sigmoid paths in AshDecoderBlock::forward_prepared.
- Replaced FFN gate sigmoid paths in NativeLoadedModel::forward_block_prefill.
- Replaced FFN gate sigmoid paths in NativeLoadedModel::forward_block_decode.

Validation:
- grep gate= sigmoids: no FFN gate sigmoid matches expected.
- cargo check was not run in this container because cargo is unavailable.
