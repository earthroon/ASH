# SFT-GPU-SAFETY-02 Bake Report

## Patch

`SFT-GPU-SAFETY-02 — Partial Artifact Quarantine / Failed Train Output Guard`

## Purpose

This patch consumes the SAFETY-01 GPU fault recovery seal and adds a quarantine layer for failed train outputs and partial artifacts. The layer treats zero-byte safetensors, partial manifests, incomplete adapter payloads, interrupted optimizer states, failed save-reload parity, digest mismatch, missing required files, and unknown failed outputs as quarantine material.

## Implemented

### ash_core

- Adds `AshPartialArtifactKind`.
- Adds `AshPartialArtifactDisposition`.
- Adds `AshPartialArtifactEntry`.
- Adds `AshPartialArtifactQuarantineGuard`.
- Adds `AshPartialArtifactQuarantineInput`.
- Adds `AshPartialArtifactQuarantineReceipt`.
- Adds `AshPartialArtifactQuarantineSeal`.
- Adds `build_sft_gpu_partial_artifact_quarantine`.

### lora_train

- Adds a receipt facade for partial artifact quarantine.
- Exposes `PartialArtifactQuarantineSummary`.
- Adds success-path closure helper.

### burn_webgpu_backend

- Adds backend boundary for failed output reporting and quarantine ledger append.
- Keeps registry intake, promotion, current binding, lifecycle action, auto repair, digest replacement, CPU fallback success artifact acceptance, and textureSample weight fetch closed.

## Closed Paths

- partial artifact registry intake
- partial artifact promotion
- partial artifact current pointer binding
- failed artifact lifecycle action path
- auto manifest repair
- silent digest replacement
- silent registry correction
- runtime SFT training after quarantine
- gradient write after quarantine
- optimizer step after quarantine
- textureSample weight fetch

## Verification Status

Static verification only in this container. Rust compile/test must be run in a Rust-enabled local environment.
