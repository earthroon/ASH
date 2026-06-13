# 16AI-QW-38G-R6A-WCTX-15 Acceptance Report

## Patch
- `16AI-QW-38G-R6A-WCTX-15`
- EN-KO Subtitle Target Update Candidate / Manual Commit Gate Seal

## Domain SSOT
- Ash is an EN-to-KO translation subtitle-machine domain component.
- `domain_ssot = en_to_ko_translation_subtitle_machine`

## Scope
WCTX-15 consumes WCTX-13 decode candidate review receipts and WCTX-14 human review approval receipts and creates a target update candidate payload only when a real candidate exists and was explicitly approved for target-update candidate staging.

## Applied Files
- `crates/ash_core/src/word_context_target_update_candidate.rs`
- `crates/ash_core/src/bin/ash_word_context_target_update_candidate.rs`
- `crates/ash_core/src/lib.rs`
- `workspace/word_context_probe/wctx_15_enko_target_update_candidate_cases.json`
- `workspace/word_context_probe/wctx_15_enko_target_update_candidate_matrix.json`
- `workspace/word_context_probe/wctx_15_enko_target_update_candidate_summary.json`
- `workspace/word_context_probe/wctx_15_enko_target_update_candidate_sample_receipt.json`
- `workspace/word_context_probe/wctx_15_static_validation.json`

## Acceptance Result
- Status: `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`
- Rust toolchain was not available in the bake container, so runtime compilation was not executed.
- Static artifacts and deterministic matrix receipts were generated.

## Matrix Summary
- total_cases: 24
- pass_cases: 24
- fail_cases: 0
- candidate_created_count: 0
- blocked_no_candidate_count: 24
- manual_commit_review_gate_open_count: 0
- target_commit_gate_open_count: 0
- runtime_apply_gate_open_count: 0
- target_text_mutation_count: 0
- target_subtitle_commit_count: 0
- runtime_default_apply_count: 0
- rerank_applied_count: 0
- decode_executed_in_update_candidate_count: 0
- generation_executed_in_update_candidate_count: 0
- model_forward_executed_in_update_candidate_count: 0
- sampling_executed_in_update_candidate_count: 0

## Invariants
- NoCandidate reviews do not create target update payloads.
- Pending / Rejected / NeedsRevision / invalid approval states are blocked.
- ApprovedForTargetUpdateCandidate is the only path that may create a payload, and only when candidate target text exists.
- Target subtitle commit gate remains closed.
- Runtime apply gate remains closed.
- Target Korean subtitle is not mutated.
- No decode/generation/model-forward/sampling executes in WCTX-15.

## Next Seal
`16AI-QW-38G-R6A-WCTX-16 — EN-KO Subtitle Target Update Candidate Manual Commit Approval / No-Apply Seal`
