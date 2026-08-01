# ASH-ATTN-INTERCONNECT-W6

## Stage10 Live Chunk Statistics Adoption /
## Canonical Chunk-Order Merge /
## Running Row Maximum /
## Rescaled Exponential Sum /
## Cross-Chunk Online Softmax /
## All-Masked Row Preservation /
## Dynamic Partition Generation Binding /
## Device-Local Statistics Streaming /
## No Full Score Matrix Materialization /
## No V Consumption Yet /
## No Stage12 /
## Headwise FullActive Authority Preservation Seal

> Status: implementation specification rev.1
> Parent runtime: `ASH-ATTN-INTERCONNECT-W5` physical PASS
> Build revision: `W6-stage10-statistics-canonical-online-softmax-r1`
> Production output authority: `HeadwiseFullActive`

---

## 0. Goal

W6 adopts W5 TensorCube Stage10 live chunk statistics and merges them in canonical partition order into a device-local global softmax state.

```text
W5 Stage10 live statistics
-> retained device-local handles
-> partition generation validation
-> canonical token_start / block order
-> running row maximum
-> rescaled exponential sum
-> global softmax state
-> Stage10 owner-zero retirement
```

W6 does not consume V, produce attention context, run Stage12, mutate Headwise output, or promote TensorCube authority.

---

## 1. Authority SSOT

| State | Authority |
|---|---|
| model/layer/session/step identity | W4 live invocation identity |
| partition generation | Texture-06 frozen partition receipt |
| local chunk statistics | W5 Stage10 candidate/oracle handles |
| canonical numerical order | W6 canonical descriptor plan |
| global softmax state | W6 Stage11 state buffer |
| production context writer | Headwise FullActive |

Physical completion order, texture slot order, Q-wave heat order, and submission callback order are not numerical merge authority.

---

## 2. Stage10 retained handoff

W5 finish logic must be split so parity evidence can be emitted without dropping the statistics buffers required by W6.

```rust
pub struct TensorCubeStage10StatisticsReadyHandle {
    pub partition_generation: u64,
    pub slice_id: String,
    pub chunk_ordinal: u32,
    pub token_start: u32,
    pub token_count: u32,
    pub query_tile_index: u32,
    pub query_row_start: u32,
    pub active_query_rows: u32,
    pub kv_block_index: u32,
    pub candidate_statistics: wgpu::Buffer,
    pub oracle_statistics: wgpu::Buffer,
    pub statistics_record_count: u32,
    pub submission_serial: u64,
    pub completion_observed: bool,
    pub owner_resource_ids: Vec<String>,
}
```

Serialized receipt and physical ownership are separate objects. A JSON receipt cannot substitute for a live GPU handle.

Required:

```text
W5 parity PASS before handoff
completion observed true
same device and queue lineage
partition generation exact
statistics payload host readback 0
owner count > 0 until W6 consumption completes
```

---

## 3. Canonical merge order

Canonical order is:

```text
query tile ascending
-> query head ascending
-> token_start ascending
-> chunk ordinal ascending
-> KV block index ascending
```

Physical readiness may be out of order, but numerical merge may not consume descriptor N+1 before descriptor N.

The canonical plan includes:

```rust
pub struct TensorCubeStage11CanonicalMergeDescriptor {
    pub partition_generation: u64,
    pub descriptor_ordinal: u32,
    pub query_tile_index: u32,
    pub query_head: u32,
    pub token_start: u32,
    pub token_count: u32,
    pub chunk_ordinal: u32,
    pub kv_block_index: u32,
    pub stage10_handle_digest: String,
}
```

Required:

```text
first ordinal 0
ordinal gaps 0
ordinal duplicates 0
coverage holes 0
coverage overlaps 0
partition generation mismatch 0
```

---

## 4. Global state ABI

Each query-row/head pair owns one 16-byte state record.

```rust
#[repr(C)]
pub struct TensorCubeStage11GlobalSoftmaxState {
    pub running_max: f32,
    pub rescaled_exp_sum: f32,
    pub admitted_count: u32,
    pub flags: u32,
}
```

Flags:

```text
bit 0 initialized
bit 1 valid
bit 2 all_masked
bit 3 final
```

Initial state:

```text
running_max       -infinity
rescaled_exp_sum   0
admitted_count     0
initialized        false
valid              false
all_masked         true
final              false
```

---

## 5. Online merge equation

For current global state `(M, S, N)` and Stage10 local state `(m, s, n)`:

```text
M_next = max(M, m)
S_next = S * exp(M - M_next) + s * exp(m - M_next)
N_next = N + n
```

Special cases:

```text
n == 0 and N == 0
  preserve all-masked state

n == 0 and N > 0
  preserve prior valid state

n > 0 and N == 0
  initialize from local state

non-finite valid local values
  fail closed
```

No epsilon is silently added to the denominator.

---

## 6. Candidate and oracle streams

W6 maintains two independent global states:

```text
candidate: Texture-K Stage10 statistics
oracle:    Raw-K Stage10 statistics
```

Both consume the same canonical descriptor sequence. Final candidate/oracle state parity is checked on GPU.

This comparison alone is not a mathematical oracle. The physical gate must additionally calculate a CPU f64 reference directly from the original Q/K values and compare final running max and denominator.

---

## 7. Device-local streaming

Required path:

```text
retained Stage10 statistics buffer
-> Stage11 merge bind group
-> persistent global state buffer
-> descriptor completion
-> Stage10 statistics owner-zero
-> next descriptor
```

Forbidden:

```text
Stage10 statistics payload readback
full Stage10 atlas materialization
full score matrix
full probability matrix
host-side merge
texture-to-buffer K rehydration
```

Compact status and final global state readback are allowed in physical verification only.

---

## 8. All-masked row preservation

If no key position is causally admitted across every chunk:

```text
running_max       -infinity
rescaled_exp_sum   0
admitted_count     0
valid              false
all_masked         true
```

Forbidden substitutions:

```text
max = 0
sum = 1
uniform probability
NaN normalization
row silently dropped
```

---

## 9. Dynamic partition generation binding

All Stage10 handles and Stage11 descriptors in one merge session must share:

```text
model instance
layer
session
step
Q position snapshot
source KV generation
partition generation
exact coverage digest
device and queue lineage
```

Repartitioning during one Stage11 session is forbidden.

---

## 10. Lifetime and owner-zero

State flow:

```text
Stage10Ready
-> Stage11ConsumerAcquired
-> Stage11Submitted
-> Stage11Completed
-> Stage10StatisticsOwnerZero
```

The W5 handle cannot retire before Stage11 completion. Global state remains owned until W7 handoff or explicit session retirement.

Completion is proven by queue completion evidence, not synthetic submission serial alone.

---

## 11. No V and no Stage12

Required zero counters:

```text
v_texture_read_count                 0
v_buffer_read_count                  0
stage12_pipeline_acquire_count       0
stage12_dispatch_count               0
context_accumulator_write_count      0
attention_output_commit_count        0
production_route_mutation_count      0
```

W6 output is global softmax normalization state only.

---

## 12. Headwise authority preservation

Before and after W6:

```text
production state            HeadwiseFullActive
pointer generation          unchanged
pointer digest              unchanged
Headwise output writer      exactly 1
TensorCube output writer    0
W6 authority CAS            0
```

W6 failure may HOLD the shadow route but cannot replace or mutate Headwise production output.

---

## 13. Runtime sequence

```text
1. Revalidate W4 invocation identity
2. Revalidate W5 physical PASS lineage
3. Acquire retained Stage10 handles
4. Validate partition generation and coverage
5. Build canonical merge descriptor stream
6. Allocate candidate/oracle global state buffers
7. Initialize all rows as all-masked
8. For each descriptor in canonical order:
   a. bind candidate/oracle Stage10 statistics
   b. dispatch Stage11 merge
   c. record submission lineage
   d. retire descriptor after completion
9. Mark final state
10. Run candidate/oracle GPU parity
11. Run CPU f64 physical oracle comparison
12. Publish W6 receipt
13. Preserve Headwise authority
```

---

## 14. Physical verification matrix

Minimum matrix:

```text
q_seq                 1, 8, 16, 32
committed KV          32, 64, 192, 384, 768, 1280, 1792
chunk count           1, 2, 3, 4+
partial final chunk   required
all-masked row        required
GQA heads             32 query / 4 KV
layers                0, 10, 21
slot count            3, 4
```

Checks:

```text
canonical descriptor order exact
online max parity PASS
rescaled exp-sum parity PASS
admitted count exact
all-masked state exact
candidate/oracle GPU parity PASS
CPU f64 oracle parity PASS
Stage10 payload readback 0
full score/probability allocation 0
V/Stage12 counters 0
Headwise authority unchanged
```

---

## 15. Negative controls

```text
wrong partition generation
mixed model/layer/session/step
missing chunk
repeated chunk
reversed canonical order
out-of-order numerical consumption
non-finite local state
all-masked row converted to valid
Stage10 buffer retired before merge
host payload readback
full score allocation
V binding
Stage12 dispatch
TensorCube context commit
Headwise authority mutation
```

All must fail closed with explicit receipts.

---

## 16. W7 handoff

W6 hands W7:

```rust
pub struct TensorCubeStage11GlobalSoftmaxReadyReceipt {
    pub invocation_identity_digest: String,
    pub partition_generation: u64,
    pub canonical_merge_plan_digest: String,
    pub global_state_buffer_digest: String,
    pub query_tile_count: u32,
    pub query_head_count: u32,
    pub state_record_count: u32,
    pub all_masked_row_count: u32,
    pub cpu_f64_oracle_pass: bool,
    pub receipt_digest: String,
}
```

W7 may use the same frozen partition for a second streaming pass over K/V and perform normalized V weighted accumulation.

---

## PASS token

```text
PASS_ASH_ATTN_INTERCONNECT_W6_STAGE10_LIVE_CHUNK_STATISTICS_ADOPTION_CANONICAL_CHUNK_ORDER_MERGE_RUNNING_ROW_MAXIMUM_RESCALED_EXPONENTIAL_SUM_CROSS_CHUNK_ONLINE_SOFTMAX_ALL_MASKED_ROW_PRESERVATION_DYNAMIC_PARTITION_GENERATION_DEVICE_LOCAL_STATISTICS_STREAMING_NO_FULL_SCORE_MATRIX_NO_V_NO_STAGE12_HEADWISE_FULLACTIVE_OUTPUT_AUTHORITY_SEALED
```

## Success definition

W6 succeeds when live W5 Stage10 chunk statistics are retained and merged on the same GPU device in canonical partition order into numerically stable global softmax states, with all-masked rows preserved, no score/probability matrix materialized, no V or Stage12 activity, and Headwise FullActive remaining the sole production output authority.
