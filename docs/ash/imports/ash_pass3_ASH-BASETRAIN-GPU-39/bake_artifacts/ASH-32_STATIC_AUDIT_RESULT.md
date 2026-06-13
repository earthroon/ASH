# ASH-32 Static Audit Result

## Status
PASS_STATIC_AUDIT

## Checked
- Core modules present.
- Orchestrator report module and audit bin present.
- Core tests and orchestrator tests present.
- Acceptance report present.
- No `tools/validate_ash_32_static.py` Python validator present.
- `requires_explicit_apply` preserved in replay-derived proposals.
- `applied=false` preserved in replay-derived proposal set.
- Source fingerprint trace preserved in feedback events and proposal reasons.
- Registry/current pointer mutation code was not introduced.

## Not Executed
- `cargo test` was not executed because cargo/rustc are unavailable in the execution container.
