# TCU-24I Static Audit Result

## Result

`PASS_STATIC_TCU_24I_WITH_NATIVE_TESTS_NOT_RUN`

## Static Checks

- New dry-run module exists.
- `lib.rs` exports the dry-run module.
- Orchestrator report/bin/test files exist.
- Runtime JSON fixtures exist.
- Apply/switch/production flags are sealed false.
- Current/active backend mutation flags are sealed false.

## Native Tests

Rust toolchain was unavailable in the baking container, so native cargo tests were not executed.
