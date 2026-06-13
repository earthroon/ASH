# 16AI-QW-38G-R6A-KV-ROLLBACK-00
## KV Snapshot Restore Probe Seal

### 확정
- `crates/model_core/src/kv_rollback00_probe.rs`를 추가했다.
- `KvRollback00Mode`를 `Off / SnapshotOnly / DryRunRestoreProbe / ForkedReplayProbe / StrictProbe`로 정의했다.
- `KVSnapshotLedger + TokenLedger + PositionState`를 rollback SSOT로 명시했다.
- `sampler_parity::append_receipt()` 체인에 `append_kv_rollback00_receipt_from_sampler03()`를 연결했다.
- 기본 계약은 `behavior_change=false`, `probe_only=true`, `main_state_unchanged=true`다.

### 추정
- 이 패치는 SALAD-03 rollback plan을 실제 실행하기 전에 KV snapshot/position/token ledger가 rollback 가능한 형태인지 확인하는 probe layer다.
- 실제 rollback/resample execute는 열지 않았다.

### 판단불가
- 현재 컨테이너에 cargo/rustc가 없어 빌드와 런타임 smoke는 수행하지 못했다.
- 실제 backend KV clone/restore/forked replay 가능성은 런타임에서 `ASH_KV_ROLLBACK00_MODE=dry_run_restore_probe` 또는 `forked_replay_probe`로 receipt를 찍어야 판단 가능하다.
