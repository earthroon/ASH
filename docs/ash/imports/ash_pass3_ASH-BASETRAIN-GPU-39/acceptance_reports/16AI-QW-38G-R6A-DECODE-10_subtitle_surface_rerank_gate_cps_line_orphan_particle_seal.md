# 16AI-QW-38G-R6A-DECODE-10
## Subtitle Surface Rerank Gate / CPS-Line-Orphan Particle Seal

status: PASS_STATIC_SUBTITLE_SURFACE_RERANK_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine
depends_on:
  - 16AI-QW-38G-R6A-DECODE-04
  - 16AI-QW-38G-R6A-DECODE-05
  - 16AI-QW-38G-R6A-DECODE-06
  - 16AI-QW-38G-R6A-DECODE-07
  - 16AI-QW-38G-R6A-DECODE-08
  - 16AI-QW-38G-R6A-DECODE-09

surface_rerank_policy_created_count: 1
valid_surface_fixture_created_count: 1
orphan_particle_fixture_created_count: 1
cps_overflow_fixture_created_count: 1
pool_not_ready_fixture_created_count: 1
all_rejected_fixture_created_count: 1

surface_rerank_receipt_created_count: 5
deterministic_key_created_count: 5

rerank_applied_count: 4
final_candidate_selected_count: 3
review_required_count: 2

pool_not_ready_skip_count: 1
all_rejected_no_selection_count: 1

cps_overflow_detected_count: 1
orphan_particle_detected_count: 1
line_length_penalty_applied_count: 2
line_balance_penalty_applied_count: 1
repeated_punctuation_penalty_applied_count: 0

runtime_decode_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0
qe_model_executed_count: 0

decode09_candidate_pool_required: true
decode04_quality_receipt_score_slot_extended: true

duplicate_receipt_key_count: 0
domain_ssot_mismatch_count: 0

## Canonical receipt keys

valid_surface: q4sha256:eefe2f57d0ab209b254f0761bd2716fb4965117c280565bc234e5d7387f9f452
orphan_particle: q4sha256:6880470c27f16c07bea6c1b6dd8b4013e9b58385b60f789c2826f4322a5835d9
cps_overflow: q4sha256:f1318d2be8465f64e5ea70fd69d187dc2f3078a0ff1dfba7ebbcb68efbaea9ae
pool_not_ready: q4sha256:f97eab1fcea156a2b2ac3fc5de8187e18708c7972b92115de9276408e8d167f7
all_rejected: q4sha256:e4fa32279e81fcd30ce888d825bf0b2aa16b56fcdc152f9b689fa4339036e052
