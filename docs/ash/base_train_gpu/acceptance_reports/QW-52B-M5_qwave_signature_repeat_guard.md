# QW-52B-M5 — QWave Signature Repeat Guard / Diversity Hash Trace Seal

## Status
PASS_STATIC_QWAVE_SIGNATURE_REPEAT_GUARD

## Base
QW-52B-M4

## Purpose
A trace-only structural diversity hash detector was added to record token, piece, QWave signature, CJI XYZ, and transition repeat patterns.

## Added Detector
- QWaveSignatureRepeatGuard

## Confirmed
- Token n-gram hash repetition is recorded.
- Piece n-gram hash repetition is recorded.
- QWave signature repetition is recorded when available.
- Transition hash repetition is recorded when available.
- Missing structural traces become Unavailable or Partial.
- No runtime behavior changes.

## Fixture Results
- normal_diverse_signature_window: PASS / risk_level = None
- surface_piece_repeat_guard: PASS / risk_level = High
- qwave_signature_repeat_without_piece_repeat: PASS / risk_level = Critical
- transition_ping_pong_repeat: PASS / risk_level = Critical
- missing_all_hash_inputs: PASS / risk_level = Unavailable

## Mutation Policy
- runtime_apply = false
- hidden_state_mutation = false
- logit_mutation = false
- sampler_mutation = false
- token_rank_mutation = false
- token_selection_mutation = false
- token_ban = false
- memory_mutation = false

## Language Policy
- frontend_js_ts_allowed = true
- desktop_js_ts_allowed = true
- crate_js_ts_allowed = false
- detector_language = Rust
- validator_language = Rust
- patch_added_crate_js_ts_files = []

## Next
QW-52B-M6 — Stable Phrase / Quarantine Memory Receipt Seal
or
QW-52B-C1 — Cheonjiin XYZ Tensor Projection / Candidate Structural Map Seal
