# QW-52C — Controlled Awareness Soft Rerank Shadow / No Hard Ban Seal

## Status
PASS_STATIC_CONTROLLED_AWARENESS_SOFT_RERANK_SHADOW

## Base
QW-53C

## Purpose
A controlled awareness soft rerank shadow was computed from detector, structural, and dream-collapse replay evidence.

## Generated
- ControlledAwarenessSoftRerankShadowTrace
- SoftRerankShadowCandidate JSONL
- SoftRerankShadowManifest

## Confirmed
- Salad-like candidates can be demoted in shadow.
- Stable candidates can be preserved in shadow.
- Shadow top1 may differ from actual top1.
- Actual token rank is not changed.
- Actual token selection is not changed.
- No hard ban is applied.
- No blacklist is created.
- No runtime behavior changes.

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
- shadow_language = Rust
- validator_language = Rust

## Next
QW-52C-R1 — Shadow Rerank Dataset Replay / Top1 Diff Audit Seal
or
QW-52D — Emergency Loop Brake Candidate / No Runtime Stop Seal
