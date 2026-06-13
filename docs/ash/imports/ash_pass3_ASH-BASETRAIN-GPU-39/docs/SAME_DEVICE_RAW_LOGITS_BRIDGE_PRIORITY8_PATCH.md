# SAME_DEVICE_RAW_LOGITS_BRIDGE_PRIORITY8_PATCH

## 목표
로드맵 5단계: finish_reason 를 model_core 주권으로 끌어올린다.

## 이번 패치
- `crates/model_core/src/lib.rs`
  - `GenerationFinishReason` 에 `StopSequence`, `Interrupted` 추가
  - `GenerationTelemetry` 에 `stop_hit` 필드 추가
  - `finalize_generation_finish_reason(...)` helper 추가
  - `greedy_generate_cached_with_telemetry(...)` 추가
  - sampled cached telemetry finalize 가 helper를 쓰도록 정리
- `crates/runtime/src/infer.rs`
  - `StandardInferFinishReason` 추가
  - `StandardInferResult` 에
    - `generation_finish_reason`
    - `mean_logprob`
    - `min_logprob`
    - `sampled_decode_applied`
    필드 추가
  - native path 에서 `greedy_generate_cached_with_telemetry(...)` 를 사용
  - infer 결과가 telemetry truth 를 실어서 반환하도록 변경

## 현재 한계
- reference/CPU fallback path 는 아직 telemetry 없음
- stop sequence 최종 판정은 아직 model_core 내부에서 실제로 닫히지 않음
  - enum/필드/매핑만 먼저 열어둔 상태
- cargo check 미실행

## 의미
이번 패치로 native cached generation 에 한해서는 infer 가 finish_reason / mean_logprob / min_logprob / sampled_decode_applied 를 model_core telemetry 에서 직접 받는다.
