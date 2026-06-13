# 16AI-QW-38G-R6A-DECODE-09 Bake Report

## 확정

- Base: 16AI-QW-38G-R6A-DECODE-08 baked tree.
- Added N-best subtitle candidate pool SSOT modules.
- Added default 5-profile decode plan and retry-linked 6-profile plan.
- Added candidate pool receipts for valid, duplicate-negative, and retry-linked cases.
- Preserved final_candidate_selected=false and rerank_applied=false.

## 추가 파일

- crates/ash_core/src/source_cue_snapshot.rs
- crates/ash_core/src/subtitle_candidate_profile.rs
- crates/ash_core/src/subtitle_candidate_snapshot.rs
- crates/ash_core/src/subtitle_candidate_pool.rs
- crates/ash_core/src/subtitle_candidate_pool_receipt.rs

## 수정 파일

- crates/ash_core/src/enko_decode_quality_receipt.rs
- crates/ash_core/src/lib.rs

## 봉인 상태

status: PASS_STATIC_NBEST_CANDIDATE_POOL_CONTRACT
runtime_decode_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0
final_candidate_selected_count: 0
rerank_applied_count: 0

## 판단불가

cargo/rustc unavailable in this bake environment; Rust compile was not verified.
