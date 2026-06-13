# Acceptance Report — 16AI-QW-38G-R6A-KV-ROLLBACK-00

## Status
STATIC_BAKE_DEFINED_NOT_RUN

## Baked Contracts
- behavior_change=false
- probe_only=true
- main_state_unchanged=true
- restore_verified 없이는 SALAD-03 controlled execute로 승격하지 않음
- 문자열-only rollback 금지: rollback SSOT는 KVSnapshotLedger + TokenLedger + PositionState

## Added Files
- crates/model_core/src/kv_rollback00_probe.rs
- workspace/kv_rollback00_probe_schema.json
- workspace/kv_rollback00_steps.jsonl
- workspace/kv_rollback00_summary.json
- workspace/kv_rollback00_static_checks.json
- workspace/kv_rollback00_probe_prompts.jsonl
- workspace/kv_rollback00_report.md

## Not Run
- cargo check: unavailable in container
- runtime smoke: not run
- forked replay: not run
