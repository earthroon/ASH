# SFT-FFN-LORA-06 Bake Report

## Patch

SFT-FFN-LORA-06 — Adapter Eval Candidate / Loss Direction Smoke Seal

## Applied on

SFT-FFN-LORA-05 adapter artifact candidate capture baked tree.

## Added

- `crates/ash_core/src/sft_ffn_lora_eval_candidate.rs`
- `crates/ash_core/tests/sft_ffn_lora_06_eval_candidate.rs`
- `crates/burn_webgpu_backend/src/ffn_lora_eval_candidate.rs`
- `acceptance_reports/SFT-FFN-LORA-06_adapter_eval_candidate.md`
- `bake_artifacts/SFT-FFN-LORA-06_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-LORA-06_STATIC_VALIDATION.txt`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- adapter eval candidate smoke
- artifact read for eval
- eval fixture evidence
- loss direction evidence
- output sanity evidence
- non-regression policy
- artifact mutation guard
- no promotion guard

## Closed

- artifact write during eval
- runtime attach
- promotion apply
- current pointer update
- promotion review enqueue
- operator approval
- SFT training in core
- gradient write in core
- optimizer step in core

## SSOT

SFT-FFN-LORA-06 reads the SFT-FFN-LORA-05 artifact candidate seal and creates an eval candidate seal from fixture digest, loss evidence, output sanity evidence, artifact mutation guard, and no-promotion guard. It does not attach, promote, update current pointers, enqueue review, or record operator approval.

## Compile status

Not executed in this environment because Rust toolchain availability is not guaranteed here. Static validation was performed instead.
