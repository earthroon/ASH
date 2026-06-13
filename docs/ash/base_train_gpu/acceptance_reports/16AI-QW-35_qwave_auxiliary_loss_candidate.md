# 16AI-QW-35 — QWave Auxiliary Loss Candidate / Read-only Side-channel Lift Seal

## Status

STATIC_BAKED_NOT_EXECUTED

## Implemented

- Added `crates/lora_train/src/qwave_auxiliary_loss_candidate.rs`.
- Registered and re-exported the module from `crates/lora_train/src/lib.rs`.
- Added QW-35 artifact receipts under `artifacts/qwave_aux_loss/`.

## SSOT

New SSOT type:

- `QWaveAuxiliaryLossCandidateReceipt`

Supporting types:

- `QWaveAuxiliaryLossCandidateInput`
- `QWaveAuxiliaryLossCandidatePolicy`
- `QWaveCandidateLossBundle`
- `QWaveAuxiliaryLossReport`
- `QWaveAuxiliaryLossCandidateManifest`
- `QWaveAuxiliaryLossCandidatePlan`

## Candidate Losses

- `qwave_coverage_loss`
- `qwave_continuity_loss`
- `qwave_boundary_loss`
- `qwave_mask_validity_loss`
- `qwave_feature_stability_loss`
- `candidate_total`
- `weighted_candidate_total`

## Guard Contract

QW-35 deliberately keeps the QWave signal candidate-only.

Required policy defaults:

- `affects_loss_candidate = true`
- `affects_loss = false`
- `affects_gradient = false`
- `affects_optimizer = false`
- `affects_lora_weights = false`
- `affects_base_model = false`

Forbidden mutations:

- total-loss application
- backward execution
- optimizer step
- gradient scaling
- LoRA weight mutation
- base model mutation
- token id mutation
- vocab mutation
- embedding resize
- runtime pointer mutation
- sampler mutation
- backend switch

## Acceptance Criteria

- QWave feature matrix can be read into a candidate loss calculator.
- Candidate loss bundle is finite when inputs are finite.
- NaN/Inf features are rejected by default policy.
- Any request to run backward, step optimizer, mutate LoRA/base/tokenizer/runtime state is rejected.
- QW-12/QW-17 read-only semantics are not silently overturned.

## Execution Note

Native Rust checks were not executed in this container because `cargo` and `rustc` are unavailable. This patch is a static source bake.
