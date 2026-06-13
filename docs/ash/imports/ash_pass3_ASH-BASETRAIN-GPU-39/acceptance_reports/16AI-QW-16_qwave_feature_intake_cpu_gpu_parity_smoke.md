# 16AI-QW-16 — QWave Feature Intake CPU/GPU Parity Smoke / Matrix Load Determinism Seal

## 확정

- 베이스 ZIP: `ash_pass3_16AI-QW-15_qwave_curriculum_metadata_bridge_baked.zip`
- 입력 SSOT: `crates/lora_train/src/qwave_sft_feature_intake.rs`
- 참조 SSOT: `qwave_feature_coverage_telemetry.rs`, `qwave_sample_weight_candidate.rs`, `qwave_curriculum_metadata.rs`
- 신규 SSOT: `QWaveFeatureIntakeParityReceipt`
- 신규 모듈: `crates/lora_train/src/qwave_feature_intake_parity_smoke.rs`
- QW-12 intake receipt 소비: PASS
- QW-13 telemetry receipt 참조: PASS
- QW-14 candidate receipt 참조: PASS
- QW-15 curriculum receipt 참조: PASS
- CPU snapshot 검증: PASS
- GPU snapshot 검증: PASS
- feature matrix checksum parity: PASS
- feature mask checksum parity: PASS
- coverage mask checksum parity: PASS
- shape/dtype/layout/stride parity: PASS
- finite/stat parity: PASS
- read-only CPU load: PASS
- read-only GPU upload: PASS
- GPU write buffer 금지: PASS
- shader mutation 금지: PASS
- smoke-only manifest: PASS
- loss/gradient/optimizer/scheduler unchanged: PASS
- sample weight/curriculum unchanged: PASS
- deterministic receipt: PASS

## 추정

QW-16은 실제 GPU 커널을 실행하는 패치가 아니라, CPU load snapshot과 GPU upload snapshot의 shape/checksum/layout/read-only 계약을 봉인하는 smoke-only parity gate다. MockGpu backend는 CI/컨테이너 환경에서 contract 검증용으로 허용하되, receipt와 manifest에 backend kind가 남는다.

## 판단불가

- native Rust compile/test: NOT_RUN_TOOLCHAIN_UNAVAILABLE
- 실제 WGPU/Vulkan/Metal/DX12 업로드 실행: 판단불가
- QWave feature가 SFT 품질을 개선하는지 여부: 판단불가
