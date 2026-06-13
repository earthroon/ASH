# SFT-FFN-INFRA-PERF-01 Acceptance

## Status

PASS_STATIC / PENDING_LOCAL_RUST_TEST

## Scope

Hot path allocation hygiene before SFT-FFN-LORA-09 runtime attach dry-run.

## SSOT

- Error enum registry digest
- Dedup utility digest
- Calibration weight config digest
- Stable hash parts digest
- Clone audit scope digest
- Public report string preservation
- Routing semantics preservation
- Seal id semantics preservation

## Confirmed Static Gates

- Error enum path is available through `infra_error`.
- Error strings are rendered lazily through `render_infra_errors` / `render_message`.
- Public failure string report format remains available.
- String dedup utility is centralized in `infra_string`.
- `sort_unstable + dedup` is preferred for simple string dedup.
- Calibration weights are separated into `AshTagRouterCalibrationWeights`.
- Default calibration values are preserved.
- Legacy stable hash is preserved as `stable_hash64_legacy`.
- Allocation-free formatting hash path is available as `stable_hash_fmt_v2(format_args!(...))`.
- Clone audit marker and `AshSharedStr = Arc<str>` candidate are available.
- Event-driven router id generation no longer allocates an intermediate `format!` string before hashing.
- Event tag calibration attribution / score ids use allocation-free format-argument hashing for patched hot paths.
- Current pointer update remains closed.

## Opened

- error enum validation path
- delayed error string rendering
- dedup utility unification
- calibration weight config
- stable hash parts / format-args hashing path
- clone audit marker
- Arc<str> type alias candidate

## Closed

- routing semantic change
- curriculum semantic change
- seal id semantic change
- event id legacy rewrite
- runtime attach
- promotion apply
- current pointer update

## Runtime Acceptance Pending

Requires local Rust toolchain validation.
