# Native trace handles gate removal bake

Changes included:
- Enable `burn-raw-access-local` feature for `burn_webgpu_backend` in `crates/model_core/Cargo.toml`
- Add lazy runtime handle extraction helper in `crates/model_core/src/lib.rs`
- Relax native trace precheck to use live-extracted runtime handles rather than only cached field state
- Expand debug logs with `runtime_handles_field_ok` and `runtime_handles_ok`
- Fix native trace staging stats log to use actual `BridgeStats` fields
- Carry forward local lora_train compile fixes:
  - remove `drop(pack_shard_tx)` after move
  - remove unnecessary `mut` in `in_flight.pop_front()` loop
  - rename one unused `plan` parameter to `_plan`

Intent:
- stop native trace submit/poll from failing early only because cached `runtime_handles` field is `None`
- enable the backend feature that provides raw runtime handle extraction in the first place
