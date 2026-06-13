# QW-52B-M2 — Self Echo / Reflection Lock Detector Seal

## Status
PASS_STATIC_SELF_ECHO_DETECTOR

## Base
QW-52B-M1

## Purpose
A trace-only detector was added to detect output self-reflection loops.

## Added Detector
- SelfEchoDetector

## Confirmed
- Token echo is recorded.
- Piece echo is recorded.
- N-gram echo is recorded.
- QWave echo is recorded when available.
- Contextless reentry is recorded as evidence only.
- Missing recent window becomes Unavailable.
- No runtime behavior changes.

## Fixture Results
- normal_non_echo_output: PASS / Low
- piece_echo_loop_output: PASS / High
- contextless_reentry_attractor: PASS / Medium
- missing_recent_window: PASS / Unavailable

## Mutation Policy
- runtime_apply = false
- hidden_state_mutation = false
- logit_mutation = false
- sampler_mutation = false
- token_rank_mutation = false
- token_selection_mutation = false
- token_ban = false

## Notes
SelfEchoDetector separates output self-reflection from input-output mirror resonance.
Normal words are not banned; contextless reentry is evidence only.

## Next
QW-52B-M3 — Residual Loop Eligibility Trace / Decay Threshold Seal
