# `ASH-BASETRAIN-RAM-BUDGET-EXACT-INVENTORY-R1`

## BaseTrain Host-RAM Ownership Inventory / Exact Owned-Capacity Ledger / Pre-36GiB Admission Closure

---

## 0. Status

| Item | Authority |
|---|---|
| Patch ID | `ASH-BASETRAIN-RAM-BUDGET-EXACT-INVENTORY-R1` |
| Parent | Current R6/CF1 BaseTrain + RAM-resident Adam M/V line |
| Role | Observe, classify, and account host RAM before hard-cap admission |
| Adam M/V hot SSOT | Host physical RAM |
| Adam M/V sizing | Packed runtime-state manifest |
| Dataset sizing | Runtime owned capacities |
| Process observation | Private Usage + Working Set + available physical RAM |
| 36 GiB enforcement | **HOLD / not implemented in R1** |
| Allocation behavior change | Forbidden |
| Optimizer math change | Forbidden |
| Batch/prefetch geometry change | Forbidden |

```text
ASH-BASETRAIN-RAM-BUDGET-EXACT-INVENTORY-R1

BaseTrain Host-RAM Ownership Inventory /
Exact Allocation-Site Accounting /
Manifest-Bound Adam M/V Sizing /

Run-Resident vs Phase-Transient Classification /
Allocation Identity Deduplication /
Phase Co-Residency Observation /

Dataset Materialization Accounting /
Optimizer Segment Live-Capacity Accounting /
Optimizer Serialization Live-Overlap Accounting /

PCIe Host Staging Configured-Bound Separation /
Process Baseline Observation /
Managed Payload vs Physical Private Memory Separation /
Working Set Diagnostic Separation /

Vec Capacity Authority /
String Capacity Authority /
Opaque Nested Allocator Fail Closed /
Unknown Owner Fail Closed /
Duplicate Owner Fail Closed /

No 36 GiB Enforcement Yet /
No Job-Object Memory Limit Yet /
No Allocation Behavior Change /
No Optimizer Math Change /
No Silent Spill /

RAM Budget Inventory SSOT Closure
```

---

## 1. Revision boundary

Canonical order:

```text
RAM-resident Adam M/V
→ RAM Adam M/V PCIe overlap
→ RAM resume-cut exactness
→ RAM-BUDGET-EXACT-INVENTORY-R1
→ RAM36 process-budget authority
→ byte-bounded production data window
```

R1 MUST NOT modify what it measures.

Forbidden:

```text
batch reduction
prefetch reduction
Adam eviction
Adam disk fallback
memory pooling
optimizer quantization/compression
sequence-length mutation
36 GiB hard-limit rejection
Windows Job Object process-memory limit
```

---

## 2. Accounting domains

R1 separates four authorities.

### ManagedPayload

Explicit BaseTrain-owned payload with stable sizing authority.

Examples:

```text
Adam M/V resident Vec<f32>
production BaseBatchCpu buffers
optimizer work weight/M/V
candidate weight/M/V
optimizer serialization Vec<u8>
```

### ConfiguredBound

A maximum geometry, not proof that all bytes are allocated now.

```text
Adam hydration chunk bound
PCIe overlap host-staging bound
```

### ProcessObservation

Windows authority:

```text
PROCESS_MEMORY_COUNTERS_EX.PrivateUsage
PROCESS_MEMORY_COUNTERS_EX.WorkingSetSize
GlobalMemoryStatusEx.ullAvailPhys
```

### FutureProjection

Future, not-yet-active state. It MUST NOT enter the current physical peak.

---

## 3. Baseline authority

Canonical baseline point:

```text
BaseTrain/runtime bootstrap complete
+
production batch materialization not started
+
RAM Adam M/V hydration not started
```

Revision:

```text
BASETRAIN_BOOTSTRAP_BEFORE_PRODUCTION_BATCH_MATERIALIZATION_V1
```

The baseline is observed process memory. It is not reconstructed from model size.

---

## 4. Adam M/V exact sizing

```text
AdamMBytes = packed_manifest.adam_m_pack_bytes
AdamVBytes = packed_manifest.adam_v_pack_bytes
```

Requirements:

```text
bytes > 0
bytes % 4 == 0
sizing authority = PackedStateManifest
lifetime = RunResident
```

When the packed manifest exists, parameter-count estimates are not authoritative.

---

## 5. Hydration scratch

Current read-chunk maximum:

```text
8 MiB = 8,388,608 bytes
```

Classification:

```text
ConfiguredBound
PhaseTransient
AdamHydration
```

It is not run-resident RAM.

---

## 6. PCIe overlap geometry

Current configured geometry:

```text
3 slots × 6 host vectors × 16 MiB
= 288 MiB
= 301,989,888 bytes
```

Critical SSOT:

> `288 MiB` is a configured maximum staging geometry, not an always-resident allocation.

R1 therefore records separately:

```text
configured PCIe staging bound
actual optimizer transient owned-capacity peak
```

---

## 7. Optimizer transient exact owned-capacity observation

For each RAM-resident Adam segment batch, actual Rust-owned capacity is measured.

### Work side

```text
Vec<RamResidentSegmentWork> outer capacity
+ weight.capacity() * sizeof(f32)
+ m.capacity() * sizeof(f32)
+ v.capacity() * sizeof(f32)
+ label.capacity()
```

### PCIe triple-batch input side

When overlap is active:

```text
Vec<R6AdamwTripleBatchInput> outer capacity
```

is counted while work buffers remain live.

### Candidate output side

```text
Vec<R6AdamwCandidateOutput> outer capacity
+ candidate_weight.capacity() * sizeof(f32)
+ candidate_m.capacity() * sizeof(f32)
+ candidate_v.capacity() * sizeof(f32)
```

### Serialization overlap

While candidate buffers are still live:

```text
weight_bytes.capacity()
+ m_bytes.capacity()
+ v_bytes.capacity()
```

is added to the actual live transient observation.

Receipt fields:

```text
optimizerSegmentTransientPeakBytes
optimizerSerializationTransientPeakBytes
optimizerTransientObservationCount
```

Exact owned-payload PASS requires:

```text
optimizerTransientObservationCount > 0
```

---

## 8. Dataset materialization truth

Current production route is preserved exactly:

```text
manifest split
→ raw source Vec
→ tokenized sample Vec
→ Vec<BaseBatchCpu>
→ execute_r6_production_multistep_loop(&batches)
```

R1 does not convert this to streaming.

Tracked values:

```text
rawSourceLogicalBytes
rawSourceOwnedCapacityBytes
rawSourcePayloadExact

tokenizedLogicalBytes
tokenizedOwnedCapacityBytes

outputBatchLogicalBytes
outputBatchOwnedCapacityBytes
managedBuildPeakBytes
```

`managedBuildPeakBytes` records the raw + tokenized + batch coexistence in the current builder lifecycle.

---

## 9. Capacity authority

Owned `Vec<T>`:

```text
Vec::capacity() * sizeof(T)
```

Owned `String` payload:

```text
String::capacity()
```

Borrowed slices create no second RAM owner.

`len()` is not accepted as allocation-capacity authority.

---

## 10. Opaque nested allocators

Where stable public APIs cannot establish allocator node capacity exactly, R1 does not invent it.

```text
opaqueNestedAllocatorCount
```

must be zero for exact owned-payload PASS.

This is fail-closed behavior, not a zero-byte fallback.

---

## 11. Process observation vs managed payload

R1 samples process memory at lifecycle boundaries including:

```text
bootstrap baseline
dataset raw/tokenized/batch materialization
Adam hydration
forward/backward
optimizer live transient points
final writeback
run shutdown
```

Receipt fields:

```text
processBaselinePrivateBytes
observedProcessPrivatePeakBytes
observedWorkingSetPeakBytes
processObservationSupported
```

Important separation:

```text
ManagedPayload != Process PrivateUsage
Process PrivateUsage != Working Set
```

Allocator metadata, fragmentation, stacks, libraries, and runtime/driver allocations remain process-observation territory unless BaseTrain has an explicit stable owned-capacity authority for them.

---

## 12. Allocation identity and fail-closed rules

One owned allocation has one accounting owner.

Duplicate identity:

```text
E_RAM_INVENTORY_DUPLICATE_ALLOCATION_OWNER
```

Unknown managed owner:

```text
E_RAM_INVENTORY_UNKNOWN_MANAGED_OWNER
```

No generic `Other`, no silent estimate, and no `unwrap_or(0)` ownership repair.

---

## 13. CLI admission

New flag:

```text
--admit-ram-budget-exact-inventory
```

Required parent:

```text
--admit-ram-resident-adam-mv
```

CLI failure:

```text
BASETRAIN_RAM_BUDGET_EXACT_INVENTORY_REQUIRES_RAM_RESIDENT_ADAM_MV
```

Direct production callers are separately guarded:

```text
RamBudgetExactInventoryRamResidentAdamMvRequired
```

so CLI validation cannot be bypassed silently.

---

## 14. Runtime evidence

Inventory admission writes:

```text
basetrain_ram_exact_inventory.json
basetrain_ram_phase_residency.json
basetrain_ram_peak_plan.json
basetrain_ram_exact_inventory_receipt.json
```

These are runtime evidence files and are not source-code ZIP payloads.

---

## 15. Structural PASS vs runtime exactness

Static validator token:

```text
PASS_RAM_BUDGET_EXACT_INVENTORY_R1_STATIC
```

Runtime exact-owned-payload token:

```text
PASS_ASH_BASETRAIN_RAM_BUDGET_EXACT_INVENTORY_R1
```

If current owned payload cannot be established exactly:

```text
HOLD_ASH_BASETRAIN_RAM_BUDGET_EXACT_INVENTORY_OWNED_PAYLOAD_NOT_FULLY_EXACT
```

The next hard-cap authority remains independently held:

```text
HOLD_ASH_BASETRAIN_RAM_36GIB_PROCESS_CAP_NOT_YET_ADMITTED
```

R1 PASS is not a declaration that the process is already capped at 36 GiB.

---

## 16. 36 GiB future boundary

Future user-selected BaseTrain maximum:

```text
36 GiB
= 36 × 1024^3
= 38,654,705,664 bytes
```

R1 documents this target but MUST NOT enforce it.

Forbidden in R1 source:

```text
BASETRAIN_HOST_RAM_CAP_BYTES
36 * 1024 * 1024 * 1024 enforcement
JOB_OBJECT_LIMIT_PROCESS_MEMORY
JobObjectExtendedLimitInformation memory admission
allocation rejection based on 36 GiB
```

Existing:

```text
--adam-mv-ram-reserve-bytes
```

remains an external physical-RAM reserve. It is not reinterpreted as the 36 GiB process cap.

---

## 17. Static gates

Minimum structural gates:

```text
patch identity
module export/re-export
config admission default false
CLI admission + parent gate
direct production parent gate
baseline before dataset materialization
instrumented production builder under admission
Adam M/V manifest sizing
8 MiB hydration configured bound
PCIe 288 MiB configured-bound classification
Vec/String capacity accounting
opaque allocator fail-closed accounting
Windows PrivateUsage observation
GlobalMemoryStatusEx available physical RAM
Working Set separation
optimizer work capacity observation
candidate-output capacity observation
serialization live-overlap observation
runtime inventory writeout
36 GiB enforcement absent
Job Object memory enforcement absent
```

---

## 18. Required Rust tests

```text
vec_accounting_uses_capacity_not_len
batch_capacity_includes_nested_owned_buffers
pcie_staging_bound_is_288_mib
json_object_marks_opaque_node_overhead
duplicate_allocation_identity_is_rejected
```

Physical process peaks and optimizer transient peaks require an actual production run.

---

## 19. Next revision

Natural successor:

```text
ASH-BASETRAIN-RAM-RESIDENT-ADAM-MV-36GIB-PROCESS-BUDGET-AUTHORITY-R1
```

That revision may consume this ledger and add:

```text
38,654,705,664-byte hard authority
one unified HostMemoryBudget
pre-allocation lease/admission
Windows process-commit outer fuse
available-physical-RAM gate
Adam M/V non-eviction
minimum accumulation8 data-window admission
```

Only after the hard budget authority is closed should the current whole-horizon `Vec<BaseBatchCpu>` path be replaced by a byte-bounded production window.

---

## 20. Final SSOT

```text
ADAM M SIZE
= packed manifest adam_m_pack_bytes

ADAM V SIZE
= packed manifest adam_v_pack_bytes

OWNED VEC
= capacity * sizeof(T)

OWNED STRING
= capacity

BORROWED VIEW
= no second owner

PCIe 288 MiB
= configured maximum bound
!= permanent resident bytes

OPTIMIZER TRANSIENT PEAK
= actual simultaneous owned-capacity observation

DATASET BUILD PEAK
= current raw + tokenized + batch lifecycle

MANAGED PAYLOAD
!= process PrivateUsage

PROCESS PRIVATE USAGE
!= Working Set

OPAQUE MANAGED ALLOCATOR
= exact PASS denied

DUPLICATE OWNER
= failure

UNKNOWN MANAGED OWNER
= failure

R1
= observe / classify / account

36 GiB enforcement
= next RAM36 authority

NO SILENT FALLBACK
NO SILENT SPILL
NO SILENT CAP SEMANTIC REWRITE
```

> **R1 is the RAM ledger, not the RAM gate. It establishes current owned payload and process-observed memory as separate reproducible authorities. The exact 36 GiB gate is allowed to exist only after this ledger is available.**
