# 16AI-QW-24 — QWave-Conditioned SFT Smoke / Finite Loss & No Regression Seal

## Status

STATIC_VALIDATION: PASS  
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE

## Base

- Base ZIP: `ash_pass3_16AI-QW-23_qwave_conditioning_train_candidate_baked.zip`
- New module: `crates/lora_train/src/qwave_conditioned_sft_smoke.rs`
- New tests: `crates/lora_train/tests/qwave_conditioned_sft_smoke.rs`
- Export: `crates/lora_train/src/lib.rs`

## Input SSOT

- `QWaveConditioningTrainCandidateReceipt` lineage from QW-23
- QW-22 projection dry-run receipt reference
- QW-21 LoRA conditioning candidate reference
- QW-20 runtime hint candidate reference
- QW-19 promotion gate reference
- QW-18/QW-17/QW-16/QW-12 references
- QW-13/QW-14/QW-15 metadata references

## New SSOT

- `QWaveConditionedSftSmokeInput`
- `QWaveConditionedSftTrainCandidateRef`
- `QWaveConditionedSftSmokeSnapshot`
- `QWaveConditionedSftLossReport`
- `QWaveConditionedSftGradientReport`
- `QWaveConditionedAdapterDeltaReport`
- `QWaveConditionedNoRegressionReport`
- `QWaveConditionedSftSmokeManifest`
- `QWaveConditionedSftSmokePlan`
- `QWaveConditionedSftSmokeReceipt`

## Implemented Guards

1. QW-23 train candidate receipt is required.
2. Train candidate must remain gradient-isolated before smoke.
3. Baseline and conditioned smoke snapshots are required.
4. Baseline and conditioned smoke must be sandboxed.
5. Conditioned loss must be finite.
6. Conditioned gradient must be finite.
7. QWave feature gradient must remain disconnected.
8. Base model gradient must remain disconnected.
9. Adapter delta must be finite, nonzero, and bounded.
10. Projection delta must be finite and bounded.
11. Token IDs must remain unchanged.
12. Vocab must remain unchanged.
13. Embeddings must remain unchanged.
14. Base model checksum must remain unchanged.
15. Adapter pointer checksum must remain unchanged.
16. Current pointer must remain unchanged.
17. Artifact pointer must remain unchanged.
18. Production state must remain unchanged.
19. Loss no-regression must pass.
20. Gradient no-regression must pass.
21. Production training apply is rejected.
22. Runtime apply is rejected.
23. Base model mutation is rejected.
24. Token/vocab/embedding mutation is rejected.
25. Sampler/logit/backend mutation is rejected.
26. Sample weight/curriculum/batch reorder/loss rewrite/global gradient scaling are rejected.
27. Optimizer/scheduler mutation outside sandbox is rejected.

## Smoke Contract

QW-24 permits a bounded sandbox SFT smoke snapshot. It does not permit production training apply, runtime apply, current pointer mutation, artifact pointer mutation, base model mutation, tokenizer mutation, or production state mutation.

## Native Test Note

`cargo` and `rustc` are unavailable in this container, so native Rust tests were not executed here. Run:

```bash
cargo test -p lora_train qwave_conditioned_sft_smoke
```
