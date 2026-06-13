# 16AI-QW-38G-R6A-DECODE-09
## N-best Subtitle Candidate Pool / Multi-Profile Decode Seal

status: PASS_STATIC_NBEST_CANDIDATE_POOL_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine
depends_on:
  - 16AI-QW-38G-R6A-DECODE-04
  - 16AI-QW-38G-R6A-DECODE-05
  - 16AI-QW-38G-R6A-DECODE-06
  - 16AI-QW-38G-R6A-DECODE-07
  - 16AI-QW-38G-R6A-DECODE-08

source_cue_fixture_created_count: 1
multi_profile_decode_plan_created_count: 1
candidate_pool_fixture_created_count: 1
duplicate_negative_fixture_created_count: 1
retry_request_linked_fixture_created_count: 1

default_profile_count: 5
retry_linked_profile_count: 6

candidate_pool_receipt_created_count: 3
candidate_quality_receipt_created_count: 11
deterministic_key_created_count: 3

pool_ready_for_rerank_count: 2
pool_not_ready_duplicate_count: 1
duplicate_candidate_detected_count: 1

final_candidate_selected_count: 0
rerank_applied_count: 0

runtime_decode_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0

decode04_quality_receipt_required: true
decode08_retry_request_supported: true

duplicate_receipt_key_count: 0
domain_ssot_mismatch_count: 0

canonical_receipt_keys:
  valid_pool: q4sha256:33fef3dbbaf646a6ebedd679b6a2e12cb0217b1ed42eff29096af188c774cf9c
  duplicate_negative_pool: q4sha256:e95a3c843819ca4a482f364b49a9d8c5ce0097652acf9cdba2a51a0dbe01ee42
  retry_linked_pool: q4sha256:bff8650392886338308a6b080d865d834d9c3bbbf2dbe35bf234e91f9369ccdb
