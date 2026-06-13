# 16AI-QW-38G-R6A-DECODE-11
## Salad-Aware Candidate Rejection / Degeneration Risk Final Gate Seal

status: PASS_STATIC_DEGENERATION_RISK_FINAL_GATE_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine
depends_on:
  - 16AI-QW-38G-R6A-DECODE-04
  - 16AI-QW-38G-R6A-DECODE-05
  - 16AI-QW-38G-R6A-DECODE-06
  - 16AI-QW-38G-R6A-DECODE-07
  - 16AI-QW-38G-R6A-DECODE-08
  - 16AI-QW-38G-R6A-DECODE-09
  - 16AI-QW-38G-R6A-DECODE-10

degeneration_policy_created_count: 1
accept_fixture_created_count: 1
selected_salad_reject_fixture_created_count: 1
morph_loop_reject_fixture_created_count: 1
transition_hard_risk_reject_fixture_created_count: 1
fallback_candidate_fixture_created_count: 1
all_unsafe_review_fixture_created_count: 1
surface_missing_skip_fixture_created_count: 1

final_gate_receipt_created_count: 7
deterministic_key_created_count: 7

accept_selected_candidate_count: 1
reject_selected_candidate_count: 3
fallback_candidate_selected_count: 1
review_required_count: 2
surface_missing_skip_count: 1

salad_hard_threshold_detected_count: 3
morph_loop_hard_threshold_detected_count: 2
transition_hard_risk_detected_count: 2
byte_or_mojibake_risk_detected_count: 2

runtime_decode_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0
qe_model_executed_count: 0
source_adequacy_executed_count: 0
glossary_constraint_executed_count: 0

decode10_surface_rerank_required: true
decode04_quality_receipt_required: true
decode06_transition_risk_supported: true
decode07_morph_risk_supported: true
decode08_recovery_risk_supported: true

duplicate_receipt_key_count: 0
domain_ssot_mismatch_count: 0

## Canonical receipt keys

- accept: q4sha256:5733624f19b98ce0f51edac2fb6a7ad8326736b8e0ef4b56c458e7af5029fe58
- selected_salad_reject: q4sha256:6a6be7d2808cee3f02f727d4fbfdd170c9768a197f10f0e4b4e02839e4386521
- morph_loop_reject: q4sha256:46ead68eab19e2939e301e95bf5c9c2f06f1f06d23eb33d54e719ec9c698ad2a
- transition_hard_risk_reject: q4sha256:b7a9d7aef9b5421e81270dd65f575793a4a735c5fb57abe2f4aa564cccf6cdb8
- fallback_candidate: q4sha256:572fc61209a5b7bee4449b2f8458acac0e5cf88aa2f75de39b6bbd9b7fde5af5
- all_unsafe_review: q4sha256:103ad7cf034fcb74c14815bee4a48e688f41e8fbf97cd5961bc6965cc0750657
- surface_missing_skip: q4sha256:45d5aa0945831ffed3c6d922a38f9271476404759ea8885ebeb129adb3efca81

## Runtime boundary

No model forward, real sampling, QE, source adequacy, glossary constraint, retry decoding, or rollback execution is performed by this seal.
