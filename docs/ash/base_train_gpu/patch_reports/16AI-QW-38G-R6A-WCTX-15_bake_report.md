# 16AI-QW-38G-R6A-WCTX-15 Bake Report

## Patch
`16AI-QW-38G-R6A-WCTX-15 — EN-KO Subtitle Target Update Candidate / Manual Commit Gate Seal`

## Source
Based on WCTX-14 baked artifact.

## Implemented
- Added `word_context_target_update_candidate.rs`.
- Added `ash_word_context_target_update_candidate.rs` runner.
- Exported the module from `lib.rs`.
- Generated WCTX-15 static matrix, summary, sample receipt, and validation receipt.

## SSOT
Ash remains bound to the EN-to-KO translation subtitle-machine domain.

## Current Default Line
WCTX-13/WCTX-14 default line has no decode candidate text because WCTX-12 used detached candidate staging. Therefore WCTX-15 correctly blocks all default cases as `BlockedNoCandidate`.

## Safety Locks
- `payload_created = false` for NoCandidate cases.
- `manual_commit_review_gate_open = false` for default cases.
- `target_commit_gate_open = false`.
- `target_text_mutated = false`.
- `target_subtitle_committed = false`.
- `runtime_default_apply = false`.
- `rerank_applied = false`.
- No decode/generation/model-forward/sampling execution.

## Validation Status
`PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

`cargo` / `rustc` were not available in the bake container. Local verification command:

```bash
cargo run -p ash_core --bin ash_word_context_target_update_candidate
```
