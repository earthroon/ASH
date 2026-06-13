# SFT-FFN-LORA-07 Bake Report

## Patch

SFT-FFN-LORA-07 — Adapter Promotion Review Candidate / Operator Approval Gate

## Source

Baked on top of SFT-FFN-LORA-06 adapter eval candidate package.

## Added

- crates/ash_core/src/sft_ffn_lora_promotion_review.rs
- crates/ash_core/tests/sft_ffn_lora_07_promotion_review.rs
- crates/burn_webgpu_backend/src/ffn_lora_promotion_review.rs
- acceptance_reports/SFT-FFN-LORA-07_promotion_review_candidate.md
- bake_artifacts/SFT-FFN-LORA-07_BAKE_REPORT.md
- bake_artifacts/SFT-FFN-LORA-07_STATIC_VALIDATION.txt

## Modified

- crates/ash_core/src/lib.rs
- crates/burn_webgpu_backend/src/lib.rs

## Opened

- promotion review candidate
- review queue enqueue
- review packet digest
- approval gate creation
- operator approval required state
- no runtime promotion guard

## Closed

- operator approval record
- runtime attach
- promotion apply
- current pointer update
- slot ready mark
- ASH binding
- SFT training in core
- gradient write in core
- optimizer step in core

## SSOT

SFT-FFN-LORA-07 is a promotion review candidate and operator approval gate layer. It enqueues an eval-accepted adapter artifact candidate for review but does not record approval, attach runtime state, apply promotion, switch current pointer, mark slot ready, or bind ASH.
