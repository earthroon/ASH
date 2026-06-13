# 16AI-QW-38G-R6A-WCTX-07 Acceptance Report

## Patch

- Patch ID: `16AI-QW-38G-R6A-WCTX-07`
- Name: `EN-KO Subtitle ContextPlan Shadow Replay / No-Prompt-Mutation Receipt Seal`
- Domain SSOT: `en_to_ko_translation_subtitle_machine`

## Purpose

WCTX-07 consumes WCTX-06 `EnKoContextPlanShadowReceipt` values and creates a replay/no-mutation receipt proving that the ContextPlan remains shadow-only. The plan may exist, but it is not injected into prompt text, generation input, rerank paths, runtime defaults, source English, target Korean, or timing.

## Added files

- `crates/ash_core/src/word_context_context_plan_replay.rs`
- `crates/ash_core/src/bin/ash_word_context_context_plan_replay.rs`
- `workspace/word_context_probe/wctx_07_enko_context_plan_replay_cases.json`
- `workspace/word_context_probe/wctx_07_enko_context_plan_replay_matrix.json`
- `workspace/word_context_probe/wctx_07_enko_context_plan_replay_summary.json`
- `workspace/word_context_probe/wctx_07_enko_context_plan_replay_sample_receipt.json`
- `workspace/word_context_probe/wctx_07_static_validation.json`

## Modified files

- `crates/ash_core/src/lib.rs`

## Static summary

```json
{
  "patch_id": "16AI-QW-38G-R6A-WCTX-07",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "total_cases": 24,
  "pass_cases": 24,
  "fail_cases": 0,
  "deterministic_failures": 0,
  "risk_failures": 0,
  "prompt_mutation_count": 0,
  "generation_input_mutation_count": 0,
  "context_plan_prompt_leak_count": 0,
  "context_plan_generation_input_leak_count": 0,
  "context_plan_applied_count": 0,
  "rerank_applied_count": 0,
  "runtime_default_apply_count": 0,
  "source_text_mutation_count": 0,
  "target_text_mutation_count": 0,
  "timing_mutation_count": 0
}
```

## Acceptance criteria

- PASS: EN-KO translation subtitle domain SSOT maintained.
- PASS: `EnKoContextPlanReplayReceipt` added.
- PASS: replay/no-mutation snapshot structs added.
- PASS: replay matrix structs added.
- PASS: WCTX-06 ContextPlan receipt replay input supported.
- PASS: detached shadow replay mode supported.
- PASS: ContextPlan created state preserved.
- PASS: `context_plan_applied=false`.
- PASS: `prompt_mutated=false`.
- PASS: `generation_input_mutated=false`.
- PASS: `rerank_applied=false`.
- PASS: `runtime_default_apply=false`.
- PASS: source English, target Korean, and timing remain unchanged.
- PASS: ContextPlan prompt/generation leak detector added.
- PASS: matrix/summary/sample receipt JSON emitted.

## Verification status

`PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

The current container does not provide `cargo` or `rustc`, so this bake includes static Rust source integration and deterministic JSON receipts, but not a live cargo build/test run.

## Local verification command

```bash
cargo run -p ash_core --bin ash_word_context_context_plan_replay
```
