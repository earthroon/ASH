# 16AI-QW-38G-R6A-DECODE-12
## Reference-Free QE Adapter Stub / Source-Candidate Quality Slot Seal

status: PASS_STATIC_REFERENCE_FREE_QE_ADAPTER_STUB_CONTRACT
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

qe_adapter_config_created_count: 1
low_risk_fixture_created_count: 1
omission_risk_fixture_created_count: 1
hallucination_risk_fixture_created_count: 1
polarity_risk_fixture_created_count: 1
missing_source_fixture_created_count: 1
missing_final_gate_fixture_created_count: 1

qe_adapter_receipt_created_count: 6
deterministic_key_created_count: 6

pass_qe_stub_count: 1
review_recommended_count: 5
hard_fail_recommended_count: 0
skipped_missing_source_count: 1
skipped_final_gate_missing_count: 1

omission_risk_detected_count: 1
hallucination_risk_detected_count: 1
polarity_risk_detected_count: 1
number_mismatch_risk_detected_count: 1

adapter_mode: DeterministicStub
deterministic_stub_score_count: 6
external_model_allowed: false
external_model_executed_count: 0

runtime_decode_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0
qe_model_executed_count: 0
source_adequacy_executed_count: 0
glossary_constraint_executed_count: 0

decode11_final_gate_required: true
decode04_quality_receipt_qe_slot_extended: true

duplicate_receipt_key_count: 0
domain_ssot_mismatch_count: 0

## Canonical receipt keys

- low_risk: `q4sha256:63a55d9fdd5e216cf7d93f56c02f4fb70a54789d484e399d500419976305e3df`
- omission: `q4sha256:bf03fdc9431983c8fc9e672c205acc57b6d268c7afc5e9e184253dddf67fa256`
- hallucination: `q4sha256:ff01a6a638759c1e284afbfa7506abcdfbbe3cf22dc9e4b2be961e4fe92b9877`
- polarity: `q4sha256:63a62efe2f4c9074d3913a986c3467ae1b1d7a5ce7e55f269c2682d20659bb41`
- missing_source: `q4sha256:f0d3667123ad6ed8b9bd6a4fca8d9b091a49f61bc7977e55161937dd3edb539b`
- missing_final_gate: `q4sha256:11496a78a715decbb870bf4cb9beb0faf3a1e95f818519bceae7235a54f29055`
