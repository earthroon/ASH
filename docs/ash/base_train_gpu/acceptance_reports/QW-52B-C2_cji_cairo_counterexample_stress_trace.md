# QW-52B-C2 — CJI Cairo Counterexample Stress Trace / Tube Concentration Seal

## Status
PASS_STATIC_CJI_CAIRO_COUNTEREXAMPLE_STRESS_TRACE

## Base
QW-52B-C1

## Purpose
CJI XYZ candidate tensors were analyzed with Cairo-style curvature/concentration stress traces.

## Added Detector
- CjiCairoCounterexampleStressTrace

## Confirmed
- Closure integral is recorded.
- Pressure integral is recorded.
- Release impulse is recorded.
- Curvature spike is recorded.
- Tube concentration is recorded.
- Cairo loss mean / peak / p95 are recorded.
- Fortis / aspirated / plain Cairo evidence scores are recorded.
- No force-class classification is applied.
- No runtime behavior changes.

## Fixture Results
- plain_low_cairo_stress: PASS / Available
- fortis_internal_concentration: PASS / Available / fortis evidence raised
- aspirated_release_curvature: PASS / Available / aspirated evidence raised
- partial_missing_pressure: PASS / Partial
- missing_cji_xyz_trace: PASS / Unavailable

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
- cairo_gate_apply = false
- force_class_apply = false

## Language Policy
- crate_js_ts_allowed = false
- detector_language = Rust
- validator_language = Rust
- frontend_js_ts_allowed = true
- desktop_js_ts_allowed = true

## Notes
High Cairo stress is evidence, not a ban. C2 does not classify ㄱ/ㄲ/ㅋ; C3 owns minimal-pair force-class validation.

## Next
QW-52B-C3 — CJI Plosive / Fortis / Aspirated Minimal Pair Fixture Seal
