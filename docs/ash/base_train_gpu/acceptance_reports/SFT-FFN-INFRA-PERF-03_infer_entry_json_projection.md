# SFT-FFN-INFRA-PERF-03 Acceptance

## Status

PASS_STATIC / PENDING_LOCAL_RUST_TEST

## Scope

Infer entry JSON projection and manual low-level probe mapping collapse.

## SSOT

- Result serde projection digest
- Probe projection digest
- Entry overlay digest
- Legacy field parity guard
- Manual mapping guard
- Infer entry JSON projection seal

## Confirmed Static Gates

- `infer_entry.rs` no longer directly maps low-level `native_vocab_allocation_probe.*` fields.
- `infer_entry.rs` no longer directly maps low-level GPU sampling / raw bridge / tensorcube probe internals.
- `infer_entry_json_projection.rs` owns result serde projection and compatibility alias overlay.
- `StandardInferResult` now derives `Serialize` so `serde_json::to_value(&result)` can project newly-added result/probe fields without entry-layer edits.
- Entry-only fields remain explicit overlays: artifact freshness, request/run/output metadata, hard-case response additions, candidate-pool response additions.
- Overlay collision policy exists and fails closed by default.
- Projection seal is emitted into output and response JSON.
- Current pointer update remains closed.
- Promotion apply remains closed.
- Runtime mutation remains closed.

## Opened

- serde result projection
- probe serde projection
- entry overlay merge
- legacy compatibility alias boundary
- manual probe mapping guard
- infer entry JSON projection seal

## Closed

- manual low-level probe field mapping in `infer_entry.rs`
- silent response schema change
- current pointer update
- promotion apply rerun
- runtime mutation
- SFT training in core
- gradient write in core
- optimizer step in core

## Runtime Acceptance Pending

Requires local Rust compile/test because this environment has no `cargo` or `rustc`.
