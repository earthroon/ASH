# TENSORCUBE-TABLE-R4D-R1

## ADAMW STATUS DEVICE AGGREGATION

```text
TENSORCUBE-TABLE-R4D-R1

ADAMW STATUS DEVICE AGGREGATION

+ EXISTING 4B PER-SEGMENT ADAMW STATUS SEMANTICS PRESERVED
+ PER-SEGMENT DEVICE STATUS RETENTION
+ STEP-SCOPED STATUS COMPACTION
+ STATUS-ONLY REDUCER WGSL
+ ONE 16-BYTE STEP SUMMARY READBACK
+ ACTIVE PER-SEGMENT READBACK / MAP_ASYNC ELIMINATION
+ OBSERVE LEGACY / DEVICE PARITY
+ STATUS ADMISSION BEFORE GENERATION PROMOTION
+ B06 STATUS-ADMISSION CONSUMPTION
+ NO ADAM NUMERICAL MATH CHANGE
```

## Purpose

The parent AdamW path creates one exact 4-byte GPU status counter per segment, copies it to a per-segment MAP_READ buffer, requests `map_async`, and collects it through nonblocking polling.

R1 removes the repeated host-boundary transaction. It does **not** claim that the parent uses one blocking `PollType::Wait` per segment.

ACTIVE:

```text
N exact 4B device status buffers
        |
        v
one compact device buffer
        |
        v
status-only reducer WGSL
        |
        v
16-byte summary
        |
        v
one map/readback
        |
        v
status admission
        |
        v
generation promotion
```

## Implementation Resolution

The parent AdamW candidate shader is byte-identical to CF8.

R1 does not make the candidate shader write a shared ledger. Instead it retains the exact existing 4-byte status buffers until the step barrier, then adds one reducer shader:

```text
crates/base_train/src/shaders/tensorcube_table_r4d_r1_adamw_status_reduce.wgsl
```

Therefore:

```text
parent AdamW WGSL changed = 0
new status-only reducer WGSL = 1
Adam numerical math changed = 0
```

The reducer outputs:

```text
word 0  total_status_failure_count
word 1  first_failed_segment_slot, U32_MAX when none
word 2  failure_bits (current schema: FAILURE_ANY)
word 3  gpu_covered_segment_count
```

## Runtime Mode

```text
ASH_TENSORCUBE_TABLE_R4D_R1_MODE

OFF / DISABLED / 0
OBSERVE / OBSERVE_ONLY
ACTIVE / ACTIVE_VERIFIED / 1
```

Default is OFF.

OBSERVE/ACTIVE requires R4D-R0A ACTIVE and R4D-R0B ACTIVE.

## OFF / OBSERVE / ACTIVE

OFF preserves the parent per-segment status readback.

OBSERVE preserves the parent 4-byte readbacks and additionally executes the R1 barrier. Compact GPU segment values are compared against the already-observed parent values.

ACTIVE:

```text
per-segment status_readback allocation = absent
per-segment copy to MAP_READ = absent
per-segment map_async = absent
original 4B GPU status retained until barrier
```

## Device Status Slot

Backend materializes `AdamWDeferredStatusDeviceSlotR4DR1`, binding:

```text
source_generation
target_generation
canonical_parameter_index
element_start
element_count
submission_epoch
status device buffer
status physical allocation
tracked submission / arena retirement authority
```

After segment submission completion, source/params/gradient leases may retire, candidate weight/M/V remain provisional device candidate state, and status remains retained for the R1 barrier.

Submission completion is not status admission.

## Deterministic Slot Order

The scheduler drains retained status slots in its canonical `BTreeSet` submitted-key order.

Required:

```text
status slot count == submitted segment count
no duplicate status slot
no missing status slot
```

## Summary Geometry

```text
R4D_R1_SUMMARY_BYTES = 16
R4D_R1_STATUS_BYTES_PER_SEGMENT = 4
R4D_R1_MAX_STATUS_SEGMENTS = 1,048,576
```

For N segments:

```text
PARENT
  status D2H = 4N bytes
  status readback transactions = N
  status map requests = N

R1 ACTIVE SUCCESS
  status D2H = 16 bytes
  status readback transactions = 1
  status map requests = 1
```

For small N, byte count may not improve. The primary target is transaction cardinality.

The barrier completion loop uses existing nonblocking poll/submission-completion authority. R1 adds no `PollType::Wait`.

## Numerical / Residency Preservation

The parent AdamW shader remains unchanged, including Adam equations, finite predicate, candidate weight/M/V writes, dispatch geometry, and existing status increments.

R1 adds no candidate:

```text
weight D2H
M D2H
V D2H
host Vec materialization
```

R1 reads only status buffers.

## Status Admission

`AdamWStepStatusAdmissionReceiptR4DR1` binds:

```text
source / target generation
optimizer step
expected segment count
GPU-covered segment count
total status failure count
first failed segment slot + parameter/range identity
failure bits
parent-equivalent / actual / avoided status D2H bytes
per-segment / step readback-map counts
OBSERVE parity failures
admitted
receipt digest
```

Success requires:

```text
expected_segment_count > 0
gpu_covered_segment_count == expected_segment_count
total_status_failure_count == 0
first_failed_segment_slot = none
failure_bits == 0
observe_parity_failure_count == 0
```

ACTIVE additionally requires:

```text
per_segment_status_readback_count = 0
per_segment_status_map_async_count = 0
step_status_readback_count = 1
step_status_map_async_count = 1
actual_status_d2h_bytes = 16
```

## Promotion / B06 Gate

When R1 is enabled, `AdamWActiveDevicePendingGenerationSchedulerR1::take_generation()` requires an admitted status receipt.

Failure token:

```text
FAIL_R4D_R1_CANDIDATE_PROMOTED_BEFORE_STATUS
```

The production B06 staging callsite additionally requires:

```text
r4d_r1_status_admitted = true
r4d_r1_status_admission_digest present
```

Thus physically completed candidate segments cannot become generation-promotion authority before status admission.

## Poll Attribution Boundary

R1 does not claim removal of submission-completion polling required for resource and arena lifetime.

It removes migrated per-segment **status map/readback transactions** in ACTIVE.

## Actual Delta

```text
MOD 4
ADD 3
DEL 0
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/unified_atlas_mcu_adamw_active_device_pending_generation_scheduler_r1.rs
crates/burn_webgpu_backend/src/adamw_active_device_candidate_r1.rs
```

Added:

```text
crates/base_train/src/shaders/tensorcube_table_r4d_r1_adamw_status_reduce.wgsl
crates/base_train/src/tensorcube_table_r4d_r1_adamw_status_device_aggregation.rs
tools/validate_ash_tensorcube_table_r4d_r1_adamw_status_device_aggregation_static.py
```

No parent validator source required successor modification.

## Build Graph / WGSL Seal

```text
Cargo.toml byte-identical
Cargo.lock byte-identical
parent WGSL files = 320
parent WGSL changed = 0
new WGSL files = 1
work WGSL total = 321
```

## Static Acceptance

```text
PASS_TENSORCUBE_TABLE_R4D_R1_ADAMW_STATUS_DEVICE_AGGREGATION_STATIC checks=145
PASS_TENSORCUBE_TABLE_R4C_CF8_RESIDENT_VALIDATION_RECEIPT_CACHE_STATIC checks=136
PASS_TENSORCUBE_TABLE_R4C_CF7_PARTIAL_VRAM_HOT_WEIGHT_REUSE_STATIC checks=151
PASS_TENSORCUBE_TABLE_R4D_R0B_GRADIENT_OBSERVABILITY_DEVICE_AGGREGATION_STATIC checks=178
PASS_TENSORCUBE_TABLE_R4D_R0A_HOT_PATH_PIPELINE_RESIDENCY_STATIC checks=104
PASS_TENSORCUBE_TABLE_R4C_CF6_DIRECT_BOUNDED_WEIGHT_UPLOAD_STATIC checks=135
PASS_TENSORCUBE_TABLE_R4C_CF5_HOST_COPY_COLLAPSE_STATIC checks=127
PASS_TENSORCUBE_TABLE_R4C_CF4_HOST_DEVICE_IO_ROUNDTRIP_ATTRIBUTION_STATIC checks=67
PASS_TENSORCUBE_TABLE_R4C_CF3_SLOT_LIFECYCLE_STATIC checks=77
PASS_TENSORCUBE_TABLE_R4B_CF3_FULL_ROUTE_HOST_LEDGER_COMPACTION_STATIC checks=127
PASS_TENSORCUBE_TABLE_R1_CF1_IMMUTABLE_BYTE_ACCOUNTING_STATIC
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF1_STATIC checks=63
PASS_EVE_MCU_R3H_CF11_PAGED_COW_CANDIDATE_WEIGHT_SUCCESSOR_STATIC checks=64
```

## Artifact Seals

```text
Overlay code-only ZIP
SHA-256 3533c3d50ed220f881f423f794e07f4f4523bc340b62936032e6081ad07fd77e
files=7
CRC=PASS

Full code-only ZIP
SHA-256 43308724d6c5f0d45264ad187787d8783d814188c35d908a332af7bf3d81b66a
files=8527
CRC=PASS
```

## Evidence State

The bake environment has no Rust toolchain.

```text
SOURCE       BAKED
STATIC       PASS
COMPILE      UNVERIFIED IN BAKE ENVIRONMENT
RUNTIME      UNVERIFIED AFTER R1
PHYSICAL     UNVERIFIED AFTER R1
PERFORMANCE  UNVERIFIED
```

No compile or speedup claim is inferred from static evidence.

## Local Compile Acceptance

```powershell
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo build -p base_train --bin base_train --release --locked -j 1
```

## Physical Acceptance

First run OBSERVE for successful-path parent/device parity. Then ACTIVE must establish:

```text
expected segments == GPU-covered segments
per-segment status readback count = 0
per-segment status map_async count = 0
one 16-byte step summary readback
one step summary map_async
candidate not promoted before status admission
B06 consumes status admission digest
R1 adds no candidate weight/M/V D2H
R1 adds no host candidate Vec materialization
no new PollType::Wait
generation closure PASS
```

A negative/nonfinite physical fixture should prove first-failed-slot attribution and rejection before promotion.

## Performance Boundary

Same-source A/B:

```text
CF8 parent + R1 OFF
vs
same source + R1 ACTIVE
```

Measure status map/readback transaction counts, status D2H bytes, submission-completion poll attempts, status-map poll attempts, CPU process time, AdamW scheduler wall time, optimizer-step wall time, and generation wall time.

No exact speedup claim before physical A/B.

## Successor

```text
TENSORCUBE-TABLE-R4D-R2
DURABLE PROJECTION HOST COPY COLLAPSE
```

## Final Law

> The AdamW status payload is tiny, but the parent pays one host-boundary transaction per segment.

> R4D-R1 preserves each exact existing 4-byte status on device, defers host observation to the optimizer-step semantic barrier, reduces all statuses into one fixed 16-byte summary, and crosses the host boundary once.

> AdamW numerical math, candidate weight/M/V residency, and submission-completion ownership remain unchanged. Generation promotion is forbidden until the status summary is admitted.
