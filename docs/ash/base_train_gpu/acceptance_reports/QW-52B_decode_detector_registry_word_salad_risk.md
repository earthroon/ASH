# QW-52B — Decode Detector Registry / Word Salad Risk Seal

## Status
PASS_STATIC_DETECTOR_REGISTRY

## Base
QW-52A-R4-M0

## Purpose
R0W/R0W-A/QW-52A/R1/R2/R3/R4 traces were registered into a decode detector registry. This patch records risk evidence only and does not correct output.

## Registered Detectors
- TokenRepeatDetector
- PieceRepeatDetector
- NgramRepeatDetector
- KoreanMorphLoopDetector
- HangulStructureDetector
- CheonjiinQWaveDetector
- ContextAttractorDetector
- ProjectionAlignmentDetector
- GatedFusionCandidatePolicyDetector

## Confirmed Mutation Policy
- runtime_apply = false
- hidden_state_mutation = false
- logit_mutation = false
- sampler_mutation = false
- token_rank_mutation = false
- token_selection_mutation = false
- token_ban = false
- lora_scale_mutation = false
- webgpu_shader_added = false
- python_detector_allowed = false

## Registry Summary
- detector_count = 9
- available_detector_count = 9
- aggregate_risk_level = None
- action_recommendation = TraceOnly

## Confirmed
QW-52B does not rerank candidates.
QW-52B does not retry decoding.
QW-52B does not mutate logits.
QW-52B does not mutate hidden state.
QW-52B does not ban tokens.
QW-52B only records detector evidence.

## Local Runtime Pending
- cargo check --workspace --all-targets
- runtime probe
- qw52b_decode_detector_registry_validate cargo execution

## Next
QW-52B-M1 — Input-Output Mirror Resonance Detector / Trace Only Seal
or
QW-52B-C1 — Cheonjiin XYZ Tensor Projection / Candidate Structural Map Seal
