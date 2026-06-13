# 16AI-QW-38G-R6A-MEM-01A

## Memory Budget Receipt Serialization Macro Recursion Hotfix Seal

## 확정

`MEM-01` 빌드 실패 원인은 `crates/orchestrator_local/src/memory_budget_guard.rs`의 `decision_receipt_json()` 내부 대형 `serde_json::json!({...})` 리터럴입니다. Rust 매크로 확장 중 `$crate::json_internal!` 재귀 한계에 닿아 `orchestrator_local` lib 컴파일이 중단되었습니다.

## 반영

- `serde_json::{json, Value}` import를 `serde_json::Value`로 축소
- `MEM01_PATCH_ID`를 `16AI-QW-38G-R6A-MEM-01A`로 갱신
- `MemoryBudgetReceipt<'a>` typed receipt struct 추가
- `decision_receipt_json()`을 대형 `json!` 매크로 대신 `serde_json::to_value(receipt)`로 직렬화
- `#![recursion_limit = "256"]` 같은 crate-wide 우회는 추가하지 않음

## 판단

이 패치는 RAM guard 정책값을 바꾸지 않습니다. 오직 receipt serialization path의 컴파일 블로커만 제거합니다.

## 검증

베이크 컨테이너에는 cargo가 없어 로컬 빌드는 수행하지 못했습니다. 정적 검증 기준으로 `json!` macro call 제거, typed receipt struct 추가, `serde_json::to_value` 경로 적용을 확인했습니다.

## 로컬 확인

```powershell
cargo build
```

빌드 통과 후 기존 MEM-01 guard 실행 명령을 그대로 재실행하면 됩니다.
