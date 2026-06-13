# 16AI-QW-38G-R6A-WCTX-17 Acceptance Report

## SSOT
- domain_ssot: `en_to_ko_translation_subtitle_machine`
- patch: EN-KO Subtitle Target Commit Receipt / Single-Cue Apply Seal

## Static Result
- status: PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE
- total_cases: 24
- pass_cases: 24
- committed_count: 0
- blocked_no_update_candidate_count: 24
- target_subtitle_commit_count: 0
- target_text_mutation_count: 0
- runtime_default_apply_count: 0
- multiple_cue_mutation_detected_count: 0

## Seal
Default WCTX line contains no target update candidate, so WCTX-17 correctly emits `BlockedNoUpdateCandidate` receipts and does not create commit patches.

## Toolchain
`cargo` / `rustc` unavailable in this container. Rust source and deterministic static receipts were materialized for local verification.
