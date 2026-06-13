# 16AI-QW-38G-R6A-DECODE-12 Bake Report

- status: PASS_STATIC_REFERENCE_FREE_QE_ADAPTER_STUB_CONTRACT
- base: ash_pass3_16AI-QW-38G-R6A-DECODE-11_salad_aware_candidate_rejection_degeneration_risk_final_gate_seal_baked.zip
- output: ash_pass3_16AI-QW-38G-R6A-DECODE-12_reference_free_qe_adapter_stub_source_candidate_quality_slot_seal_baked.zip
- domain_ssot: en_to_ko_translation_subtitle_machine

## Added modules

- `reference_free_qe_adapter.rs`
- `reference_free_qe_input.rs`
- `reference_free_qe_score.rs`
- `reference_free_qe_stub.rs`
- `reference_free_qe_receipt.rs`

## Boundary

- External COMET/xCOMET/LLM judge execution: not executed.
- Model forward: not executed.
- Real sampling: not executed.
- Source adequacy hard gate: not executed.
- Glossary constraint: not executed.

## Summary

```json
{
  "status": "PASS_STATIC_REFERENCE_FREE_QE_ADAPTER_STUB_CONTRACT",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "qe_adapter_config_created_count": 1,
  "low_risk_fixture_created_count": 1,
  "omission_risk_fixture_created_count": 1,
  "hallucination_risk_fixture_created_count": 1,
  "polarity_risk_fixture_created_count": 1,
  "missing_source_fixture_created_count": 1,
  "missing_final_gate_fixture_created_count": 1,
  "qe_adapter_receipt_created_count": 6,
  "deterministic_key_created_count": 6,
  "pass_qe_stub_count": 1,
  "review_recommended_count": 5,
  "hard_fail_recommended_count": 0,
  "skipped_missing_source_count": 1,
  "skipped_final_gate_missing_count": 1,
  "omission_risk_detected_count": 1,
  "hallucination_risk_detected_count": 1,
  "polarity_risk_detected_count": 1,
  "number_mismatch_risk_detected_count": 1,
  "adapter_mode": "DeterministicStub",
  "deterministic_stub_score_count": 6,
  "external_model_allowed": false,
  "external_model_executed_count": 0,
  "runtime_decode_executed_count": 0,
  "model_forward_executed_count": 0,
  "sampling_executed_count": 0,
  "qe_model_executed_count": 0,
  "source_adequacy_executed_count": 0,
  "glossary_constraint_executed_count": 0,
  "decode11_final_gate_required": true,
  "decode04_quality_receipt_qe_slot_extended": true,
  "duplicate_receipt_key_count": 0,
  "domain_ssot_mismatch_count": 0
}
```
