# ASH-FT-13 Acceptance

## Required checks

- FT-12 runtime bind plan is read.
- FT-12 candidate slot receipt is PASS.
- FT-12 backend compatibility is PASS.
- FT-12 required handle lookup is PASS.
- FT-12 no-decode guard is clean.
- Shadow candidate exists and sha256 matches expected or auto-observed hash.
- Synthetic input is bounded and does not use a user prompt.
- Output shape receipt is generated.
- Forward finite receipt is PASS.
- No decode/sampling/generation guard is PASS.

## Guard checks

- `token_decode_executed = false`
- `token_selection_executed = false`
- `sampling_executed = false`
- `generation_executed = false`
- `decoded_text_created = false`
- `runtime_default_apply_executed = false`
- `checkpoint_alias_rebind_executed = false`
- `promotion_executed = false`
- `train_executed = false`
