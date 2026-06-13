# SFT-GPU-8J Bake Report

## Status
PASS_STATIC / PENDING_RUNTIME_QUALITY_EVAL

## Added
- lm_head_vocab_atlas_quality_eval.rs
- lm_head_vocab_atlas_promotion_gate.rs
- quality_eval config schema
- quality_eval prompt set
- promotion gate reports
- static validator

## Runtime contract
Quality eval consumes runtime_delta_verify_report, loss trace, final adapter artifact, and eval prompts. Promotion is strict and writes PROMOTED only when runtime delta, loss guard, and generation sanity pass.
