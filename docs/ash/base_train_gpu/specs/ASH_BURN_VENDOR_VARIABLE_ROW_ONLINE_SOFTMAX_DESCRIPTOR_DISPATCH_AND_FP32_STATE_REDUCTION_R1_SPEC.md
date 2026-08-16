# ASH-BURN-VENDOR-VARIABLE-ROW-ONLINE-SOFTMAX-DESCRIPTOR-DISPATCH-AND-FP32-STATE-REDUCTION-R1

## Patch

```text
ASH-BURN-VENDOR-VARIABLE-ROW-ONLINE-SOFTMAX-DESCRIPTOR-DISPATCH-AND-FP32-STATE-REDUCTION-R1

Generic Variable-Row Softmax Primitive /
TensorCube Stage11 Semantic Authority Preservation /
Per-Row Descriptor Authority /
Exact Active-Block Dispatch /
Online FP32 State Merge /
F32 / Packed FP16 / Packed BF16 Score Storage /
FP32 Running Maximum /
FP32 Running Denominator /
FP32 Normalization /
Caller-Owned Command Encoder /
No Primitive-Owned Queue Submit /
No Primitive-Owned Readback /
No Primitive-Owned Blocking Poll /
No Automatic Stage11 Production Promotion
```

## Parent SSOT

Direct parent:

```text
ASH-BURN-VENDOR-MIXED-PRECISION-TENSOR-PRIMITIVES-FP16-BF16-STORAGE-FP32-ACCUMULATION-R1
```

Infrastructure parent:

```text
ASH-BURN-VENDOR-GPU-RESIDENT-VERIFICATION-COMPACT-READBACK-RECEIPT-ASYNC-STAGING-RING-AND-SUBMISSION-COALESCING-R1
```

The existing `TensorCubeStage11OnlineSoftmaxPipeline` remains the attention/causal/global-state semantic authority. This patch adds a vendor physical primitive only.

## Authority boundary

```text
burn-wgpu-local
= row/block descriptor execution
= score storage decode
= block-local max/sum reduction
= deterministic block-state merge
= FP32 normalization
= reusable descriptor/state/scratch buffers

burn_webgpu_backend / TensorCube Stage11
= attention semantics
= causal/mask policy
= query/KV geometry authority
= Stage11 state lifecycle authority
= production adoption decision
```

The vendor primitive contains no query-position/key-position causal policy and does not replace Stage11 in this revision.

## Descriptor ABI

```text
VARIABLE_ROW_SOFTMAX_DESCRIPTOR_ABI_V1 = 1
VARIABLE_ROW_SOFTMAX_DESCRIPTOR_BYTES = 64
VARIABLE_ROW_SOFTMAX_BLOCK_DESCRIPTOR_BYTES = 16
VARIABLE_ROW_SOFTMAX_BLOCK_ELEMENTS = 256
VARIABLE_ROW_SOFTMAX_STATE_BYTES = 16
VARIABLE_ROW_SOFTMAX_STATUS_BYTES = 96
```

Each row descriptor binds:

```text
source_offset_elements
destination_offset_elements
active_length
physical_stride
mask_begin
mask_end
state_index
state_epoch
Initialize | Continue
bucket
block_offset
block_count
effective_count
```

Rows with zero effective domain, invalid mask extents, `active_length > physical_stride`, out-of-range source/destination domains, mismatched dispatch epoch, or duplicate `state_index` inside one wave fail closed before physical dispatch.

## Exact active-block scheduling

The CPU-side descriptor compiler deterministically sorts rows by:

```text
length bucket
state index
source offset
destination offset
```

Bucket policy revision:

```text
DETERMINISTIC_LENGTH_BUCKET_BLOCK256_R1
```

Buckets:

```text
1..64
65..128
129..256
257..512
513..1024
1025..2048
2049+
```

Each row's effective mask span is split into exact 256-element-or-smaller block descriptors. There is no max-row rectangle allocation authority and no block descriptor is created for inactive physical tail elements.

## GPU pipeline

New vendor WGSL:

```text
vendor_fork_scaffold/burn-wgpu-local/src/shaders/variable_row_online_softmax.wgsl
```

Physical passes:

```text
prepare_rows
    -> clear active destination domain
    -> validate defensive row contract

reduce_blocks
    -> exact active block only
    -> workgroup FP32 maximum
    -> FP32 exp(score - max) sum
    -> nonfinite observation
    -> 16-byte block state

merge_rows
    -> deterministic ascending block merge
    -> Initialize or Continue previous state
    -> FP32 running maximum
    -> FP32 running denominator
    -> state epoch validation

normalize_blocks
    -> exact active block only
    -> exp(score - running_max) / running_denominator
    -> F32 output
```

## Mixed-precision score storage

Input score storage supports:

```text
F32Safe
Fp16StorageF32Accum
Bf16StorageF32Accum
```

The existing vendor packed-half storage contract is reused:

```text
FP16 packed u32 pairs -> unpack2x16float -> f32
BF16 packed u32 pairs -> exact BF16 expansion -> f32
```

Only score storage is half precision. The following remain FP32:

```text
block maximum
block exponential sum
running maximum
running denominator
cross-block merge arithmetic
continuation-state merge arithmetic
final normalization
F32 destination probability
```

There is no native `f16` running state and no half-precision denominator authority.

## Online state

State record revision:

```text
FP32_MAX_DENOM_COUNT_EPOCH_R1
```

Each 16-byte state record stores:

```text
running_max f32 bits
running_denominator f32 bits
running_count u32
state_epoch u32
```

`Initialize` ignores prior state and writes a new state.

`Continue` requires the existing state epoch to match the descriptor epoch and merges the previous FP32 state with the current row's deterministic block state. Stale epochs fail closed and do not overwrite the prior state.

The physical harness verifies both a valid same-epoch continuation and a stale-epoch negative control.

### Continuation output boundary

For a continuation call, newly processed score blocks are normalized against the merged running state. Previously materialized output from an earlier call is not retroactively rescaled by this R1 primitive.

Therefore continuation state is valid evidence for future Stage11 state adoption, but this R1 does not claim that independently materialized multi-call probability buffers already constitute final attention-output authority. A later Stage11 adoption must bind the primitive according to Stage11's actual state/output contract.

## Persistent resources

`VendorVariableRowOnlineSoftmax` owns reusable:

```text
uniform params buffer
row descriptor buffer
block descriptor buffer
FP32 state buffer
block-state scratch buffer
status scratch buffer
```

Row/block/state capacities grow geometrically. State-buffer growth is rejected when continuation state is authoritative; growth is allowed only when all submitted rows initialize state.

The primitive tracks descriptor/state/scratch allocation and reuse separately.

## Caller-owned execution boundary

The primitive accepts `&mut wgpu::CommandEncoder` and does not call:

```text
queue.submit
MAP_READ
PollType::Wait
```

Physical submission and diagnostic readback belong to the harness/caller. This preserves the submission-coalescing and compact-readback architecture established by the parent vendor patches.

## Status receipt

The 96-byte GPU status surface records:

```text
descriptor reject count
nonfinite input count
nonfinite state count
zero denominator count
stale state epoch count
active element count
skipped physical tail count
masked active-domain count
processed row count
logical block count
block merge count
bucket row counts
F32 input element count
FP16 input element count
BF16 input element count
Initialize row count
Continue row count
```

No full score tensor readback is required by the primitive itself.

## Physical harness

New BaseTrain binary:

```text
ash_burn_vendor_variable_row_online_softmax_harness_r1
```

The harness covers:

```text
F32 reference path
packed FP16 score-storage path
packed BF16 score-storage path
mixed row lengths
explicit masked prefix
inactive-tail NaN / large-value canaries
F32 normalization parity
half-storage finite + normalization gates
masked-domain zeroing
inactive-tail no-write proof
invalid-descriptor CPU fail-closed control
same-epoch valid continuation state merge
stale-epoch GPU negative control
persistent descriptor/state/scratch reuse
primitive submit/readback/blocking-poll counters == 0
```

The fixture deliberately places NaN/large values in inactive physical tail positions. They must not contribute to maximum, denominator, nonfinite count, or normalized output.

## Static validation

```text
tools/validate_ash_burn_vendor_variable_row_online_softmax_r1_static.py
100/100 PASS
```

Parent regression validation retained in the bake environment:

```text
Vendor mixed precision primitives                70/70 PASS
Vendor compact readback                         64/64 PASS
Generation-sealed Muon cache                    66/66 PASS
Muon backend surface rebind                     35/35 PASS
Local Muon multi-tile                           PASS
Local Muon production                           PASS
Local Muon PAD17                                PASS
FFN multi-slot                                  PASS
FFN persistent slab                             PASS
FFN GPU timestamp/perf                          PASS
FFN physical perf                               PASS
FFN fused production                            PASS
GPU70K G45                                      42/42 PASS
GPU70K G27                                      35/35 PASS
GPU70K export                                   13/13 PASS
Atlas/HOTPATH                                   56/56 PASS
HOTPATH allocation                              26/26 PASS
```

## Bake files

Overlay contains exactly seven files:

```text
vendor_fork_scaffold/burn-wgpu-local/src/variable_row_softmax.rs
vendor_fork_scaffold/burn-wgpu-local/src/shaders/variable_row_online_softmax.wgsl
vendor_fork_scaffold/burn-wgpu-local/src/lib.rs
crates/burn_webgpu_backend/src/lib.rs
crates/base_train/src/bin/ash_burn_vendor_variable_row_online_softmax_harness_r1.rs
crates/base_train/Cargo.toml
tools/validate_ash_burn_vendor_variable_row_online_softmax_r1_static.py
```

Code ZIPs contain no Markdown and no `*.sha256` files.

## Evidence status

The bake environment contains no Cargo/Rust/WGSL compiler toolchain. Therefore:

```text
STATIC_BAKED_READY
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_WGSL_COMPILE_CLAIM
PHYSICAL_GPU_HARNESS_REQUIRED
NO_STAGE11_PRODUCTION_ADOPTION_CLAIM
NO_PERFORMANCE_SPEEDUP_CLAIM
```

User-local Cargo and physical GPU output are the final execution SSOT.

## Physical promotion targets

```text
F32 variable-row reference parity PASS
FP16-storage finite + normalization PASS
BF16-storage finite + normalization PASS
inactive-tail canary isolation PASS
masked-domain isolation PASS
valid continuation state merge PASS
stale epoch rejection PASS
invalid descriptor rejection PASS
primitiveSubmitCount = 0
primitiveReadbackCount = 0
primitiveBlockingPollCount = 0
descriptorReuseCount > 0
stateReuseCount > 0
scratchReuseCount > 0
```

Performance evidence must compare active elements, dispatched block capacity, fixed-rectangle equivalent work, descriptor upload cost, GPU softmax time, and CPU descriptor-build cost before any speedup claim.

## Non-goals

```text
No TensorCube Stage11 default replacement
No causal-policy migration
No attention-mask-policy migration
No Stage12 V accumulation
No half running maximum
No half denominator
No approximate exponential
No FlashAttention semantic adoption
No fused QK+softmax
No GPU descriptor generation
No automatic production promotion
```

## Next revision

Natural adoption step:

```text
ASH-ATTN-TENSORCUBE-STAGE11-VARIABLE-ROW-VENDOR-PRIMITIVE-ADOPTION-R1
```

That revision must prove exact Stage11 state identity, causal/mask descriptor projection, canonical stream-order parity, and physical candidate-vs-existing-Stage11 receipts before authority can move.

## Promotion seal

```text
PROMOTE_ASH_BURN_VENDOR_VARIABLE_ROW_ONLINE_SOFTMAX_DESCRIPTOR_DISPATCH_AND_FP32_STATE_REDUCTION_R1

GENERIC_VENDOR_PRIMITIVE_ONLY
TENSORCUBE_STAGE11_SEMANTIC_AUTHORITY_PRESERVED
EXPLICIT_ROW_DESCRIPTOR
EXACT_ACTIVE_BLOCK_DISPATCH
NO_MAX_ROW_RECTANGLE_AUTHORITY
F32_SCORE_INPUT
PACKED_FP16_SCORE_INPUT
PACKED_BF16_SCORE_INPUT
FP32_BLOCK_MAX
FP32_BLOCK_DENOMINATOR
FP32_RUNNING_MAX
FP32_RUNNING_DENOMINATOR
DETERMINISTIC_BLOCK_MERGE
EXPLICIT_STATE_EPOCH
VALID_CONTINUATION_STATE_MERGE
STALE_EPOCH_FAIL_CLOSED
PERSISTENT_DESCRIPTOR_STATE_SCRATCH
CALLER_OWNED_ENCODER
NO_PRIMITIVE_QUEUE_SUBMIT
NO_PRIMITIVE_READBACK
NO_PRIMITIVE_BLOCKING_POLL
NO_STAGE11_SEMANTIC_MUTATION
NO_MUON_FORMULA_MUTATION
NO_OPTIMIZER_FORMULA_MUTATION
NO_AUTOMATIC_PRODUCTION_PROMOTION
SEALED
```