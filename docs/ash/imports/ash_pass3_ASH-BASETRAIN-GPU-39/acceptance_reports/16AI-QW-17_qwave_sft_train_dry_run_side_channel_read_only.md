# 16AI-QW-17 — QWave SFT Train Dry-run / Side-channel Read Only Seal

## SSOT

- Base ZIP: `ash_pass3_16AI-QW-16_qwave_feature_intake_cpu_gpu_parity_smoke_baked.zip`
- Input SSOT:
  - `crates/lora_train/src/qwave_sft_feature_intake.rs`
  - `crates/lora_train/src/qwave_feature_intake_parity_smoke.rs`
  - `crates/lora_train/src/qwave_feature_coverage_telemetry.rs`
  - `crates/lora_train/src/qwave_sample_weight_candidate.rs`
  - `crates/lora_train/src/qwave_curriculum_metadata.rs`
- New SSOT:
  - `crates/lora_train/src/qwave_sft_train_dry_run.rs`
  - `QWaveSftTrainDryRunReceipt`

## Scope

QW-17 attaches the QWave side-channel to the SFT train loop as a read-only dry-run and verifies that baseline train-step results remain unchanged.

## Acceptance Matrix

| Check | Status |
|---|---|
| QW-12 intake receipt consumed | PASS |
| QW-16 parity receipt consumed | PASS |
| QW-13 telemetry receipt referenced | PASS |
| QW-14 sample weight candidate receipt referenced | PASS |
| QW-15 curriculum metadata receipt referenced | PASS |
| Baseline snapshot verified | PASS |
| QWave dry-run snapshot verified | PASS |
| Side-channel attached | PASS |
| Side-channel read-only | PASS |
| Side-channel write counts zero | PASS |
| Token ids / attention mask / labels parity | PASS |
| Logits / loss parity | PASS |
| Gradient parity | PASS |
| Optimizer / scheduler parity | PASS |
| Adapter pointer / LoRA route parity | PASS |
| Sample weights unchanged | PASS |
| Curriculum order unchanged | PASS |
| Finite parity | PASS |
| Dry-run-only manifest | PASS |
| Train result unchanged | PASS |
| Mutation request rejection | PASS |
| Deterministic receipt | PASS |

## Explicit Rejections

QW-17 rejects:

- missing QW-12 intake receipt
- missing QW-16 parity receipt
- missing baseline snapshot
- missing QWave dry-run snapshot
- missing side-channel read report
- side-channel not attached
- side-channel not read-only
- side-channel write detected
- token/logit/loss/gradient/optimizer/scheduler mismatch
- sample weights mismatch
- curriculum order mismatch
- finite mismatch
- sample weight apply
- curriculum apply
- batch reorder
- loss rewrite
- gradient scaling
- optimizer mutation
- scheduler mutation
- direct logit mutation
- token id mutation
- vocab augmentation
- embedding resize
- new token creation
- LoRA routing finalization
- adapter pointer mutation
- sampler mutation
- backend switch
- GPU write buffer
- shader mutation

## Static Validation

- Static validation: PASS
- Test cases present: 48
- Native Rust test: NOT_RUN_TOOLCHAIN_UNAVAILABLE

## Native Test Command

```bash
cargo test -p lora_train qwave_sft_train_dry_run
```

## Judgment

QW-17 is a side-channel read-only dry-run gate. It does not prove training quality improvement. It proves that QWave feature side-channel attachment can be observed without mutating train results.
