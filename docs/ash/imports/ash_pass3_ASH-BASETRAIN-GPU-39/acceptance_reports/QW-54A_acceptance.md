# QW-54A Acceptance

## Status
`PATCH_IMPLEMENTED_PENDING_LOCAL_CARGO_RUNTIME_WGPU_TRACE`

## PASS criteria
1. `cargo check` passes locally.
2. `cargo test -p runtime qw54a` passes locally.
3. `cargo test -p model_core qw54a` passes locally.
4. QW-53E-RTA-R1 sampler handoff trace is observed.
5. QW-54A candidate source is WGPU/Rust-WGPU backed.
6. CPU oracle/mock source is rejected.
7. Top-k candidate facade records are generated.
8. Hangul candidates use the existing Cheonjiin facade.
9. Non-Hangul candidates are explicitly marked unavailable.
10. Token/logit/sampler/runtime apply mutation remains false.

## Not verified in this environment
- Local cargo build.
- Real checkpoint inference.
- Native WGPU runtime trace.
