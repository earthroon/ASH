# SFT-GPU-RUN-13 Bake Report

## Summary

Implemented GPU-trained operator action apply as a reviewed lifecycle transition gate.

## Implementation

- `ash_core` owns the SSOT decision and deterministic seal generation.
- `lora_train` summarizes the action apply report into a receipt facade.
- `burn_webgpu_backend` declares the backend boundary: reviewed action apply is allowed; unreviewed/mismatched/silent/runtime-training paths remain closed.

## Actions

Opened, but gated:
- KeepActive
- ActivateFallback
- ApplyDemotion
- ApplyQuarantine
- SwitchCandidate
- Hold

Still closed:
- unreviewed action apply
- recommendation mismatch apply
- silent registry correction
- runtime SFT training
- runtime gradient write
- runtime optimizer step
- textureSample/sampler/normalized UV weight fetch
- CPU fallback as success

## Verification

Static checks passed. Cargo tests were not run because the container lacks Rust tooling.
