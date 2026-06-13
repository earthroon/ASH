# Native trace debug log patch report

## 목적
`native submit fallback ... reason=native trace runtime handles unavailable` 원인을 더 잘게 쪼개서 드러내기 위한 디버그 패치입니다.

## 반영 파일
- `crates/model_core/src/lib.rs`
- `crates/lora_train/src/bridge.rs`

## 추가 로그
- `[native-trace][init] ...`
- `[native-trace][submit][precheck] ...`
- `[native-trace][submit] stage=trace_hidden_pair ...`
- `[native-trace][submit] stage=bridge_native_tensor ...`
- `[native-trace][submit][raw-borrow] ...`
- `[native-trace][submit] stage=create_staging ...`
- `[native-trace][submit] stage=queue_submit ...`
- `[native-trace][poll][precheck] ...`
- bridge fallback 로그에 `batch_index` 추가

## 기대 효과
다음 실행에서 아래를 바로 구분할 수 있습니다.
- runtime handles 자체가 비었는지
- atlas dispatcher가 비었는지
- gpu sampling runtime이 비었는지
- same-device raw bridge가 비었는지
- raw zero-copy borrow가 실패하는지
- queue submit 단계까지 진입하는지

## 주의
이 환경에서는 `cargo check`를 실행하지 못했습니다. 로컬 빌드에서 컴파일 확인이 필요합니다.
