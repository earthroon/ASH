# ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R2
# GPU Readback Map Lifecycle Ownership / Route-Isolated Live Decode Worker / Panic-to-HOLD Orphan Attempt Quarantine Repair

- Patch ID: `ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R2_GPU_READBACK_MAP_LIFECYCLE_OWNERSHIP_ROUTE_ISOLATED_LIVE_DECODE_WORKER_PANIC_TO_HOLD_ORPHAN_ATTEMPT_QUARANTINE_REPAIR`
- Parent attempt: R8-R2 release execution ending with `BufferAsyncError`, exit code `101`
- Parent attempt classification: `OrphanLiveDecodeAttempt`
- Parent promotion contribution: `0`
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R3`
- R8-R2 live timing PASS: `false`
- R8-R3 authorization: `false`
- R4-R5-R2 authorization: `false`
- Legacy removal/retirement: `false`
- General production apply: `false`

## Problem

The parent R8-R2 run entered the real `NativeWgpuModel` path, observed embedding row gather, vocab-atlas work, GPU sampling shadow comparison and token selection, then panicked in `cubecl-wgpu` while mapping a buffer:

```text
Failed to map buffer: BufferAsyncError
exit code=101
shadow lifecycle final state=Started
```

No authoritative R8-R2 PASS or HOLD manifest was emitted. The attempt is an orphan and contributes zero promotion evidence.

## Ownership repair

The repair separates:

```text
coordinator process
route live-decode worker processes
performance cohort worker processes
GPU readback lifecycle owner
staging publication owner
orphan quarantine owner
final HOLD/PASS reducer
```

The coordinator never owns a `NativeWgpuModel`, WGPU device/queue, CubeCL stream, mapped range, KV state or route-local publication transaction.

## Route isolation

The four live routes run in separate child processes:

```text
greedy_cached
sampled_cached
greedy_streaming
sampled_streaming
```

Each worker owns a fresh model, device, queue, CubeCL stream, KV state, DecodeState, sampler/RNG state, staging directory and process clock domain.

A live worker receives exactly one route. Cross-route device, stream, readback-buffer or readback-lease reuse is forbidden.

## Performance cohort isolation

The performance cohorts are:

```text
LegacyOnly
FullDual
BoundedReduced
```

The canonical topology is one process per cohort-route pair. Cross-cohort model or stream reuse is forbidden.

## Readback lifecycle

The only promotion readback owner is `GpuReadbackLease` at the process-isolated worker boundary.

Required lifecycle:

```text
copy scheduled
queue submitted
device progress driven
map requested
map callback completed
mapped range acquired
mapped bytes consumed
mapped range released
buffer unmapped
lease closed
```

The worker may publish evidence only after required readbacks close. At worker exit the following must all be zero:

```text
open generation transactions
open readback leases
live mapped ranges
mapped buffers
outstanding submissions
```

## Panic containment

All GPU work executes in child processes. A child panic cannot terminate the coordinator.

A panic before authoritative commit becomes:

```text
orphan duration contribution=0
orphan generation contribution=0
orphan selected-token contribution=0
orphan oracle contribution=0
orphan performance contribution=0
```

The staging attempt, stdout, stderr, child exit, readback receipts and panic digest are moved to durable orphan quarantine.

Recoverable GPU readback failure yields HOLD and permits one retry using a fresh process, token, nonce, model, device, queue and CubeCL stream.

Ambiguous partial authoritative commit, ledger drift, orphan counting, token reuse or discarded panic evidence yields FAIL.

## Durable directories

```text
workspace/runtime/tensorcube/soak/r4_r5_r1_r8_r2_r2/staging/<attempt_id>/
workspace/runtime/tensorcube/soak/r4_r5_r1_r8_r2_r2/committed/<attempt_id>/
workspace/runtime/tensorcube/soak/r4_r5_r1_r8_r2_r2/orphan_quarantine/<attempt_id>/
workspace/runtime/tensorcube/soak/r4_r5_r1_r8_r2_r2/coordinator_state.json
workspace/runtime/tensorcube/soak/r4_r5_r1_r8_r2_r2/coordinator_journal.jsonl
```

The journal is a strict digest chain. Directory enumeration is not authority.

## Stress budgets

Final repair PASS requires cumulative durable evidence:

```text
route worker successes per route >=25
route worker successes total >=100
performance worker successes per cohort-route >=5
performance worker successes total >=60
zero promotion-stress BufferAsyncError
zero device loss
zero uncaptured error
zero readback leak
```

The canonical command is resumable. Bounded invocations may return HOLD until cumulative counts close.

## PASS authority

```text
r4_r5_r1_r8_r2_r2_gpu_readback_repair_pass=true
r4_r5_r1_r8_r2_r3_authorized=true
r4_r5_r1_r8_r2_live_timing_repair_pass=false
r4_r5_r1_r8_r3_authorized=false
r8_final_budget_closure_authorized=false
bounded_oracle_reduction_production_soak_proven=false
decode04_r4_r5_r2_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
general_production_apply_authorized=false
```

## Canonical binary

```text
ash_tcu_decode_04_r4_r5_r1_r8_r2_r2_gpu_readback_map_lifecycle_ownership_repair_gate
```

## Next gate

```text
ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R3
Route-Isolated Live Timing Repair Rerun /
Fresh Measurement Epoch Bootstrap /
Production-Equivalent Cohort Revalidation Gate
```
