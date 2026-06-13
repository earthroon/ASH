# 16AI-QW-38G-R6A-KV-ROLLBACK-01 Acceptance

## Status
STATIC_BAKE_DEFINED_NOT_RUN

## Confirmed static contracts
- `behavior_change=false`
- `probe_only=true`
- forked replay verification is separated from main generation state
- `restore_verified_for_salad03b` requires replay verification evidence
- main state unchanged is part of the verification result
- default mode is `PlanOnly`

## Files added
- `crates/model_core/src/kv_rollback01_forked_replay.rs`
- `workspace/kv_rollback01_forked_replay_schema.json`
- `workspace/kv_rollback01_steps.jsonl`
- `workspace/kv_rollback01_summary.json`
- `workspace/kv_rollback01_static_checks.json`
- `workspace/kv_rollback01_probe_prompts.jsonl`
- `workspace/kv_rollback01_report.md`
- `workspace/kv_rollback01.patch`
- `workspace/kv_rollback01_source_hash_manifest.json`

## Not run
- cargo check
- cargo test
- runtime smoke
- backend forked replay

## Required runtime command sketch
```bash
ASH_KV_ROLLBACK01_MODE=forked_replay_probe \
ASH_KV_ROLLBACK01_REQUIRE_KV_ROLLBACK00=true \
ASH_KV_ROLLBACK01_REQUIRE_MAIN_STATE_UNCHANGED=true \
ASH_KV_ROLLBACK01_RECEIPT=workspace/kv_rollback01_steps.jsonl \
ASH_KV_ROLLBACK01_SUMMARY=workspace/kv_rollback01_summary.json
```
