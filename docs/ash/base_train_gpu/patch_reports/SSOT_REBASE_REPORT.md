# SSOT Rebase Report

이 베이크본은 사용자가 업로드한 `ash_pass3 (11).zip`을 **새 SSOT**로 고정한 버전입니다.

## 기준
- 이전 비교 기준: `ash_pass3.zip`
- 새 SSOT 기준: `ash_pass3 (11).zip`
- 코드 내용은 업로드본을 우선하며, 이번 베이크는 **SSOT 재고정 + 보고서 추가**를 수행했습니다.

## diff 요약
- changed files: 62
- added files: 239
- removed files: 3875
- unchanged files: 217

## 주목할 변경 축
- desktop 앱/overlay/live tooling 갱신
- `crates/model_core`, `crates/lora_train`, `crates/burn_webgpu_backend` 대규모 변경
- `vendor_fork_scaffold` 변경 포함
- v5 tokenizer/artifact/config 추가
- 다수의 `patch_reports/` 및 문서 추가

## 주의
- 이번 베이크는 업로드본을 SSOT로 **재기준화**한 것입니다.
- 별도의 자동 로직 병합이나 추가 리팩토링은 넣지 않았습니다.
- 즉, 이후 추가 패치는 이 베이크본을 기준으로 이어가는 것이 맞습니다.
