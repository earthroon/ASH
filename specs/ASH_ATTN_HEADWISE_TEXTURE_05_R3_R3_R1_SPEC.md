# ASH-ATTN-HEADWISE-TEXTURE-05-R3-R3-R1

## BaseTrain Atlas Schedule Reuse /
## LoRA Streaming LogSumExp Reuse /
## BufferAtlas·Texture Shared Wave Schedule /
## Single Active Wave Admission /
## Wave-Addressable WGSL /
## Deterministic Partial Merge /
## Fence-Gated Sequential Barrier /
## Bounded GPU Occupancy Proxy Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-05-R3-R3-R1`  
> Build revision: `HEADWISE-TEXTURE-05-R3-R3-R1-parallel-sequential-basetrain-lora-reuse-v1`  
> Parent physical evidence: `ASH-ATTN-HEADWISE-TEXTURE-05-R4`  
> Production authority: `BufferAtlasV1` unchanged  
> Candidate authority: `KvTextureGqa4V1` remains shadow-only

## 1. R4 physical basis

The R4 physical run localized the remaining latency to BufferAtlas reference execution:

```text
queue_span_ns       16,321,637,376
active_sum_ns       16,312,723,456
reference_ns        16,285,572,096
capture_ns                 102,400
candidate_ns            26,722,304
normalize_ns               159,744
compare_ns                 159,744
finalize_ns                  7,168
unattributed_ns          8,913,920
reference_gpu_share         0.998336
dominant_layer                    11
worst_seq_q                        1
worst_seq_kv                    1792
classification bufferatlas_reference_gpu_dominant
```

The host wave-poll duration is treated as coupled waiting on GPU completion rather than an independent CPU bottleneck.

## 2. Root cause

The prior reference path launches only a narrow row dispatch but each invocation performs long internal KV traversal. The shader recomputes score work across output dimensions and holds a single kernel for the full visible KV span.

R3-R3 removed full-span candidate scratch but did not make the WGSL dispatch domain wave-addressable. Microtiles remained shader-internal loop units rather than admission units.

R3-R3-R1 therefore changes both executors:

```text
BufferAtlas reference
Texture candidate
```

Both use the same bounded row×tile schedule while keeping their state, output and authority separate.

## 3. Reused ASH structures

### Base train reuse

```text
AtlasParallelBucket
SequentialLoadStep
deterministic schedule order and digest
single active group authority
bounded prepared-work queue
```

### LoRA train reuse

```text
bounded microbatch ranges
streaming logsumexp state
partial-reduce barrier
depth-one prefetch semantics
module-local lease validation
```

### TensorCube reuse

```text
deterministic tile step index
ordered accumulation
explicit partial/final operation split
```

The LoRA occupancy-minimum policy is not reused. R3-R3-R1 uses a maximum-work proxy because the objective is bounded GPU saturation, not minimum utilization.

## 4. Canonical schedule

```text
token_tile_size              32
tiles_per_wave                4
max_workgroups_per_dispatch  64
max_in_flight_waves           1
prepared_wave_capacity        1
layer_bucket_size             2
```

Schedule coverage is over:

```text
row = q_head × query_position
tile = ceil(seq_kv / 32)
```

Every `(row, tile)` pair must be covered exactly once. Each schedule step records row range, tile range, token range, workgroup count, first/last-wave flags, deterministic sort key and digest.

## 5. WGSL split

R3-R3-R1 introduces:

```text
headwise_bufferatlas_wave_partial.wgsl
headwise_texture_wave_partial.wgsl
headwise_wave_partial_merge.wgsl
headwise_wave_finalize.wgsl
```

### Partial kernels

Each workgroup owns one row and processes at most four contiguous 32-token tiles. The shader receives `tile_begin` and `tile_count`; it never starts a full-KV loop from zero.

Partial state:

```text
partial_max[row]
partial_sum[row]
partial_output[row, head_dim]
```

### Deterministic merge

For running state `(m, s, o)` and partial state `(mt, st, ot)`:

```text
m2 = max(m, mt)
s2 = s  * exp(m  - m2) + st * exp(mt - m2)
o2 = o  * exp(m  - m2) + ot * exp(mt - m2)
```

Merge order is the canonical schedule order. No atomic multi-writer reduction is admitted.

### Finalize

Final normalization runs only for the last tile wave of the row range:

```text
output = running_output / running_sum
```

## 6. Admission authority

The GPU executor owns physical admission. Planner receipts are not execution authority.

For every wave:

```text
assert in_flight == 0
encode partial + merge (+ final/compare when applicable)
submit exactly one command buffer
increment in_flight
wait for device completion
record completion receipt
decrement in_flight
admit next wave
```

Required invariants:

```text
observed_max_in_flight_waves <= 1
queue_ahead_submission_count == 0
next_wave_before_completion_count == 0
queue_submit_count == scheduled_wave_count
completion_poll_count == scheduled_wave_count
```

## 7. Shared schedule, separated authority

Reference and candidate use the same schedule digest for equivalent geometry.

Shared:

```text
row coverage
tile coverage
wave ordering
workgroup cap
completion barrier
```

Separated:

```text
partial buffers
running softmax state
final outputs
receipts
production/candidate authority
```

BufferAtlas remains the production reference. Texture output remains diagnostic shadow evidence and cannot commit into production state.

## 8. Pipeline closure

The device-scoped pipeline factory expands from nine to thirteen kinds:

```text
bufferatlas_reference
texture_population
texture_persistent_population
texture_validation
texture_incremental_append
candidate_microtile_accumulate
candidate_microtile_normalize
bufferatlas_wave_partial
texture_wave_partial
wave_partial_merge
wave_finalize
compare
finalize
```

Legacy candidate microtile pipelines remain registered for compatibility but acquire count must be zero on the R3-R3-R1 physical path.

## 9. Receipts and artifacts

Across sixty healthy commits:

```text
reference admission receipts  1320
candidate admission receipts  1320
```

Each receipt records:

```text
executor kind
layer index
schedule digest
scheduled waves
submit count
poll count
observed in-flight maximum
queue-ahead count
next-before-completion count
missing/duplicate coverage
maximum workgroups
full-KV-loop count
score-recompute count
partial-readback count
CPU-reduce count
pass and digest
```

Physical artifacts:

```text
workspace/runtime/attention/headwise/texture/05/r3_r3_r1/
  reference_admission_receipts.json
  candidate_admission_receipts.json
  session_summary.json
  r4_physical_basis.json

workspace/runtime/attention/headwise/texture/
  ash_attn_headwise_texture_05_r3_r3_r1_runtime_artifact.json
  ash_attn_headwise_texture_05_r3_r3_r1_local_manifest.json
```

Verification artifacts:

```text
workspace/runtime/attention/headwise/texture/05/r3_r3_r1_verification/
  source_admission_audit.json
```

## 10. Completion gate

```text
reference admission receipts             1320
candidate admission receipts             1320
missing row-tile coverage                    0
duplicate row-tile coverage                  0
maximum workgroups per dispatch            64
maximum in-flight waves                      1
queue-ahead submissions                      0
next-wave-before-completion                  0
internal full-KV loops                       0
output-dimension score recomputation         0
partial readbacks                            0
CPU reductions                               0
production authority mutations               0
candidate output commits                     0
numeric reference/candidate parity        PASS
R3-R2 residency plateau                   PASS
R3-R3 transient peak closure              PASS
```

Patch-local PASS does not relax the original Texture-05 p95 or p99 latency budgets. It establishes the bounded parallel-sequential execution authority needed to rerun those gates.

## 11. Direct execution

Verification gate:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_r3_r3_r1_gate -- "@specs/cli/ash_attn_headwise_texture_05_r3_r3_r1.args"
```

Physical Texture-05 gate:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_gate -- "@specs/cli/ash_attn_headwise_texture_05.args"
```

Expected new disclosure:

```text
[ash-attn-headwise-texture-05][r3-r3-r1]
reference_receipts
candidate_receipts
total_waves
submits
polls
max_in_flight
queue_ahead
next_before_completion
max_workgroups
tiles_per_wave
pass
```

The original eligibility output remains authoritative and may still report HOLD if physical p95 or p99 remain outside budget.
