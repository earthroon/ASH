# 16AI-QW-38G-R6A-DECODE-05
## Sampler Step Propagation / Runtime Context Integrity Seal

status: PASS_STATIC_STEP_INTEGRITY_CONTRACT  
domain_ssot: en_to_ko_translation_subtitle_machine  
depends_on: 16AI-QW-38G-R6A-DECODE-04

## SSOT

The decode generation loop owns `generation_step`. Sampler, CPU oracle, transition guard, token trace, and decode-quality receipt layers must consume the same step value. Placeholder `0` is allowed only for the first generated token.

## Acceptance Counters

step_fixture_created_count: 1  
negative_fixture_created_count: 1  
step_integrity_receipt_created_count: 3  
negative_step_integrity_receipt_created_count: 1  
deterministic_key_created_count: 4  

generation_step_source: generation_loop  
all_steps_aligned: true  
aligned_pass_count: 3  
mismatch_count: 0  
placeholder_zero_detected: false  
negative_placeholder_zero_detected: true  
negative_placeholder_zero_validation_failed: true  

runtime_decode_executed_count: 0  
model_forward_executed_count: 0  
sampling_executed_count: 0  
guard_executed_count: 0  

decode04_token_snapshot_extended: true  
token_trace_step_range_present: true  
step_integrity_hash_present: true  

duplicate_receipt_key_count: 0  
domain_ssot_mismatch_count: 0

## Canonical Receipt Keys

aligned_final_step_receipt_key: `q4sha256:729666d2b50d0e1ae2d57a9f4ee8c4b67d0672417ad208fdf9b1274df5468722`  
negative_placeholder_zero_receipt_key: `q4sha256:075a38bbcb9f28d41bb456b90ae2ae2b7e5a4823f9bac71a044e211aca198cb1`

## Files

- `crates/ash_core/src/decode_step_context.rs`
- `crates/ash_core/src/decode_step_integrity.rs`
- `crates/ash_core/src/decode_step_receipt.rs`
- `workspace/qw38g_r6a_decode05_step_integrity_fixture.json`
- `workspace/qw38g_r6a_decode05_step_integrity_negative_fixture.json`
- `workspace/qw38g_r6a_decode05_step_integrity_receipt.json`
- `workspace/qw38g_r6a_decode05_step_integrity_report.json`

## Runtime Execution Seal

This patch does not execute model forward, runtime decode, sampling, guard behavior mutation, rerank, or QE. It only materializes the step-integrity contract and deterministic receipts.
