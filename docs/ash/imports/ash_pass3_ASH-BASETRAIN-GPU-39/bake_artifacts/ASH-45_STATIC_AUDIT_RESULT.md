# ASH-45 Static Audit Result

## Status
PASS_STATIC_AUDIT_ASH_45

## Checked
- ASH-45 core source files exist.
- ASH-45 orchestrator report and audit bin exist.
- ASH-45 tests exist.
- `tools/validate_ash_45_static.py` does not exist.
- ASH-45 candidate code does not set `applied: true`.
- ASH-45 candidate code does not set `requires_explicit_apply: false`.
- ASH-45 candidate code does not set `runtime_apply_started: true`.
- `ash_core/src/lib.rs` exports ASH-45 modules.
- `orchestrator_local/src/lib.rs` exports ASH-45 report module.

## Result
Static audit passed in the baking container.

## Limitation
`cargo` is not installed in this container, so Rust compile/test execution could not be performed here.
