# QW-52B-C3 — CJI Plosive / Fortis / Aspirated Minimal Pair Fixture Seal

## Status
PASS_STATIC_CJI_FORCE_CLASS_MINIMAL_PAIR_FIXTURE

## Base
QW-52B-C2

## Purpose
CJI Cairo force-class evidence scores were validated against Korean minimal pair fixtures.

## Added Fixture Validator
- CjiPlosiveForceFixtureTrace

## Confirmed
- G family plain / fortis / aspirated separation is validated.
- D family plain / fortis / aspirated separation is validated.
- B family plain / fortis / aspirated separation is validated.
- J family plain / fortis / aspirated separation is validated.
- S family plain / fortis separation is validated.
- Ng/H special group is kept outside plain/fortis/aspirated force classification.
- Prediction scope is fixture-only.
- No runtime behavior changes.

## Fixture Summary
- fixture_case_count = 16
- pass_case_count = 16
- fail_case_count = 0
- group_count = 6
- pass_group_count = 6

## Mutation Policy
- runtime_apply = false
- hidden_state_mutation = false
- logit_mutation = false
- sampler_mutation = false
- token_rank_mutation = false
- token_selection_mutation = false
- token_ban = false
- rerank_execution = false
- memory_mutation = false
- force_class_runtime_apply = false
- force_class_sampler_apply = false

## Language Policy
- crate_js_ts_allowed = false
- detector_language = Rust
- validator_language = Rust

## Runtime Validation
cargo / rustc were unavailable in the bake environment, so cargo check and the Rust validator execution remain local-runtime pending.

## Next
QW-53A — Salad Alignment Dataset / Normal-vs-Collapse Trace Seal
