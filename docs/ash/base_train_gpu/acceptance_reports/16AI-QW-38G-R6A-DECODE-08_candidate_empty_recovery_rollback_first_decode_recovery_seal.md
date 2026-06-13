# 16AI-QW-38G-R6A-DECODE-08
## Candidate Empty Recovery / Rollback-First Decode Recovery Seal

status: PASS_STATIC_ROLLBACK_FIRST_RECOVERY_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine
depends_on:
  - 16AI-QW-38G-R6A-DECODE-04
  - 16AI-QW-38G-R6A-DECODE-05
  - 16AI-QW-38G-R6A-DECODE-06
  - 16AI-QW-38G-R6A-DECODE-07

recovery_policy_created_count: 1
candidate_empty_fixture_created_count: 1
morph_rollback_fixture_created_count: 1
top1_recovery_block_fixture_created_count: 1
safe_eos_fixture_created_count: 1
step_integrity_fail_fixture_created_count: 1

candidate_recovery_receipt_created_count: 5
deterministic_key_created_count: 5

rollback_first_enabled: true
global_top1_recovery_allowed: false
production_default_apply: false

rollback_retry_requested_count: 2
top1_recovery_blocked_count: 1
safe_eos_recommended_count: 1
step_integrity_skip_count: 1

rollback_anchor_created_count: 2
strict_retry_profile_created_count: 2
retry_request_created_count: 2

runtime_decode_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0
rollback_executed_count: 0

decode04_risk_snapshot_extended: true
decode05_step_integrity_required: true
decode06_transition_guard_required: true
decode07_morph_receipt_supported: true

duplicate_receipt_key_count: 0
domain_ssot_mismatch_count: 0

canonical_receipt_keys:
  candidate_empty: q4sha256:82db2dc4669fdf13a3f864060e0511485b79fcdfe6409f0c41f99f90ba687e00
  morph_rollback: q4sha256:53fdef489bdb592e088ec0bc28fea23c075af8e66d83a46d84931a8462b9203f
  top1_recovery_block: q4sha256:273c56997bd898065f0990d1e984b7a5e90ad9a86a82f7731c9d9602ecfbdf98
  safe_eos: q4sha256:15b45b8657a668d907fe566ae6087f156c7b060cdc6b2f42cbcbde11ec45ad7b
  step_integrity_fail: q4sha256:653133f349a7407f7f6b3224ff285fde22a6d20f054ed0e68beb7055ac58bde8

notes:
  - DECODE-08 creates rollback anchors and retry requests only.
  - It never executes model forward, real sampling, or live rollback mutation.
  - Global top1 recovery is explicitly blocked by policy.
