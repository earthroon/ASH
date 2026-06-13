# QW-53D Acceptance Report

## Status

`PATCH_IMPLEMENTED_PENDING_LOCAL_CARGO_RUNTIME_TRACE`

## Implemented

- Rust model_core audit module: `crates/model_core/src/qw53d_soft_demotion_audit.rs`
- Rust runtime facade modules:
  - `crates/runtime/src/qw53d_soft_demotion.rs`
  - `crates/runtime/src/qw53d_candidate_rerank.rs`
  - `crates/runtime/src/qw53d_policy_loader.rs`
  - `crates/runtime/src/qw53d_no_hard_ban_invariant.rs`
- CLI binaries:
  - `crates/runtime/src/bin/qw53d_soft_demotion_probe.rs`
  - `crates/model_core/src/bin/qw53d_soft_demotion_audit_validate.rs`
- Tests:
  - `crates/runtime/tests/qw53d_no_hard_ban_invariant.rs`
  - `crates/runtime/tests/qw53d_delta_cap.rs`
  - `crates/runtime/tests/qw53d_protected_token_no_demotion.rs`
  - `crates/model_core/tests/qw53d_no_hard_ban_validation.rs`

## Invariants

- Hard ban: forbidden
- Token mask: forbidden
- Vocab removal: forbidden
- Runtime default apply: forbidden
- Explicit enable required: true
- Core logic language: Rust + WGPU/WGSL only
- JS/TS core logic: forbidden

## Not executed in bake environment

This bake environment does not provide `cargo` or `rustc`, so local compile/runtime validation is pending.
