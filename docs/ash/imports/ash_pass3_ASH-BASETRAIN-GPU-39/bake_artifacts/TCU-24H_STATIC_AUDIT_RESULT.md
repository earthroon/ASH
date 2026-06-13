# TCU-24H Static Audit Result

Status: `PASS_STATIC_TCU_24H_WITH_NATIVE_TESTS_NOT_RUN`

## Static checks

- `qwave_atlas_backend_router.rs` exists.
- Backend router module is exported from `burn_webgpu_backend/src/lib.rs`.
- Orchestrator runtime report module and audit binary exist.
- Runtime JSON fixtures exist.
- Acceptance and bake reports exist.
- Apply/switch/production mutation flags are explicitly sealed false.

## Not run

Rust native tests and WGPU shader validation were not executed in this container.
