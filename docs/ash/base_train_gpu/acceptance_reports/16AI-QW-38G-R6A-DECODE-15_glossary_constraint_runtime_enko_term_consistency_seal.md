# 16AI-QW-38G-R6A-DECODE-15
## Glossary Constraint Runtime / EN-KO Term Consistency Seal

status: PASS_STATIC_GLOSSARY_CONSTRAINT_CONTRACT
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
  - 16AI-QW-38G-R6A-DECODE-14

glossary_policy_created_count: 1
glossary_registry_fixture_created_count: 1
glossary_receipt_created_count: 7
deterministic_key_created_count: 7

pass_glossary_constraint_count: 1
review_required_count: 3
reject_candidate_recommended_count: 2
rewrite_recommended_count: 1
missing_glossary_registry_skip_count: 1

required_term_missing_detected_count: 1
wrong_target_term_used_detected_count: 1
forbidden_alias_used_detected_count: 1
variant_term_used_detected_count: 1
named_entity_mismatch_detected_count: 1

candidate_reject_executed_count: 0
rewrite_executed_count: 0
fallback_apply_executed_count: 0
rollback_executed_count: 0

runtime_decode_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0
external_glossary_lookup_executed_count: 0

decode14_source_adequacy_receipt_required: true
decode04_quality_score_glossary_slot_extended: true

duplicate_receipt_key_count: 0
domain_ssot_mismatch_count: 0

## Canonical receipt keys

- glossary_pass: `q4sha256:f7adee191f8eabe754e604d73823a028886127c979fd2af7e7a6068a0e00c7ca`
- required_term_missing: `q4sha256:d4723c9bd37595dfef1bc657a224317424b6cfb42b7f10a2c5685c6c8ac060cd`
- wrong_term: `q4sha256:5ddb5a9c8611a36d6b8c5120366d330d2a2644b815c79356bc81d093693dd712`
- forbidden_alias: `q4sha256:e045a45e8c180946c136ab38183a6ef46ee8f025b2921615bcfe6e68a97221e7`
- optional_term_review: `q4sha256:0f74c1a4a99ef250997eb786441634f8d4f08d3bc8735b239b0ac43a956e5eef`
- named_entity_gate: `q4sha256:06efbc846468d1c413e2d9caac16c717c5cd75c358cfdb067ee9b02ba5d51d10`
- missing_glossary_registry: `q4sha256:a373b0a7af73b5d82d040790d88bc7ac50d7b0a6e68fc9a84e05f0e053671ae6`

## Static boundary

This patch creates glossary constraint policy, static glossary registry, source/target term match snapshots, violation snapshots, and glossary constraint receipts. It does not execute candidate rewrite, reject, fallback, rollback, real sampling, model forward, or external glossary lookup.
