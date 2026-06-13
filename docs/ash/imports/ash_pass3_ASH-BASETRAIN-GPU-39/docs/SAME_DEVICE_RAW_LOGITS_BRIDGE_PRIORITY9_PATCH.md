# SAME DEVICE RAW LOGITS BRIDGE PRIORITY9 PATCH

## 목적
6단계 패치.

sampled cached/native path에서 model_core가 봉인한 telemetry
- finish_reason
- mean_logprob
- min_logprob
- sampled_decode_applied
를 Ash/runtime reranker가 실제 점수에 반영할 수 있게 하는 1차 telemetry-aware rerank 패치.

## 이번 패치에서 추가된 것
- `crates/runtime/src/rerank.rs`
  - `TelemetryRerankProfile`
  - `TelemetryRerankWeights`
  - `TelemetryRerankScore`
  - `TelemetryRerankDecision`
  - `score_candidate(...)`
  - `select_best_candidate(...)`
  - `run_standard_infer_reranked(...)`
- `crates/runtime/src/lib.rs`
  - rerank module export

## 현재 점수 축
- 길이 적절성
- finish_reason quality
- mean_logprob
- min_logprob
- sampled_decode_applied bonus
- anti-shorts penalty

## 현재 한계
- candidate generation diversity는 seed 분기 중심
- task/profile은 request.task 문자열 기반
- QWave/ΔK latent까지 점수에 반영한 critic는 아직 아님
- infer candidate pool / decode override 통합은 후속
