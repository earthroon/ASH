# ASH-BURN-VENDOR-GPU-RESIDENT-VERIFICATION-COMPACT-READBACK-RECEIPT-ASYNC-STAGING-RING-AND-SUBMISSION-COALESCING-R1

## Patch

```text
ASH-BURN-VENDOR-GPU-RESIDENT-VERIFICATION-COMPACT-READBACK-RECEIPT-ASYNC-STAGING-RING-AND-SUBMISSION-COALESCING-R1

GPU-Resident Verification Authority /
Compact Verification Receipt /
Persistent Readback Staging Ring /
Commit-Critical Compact Harvest /
Caller-Owned Alias Materialization Encoder /
Submission Coalescing /
No Eligible Source Boundary Full Tensor Readback /
No Muon Or Optimizer Math Mutation
```

## Parent SSOT

Code parent:

```text
ASH-BASETRAIN-TENSORCUBE-MUON-IMMUTABLE-CACHE-BACKEND-SURFACE-REBIND-R1
```

The parent BaseTrain/TensorCube/Muon authority remains unchanged. This patch is confined to the local Burn vendor scaffold readback, verification, and external-alias materialization mechanics.

## Problem inventory

The parent `burn-wgpu-local` native LoRA path performed source/candidate verification with repeated full GPU-to-CPU readbacks:

```text
candidate source-no-write boundary:
source A before
source B before
candidate dispatch
source A after
source B after

guarded source-plus-delta commit:
source A before
source B before
candidate delta A
candidate delta B
commit dispatch
source A after
source B after
```

Each helper readback allocated a MAP_READ staging buffer, created a command encoder, submitted a copy, mapped it, and called `device.poll(PollType::Wait)`.

The full candidate direction-vector readback is not retired in this R1 because upper parity code still consumes actual vector values. It is not classified as reducible verification until that upper contract changes explicitly.

## Authority boundary

```text
burn-wgpu-local
= GPU evidence production
= snapshot buffers
= compact compare kernels
= staging ring
= map lifecycle
= local queue submission batching

ASH/model_core/BaseTrain
= semantic PASS/FAIL authority
= optimizer commit authority
= generation authority
= training route authority
```

The vendor scaffold does not become trainable tensor, optimizer, or checkpoint authority.

## GPU compact verification module

New module:

```text
vendor_fork_scaffold/burn-wgpu-local/src/gpu_resident_verification.rs
```

New WGSL:

```text
vendor_fork_scaffold/burn-wgpu-local/src/shaders/gpu_resident_verification_compact.wgsl
```

Receipt ABI:

```text
GPU_VERIFICATION_RECEIPT_ABI_V1 = 1
GPU_VERIFICATION_RECEIPT_BYTES = 64
GPU_VERIFICATION_RECEIPT_MAGIC = 0x41534856
```

## Verification modes

```text
SourceUnchanged
SourcePlusDelta
```

`SourceUnchanged` compares GPU snapshots captured before candidate generation against the same source buffers after the candidate kernel.

`SourcePlusDelta` compares `snapshot_before + candidate_delta` against the actual source buffers after the guarded commit.

The tolerance remains the parent semantic value `1.0e-5`. No new optimizer or Muon tolerance is introduced.

## GPU-side receipt

WGSL produces bounded evidence:

```text
magic
ABI revision
mode
A/B element count
mismatch count
nonfinite count
changed count
maximum absolute verification error
submission epoch
verification epoch
slot generation
```

No variable-length tensor payload is part of the compact receipt.

## Candidate source-no-write binding

The candidate path now performs in one coalesced encoder:

```text
GPU copy source A -> persistent snapshot A
GPU copy source B -> persistent snapshot B
candidate delta compute
GPU source-unchanged verification
64-byte receipt copy
one queue submit
```

The existing `NativeLoraSourceNoWriteProof` authority is populated through `from_compact_candidate_boundary(...)`. Old candidate source before/after full-readback labels are retired.

## Commit verification binding

The guarded source-plus-delta commit now performs in one coalesced encoder:

```text
GPU copy source A -> persistent snapshot A
GPU copy source B -> persistent snapshot B
commit_source_plus_delta compute
GPU snapshot + delta vs source-after verification
64-byte receipt copy
one queue submit
```

The existing proof is updated through `with_compact_commit_verification(...)`. The old source-before, candidate-delta, and source-after full-tensor commit readbacks are retired from the commit path.

## Persistent resources

The verifier owns a reusable snapshot pair and a bounded readback ring. Default ring depth is 3, clamped to 2..8.

Each ring slot owns persistent:

```text
GPU receipt storage buffer
MAP_READ staging buffer
uniform params buffer
slot generation
submission epoch
verification epoch
map receiver
state
```

States are `Idle`, `Encoded`, `Submitted`, `Mapping`, and `Ready`. Busy slots are not silently overwritten.

## Async map and blocking boundary

Receipt mapping uses `map_async`. A nonblocking harvest path uses `PollType::Poll` for delayed/informational receipts.

The currently integrated candidate source-boundary and commit receipts are commit-critical. They use one explicit `PollType::Wait` for the 64-byte receipt before returning the semantic gate result.

This R1 does not claim zero blocking waits for commit-critical verification. It replaces multiple full-tensor blocking readbacks with one compact blocking receipt per required boundary.

Telemetry distinguishes:

```text
commit_critical_blocking_poll_count
hot_path_blocking_poll_count
```

## Full vector parity preservation

`readback_actual_candidate_delta_buffers(...)` remains because upper native parity code consumes actual candidate delta vectors and direction samples.

Therefore:

```text
full candidate direction vector readback preserved
source-boundary reducible full readback retired
commit reducible full readback retired
```

No silent weakening of parity evidence is allowed.

## Telemetry

```text
eligible_full_tensor_readback_count
full_tensor_readback_avoided_bytes
compact_receipt_readback_count
compact_receipt_readback_bytes
staging_buffer_allocation_count
staging_buffer_reuse_count
async_map_count
commit_critical_blocking_poll_count
hot_path_blocking_poll_count
submission_count
coalesced_copy_count
ring_slot_busy_reject_count
stale_receipt_reject_count
receipt_harvest_latency_ns_total
snapshot_allocation_count
snapshot_reuse_count
```

`BurnWgpuLocalNativeTrainExecutor` exposes vendor-local telemetry via `gpu_resident_verification_telemetry()`.

## External alias submission coalescing

`WgpuStorage` now provides `encode_external_alias_materialization(...)`, which records alias-to-owned copies into a caller-owned `CommandEncoder` without submitting immediately.

The returned `ExternalOwnedMaterializePending` must be finalized only after the caller submits the encoder through `finalize_after_submit()`.

The existing `materialize_external_alias_to_owned(...)` compatibility wrapper is preserved and still performs its own one-copy submit.

## Failure boundaries

Fail closed on:

```text
receipt ABI mismatch
receipt epoch mismatch
ring exhaustion
slot generation drift
map callback failure
nonfinite verification data
source boundary mismatch
source-plus-delta mismatch
```

No source verification failure silently falls back to the retired full-readback route.

## Static validation

```text
tools/validate_ash_burn_vendor_gpu_resident_verification_compact_readback_r1_static.py
64/64 PASS
```

Regression validators in the bake environment:

```text
TensorCube Local Muon multi-tile       61/61 PASS
TensorCube Local Muon production       62/62 PASS
TensorCube Local Muon PAD17            52/52 PASS
Generation-Sealed Muon cache           66/66 PASS
Muon backend surface rebind            35/35 PASS
FFN multi-slot residency               78/78 PASS
FFN persistent slab                    66/66 PASS
FFN GPU timestamp/perf                101/101 PASS
FFN physical perf                      72/72 PASS
FFN fused production                   45/45 PASS
GPU70K G45                             42/42 PASS
GPU70K G27                             35/35 PASS
GPU70K export                          13/13 PASS
Atlas/HOTPATH                          56/56 PASS
HOTPATH allocation                     26/26 PASS
```

## Bake files

```text
vendor_fork_scaffold/burn-wgpu-local/src/gpu_resident_verification.rs
vendor_fork_scaffold/burn-wgpu-local/src/shaders/gpu_resident_verification_compact.wgsl
vendor_fork_scaffold/burn-wgpu-local/src/native_lora_train.rs
vendor_fork_scaffold/burn-wgpu-local/src/compute/storage.rs
vendor_fork_scaffold/burn-wgpu-local/src/lib.rs
tools/validate_ash_burn_vendor_gpu_resident_verification_compact_readback_r1_static.py
```

Markdown specs and `*.sha256` are excluded from the code ZIP.

## Current evidence status

```text
STATIC_BAKED_READY
PHYSICAL_CARGO_COMPILE_REQUIRED
PHYSICAL_GPU_PARITY_REQUIRED
PHYSICAL_PERFORMANCE_RECEIPT_REQUIRED
```

The bake environment has no `cargo`, `rustc`, or `rustfmt`, so Rust compile and physical GPU execution PASS are not claimed. User-local Cargo and physical GPU receipts are the final execution SSOT.

## Physical promotion targets

```text
candidate compact source-no-write parity PASS
source-plus-delta compact commit parity PASS
nonfinite rejection PASS
mismatch negative control PASS
ring slot generation guard PASS
ring saturation guard PASS
external alias batch encode parity PASS
```

Performance evidence should record full-tensor readback bytes avoided, compact receipt bytes, blocking polls before/after, queue submissions before/after, snapshot reuse, staging reuse, and CPU wait time. No percentage speedup is claimed until those physical receipts exist.

## Promotion seal

```text
PROMOTE_ASH_BURN_VENDOR_GPU_RESIDENT_VERIFICATION_COMPACT_READBACK_RECEIPT_ASYNC_STAGING_RING_AND_SUBMISSION_COALESCING_R1

GPU_RESIDENT_SOURCE_VERIFICATION
COMPACT_64_BYTE_RECEIPT
PERSISTENT_READBACK_RING
PERSISTENT_SOURCE_SNAPSHOT_REUSE
SOURCE_BOUNDARY_FULL_READBACK_RETIRED
COMMIT_FULL_READBACK_RETIRED
FULL_DIRECTION_VECTOR_PARITY_PRESERVED
COMMIT_CRITICAL_WAIT_EXPLICIT
NONBLOCKING_HARVEST_SURFACE_PRESENT
CALLER_OWNED_ALIAS_ENCODER_PRESENT
COMPAT_ALIAS_WRAPPER_PRESERVED
NO_MUON_MATH_MUTATION
NO_OPTIMIZER_FORMULA_MUTATION
NO_CHECKPOINT_AUTHORITY_MUTATION
SEALED
```