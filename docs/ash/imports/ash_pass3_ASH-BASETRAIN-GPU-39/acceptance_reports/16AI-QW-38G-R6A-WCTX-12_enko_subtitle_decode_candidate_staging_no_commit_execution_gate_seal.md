# 16AI-QW-38G-R6A-WCTX-12 Acceptance Report

## Patch

`16AI-QW-38G-R6A-WCTX-12`  
EN-KO Subtitle Decode Candidate Staging / No-Commit Execution Gate Seal

## Domain SSOT

`en_to_ko_translation_subtitle_machine`

## Status

`PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

Rust toolchain was not available in the bake container, so this report seals static artifact generation and deterministic JSON receipts. Runtime compilation must be performed in a local Rust environment.

## Scope

This patch adds decode candidate staging after WCTX-11 runtime preflight. It allows only preflight-passed candidates to be staged and keeps all commit/runtime mutation gates closed.

## Added Files

- `crates/ash_core/src/word_context_decode_staging.rs`
- `crates/ash_core/src/bin/ash_word_context_decode_staging.rs`
- `workspace/word_context_probe/wctx_12_enko_decode_staging_cases.json`
- `workspace/word_context_probe/wctx_12_enko_decode_staging_matrix.json`
- `workspace/word_context_probe/wctx_12_enko_decode_staging_summary.json`
- `workspace/word_context_probe/wctx_12_enko_decode_staging_sample_receipt.json`
- `workspace/word_context_probe/wctx_12_static_validation.json`

## Modified Files

- `crates/ash_core/src/lib.rs`

## Static Matrix Summary

```json
{
  "patch_id": "16AI-QW-38G-R6A-WCTX-12",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "total_cases": 24,
  "pass_cases": 24,
  "fail_cases": 0,
  "deterministic_failures": 0,
  "risk_failures": 0,
  "staged_count": 12,
  "blocked_preflight_not_passed_count": 12,
  "candidate_output_created_count": 12,
  "candidate_output_committed_count": 0,
  "decode_executed_count": 0,
  "generation_executed_count": 0,
  "model_forward_executed_count": 0,
  "sampling_executed_count": 0,
  "target_text_mutation_count": 0,
  "timing_mutation_count": 0,
  "commit_gate_open_count": 0,
  "runtime_default_apply_count": 0,
  "rerank_applied_count": 0
}
```

## Acceptance Checks

- PASS: EN-KO translation subtitle domain SSOT maintained.
- PASS: WCTX-11 preflight receipt input supported.
- PASS: preflight-passed candidates are staged.
- PASS: preflight-blocked candidates remain blocked.
- PASS: decode candidate payload structure added.
- PASS: no-commit gate structure added.
- PASS: commit gate remains closed.
- PASS: target subtitle commit is not allowed.
- PASS: runtime apply is not allowed.
- PASS: target text mutation count is 0.
- PASS: timing mutation count is 0.
- PASS: active prompt and generation input mutation are sealed false in the Rust risk model.
- PASS: runtime default apply count is 0.
- PASS: candidate output committed count is 0.
- PASS: DetachedCandidatePayload keeps decode/model forward/sampling execution false.

## Reproduction Command

```bash
cargo run -p ash_core --bin ash_word_context_decode_staging
```

If the crate is run standalone:

```bash
cargo run --bin ash_word_context_decode_staging
```

## Seal

WCTX-12 stages decode candidates from WCTX-11 preflight-pass receipts, but it does not commit target Korean subtitles, does not mutate active prompt or runtime defaults, and does not open the commit gate.
