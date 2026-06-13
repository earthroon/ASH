# QW-53A — Salad Alignment Dataset / Normal-vs-Collapse Trace Seal

## Status
PASS_STATIC_SALAD_ALIGNMENT_DATASET

## Base
QW-52B-C3

## Purpose
A normal-vs-collapse alignment dataset was created to compare detector traces against final output status.

## Dataset
- dataset_schema_version = salad_alignment_dataset_v1
- dataset_path = artifacts/qw53a_salad_alignment_dataset.jsonl
- manifest_path = artifacts/qw53a_salad_alignment_dataset_manifest.json
- sample_count = 5
- supervised_eval_eligible_count = 3

## Included Signals
- MirrorResonanceTrace
- SelfEchoDetectorTrace
- ResidualLoopEligibilityTrace
- QWavePhaseEscapeCandidateTrace
- QWaveSignatureRepeatGuardTrace
- StablePhraseQuarantineMemoryReceipt
- CheonjiinXyzTensorProjectionTrace
- CjiCairoCounterexampleTrace
- CjiPlosiveForceFixtureTrace

## Confirmed
- Normal sample is valid.
- Salad sample is valid.
- Collapse sample is valid.
- Review sample is valid but not supervised-eval eligible.
- Unlabeled sample is preserved but not supervised-eval eligible.
- No runtime behavior changes.
- No training or LoRA update is performed.

## Mutation Policy
- runtime_apply = false
- hidden_state_mutation = false
- logit_mutation = false
- sampler_mutation = false
- token_rank_mutation = false
- token_selection_mutation = false
- token_ban = false
- rerank_execution = false
- retry_execution = false
- memory_mutation = false
- training_mutation = false
- lora_mutation = false

## Language Policy
- crate_js_ts_allowed = false
- collector_language = Rust
- validator_language = Rust

## Next
QW-53B — Legacy Dream Cycle Probe / Idle Association Sandbox Seal
or
QW-52C — Controlled Awareness Soft Rerank Shadow / No Hard Ban Seal
