# ASH-BASETRAIN-GPU-61-R1 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-61-R1`

## Title

Runtime Route Dryrun Binary Module Rebind / Bin Entry Path Local Module Seal

## Seal

No Runtime Default Apply / No Runtime Binding Install / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-61-R1` fixes the compile-time module resolution failure in the GPU-61 binary entrypoint.

Observed failure:

```text
error[E0433]: failed to resolve: could not find `ash_basetrain_gpu_61_forward_candidate_runtime_route_dryrun` in `base_train`
```

The GPU-61 module source file exists, but the binary entrypoint depended on resolving the module through the `base_train` crate namespace. R1 changes only the binary entrypoint to bind the module through an explicit local path:

```rust
#[path = "../ash_basetrain_gpu_61_forward_candidate_runtime_route_dryrun.rs"]
mod ash_basetrain_gpu_61_forward_candidate_runtime_route_dryrun;
```

The runtime logic, receipt schema, route dryrun contract, and forbidden path flags remain unchanged.

---

## 2. SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-61` | non-default runtime binding dryrun descriptor contract |
| `ASH-BASETRAIN-GPU-61-R1` | binary module resolution rebind only |

State ownership does not move.

GPU-61 remains the semantic SSOT for:

```text
runtime_binding_dryrun_created
runtime_binding_installed == false
runtime_default_apply == false
runtime_auto_bind == false
runtime_active_apply == false
live_inference_attach == false
logits_adopted == false
loss/backward/optimizer/weight_mutation == false
```

R1 owns only the compile closure of the binary entrypoint.

---

## 3. Allowed Change

Allowed:

```text
Change bin entrypoint module binding from crate namespace lookup to explicit local module path.
```

Changed file:

```text
crates/base_train/src/bin/ash_basetrain_gpu_61_forward_candidate_runtime_route_dryrun.rs
```

---

## 4. Forbidden Change

R1 must not change:

```text
GPU-61 module runtime logic
GPU-61 receipt schema
GPU-61 route dryrun descriptor fields
GPU-61 forbidden path flags
Cargo bin name
output artifact names
next patch id
runtime default apply behavior
logits adoption behavior
loss/backward/optimizer behavior
weight mutation behavior
```

---

## 5. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_61_forward_candidate_runtime_route_dryrun -- `
  --gpu60-receipt .\artifacts\ASH_BASETRAIN_GPU_60_FORWARD_CANDIDATE_POST_APPROVAL_BIND_PREFLIGHT.json `
  --route-envelope .\artifacts\ASH_BASETRAIN_GPU_60_RUNTIME_CANDIDATE_ROUTE_ENVELOPE.json `
  --gpu59-receipt .\artifacts\ASH_BASETRAIN_GPU_59_FORWARD_CANDIDATE_OPERATOR_APPROVAL_GATE.json `
  --gpu58-receipt .\artifacts\ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_COMPATIBILITY_GATE.json `
  --expected-route-id ash-basetrain-gpu-60-runtime-candidate-route-0000 `
  --expected-route-kind approved_surface_runtime_candidate_route `
  --expected-route-state preflight_only `
  --expected-route-scope runtime_candidate_preflight_only `
  --expected-route-policy-id ash-basetrain-gpu-60-runtime-candidate-route-policy-no-default-apply `
  --expected-surface-id ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000 `
  --expected-output-sha256 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33 `
  --binding-id ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-0000 `
  --binding-kind non_default_runtime_candidate_binding_dryrun `
  --binding-state dryrun_candidate `
  --binding-scope dryrun_non_default_runtime_candidate_only `
  --binding-policy-id ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-policy `
  --runtime-slot-id shadow-runtime-candidate-slot-0000 `
  --runtime-slot-state candidate_only `
  --out-binding .\artifacts\ASH_BASETRAIN_GPU_61_RUNTIME_BINDING_DRYRUN_DESCRIPTOR.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_61_FORWARD_CANDIDATE_RUNTIME_ROUTE_DRYRUN.json
```

---

## 6. PASS Meaning

GPU-61-R1 PASS means only:

> The GPU-61 binary entrypoint resolves the GPU-61 module source through an explicit local path and preserves the existing dryrun route contract.

GPU-61-R1 does not install runtime binding.
GPU-61-R1 does not apply the route.
GPU-61-R1 does not adopt logits.
GPU-61-R1 does not compute loss, backward, optimizer, or mutate weights.
