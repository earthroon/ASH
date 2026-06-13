# 16AI-QW-38G-R6A-WCTX-07 Bake Report

## Seal

`16AI-QW-38G-R6A-WCTX-07 — EN-KO Subtitle ContextPlan Shadow Replay / No-Prompt-Mutation Receipt Seal`

## SSOT

Ash is an EN-to-KO translation subtitle-machine domain component.

```text
domain_ssot = en_to_ko_translation_subtitle_machine
```

## What changed

This bake adds a Rust-native replay module that proves WCTX-06 ContextPlan receipts remain shadow-only. It creates a replay input snapshot, output snapshot, no-mutation diff, replay risk, replay receipt, and replay matrix.

## Guarded invariants

```text
context_plan_created=true
context_plan_applied=false
prompt_mutated=false
generation_input_mutated=false
rerank_applied=false
runtime_default_apply=false
source_text_mutated=false
target_text_mutated=false
timing_mutated=false
context_plan_leaked_to_prompt=false
context_plan_leaked_to_generation_input=false
```

## Non-goals preserved

- No prompt injection.
- No generation input mutation.
- No candidate rerank.
- No runtime default apply.
- No source English rewrite.
- No target Korean subtitle rewrite.
- No timing mutation.
- No glossary/preserve auto-apply.
- No Korean particle/ending auto-correction.

## Static artifact outputs

- `workspace/word_context_probe/wctx_07_enko_context_plan_replay_cases.json`
- `workspace/word_context_probe/wctx_07_enko_context_plan_replay_matrix.json`
- `workspace/word_context_probe/wctx_07_enko_context_plan_replay_summary.json`
- `workspace/word_context_probe/wctx_07_enko_context_plan_replay_sample_receipt.json`
- `workspace/word_context_probe/wctx_07_static_validation.json`

## Static result

```text
status = PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE
total_cases = 24
pass_cases = 24
fail_cases = 0
prompt_mutation_count = 0
generation_input_mutation_count = 0
context_plan_applied_count = 0
rerank_applied_count = 0
runtime_default_apply_count = 0
```

## Next recommended patch

`16AI-QW-38G-R6A-WCTX-08 — EN-KO Subtitle Controlled ContextPlan Injection Candidate / Approval Gate Seal`

WCTX-08 should create candidate prompt payloads and approval receipts, while keeping runtime default apply disabled until an explicit operator approval gate is satisfied.
