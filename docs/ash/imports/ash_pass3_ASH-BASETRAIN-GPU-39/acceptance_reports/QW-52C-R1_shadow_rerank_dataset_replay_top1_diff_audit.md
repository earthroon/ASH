# QW-52C-R1 — Shadow Rerank Dataset Replay / Top1 Diff Audit Seal

## Status
PASS_STATIC_SHADOW_RERANK_TOP1_DIFF_AUDIT

## Base
QW-52C

## Purpose
QW-52C shadow rerank results were replayed against QW-53A normal-vs-collapse dataset evidence and QW-53C dream-collapse replay outputs to audit actual-vs-shadow top1 differences.

## Generated
- ShadowRerankTop1DiffAuditTrace
- ShadowTop1DiffAudit JSONL
- ShadowRerankAuditManifest

## Summary
- sample_count = 5
- supervised_audit_eligible_count = 3
- same_top1_count = 1
- different_top1_count = 2
- beneficial_diff_count = 1
- risky_diff_count = 1
- review_only_count = 1
- unavailable_count = 1
- hard_ban_count = 0
- token_selection_change_count = 0

## Confirmed
- Beneficial top1 diff is recorded.
- Stable top1 preservation is recorded.
- Risky top1 diff is recorded as audit evidence.
- Review/unlabeled samples are not supervised-audit eligible.
- Missing shadow candidates become Unavailable.
- No actual token rank is changed.
- No actual token selection is changed.
- No hard ban is applied.
- No blacklist is created.

## Mutation Policy
- runtime_apply = false
- hidden_state_mutation = false
- logit_mutation = false
- sampler_mutation = false
- token_rank_mutation = false
- token_selection_mutation = false
- token_ban = false
- hard_ban = false
- blacklist_mutation = false
- rerank_execution = false
- retry_execution = false
- memory_mutation = false
- training_mutation = false
- lora_mutation = false

## Language Policy
- crate_js_ts_allowed = false
- audit_language = Rust
- validator_language = Rust

## Next
QW-52C-R2 — Shadow Rerank RiskyDiff Guard / No Promotion Seal
or
QW-52D — Emergency Loop Brake Candidate / No Runtime Stop Seal
