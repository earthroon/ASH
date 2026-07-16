# ASH-TCU-DECODE-03 SPEC

## LIVE_SAME_DEVICE_SHADOW_DISPATCH_SPLICE

```text
patch_id=ASH-TCU-DECODE-03_LIVE_SAME_DEVICE_SHADOW_DISPATCH_SPLICE
parent_patch=ASH-TCU-DECODE-02_VOCAB_ATLAS_REAL_SHAPE_ROUTE_IDENTITY
parent_package=ash_pass3_ASH-TCU-DECODE-02-R2_source_fp16_runtime_f32_dtype_ownership_truth_repair_code_baked_no_spec_no_docs_no_runtime_artifacts_no_sha.zip
parent_package_sha256=4ca179020a137535d1a7faa5b8d5dc8177212960700b146eee126498137e53ab
parent_execution_id=decode02-9ba88316c0199b01ffec
parent_status=PASS_ASH_TCU_DECODE_02_VOCAB_ATLAS_REAL_SHAPE_ROUTE_IDENTITY
parent_route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
mutation_class=live_runtime_shadow_dispatch_splice
output_authority=burn
production_authority=false
runtime_output_changed=false
```

## 1. Status

```text
PASS=PASS_ASH_TCU_DECODE_03_LIVE_SAME_DEVICE_SHADOW_DISPATCH_SPLICE
HOLD=HOLD_ASH_TCU_DECODE_03_LIVE_SAME_DEVICE_SHADOW_DISPATCH_SPLICE
FAIL=FAIL_ASH_TCU_DECODE_03_LIVE_SAME_DEVICE_SHADOW_DISPATCH_SPLICE
```

Expected PASS verdict:

```text
live_same_device_m1_n1024_k2048_shadow_dispatch_submitted_once_unobserved_with_burn_output_authority_preserved
```

## 2. Purpose

DECODE-03 is the first live TensorCube execution splice in ASH generation.

For one explicitly activated generation it must:

1. consume the DECODE-02 canonical route identity;
2. select generation step 0 and vocab-atlas tile 0 only;
3. resolve the actual live Fusion `last_hidden` and tile-weight primitives;
4. borrow their existing WGPU buffers without host materialization;
5. submit one `[64,1,1]` TensorCube command buffer on the model's existing Device and Queue;
6. leave the TensorCube scratch output unobserved;
7. continue through the existing Burn vocab-atlas projection;
8. return only Burn logits.

The patch does not authorize parity, readback, output merge, sampler consumption, production promotion, all-tile execution or ragged-tail execution.

## 3. Parent route

The immutable parent route is:

```text
M=1
N=1024
K=2048
runtime_dtype=f32
source_checkpoint_dtype=fp16
rhs_storage_shape=[1024,2048]
rhs_logical_shape=[2048,1024]
workgroup=[16,16,1]
dispatch=[64,1,1]
full_tile_count=47
ragged_tail_N=131
route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
```

DECODE-03 must not rewrite the route identity. Execution authorization is an overlay owned by DECODE-03.

## 4. Explicit activation

Normal model construction remains DECODE-02 observation-only.

Required API:

```rust
NativeWgpuModel::configure_tensorcube_decode03_live_shadow_dispatch()
```

The activation receipt must bind:

```text
mode=live_generation_single_full_tile_submitted_unobserved
route_digest=<DECODE-02 route digest>
max_dispatches_per_generation=1
burn_output_authority=true
production_authority=false
readback_authorized=false
parity_authorized=false
output_commit_authorized=false
```

## 5. Live Fusion raw access

The existing fixture registry is not live-model evidence.

The live path must resolve the actual `FusionTensor` through its own Fusion client:

```text
FusionTensor.client.resolve_tensor_float::<NativeWgpuRawBackend>()
```

Required properties:

```text
fusion_stream_drained_before_resolve=true
host_materialization_performed=false
fixture_override_used=false
resolved_primitive=CubeTensor<WgpuRuntime>
```

The live path must reject a pre-existing fixture override. It must not call `into_data()` or upload CPU bytes.

## 6. Raw lease contract

Two strict leases are required:

```text
lhs=last_hidden shape [1,2048]
rhs=tile_0.weight shape [1024,2048]
raw_buffer_lease_count=2
raw_borrow_count=2
host_upload_count=0
```

Both buffers must be storage-bindable and belong to the same model runtime used for submission.

No extra adapter, Device or Queue may be created.

## 7. Dispatch scope

Only this invocation is eligible:

```text
generation_step_ordinal=0
tile_id=0
tile_token_start=0
tile_token_len=1024
M=1
N=1024
K=2048
dispatch=[64,1,1]
```

The lifecycle owner must reject a second dispatch in the same generation.

The N=131 tail remains Burn-only.

## 8. Scratch and execution boundary

Scratch output:

```text
shape=[1,1024]
size_bytes=4096
usage=STORAGE
copy_src=false
copy_dst=false
map_read=false
```

Execution counters for one PASS run:

```text
raw_buffer_lease_count=2
tensorcube_dispatch_count=1
queue_submit_count=1
tensorcube_output_count=0
device_poll_count=0
buffer_map_count=0
readback_count=0
parity_comparison_count=0
downstream_output_commit_count=0
runtime_output_change_count=0
```

Queue submission proves submission only. It does not prove completion or numerical parity.

## 9. Burn continuity

The splice occurs after DECODE-02 route observation and before the existing Burn tile loop.

Required order:

```text
DECODE-02 route census and generation lock
-> DECODE-03 live raw resolution
-> DECODE-03 isolated scratch dispatch
-> existing Burn tile loop
-> existing Burn merged logits
-> existing sampler and token path
```

Dispatch failure must be diagnostic and Burn generation must continue unchanged.

The TensorCube scratch buffer must never be referenced by:

```text
merged_logits
argmax
top-k
sampler
stop logic
returned logits
```

## 10. Generation lifecycle

The DECODE-01 lifecycle remains the session owner.

A successful DECODE-03 session must finalize with:

```text
raw_buffer_lease_count=2
tensorcube_dispatch_count=1
queue_submit_count=1
tensorcube_output_count=0
parity_comparison_count=0
downstream_output_commit_count=0
burn_output_authority=true
runtime_output_changed=false
```

A generation without activation continues to require the DECODE-02 zero-execution counters.

## 11. Required source surfaces

Add or modify at least:

```text
vendor_fork_scaffold/burn-fusion-local/src/live_raw_access.rs
vendor_fork_scaffold/burn-fusion-local/src/lib.rs
crates/burn_webgpu_backend/src/raw_bridge.rs
crates/burn_webgpu_backend/src/tensorcube_decode_03_live_dispatch.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d0r1_shadow_observer_owner.rs
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/native_wgpu.rs
crates/orchestrator_local/src/ash_tcu_decode_03_live_same_device_shadow_dispatch_splice_report.rs
crates/orchestrator_local/src/bin/ash_tcu_decode_03_live_same_device_shadow_dispatch_splice.rs
crates/orchestrator_local/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

## 12. Live smoke

Static inspection is insufficient for PASS.

The Rust audit executable must:

1. validate the DECODE-02 local manifest and immutable route evidence;
2. load the local v5 model spec and checkpoint set;
3. construct `NativeWgpuModel` with vocab atlas enabled and tile size 1024;
4. explicitly activate DECODE-03;
5. run one real generation projection;
6. require a live dispatch receipt;
7. verify the exact counter and authority contract;
8. verify model spec and checkpoints were not mutated.

Missing local model assets select HOLD, not PASS.

## 13. Rust-owned artifacts

The bake ZIP contains source only.

It must contain no pre-generated:

```text
activation receipt
live dispatch receipt
report
verdict
final seal
local manifest
immutable artifact bundle
latest mirror
SHA sidecar
```

The Rust executable owns:

```text
artifacts/tensorcube/decode_03/<execution_id>/
workspace/runtime/tensorcube/ash_tensorcube_decode_03_*_latest.json
```

`local_manifest` is generated last from the actual artifact bytes produced by the same execution.

## 14. Protected state

The audit must preserve:

```text
DECODE-02 route identity and digest
model spec
checkpoint bytes
model weights
LoRA weights
sampler behavior
KV semantics
tokenizer assets
route registry and epoch
production authority
Burn returned logits
```

## 15. PASS conditions

PASS requires:

- exact DECODE-02 execution ID and route digest;
- actual model/checkpoint load;
- explicit DECODE-03 activation;
- live Fusion resolution for both inputs;
- no fixture registry use;
- two strict same-runtime raw leases;
- canonical M1/N1024/K2048 invocation;
- exactly one `[64,1,1]` dispatch and one queue submit;
- no host upload, poll, map, readback, parity or output commit;
- Burn remains the sole logits authority;
- runtime output is unchanged;
- session finalizes exactly once;
- Rust-generated artifact manifest is complete.

## 16. HOLD conditions

```text
parent_manifest_not_found
parent_route_evidence_not_found
local_model_assets_not_resolved
burn_raw_access_feature_not_enabled
runtime_handles_not_available
live_fusion_resolution_unavailable
actual_live_model_smoke_not_executed
```

## 17. FAIL conditions

```text
parent_execution_or_route_digest_mismatch
fixture_override_used
host_upload_fallback_used
cross_runtime_lease_detected
wrong_shape_or_dispatch
ragged_tail_dispatched
more_than_one_dispatch
readback_or parity_performed
shadow_output_committed
Burn output authority changed
runtime output changed
model or tokenizer assets mutated
fabricated execution receipt
```

## 18. Required execution

```powershell
cargo run --locked `
  --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_decode_03_live_same_device_shadow_dispatch_splice -- `
  --repo-root <ASH_ROOT> `
  --model-spec <MODEL_SPEC_V5_48259> `
  --checkpoint <CHECKPOINT_PATH> `
  --parent-manifest .\workspace\runtime\tensorcube\ash_tensorcube_decode_02_local_manifest_latest.json `
  --smoke-token-id 1 `
  --activate-live-shadow-dispatch `
  --run-live-generation-smoke `
  --require-single-dispatch-per-generation `
  --require-strict-live-fusion-raw-access `
  --require-same-device-and-queue `
  --require-no-host-upload `
  --require-no-readback `
  --require-no-parity `
  --require-burn-output-authority `
  --require-no-runtime-output-change `
  --write-runtime-artifacts `
  --write-local-manifest
```

## 19. Expected PASS

```text
PASS_ASH_TCU_DECODE_03_LIVE_SAME_DEVICE_SHADOW_DISPATCH_SPLICE
verdict=live_same_device_m1_n1024_k2048_shadow_dispatch_submitted_once_unobserved_with_burn_output_authority_preserved
execution_id=decode03-<digest-prefix>
route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
raw_buffer_lease_count=2
tensorcube_dispatch_count=1
queue_submit_count=1
readback_count=0
local_manifest=<ASH_ROOT>\workspace\runtime\tensorcube\ash_tensorcube_decode_03_local_manifest_latest.json
```

## 20. Next state

A PASS authorizes only:

```text
ASH-TCU-DECODE-04_LIVE_SHADOW_COMPLETION_READBACK_PARITY_GATE
```

It does not authorize output promotion, sampler consumption, all-tile dispatch, repeated per-token dispatch or Burn fallback removal.
