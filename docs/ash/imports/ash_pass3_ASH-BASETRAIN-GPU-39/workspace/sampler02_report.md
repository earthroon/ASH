# 16AI-QW-38G-R6A-SAMPLER-02 Report

## 확정

- `model_core::sampler_parity` 모듈을 추가했다.
- `SamplerParityMode`는 `Off / ProbeOnly / Strict`를 가진다.
- 환경변수 `ASH_SAMPLER_PARITY`, `ASH_SAMPLER_PARITY_TOP_N`, `ASH_SAMPLER_PARITY_MAX_STEPS`, `ASH_SAMPLER_PARITY_RECEIPT`를 정의했다.
- `CpuOracleSampleResult`에 `CpuOracleCandidateTrace`를 추가해 active/final candidate ids, counts, threshold, active stats를 보존한다.
- GPU readback의 recovery mode를 `GpuSamplingResult` 및 `GpuSamplingStepTelemetry`로 올린다.
- CPU logits dispatch 경로에서 parity mode가 켜져 있으면 CPU oracle shadow receipt를 `workspace/sampler02_runtime_parity_receipt.jsonl`에 append한다.

## 추정

현재 GPU 후보 ID trace buffer는 아직 ABI에 없다. 따라서 이번 베이크는 selected/recovery 기반 runtime receipt와 CPU oracle full trace를 우선 연결하고, candidate-set PASS는 GPU active/final candidate readback ABI가 추가된 뒤 완전 판정한다.

## 판단불가

`cargo check`, `cargo test`, WebGPU runtime dispatch는 현재 컨테이너에서 실행하지 못했다.
