# ASH-BASETRAIN-GPU-62A SPEC

## Patch ID

`ASH-BASETRAIN-GPU-62A`

## Title

Runtime Binding Registry Install / Dryrun Binding Descriptor To Installed Non-Default Runtime Binding Seal

## Seal

No Default Apply / No Live Inference Attach / No Loss / No Backward / No Optimizer

---

## Purpose

`ASH-BASETRAIN-GPU-62A` consumes the successful `ASH-BASETRAIN-GPU-61` runtime route dryrun receipt and dryrun binding descriptor, then installs that descriptor into a real runtime binding registry as an `InstalledNonDefault` runtime binding entry.

GPU-62A is a registry install stage. It is not active runtime attach, not default route promotion, not live inference apply, not logits adoption, and not training.

## SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-61` | non-default runtime binding dryrun descriptor SSOT |
| `ASH-BASETRAIN-GPU-62A` | installed non-default runtime binding registry entry SSOT |
| `ASH-BASETRAIN-GPU-63A` | scoped activation / canary attach SSOT, not part of GPU-62A |
| `ASH-BASETRAIN-GPU-64A` | default promotion + CAS rollback SSOT, not part of GPU-62A |

Primary input SSOT:

```text
artifacts/ASH_BASETRAIN_GPU_61_FORWARD_CANDIDATE_RUNTIME_ROUTE_DRYRUN.json
artifacts/ASH_BASETRAIN_GPU_61_RUNTIME_BINDING_DRYRUN_DESCRIPTOR.json
artifacts/ASH_BASETRAIN_GPU_60_RUNTIME_CANDIDATE_ROUTE_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_59_OPERATOR_APPROVAL_ENVELOPE.json
```

Output artifacts generated locally when the operator runs the patch:

```text
artifacts/ASH_BASETRAIN_GPU_62A_RUNTIME_BINDING_REGISTRY_ENTRY.json
artifacts/ASH_BASETRAIN_GPU_62A_RUNTIME_BINDING_INSTALL_RECEIPT.json
```

Candidate digest SSOT:

```text
2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
```

## Registry state contract

```rust
pub enum RuntimeBindingState {
    InstalledNonDefault,
    ActiveNonDefault,
    ActiveDefault,
    RolledBack,
}
```

GPU-62A may create only `InstalledNonDefault`. `ActiveNonDefault`, `ActiveDefault`, and `RolledBack` belong to later patches.

## Legacy alias policy

GPU-62A accepts the GPU-61 legacy slot id `shadow-runtime-candidate-slot-0000`, but the installed registry entry must write the normalized slot id `non-default-runtime-candidate-slot-0000`.

The install receipt records:

```text
legacy_slot_alias_accepted == true OR false
normalized_runtime_slot_id == non-default-runtime-candidate-slot-0000
silent_correction_used == false
```

## Implementation files

```text
crates/base_train/src/runtime_binding_registry.rs
crates/base_train/src/ash_basetrain_gpu_62a_runtime_binding_registry_install.rs
crates/base_train/src/bin/ash_basetrain_gpu_62a_runtime_binding_registry_install.rs
crates/base_train/src/lib.rs
crates/base_train/Cargo.toml
```

## Local command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_62a_runtime_binding_registry_install -- `
  --gpu61-receipt .\artifacts\ASH_BASETRAIN_GPU_61_FORWARD_CANDIDATE_RUNTIME_ROUTE_DRYRUN.json `
  --binding-descriptor .\artifacts\ASH_BASETRAIN_GPU_61_RUNTIME_BINDING_DRYRUN_DESCRIPTOR.json `
  --route-envelope .\artifacts\ASH_BASETRAIN_GPU_60_RUNTIME_CANDIDATE_ROUTE_ENVELOPE.json `
  --operator-approval .\artifacts\ASH_BASETRAIN_GPU_59_OPERATOR_APPROVAL_ENVELOPE.json `
  --out-entry .\artifacts\ASH_BASETRAIN_GPU_62A_RUNTIME_BINDING_REGISTRY_ENTRY.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_62A_RUNTIME_BINDING_INSTALL_RECEIPT.json
```

## PASS meaning

GPU-62A PASS means only that the GPU-61 dryrun binding descriptor has been installed as a real non-default runtime binding registry entry.

GPU-62A PASS does not mean the binding is active, runtime default apply occurred, live inference attach occurred, logits were adopted, final logits were claimed, vocab compatibility was verified, loss was computed, or training occurred.

## Next stage

```text
ASH-BASETRAIN-GPU-63A
Runtime Candidate Scoped Activation /
Installed Non-Default Binding To Test-Traffic Active Binding Seal
```