# QW-53E-RTA Acceptance

Status: PATCH_IMPLEMENTED_PENDING_LOCAL_CARGO_RUNTIME_WGPU_TRACE

## Implemented
- `crates/model_core/src/qw53e_rta_inline_apply_audit.rs`
- `crates/runtime/src/qw53e_rta_inline_apply.rs`
- `crates/runtime/src/qw53e_rta_live_qwave.rs`
- `crates/runtime/src/qw53e_rta_no_hard_ban.rs`
- `crates/burn_webgpu_backend/src/qw53e_rta_wgpu_candidate_bridge.rs`
- Runtime/model_core tests for no-hard-ban, explicit WGPU requirement, and CPU candidate apply rejection.

## Not locally executed here
- `cargo check`
- `cargo test`
- real checkpoint inference
- native WGPU runtime trace

## Invariants
- runtime default apply: false
- explicit enable required: true
- hard ban used: false
- token masked: false
- vocab removed: false
- CPU candidate apply used: false
- WGPU candidate source required: true
