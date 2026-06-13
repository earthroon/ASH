# 16AI-QW-38G-R6A-DECODE-14
## Source Adequacy Guard / EN-KO Meaning Preservation Seal

status: PASS_STATIC_SOURCE_ADEQUACY_GUARD_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine
depends_on:
  - 16AI-QW-38G-R6A-DECODE-04
  - 16AI-QW-38G-R6A-DECODE-05
  - 16AI-QW-38G-R6A-DECODE-06
  - 16AI-QW-38G-R6A-DECODE-07
  - 16AI-QW-38G-R6A-DECODE-08
  - 16AI-QW-38G-R6A-DECODE-09
  - 16AI-QW-38G-R6A-DECODE-10
  - 16AI-QW-38G-R6A-DECODE-11
  - 16AI-QW-38G-R6A-DECODE-12
  - 16AI-QW-38G-R6A-DECODE-13

source_adequacy_policy_created_count: 1
adequacy_pass_fixture_created_count: 1
omission_fail_fixture_created_count: 1
hallucination_fail_fixture_created_count: 1
polarity_fail_fixture_created_count: 1
number_review_fixture_created_count: 1
entity_fail_fixture_created_count: 1
missing_span_receipt_fixture_created_count: 1

source_adequacy_receipt_created_count: 7
deterministic_key_created_count: 7

pass_adequacy_guard_count: 1
review_required_count: 2
reject_candidate_recommended_count: 3
rewrite_recommended_count: 1
glossary_gate_required_count: 1
missing_span_receipt_skip_count: 1

omission_meaning_loss_detected_count: 1
hallucination_meaning_drift_detected_count: 1
polarity_inversion_detected_count: 1
number_time_mismatch_detected_count: 1
named_entity_mismatch_detected_count: 1

candidate_reject_executed_count: 0
fallback_apply_executed_count: 0
rewrite_executed_count: 0
rollback_executed_count: 0

runtime_decode_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0
qe_model_executed_count: 0
external_adequacy_model_executed_count: 0
glossary_constraint_executed_count: 0

external_adequacy_model_allowed: false
external_adequacy_model_executed: false
production_default_apply: false

decode13_span_error_receipt_required: true
decode12_qe_receipt_required: true
decode11_final_gate_required: true
decode04_quality_score_adequacy_slot_extended: true

duplicate_receipt_key_count: 0
domain_ssot_mismatch_count: 0

canonical_receipt_keys:
  adequacy_pass: q4sha256:7c05d34d94994f564f31148e2e50125295ac2aca15b5c24a7a77d09aa51ad744
  omission_fail: q4sha256:e98f6d7e13af5255c45eb1ab0ba04ff9d721ff2850bfae0a2f579e787daec552
  hallucination_fail: q4sha256:ffabcf46d82fef96720cbef3b0be9c7e6d5030db09c7d6e96549acc4306c7965
  polarity_fail: q4sha256:74673bc8c7ebe340c43ac355fd3f7e58a08b75ce623f753012060cf75a16a1ec
  number_review: q4sha256:fbe1eab4cc7adac807487ee7bdb37f1aac6b866809e67b67a427a4cffd60d711
  entity_fail: q4sha256:0e04524d9fb789054b92462b30c2dde7bfef316aa08c178dc5c616562de3668c
  missing_span_receipt: q4sha256:f0c975755cbe22e5b90eacc0f8f634f5014771bd4372f1504112324b2318d0be

No rewrite, rollback, candidate rejection, fallback apply, COMET/xCOMET, LLM judge, model forward, sampling, or glossary constraint is executed by this patch.
