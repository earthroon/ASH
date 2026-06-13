# 16AI-QW-38G-R6A-SALAD-03 베이크 리포트

## 확정
- `crates/model_core/src/salad03_rollback.rs` 추가.
- `lib.rs` module/pub use 등록.
- `sampler_parity::append_receipt()`에 SALAD-03 observe/plan hook 연결.
- 기본 모드 `PlanOnly`.
- 문자열-only rollback 금지 기준을 `TokenLedger + KvSnapshotLedger + SALAD02Detection` SSOT로 명시.
- PlanOnly에서는 `rollback_executed=false`, `kv_restore_executed=false`, `resample_executed=false`, `safe_stop_executed=false` 고정.

## 추정
- SALAD-02 HIGH/CRITICAL 위험이 감지되면 rollback depth와 safe resample config가 산출됩니다.
- KV snapshot 또는 token ledger 조건이 없으면 controlled execute로 넘어가지 않고 Denied/SafeStopCandidate로 떨어집니다.

## 판단불가
- 현재 컨테이너에는 cargo/rustc가 없어 실제 `cargo check`와 runtime smoke는 수행하지 못했습니다.
- 실제 KV restore 가능 여부는 backend runtime에서 `Salad03RollbackRuntime`을 구현하고 별도 probe로 확인해야 합니다.

## 실행 플래그
```bash
ASH_SALAD02_DETECTOR=receipt \
ASH_SALAD03_MODE=plan_only \
ASH_SALAD03_BEHAVIOR_CHANGE_ALLOWED=false \
ASH_SALAD03_RECEIPT=workspace/salad03_steps.jsonl \
ASH_SALAD03_SUMMARY=workspace/salad03_summary.json
```
