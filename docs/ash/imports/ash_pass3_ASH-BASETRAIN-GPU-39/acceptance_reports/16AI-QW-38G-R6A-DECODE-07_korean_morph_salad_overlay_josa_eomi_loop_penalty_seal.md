# 16AI-QW-38G-R6A-DECODE-07
## Korean Morph Salad Overlay / Josa-Eomi Loop Penalty Seal

status: PASS_STATIC_KOREAN_MORPH_SALAD_OVERLAY_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine
depends_on:
  - 16AI-QW-38G-R6A-DECODE-04
  - 16AI-QW-38G-R6A-DECODE-05
  - 16AI-QW-38G-R6A-DECODE-06

morph_policy_created_count: 1
allow_fixture_created_count: 1
josa_loop_fixture_created_count: 1
eomi_loop_fixture_created_count: 1
jamo_leak_fixture_created_count: 1
syllable_fragment_loop_fixture_created_count: 1
step_integrity_fail_fixture_created_count: 1

morph_receipt_created_count: 6
deterministic_key_created_count: 6

controlled_apply_enabled: true
probe_only: false
production_default_apply: false

allow_decision_count: 1
strong_penalty_decision_count: 2
recommend_rollback_decision_count: 2
step_integrity_skip_count: 1

josa_loop_detected_count: 1
eomi_loop_detected_count: 1
jamo_leak_detected_count: 1
syllable_fragment_loop_detected_count: 1

morph_penalized_count: 4
rollback_recommended_count: 2
reject_recommended_count: 0

runtime_decode_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0
transition_guard_executed_count: 6
morph_guard_executed_count: 6
rollback_executed_count: 0

decode04_risk_snapshot_extended: true
decode05_step_integrity_required: true
decode06_transition_guard_required: true

duplicate_receipt_key_count: 0
domain_ssot_mismatch_count: 0

## Canonical receipt keys

- allow: `q4sha256:d12c42af7dfdd6ff81553867aa9b9073e43d62314752de124231b7226d9b47de`
- josa_loop: `q4sha256:6751df0448f7fa53a3b84492e5ef3e80bad6ec277bf974d9f4503f79c6f5e270`
- eomi_loop: `q4sha256:ee6257cc2cceade85c2e9ebb67c4537084d0375d63ba4ba7d96eb2efed5f363c`
- jamo_leak: `q4sha256:b6823aba32c285dcc3d344b58ceb948d9df2d98ffc155b8e6b90c7ed974dfe6b`
- syllable_fragment_loop: `q4sha256:fe5d9adf864415399fce39f5a4ed14f04b37f3917e9f968981c2ee32fdf401ac`
- step_integrity_skip: `q4sha256:f41e87e78899acfea3fce1915ed1bb60b87c6b4c270c8b277e11d5d063ebf6fc`

## Scope seal

This patch does not execute runtime decode, model forward, real sampling, or rollback. It only executes fixture-bound Korean morph overlay receipts on top of DECODE-05 step integrity and DECODE-06 transition guard references.
