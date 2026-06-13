# 16AI-QW-38G-R6A-DECODE-04 Bake Report

## 확정

- `EnKoSubtitleDecodeQualityReceipt` 계층을 추가했다.
- `DecodeQualityDecision`, `CandidateDecisionReason`, `DecodeQualityRiskSnapshot`, `DecodeQualityScoreSnapshot`을 추가했다.
- 후보 1개를 `source_en_hash`, `candidate_ko_hash`, `token_trace_hash`, `sampling_config_hash`와 함께 결정론적 receipt로 봉인했다.
- `deterministic_receipt_key`는 Q4 방식의 double SHA-256 형식으로 생성했다.
- 런타임 디코딩, 모델 forward, 샘플링, rerank, QE 실행 플래그는 모두 `false`로 고정했다.

## 추정

- 다음 DECODE-05/06에서 step propagation과 transition guard가 이 receipt를 소비하면, 단어샐러드 위험 상태가 하나의 SSOT에 귀속될 수 있다.

## 판단불가

- 이 베이크 환경에는 `cargo`/`rustc`가 없어 Rust 컴파일은 검증하지 못했다.
- 실제 모델 출력 품질과 단어샐러드 발생률은 이 커밋의 검증 범위가 아니다.
