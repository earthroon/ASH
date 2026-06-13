# 16AI-QW-38G-R6A-DECODE-04
## EnKo Subtitle Decode Quality SSOT / Candidate Decision Receipt Seal

status: PASS_STATIC_RECEIPT_CONTRACT

## SSOT

- domain_ssot: `en_to_ko_translation_subtitle_machine`
- state_owner: `EnKoSubtitleDecodeQualityReceipt`
- patch_id: `16AI-QW-38G-R6A-DECODE-04`
- created_by: `ash_core::enko_decode_quality_receipt`
- schema_version: `1`

## Scope

This patch creates the deterministic quality receipt contract for one EN→KO subtitle candidate.
It does not execute runtime decode, model forward, sampling, rerank, QE, rollback, or production apply.

## Static artifact summary

- receipt_created_count: `1`
- deterministic_key_created_count: `1`
- duplicate_receipt_key_count: `0`
- domain_ssot_mismatch_count: `0`
- deterministic_failures: `0`
- pass_cases: `1`
- fail_cases: `0`

## Runtime non-execution invariants

- runtime_decode_executed_count: `0`
- generation_executed_count: `0`
- model_forward_executed_count: `0`
- sampling_executed_count: `0`
- rerank_applied_count: `0`
- qe_model_executed_count: `0`

## Candidate decision defaults

- candidate_decision_default: `not_evaluated`
- decision_reason_default: `static_fixture_only`

## Hash / key closure

- source_en_hash_present: `true`
- candidate_ko_hash_present: `true`
- token_trace_hash_present: `true`
- sampling_config_hash_present: `true`
- risk_snapshot_present: `true`
- score_snapshot_present: `true`
- deterministic_receipt_key_present: `true`
- deterministic_receipt_key: `q4sha256:590f19b19cf45efd0d7d824b477cde0ab20a18ab6826a0d344d39eca7442dc1f`

## Added source files

- `crates/ash_core/src/enko_decode_quality.rs`
- `crates/ash_core/src/enko_decode_quality_key.rs`
- `crates/ash_core/src/enko_decode_quality_receipt.rs`
- `crates/ash_core/src/enko_decode_quality_fixture.rs`

## Added workspace artifacts

- `workspace/qw38g_r6a_decode04_quality_receipt_fixture.json`
- `workspace/qw38g_r6a_decode04_quality_receipt.json`
- `workspace/qw38g_r6a_decode04_quality_receipt_key_material.json`
- `workspace/qw38g_r6a_decode04_quality_receipt_report.json`

## Static validation note

`cargo`/`rustc` were unavailable in the bake environment, so this bake is sealed as a static source + fixture + receipt contract patch. No Rust compilation claim is made in this report.

## Next patch bridge

- `16AI-QW-38G-R6A-DECODE-05`: Sampler Step Propagation / Runtime Context Integrity Seal
- `16AI-QW-38G-R6A-DECODE-06`: Transition Guard Controlled Enable / Token Penalty Runtime Seal
