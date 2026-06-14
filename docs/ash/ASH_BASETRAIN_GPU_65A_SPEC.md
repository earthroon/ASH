# ASH-BASETRAIN-GPU-65A SPEC

## Patch ID

`ASH-BASETRAIN-GPU-65A`

## Title

Default Runtime Pointer Readonly Route Probe / CAS-Promoted Default Binding To Runtime Route Resolution Seal

## Seal

No Generation / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-65A` consumes the `ASH-BASETRAIN-GPU-64A` CAS-promoted runtime default pointer and validates that it resolves to the expected `ActiveDefault` runtime binding and source runtime route chain.

This patch is not a smoke test. It is a read-only route resolution gate.

GPU-65A verifies the chain:

```text
runtime default pointer
-> ASH-BASETRAIN-GPU-64A ActiveDefault binding
-> ASH-BASETRAIN-GPU-63A ActiveNonDefault binding lineage
-> ASH-BASETRAIN-GPU-61 runtime binding descriptor lineage
-> ASH-BASETRAIN-GPU-60 runtime route id
-> ASH-BASETRAIN-GPU-57 source surface id
```

GPU-65A must not generate text, decode tokens, sample tokens, compute loss, run backward, create optimizer state, mutate weights, attach live inference, or attach production traffic.

---

## 2. SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-63A` | scoped active non-default binding SSOT |
| `ASH-BASETRAIN-GPU-64A` | active default binding and runtime default pointer SSOT |
| `ASH-BASETRAIN-GPU-65A` | read-only default route resolution receipt SSOT |
| `ASH-BASETRAIN-GPU-66A` | controlled readonly default runtime input packet probe, not part of 65A |

### Input SSOT

```text
artifacts/ASH_BASETRAIN_GPU_RUNTIME_DEFAULT_POINTER.json
artifacts/ASH_BASETRAIN_GPU_64A_ACTIVE_DEFAULT_BINDING.json
artifacts/ASH_BASETRAIN_GPU_64A_DEFAULT_POINTER_CAS_RECEIPT.json
artifacts/ASH_BASETRAIN_GPU_64A_DEFAULT_PROMOTION_ROLLBACK_SNAPSHOT.json
```

### Optional Lineage Inputs

```text
artifacts/ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVE_BINDING.json
artifacts/ASH_BASETRAIN_GPU_61_RUNTIME_BINDING_DRYRUN_DESCRIPTOR.json
artifacts/ASH_BASETRAIN_GPU_60_RUNTIME_CANDIDATE_ROUTE_ENVELOPE.json
```

If optional lineage files are missing, GPU-65A may still PASS pointer-to-active-default validation but must mark `lineage_complete == false`.

### Output SSOT

```text
artifacts/ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json
artifacts/ASH_BASETRAIN_GPU_65A_DEFAULT_RUNTIME_ROUTE_PROBE_RECEIPT.json
```

GPU-65A owns only the resolved route view and read-only route probe receipt. It does not own model state, default pointer state, runtime binding state, or route state.

---

## 3. Required 64A Input Facts

GPU-65A must validate:

```text
default_pointer.default_pointer_id == ash-basetrain-gpu-runtime-default-pointer-0000
default_pointer.default_binding_id == ash-basetrain-gpu-64a-active-default-runtime-binding-0000
default_pointer.binding_state == ActiveDefault
default_pointer.source_patch_id == ASH-BASETRAIN-GPU-64A
default_pointer.source_active_binding_id == ash-basetrain-gpu-63a-active-non-default-runtime-binding-0000
default_pointer.payload_sha256 == 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
default_pointer.cas_swap_executed == true
default_pointer.silent_default_swap_used == false
default_pointer.runtime_default_apply == true
default_pointer.runtime_auto_bind == false
default_pointer.production_attach == false
default_pointer.live_inference_attach == false

active_default_binding.active_default_binding_id == ash-basetrain-gpu-64a-active-default-runtime-binding-0000
active_default_binding.binding_state == ActiveDefault
active_default_binding.previous_binding_state == ActiveNonDefault
active_default_binding.default_pointer_written == true
active_default_binding.default_pointer_cas_pass == true
active_default_binding.cas_swap_executed == true
active_default_binding.runtime_default_apply == true
active_default_binding.runtime_active_apply == true
active_default_binding.runtime_auto_bind == false
active_default_binding.production_attach == false
active_default_binding.live_inference_attach == false
active_default_binding.logits_adopted == false
active_default_binding.final_logits_claimed == false
active_default_binding.vocab_compatibility_verified == false
active_default_binding.silent_default_swap_used == false
```

GPU-65A must validate the CAS receipt and rollback snapshot:

```text
cas_receipt.patch_id == ASH-BASETRAIN-GPU-64A
cas_receipt.pass == true
cas_receipt.verdict == PASS
cas_receipt.default_pointer_cas.cas_compare_result == PASS
cas_receipt.default_pointer_cas.default_pointer_written == true
rollback_snapshot.snapshot_kind == cas_default_promotion_pre_swap_snapshot
rollback_snapshot.target_default_binding_id == ash-basetrain-gpu-64a-active-default-runtime-binding-0000
```

---

## 4. Route Resolution Contract

PASS requires:

```text
default_pointer.default_binding_id == active_default_binding.active_default_binding_id
default_pointer.source_active_binding_id == active_default_binding.source_active_binding_id
default_pointer.payload_sha256 == active_default_binding.payload_sha256
active_default_binding.source_binding_id == expected_source_binding_id
active_default_binding.source_route_id == expected_route_id
active_default_binding.source_surface_id == expected_surface_id
```

---

## 5. Outputs

GPU-65A writes:

```text
artifacts/ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json
artifacts/ASH_BASETRAIN_GPU_65A_DEFAULT_RUNTIME_ROUTE_PROBE_RECEIPT.json
```

No `.sha256` sidecar files.

---

## 6. Must Not Write or Mutate

GPU-65A must not write default pointer, active default binding, active non-default binding, production route attach files, live inference attach markers, adopted logits artifacts, final logits artifacts, vocab compatibility artifacts, loss receipts, gradient receipts, optimizer receipts, delta candidate packets, weight checkpoints, raw payload binaries, full tensor artifacts, or unselected group artifacts.

GPU-65A must not mutate GPU-55, GPU-57, GPU-58, GPU-59, GPU-60, GPU-61, GPU-62A, GPU-63A, or GPU-64A artifacts.

---

## 7. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_65a_default_route_probe -- `
  --default-pointer .\artifacts\ASH_BASETRAIN_GPU_RUNTIME_DEFAULT_POINTER.json `
  --active-default-binding .\artifacts\ASH_BASETRAIN_GPU_64A_ACTIVE_DEFAULT_BINDING.json `
  --default-pointer-cas-receipt .\artifacts\ASH_BASETRAIN_GPU_64A_DEFAULT_POINTER_CAS_RECEIPT.json `
  --default-promotion-rollback .\artifacts\ASH_BASETRAIN_GPU_64A_DEFAULT_PROMOTION_ROLLBACK_SNAPSHOT.json `
  --scoped-active-binding .\artifacts\ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVE_BINDING.json `
  --runtime-binding-descriptor .\artifacts\ASH_BASETRAIN_GPU_61_RUNTIME_BINDING_DRYRUN_DESCRIPTOR.json `
  --runtime-route-envelope .\artifacts\ASH_BASETRAIN_GPU_60_RUNTIME_CANDIDATE_ROUTE_ENVELOPE.json `
  --expected-default-pointer-id ash-basetrain-gpu-runtime-default-pointer-0000 `
  --expected-active-default-binding-id ash-basetrain-gpu-64a-active-default-runtime-binding-0000 `
  --expected-source-active-binding-id ash-basetrain-gpu-63a-active-non-default-runtime-binding-0000 `
  --expected-source-binding-id ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-0000 `
  --expected-route-id ash-basetrain-gpu-60-runtime-candidate-route-0000 `
  --expected-surface-id ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000 `
  --expected-output-sha256 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33 `
  --resolved-route-view-id ash-basetrain-gpu-65a-resolved-default-route-view-0000 `
  --out-route-view .\artifacts\ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_65A_DEFAULT_RUNTIME_ROUTE_PROBE_RECEIPT.json
```

---

## 8. Implementation Files

```text
crates/base_train/src/ash_basetrain_gpu_65a_default_route_probe.rs
crates/base_train/src/bin/ash_basetrain_gpu_65a_default_route_probe.rs
```

Update `lib.rs`:

```rust
pub mod ash_basetrain_gpu_65a_default_route_probe;
```

Update `Cargo.toml`:

```toml
[[bin]]
name = "ash_basetrain_gpu_65a_default_route_probe"
path = "src/bin/ash_basetrain_gpu_65a_default_route_probe.rs"
```

---

## 9. Next Stage

If GPU-65A PASS:

```text
ASH-BASETRAIN-GPU-66A
Default Runtime Input Packet Preflight / Readonly Pointer-Resolved Route To First Input Envelope Seal
No Generation No Decode No Sampling No Loss No Backward No Optimizer
```

If GPU-65A BLOCKED due to route lineage shape:

```text
ASH-BASETRAIN-GPU-65A-R1
Default Route Lineage Shape Rebind / Pointer Target And Runtime Route Envelope Closure Seal
```