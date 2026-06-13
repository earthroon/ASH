# 16AI-QW-16 Bake Report

## Artifact

- Output ZIP: `ash_pass3_16AI-QW-16_qwave_feature_intake_cpu_gpu_parity_smoke_baked.zip`
- Base ZIP: `ash_pass3_16AI-QW-15_qwave_curriculum_metadata_bridge_baked.zip`

## Added / Modified

- `crates/lora_train/src/qwave_feature_intake_parity_smoke.rs`
- `crates/lora_train/tests/qwave_feature_intake_parity_smoke.rs`
- `crates/lora_train/src/lib.rs`
- `acceptance_reports/16AI-QW-16_qwave_feature_intake_cpu_gpu_parity_smoke.md`
- `acceptance_reports/16AI-QW-16_static_validation_result.md`
- `bake_artifacts/16AI-QW-16_BAKE_REPORT.md`

## Seal

QW-16 adds a smoke-only CPU/GPU parity receipt for QWave SFT feature intake. It rejects checksum, shape, dtype, layout, stride, finite, stat, read-only, GPU-write, shader-mutation, and trainer-mutation violations.

## Native Test

`cargo` / `rustc` unavailable in this container. Native test not run.
