# QW-53E-RTA-R1 Acceptance

Status: `PATCH_IMPLEMENTED_PENDING_LOCAL_CARGO_RUNTIME_WGPU_TRACE`

## Implemented

- Runtime/model_core R1 handoff types and validators.
- Real WGPU sampling branch hook trace calls in `generation_sampling.rs`.
- Runtime helper that returns the exact candidate vector that the sampler must consume.
- No CPU oracle candidate apply invariant.
- No lab-only probe invariant.
- WGPU-backed source invariant.

## Pending Local Validation

The bake environment has no `cargo`/`rustc`, so the following must be run locally:

```bash
cargo check
cargo test -p runtime qw53e_rta_r1
cargo test -p model_core qw53e_rta_r1
```

## PASS Requires

- `inline_hook_invoked_count > 0`
- `lab_probe_only == false`
- `hook_binding_point == BeforeSamplerSelection`
- `candidate_source != CpuOracle`
- `adjusted_sampler_handoff_count > 0` only for `ExplicitLabApply + explicit_enable=true`
- hard ban / token mask / vocab removal counts all zero
