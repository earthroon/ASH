# ASH-ATTN-TENSORCUBE-STAGE11-VARIABLE-ROW-VENDOR-PRIMITIVE-ADOPTION-R1

## Status

```text
Patch ID:
ASH-ATTN-TENSORCUBE-STAGE11-VARIABLE-ROW-VENDOR-PRIMITIVE-ADOPTION-R1

Mode:
ACTUAL PHYSICAL CANDIDATE BACKEND BINDING

Not Shadow:
true

Canonical Stage11 semantic authority:
burn_webgpu_backend::TensorCubeStage11OnlineSoftmaxPipeline

Candidate physical merge authority:
burn-wgpu-local::VendorVariableRowOnlineSoftmax

Oracle verification authority:
existing TensorCube Stage11 oracle merge
```

## Parent SSOT

```text
ASH-BURN-VENDOR-VARIABLE-ROW-ONLINE-SOFTMAX-DESCRIPTOR-DISPATCH-AND-FP32-STATE-REDUCTION-R1

ASH-BURN-VENDOR-MIXED-PRECISION-TENSOR-PRIMITIVES-FP16-BF16-STORAGE-FP32-ACCUMULATION-R1

ASH-BURN-VENDOR-GPU-RESIDENT-VERIFICATION-COMPACT-READBACK-RECEIPT-ASYNC-STAGING-RING-AND-SUBMISSION-COALESCING-R1
```

## Central authority rule

This revision does not create a shadow Stage11 path.

The Stage11 candidate global state handed downstream is physically produced by the vendor primitive. The previous TensorCube candidate merge kernel is removed from the candidate execution path. The existing TensorCube oracle merge remains present only as an independent verifier and is compared against the vendor-produced candidate state by the existing Stage11 verification kernel.

```text
Stage10 candidate statistics
        ↓
Stage11 descriptor projection
        ↓
Vendor pre-reduced variable-row merge
        ↓
canonical candidate_global_state
        ↓
existing Stage11 candidate/oracle verification
        ↓
Stage12 handoff
```

The downstream `AttentionInterconnectW6Stage12Handoff.global_softmax_state_handle` continues to carry the Stage11 `candidate_global_state`, therefore vendor output is the actual TensorCube candidate state consumed by the next TensorCube stage.

## Important Stage10 contract

Current TensorCube Stage11 does not consume a full score/probability matrix. Stage10 already emits retained per-row/per-head/per-KV-block statistics records:

```text
local max
local exp-sum
local count
flags
```

Therefore this adoption does not reconstruct raw scores and does not introduce Stage10 score readback or score re-materialization.

A new vendor pre-reduced descriptor surface consumes the exact Stage10 statistics ABI directly.

## Vendor pre-reduced descriptor

```rust
pub struct VariableRowPreReducedSoftmaxDescriptor {
    pub local_record_offset: u32,
    pub kv_block_count: u32,
    pub global_state_index: u32,
    pub expected_prior_write_count: u32,
    pub committed_token_count: u32,
    pub is_final_chunk: bool,
    pub merge_step_ordinal: u32,
}
```

ABI:

```text
VARIABLE_ROW_PREREDUCED_DESCRIPTOR_BYTES = 32
VARIABLE_ROW_PREREDUCED_STAGE11_REVISION =
STAGE10_PREREDUCED_MAX_SUM_COUNT_DESCRIPTOR_R1
```

The descriptor contains physical execution information only. It does not contain query-position, key-position, Q/K/V semantics, or an independently reconstructed causal rule.

## Stage11 descriptor projection authority

`TensorCubeStage11OnlineSoftmaxPipeline` projects one descriptor for each active:

```text
q tile
× active query row
× query head
```

The canonical global state index is preserved as:

```text
((q_tile_index * 16 + query_row) * query_heads) + query_head
```

The local Stage10 statistics record offset is preserved as:

```text
((query_row * query_heads) + query_head) * kv_block_count
```

Stage11, not the vendor, owns these projections.

## Actual candidate backend replacement

Retired from the candidate execution path:

```text
candidate_merge.params
candidate_merge.bind_group
candidate_merge.pass
candidate dispatch through TensorCube merge_pipeline
```

Candidate execution now calls:

```rust
VendorVariableRowOnlineSoftmax::encode_prereduced_stage11_merge(...)
```

with the live Stage10 `candidate_statistics` GPU buffer and the canonical Stage11:

```text
candidate_global_state
candidate_write_counts
candidate status lane
```

There is no baseline candidate fallback in the same stream. When the required `burn-raw-access-local` feature is absent, execution fails closed instead of silently restoring the old candidate kernel.

## Oracle preservation

The existing Stage11 oracle path remains unchanged:

```text
Stage10 oracle_statistics
    ↓
existing TensorCube merge shader
    ↓
oracle_global_state
```

The oracle is not the downstream state authority. It exists to independently verify the vendor-produced candidate state.

## Bitwise verification closure

The existing Stage11 verify shader remains authoritative and compares:

```text
candidate_state record
oracle_state record
candidate write count
oracle write count
final flags
canonical order
finite state
mask/all-masked contract
committed token count
```

`candidate_oracle_mismatch_count` must remain zero for physical promotion.

This means actual vendor adoption is guarded by the existing independent TensorCube oracle rather than by a new self-referential vendor verifier.

## Vendor pre-reduced shader semantics

New shader:

```text
vendor_fork_scaffold/burn-wgpu-local/src/shaders/
variable_row_prereduced_softmax_merge.wgsl
```

For each descriptor it:

1. reads Stage10 local statistics in canonical block order;
2. validates `FINAL_WRITE`, duplicate-write, finite max/sum, positive sum, and count contracts;
3. merges local states using FP32 online-softmax rescaling;
4. preserves the previous Stage11 global state when processing later chunks;
5. atomically verifies expected prior write count;
6. seals canonical-order/final-write/all-masked flags on the final chunk;
7. writes the canonical candidate global state record.

Core merge remains:

```text
next_max = max(running_max, local_max)

next_sum =
    running_sum * exp(running_max - next_max)
  + local_sum   * exp(local_max   - next_max)
```

No approximate exponential and no half-precision Stage11 state are introduced.

## FP32 state authority

The Stage11 global state ABI remains:

```text
16 bytes / record

x = running max f32 bits
y = running denominator f32 bits
z = accumulated valid count
w = Stage11 flags
```

The vendor mixed-precision parent remains available for later score/storage work, but this pre-reduced adoption does not quantize Stage10 statistics or Stage11 global state.

```text
Stage10 retained statistics = existing F32 semantic ABI
Stage11 running max = F32
Stage11 denominator = F32
Stage11 count = u32
Stage11 flags = u32
```

## GPU residency

This revision preserves:

```text
stage10_statistics_payload_readback_count = 0
full_score_matrix_allocation_count = 0
full_probability_matrix_allocation_count = 0
```

The candidate Stage10 statistics buffer is consumed directly as a GPU storage buffer.

No GPU -> CPU -> GPU Stage11 merge loop is introduced.

## Submission ownership

The vendor primitive receives the Stage11 caller-owned command encoder.

Inside `encode_prereduced_stage11_merge`:

```text
queue.submit = 0
MAP_READ = 0
PollType::Wait = 0
```

Stage11 retains submission ownership and existing completion/readback semantics.

## Candidate backend identity

New identity:

```text
TENSORCUBE_STAGE11_CANDIDATE_BACKEND_REVISION =
ASH-ATTN-TENSORCUBE-STAGE11-VENDOR-PREREDUCED-ACTIVE-R1
```

The revision is included in `TensorCubeStage11PipelineIdentity.identity_digest` and surfaced on the final Stage11 receipt.

This prevents a result produced by the retired candidate kernel from being silently reported as the vendor-active revision.

## No mid-stream fallback

There is no runtime branch that falls back to the previous candidate merge kernel when the vendor path fails.

```text
vendor feature missing -> fail closed
vendor descriptor invalid -> fail closed
vendor mutex poisoned -> fail closed
vendor merge encode failure -> fail closed
candidate/oracle state mismatch -> Stage11 gate failure
```

The independent oracle remains verification evidence, not fallback execution authority.

## Static closure

New static gate:

```text
tools/validate_ash_attn_tensorcube_stage11_variable_row_vendor_primitive_active_adoption_r1_static.py

82/82 PASS
```

It verifies, among other things:

```text
old candidate bind group absent
old candidate pass absent
old candidate pipeline dispatch absent
vendor candidate merge present
real Stage10 candidate statistics bound
canonical candidate global state bound
canonical candidate write counts bound
oracle path preserved
candidate/oracle verifier preserved
downstream Stage12 handoff still uses candidate global state
no raw-score reconstruction in vendor pre-reduced shader
no Q/K/V or causal-policy reconstruction in vendor shader
no primitive-owned submit/readback/blocking poll
```

Parent gates retained in the bake environment:

```text
Vendor variable-row softmax     100/100 PASS
Vendor mixed precision           70/70 PASS
Vendor compact readback          64/64 PASS
Generation-sealed Muon cache     66/66 PASS
Muon backend surface rebind      35/35 PASS
```

## Physical gate

The existing W6 physical path is now the relevant physical execution harness because `TensorCubeStage11OnlineSoftmaxPipeline` itself has been rewired.

Physical evidence must prove:

```text
burn-raw-access-local enabled
vendor pre-reduced shader compiles
vendor candidate dispatch executes
oracle merge executes
candidate/oracle mismatch count = 0
candidate write-count mismatch = 0
oracle write-count mismatch = 0
canonical-order violation = 0
nonfinite state count = 0
invalid zero-sum count = 0
stage11 pass = true
Stage12 handoff receives vendor-produced candidate_global_state
```

## Evidence boundary

The bake environment does not contain Cargo/Rust/WGSL compiler tooling, therefore:

```text
STATIC_BAKED_READY
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_WGSL_COMPILE_CLAIM
PHYSICAL_W6_GATE_REQUIRED
NO_UNMEASURED_PERFORMANCE_CLAIM
```

User-local Cargo and physical GPU output remain the final execution SSOT.

## Non-goals

```text
No shadow-only execution
No raw score reconstruction
No Stage10 score D2H
No half Stage11 global state
No Stage12 algorithm mutation
No V weighted-accumulation rewrite
No FlashAttention fusion
No old candidate fallback
No oracle retirement
No baseline verification retirement
No automatic performance claim
```

## Bake files

Overlay contains:

```text
vendor_fork_scaffold/burn-wgpu-local/src/variable_row_softmax.rs
vendor_fork_scaffold/burn-wgpu-local/src/shaders/variable_row_prereduced_softmax_merge.wgsl
vendor_fork_scaffold/burn-wgpu-local/src/lib.rs
crates/burn_webgpu_backend/src/tensorcube_stage11_online_softmax_merge.rs
crates/burn_webgpu_backend/src/lib.rs
tools/validate_ash_attn_tensorcube_stage11_variable_row_vendor_primitive_active_adoption_r1_static.py
```

Code ZIPs contain no Markdown and no `*.sha256` files.

## Promotion seal

```text
PROMOTE_ASH_ATTN_TENSORCUBE_STAGE11_VARIABLE_ROW_VENDOR_PRIMITIVE_ADOPTION_R1

ACTUAL_VENDOR_CANDIDATE_BACKEND
NOT_SHADOW_ONLY

STAGE10_PREREDUCED_STATISTICS_DIRECT_GPU_BINDING
NO_RAW_SCORE_RECONSTRUCTION
ZERO_STAGE10_STATISTICS_PAYLOAD_READBACK

STAGE11_OWNED_DESCRIPTOR_PROJECTION
QUERY_ROW_HEAD_IDENTITY_PRESERVED
KV_BLOCK_COUNT_PRESERVED
PRIOR_WRITE_ORDER_PRESERVED
COMMITTED_TOKEN_COUNT_PRESERVED
FINAL_CHUNK_SEMANTICS_PRESERVED

VENDOR_PREREDUCED_FP32_ONLINE_MERGE
CANONICAL_CANDIDATE_GLOBAL_STATE_WRITE
CANONICAL_CANDIDATE_WRITE_COUNT_WRITE
CANONICAL_CANDIDATE_STATUS_LANE_WRITE

OLD_TENSORCUBE_CANDIDATE_MERGE_RETIRED_FROM_EXECUTION
EXISTING_TENSORCUBE_ORACLE_MERGE_PRESERVED
EXISTING_CANDIDATE_ORACLE_VERIFY_PRESERVED

DOWNSTREAM_STAGE12_HANDOFF_USES_VENDOR_CANDIDATE_STATE

NO_MID_STREAM_FALLBACK
FEATURE_MISSING_FAIL_CLOSED
VENDOR_FAILURE_FAIL_CLOSED
CANDIDATE_ORACLE_MISMATCH_FAIL_CLOSED

CALLER_OWNED_ENCODER
NO_VENDOR_SUBMIT
NO_VENDOR_READBACK
NO_VENDOR_BLOCKING_POLL

NO_STAGE12_ALGORITHM_MUTATION
NO_FLASH_ATTENTION_FUSION
NO_AUTOMATIC_PERFORMANCE_CLAIM

SEALED
```