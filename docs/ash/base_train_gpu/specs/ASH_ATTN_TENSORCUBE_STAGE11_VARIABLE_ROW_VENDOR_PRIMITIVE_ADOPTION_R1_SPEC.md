# ASH-ATTN-TENSORCUBE-STAGE11-VARIABLE-ROW-VENDOR-PRIMITIVE-ADOPTION-R1

## Status

```text
Mode: ACTUAL PHYSICAL CANDIDATE BACKEND BINDING
Shadow only: false
Canonical semantic authority: burn_webgpu_backend::TensorCubeStage11OnlineSoftmaxPipeline
Candidate physical merge authority: burn-wgpu-local::VendorVariableRowOnlineSoftmax
Oracle verification authority: existing TensorCube Stage11 oracle merge
```

## Parent SSOT

```text
ASH-BURN-VENDOR-VARIABLE-ROW-ONLINE-SOFTMAX-DESCRIPTOR-DISPATCH-AND-FP32-STATE-REDUCTION-R1
ASH-BURN-VENDOR-MIXED-PRECISION-TENSOR-PRIMITIVES-FP16-BF16-STORAGE-FP32-ACCUMULATION-R1
ASH-BURN-VENDOR-GPU-RESIDENT-VERIFICATION-COMPACT-READBACK-RECEIPT-ASYNC-STAGING-RING-AND-SUBMISSION-COALESCING-R1
```

## Actual binding

This revision does not introduce a shadow candidate. The old TensorCube candidate merge dispatch is retired from the candidate execution path.

```text
Stage10 candidate statistics
        ↓
Stage11-owned descriptor projection
        ↓
Vendor pre-reduced FP32 online-softmax merge
        ↓
candidate_global_state
        ↓
existing independent Stage11 oracle verification
        ↓
Stage12 handoff
```

`candidate_global_state` is the same state handle handed to the downstream W6/Stage12 path, so the vendor-produced state is the actual candidate execution result.

## Stage10 contract

Stage11 consumes Stage10 retained statistics, not a reconstructed full score matrix:

```text
local max / local exp-sum / local count / flags
```

The vendor path consumes the existing GPU-resident Stage10 `candidate_statistics` buffer directly. No raw-score reconstruction and no Stage10 statistics payload D2H are introduced.

## Vendor descriptor

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

```text
VARIABLE_ROW_PREREDUCED_DESCRIPTOR_BYTES = 32
VARIABLE_ROW_PREREDUCED_STAGE11_REVISION = STAGE10_PREREDUCED_MAX_SUM_COUNT_DESCRIPTOR_R1
```

Stage11 owns the row/head/global-state projection. Vendor code does not reconstruct query position, key position, causal policy, or Q/K/V semantics.

## Physical candidate merge

`TensorCubeStage11OnlineSoftmaxPipeline` now calls:

```rust
VendorVariableRowOnlineSoftmax::encode_prereduced_stage11_merge(...)
```

with:

```text
live Stage10 candidate_statistics
candidate_global_state
candidate_write_counts
candidate status lane
caller-owned CommandEncoder
```

The previous `candidate_merge.bind_group`, `candidate_merge.pass`, and candidate dispatch through the old TensorCube merge pipeline are absent from the active candidate path.

## Oracle and verification

The existing TensorCube oracle merge remains independent:

```text
Stage10 oracle_statistics -> existing merge shader -> oracle_global_state
```

The existing Stage11 verify shader still compares candidate and oracle state records, candidate/oracle write counts, final flags, canonical order, finite state, all-masked contract, and committed token counts.

There is no fallback from vendor candidate failure to the retired candidate kernel inside the same stream. Missing feature, invalid descriptor, vendor encode failure, or candidate/oracle mismatch fail closed.

## Numerical authority

Stage11 global state remains:

```text
x = running max f32 bits
y = running denominator f32 bits
z = accumulated valid count
w = Stage11 flags
```

The pre-reduced vendor shader preserves FP32 online-softmax merge:

```text
next_max = max(running_max, local_max)
next_sum = running_sum * exp(running_max - next_max)
         + local_sum   * exp(local_max   - next_max)
```

No approximate exponential and no half-precision Stage11 running state are introduced.

## Candidate backend identity

```text
TENSORCUBE_STAGE11_CANDIDATE_BACKEND_REVISION =
ASH-ATTN-TENSORCUBE-STAGE11-VENDOR-PREREDUCED-ACTIVE-R1
```

This revision is bound into `TensorCubeStage11PipelineIdentity.identity_digest` and the final Stage11 receipt so an old candidate-kernel result cannot be reported as vendor-active.

## GPU residency and submission

```text
stage10_statistics_payload_readback_count = 0
full_score_matrix_allocation_count = 0
full_probability_matrix_allocation_count = 0
```

Inside `encode_prereduced_stage11_merge`:

```text
queue.submit = 0
MAP_READ = 0
PollType::Wait = 0
```

Stage11 retains encoder/submission ownership.

## Static closure

```text
tools/validate_ash_attn_tensorcube_stage11_variable_row_vendor_primitive_active_adoption_r1_static.py
83/83 PASS
```

Parent static gates retained:

```text
Vendor variable-row softmax 100/100 PASS
Vendor mixed precision       70/70 PASS
Vendor compact readback      64/64 PASS
Generation-sealed Muon cache 66/66 PASS
Muon backend surface rebind  35/35 PASS
```

The active-adoption gate verifies old candidate dispatch removal, real Stage10 candidate-statistics binding, vendor candidate state/write-count/status binding, oracle preservation, existing candidate/oracle verification, downstream Stage12 use of candidate global state, no raw-score reconstruction, and no vendor-owned submit/readback/blocking poll.

## Evidence boundary

The bake environment has no Cargo/Rust/WGSL compiler toolchain. Therefore:

```text
STATIC_BAKED_READY
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_WGSL_COMPILE_CLAIM
PHYSICAL_W6_GATE_REQUIRED
NO_UNMEASURED_PERFORMANCE_CLAIM
```

User-local Cargo and physical GPU execution are the final execution SSOT.

## Bake files

Overlay contains exactly six files:

```text
vendor_fork_scaffold/burn-wgpu-local/src/variable_row_softmax.rs
vendor_fork_scaffold/burn-wgpu-local/src/shaders/variable_row_prereduced_softmax_merge.wgsl
vendor_fork_scaffold/burn-wgpu-local/src/lib.rs
crates/burn_webgpu_backend/src/tensorcube_stage11_online_softmax_merge.rs
crates/burn_webgpu_backend/src/lib.rs
tools/validate_ash_attn_tensorcube_stage11_variable_row_vendor_primitive_active_adoption_r1_static.py
```

Code ZIPs contain no Markdown and no `*.sha256` files.

## Physical gate

Physical evidence must prove:

```text
burn-raw-access-local enabled
vendor pre-reduced shader compiles
vendor candidate dispatch executes
oracle merge executes
candidate_oracle_mismatch_count = 0
candidate_write_count_mismatch_count = 0
oracle_write_count_mismatch_count = 0
canonical_order_violation_count = 0
non_finite_state_count = 0
invalid_zero_sum_count = 0
stage11 pass = true
Stage12 handoff receives vendor-produced candidate_global_state
```

## Promotion seal

```text
PROMOTE_ASH_ATTN_TENSORCUBE_STAGE11_VARIABLE_ROW_VENDOR_PRIMITIVE_ADOPTION_R1
ACTUAL_VENDOR_CANDIDATE_BACKEND
NOT_SHADOW_ONLY
STAGE10_PREREDUCED_STATISTICS_DIRECT_GPU_BINDING
NO_RAW_SCORE_RECONSTRUCTION
ZERO_STAGE10_STATISTICS_PAYLOAD_READBACK
STAGE11_OWNED_DESCRIPTOR_PROJECTION
VENDOR_PREREDUCED_FP32_ONLINE_MERGE
CANONICAL_CANDIDATE_GLOBAL_STATE_WRITE
OLD_TENSORCUBE_CANDIDATE_MERGE_RETIRED_FROM_EXECUTION
EXISTING_TENSORCUBE_ORACLE_MERGE_PRESERVED
EXISTING_CANDIDATE_ORACLE_VERIFY_PRESERVED
DOWNSTREAM_STAGE12_HANDOFF_USES_VENDOR_CANDIDATE_STATE
NO_MID_STREAM_FALLBACK
CALLER_OWNED_ENCODER
NO_VENDOR_SUBMIT
NO_VENDOR_READBACK
NO_VENDOR_BLOCKING_POLL
NO_STAGE12_ALGORITHM_MUTATION
NO_FLASH_ATTENTION_FUSION
SEALED
```