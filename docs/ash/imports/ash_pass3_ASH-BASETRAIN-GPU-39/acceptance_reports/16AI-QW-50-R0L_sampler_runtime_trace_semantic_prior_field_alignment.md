# QW-50-R0L — sampler runtime trace semantic prior field alignment

## Scope

- Target crate: `model_core`
- Target files:
  - `crates/model_core/src/sampler_parity.rs`
  - `crates/model_core/src/generation_sampling.rs`
  - `crates/model_core/src/sampler05_parity.rs`
  - `crates/model_core/src/decode03a_entropy.rs`

## Fix

- Added `semantic_prior_enabled` and `semantic_prior_effective` to `CpuSamplerRuntimeTrace` so CPU/GPU sampler trace surfaces share the same semantic-prior fields.
- Preserved existing `GpuSamplerRuntimeTrace` semantic-prior fields.
- Wired `cpu_trace_from_result(...)` to copy semantic-prior state from the CPU oracle trace.
- Added GPU trace initializer values in `generation_sampling.rs` using the sampling semantic-prior config plus available semantic score snapshot.
- Added missing semantic-prior fields to the `sampler05_parity.rs` GPU fixture.
- Kept `decode03a_entropy.rs` CPU semantic-prior access intact now that the CPU trace field exists.

## Guard

- No semantic prior policy mutation.
- No transition controlled decision mutation.
- No sampler parity pass relaxation.
- No runtime pointer mutation.
- No adapter registry mutation.
- No production apply.

## Static Pattern Check

See `artifacts/compile_recovery/qw50_r0l_static_pattern_check.json`.

## Verification

```txt
cargo check -p model_core --lib
```

## Status

PENDING_LOCAL_CARGO_CHECK
