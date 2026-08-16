# `ASH-BASETRAIN-RAM-RESIDENT-ADAM-MV-36GIB-PROCESS-BUDGET-AUTHORITY-R1`

## Unified Host Process RAM Authority / Exact 36 GiB Ceiling / Release Physical Enforcement

## 0. Status

```text
ASH-BASETRAIN-RAM-RESIDENT-ADAM-MV-36GIB-PROCESS-BUDGET-AUTHORITY-R1

Unified Host Process RAM Authority /
Exact 36 GiB Ceiling /
38,654,705,664 Byte Hard Limit /

Windows Process PrivateUsage Authority /
Release-Profile Physical Evidence Parent /

Pre-Allocation Budget Admission /
Post-Allocation PrivateUsage Verification /
Observed High-Water Mark Tracking /

Adam M/V Resident Budget Binding /
Dataset Build Budget Binding /
Optimizer Transient Budget Binding /
PCIe Host Staging Budget Binding /

No Independent Subsystem RAM Ceilings /
One Process One RAM Budget SSOT /

No WorkingSet-as-Commit Authority /
No CurrentManagedPayload-as-Process-RAM Substitute /
No Phase-Peak Blind Summation /

36GiB Remaining Budget Projection /
Bounded Admission Before Large Allocation /

Exact Owner Ledger Preservation /
Unknown Owner Fail-Closed /
Unclassified Allocation No Production Admission /

Process Cap Enforcement /
No Silent Overcommit /
No OS-Paging-as-Budget-Success /

Release CF1 Binary Binding Preservation /
No Debug Measurement Authority /

No Adam Compression /
No Adam Quantization /
No Training Math Change /
No Optimizer Math Change /
No Batch Geometry Change /
No Dataset Streaming Rewrite /
No Checkpoint Rewrite
```

Receipt schema:

```text
ash.basetrain.ram36_process_budget_authority.v1
```

Exact hard limit:

```text
36 GiB = 36 * 1024^3 = 38,654,705,664 bytes
```

## 1. Parent physical evidence

R1 is parented by the passed Release-profile `ASH-BASETRAIN-RAM-BUDGET-EXACT-INVENTORY-R1` physical run and `ASH-BASETRAIN-CF1-RELEASE-PROFILE-AUTHORITY-REBIND-R1`.

Observed parent evidence:

```text
processBaselinePrivateBytes                  =   255,688,704
observedProcessPrivatePeakBytes              = 17,547,415,552
observedWorkingSetPeakBytes                  = 11,214,598,144
adamMResidentBytes                           =  4,666,580,992
adamVResidentBytes                           =  4,666,580,992
hydrationScratchPeakBytes                    =      8,388,608
optimizerSegmentTransientPeakBytes           =    352,323,930
optimizerSerializationTransientPeakBytes     =     50,331,648
optimizerTransferStagingConfiguredBoundBytes =    301,989,888
datasetRawSourcePeakBytes                    =    182,323,364
datasetTokenizedPeakBytes                    =        155,504
datasetBuildManagedPeakBytes                 =    182,683,792
currentManagedPayloadBytes                   =  9,333,366,908
processObservationSupported                  = true
cf1BuildProfile                              = release
cf1ReleaseBinaryExactMatch                   = true
allCurrentRouteOwnersClassified              = true
allCurrentRouteOwnedPayloadExact             = true
processCapEnforced                           = false
```

The parent observed peak leaves `21,107,290,112` bytes to the exact 36 GiB ceiling, but that value is evidence only. It is not a hardcoded future allocation pool. Each run re-observes its own process memory.

## 2. One-process one-budget SSOT

Canonical constant:

```rust
pub const RAM36_PROCESS_BUDGET_HARD_LIMIT_BYTES: u64 = 38_654_705_664;
```

`HostProcessRamBudget` is the single BaseTrain production host-RAM authority. Adam, dataset, optimizer transient state and PCIe staging do not own independent process ceilings.

No CLI may silently raise the hard limit in R1.

## 3. Process-memory authority

Windows `PROCESS_MEMORY_COUNTERS_EX.PrivateUsage` is the process-level commit authority.

`WorkingSetSize` is telemetry only and cannot admit allocations. Paging or a reduced Working Set is not interpreted as budget success.

`currentManagedPayloadBytes` remains an owner-ledger value and is not a substitute for process PrivateUsage.

## 4. Pre-allocation and post-allocation invariants

Before a managed large allocation:

```text
projectedPrivate
= currentPrivateUsage
+ reservedNotYetMaterializedBytes
+ requestedBytes
```

Admission requires:

```text
projectedPrivate <= 38,654,705,664
```

Arithmetic is checked. Overflow and underflow fail closed.

After materialization, PrivateUsage is re-observed and must satisfy:

```text
PrivateUsageAfter <= 38,654,705,664
```

The PrivateUsage high-water mark never decreases.

## 5. Reservation authority

Reservation state machine:

```text
Admitted -> Materialized -> Released
```

Invalid transitions and double release are errors. Admitted but not yet materialized bytes contribute to `reservedNotYetMaterializedBytes`.

Adam M and Adam V hydrate together. Their reservations therefore transition as one atomic materialization group before the shared post-hydration PrivateUsage verification, preventing temporary M/V double-accounting.

## 6. Owner ledger

Current managed owner identities:

```text
DatasetBuildBound
DatasetBatchResident
AdamMResident
AdamVResident
AdamHydrationScratch
OptimizerSegmentTransient
OptimizerSerializationTransient
PcieTransferStaging
RuntimeOtherExact
```

Production requires the parent exact-inventory truths:

```text
allCurrentRouteOwnersClassified = true
allCurrentRouteOwnedPayloadExact = true
nonExactOwnedPayloadCount = 0
datasetOpaqueNestedAllocatorCount = 0
```

Explicit unclassified and non-exact owner paths fail closed.

## 7. Dataset budget binding

Before production dataset construction, the process budget reserves the parent `datasetBuildManagedPeakBytes` exact bound. After the instrumented build:

1. actual managed build bytes must not exceed the parent evidence bound;
2. observed dataset PrivateUsage must remain below 36 GiB;
3. the temporary build-bound reservation transitions to the exact persistent `DatasetBatchResident` capacity;
4. the build bound and resident batch bytes are not double counted.

Dataset architecture and batch geometry remain unchanged.

## 8. Adam M/V budget binding

The current packed manifest M/V byte counts must equal the parent inventory M/V exact evidence before RAM36 admission.

Before hydration the process budget reserves:

```text
AdamMResident
AdamVResident
AdamHydrationScratch
```

After hydration, M and V are atomically committed as materialized and PrivateUsage is verified once for the joint physical state. Hydration scratch is released after use.

No Adam compression, quantization or precision conversion is introduced.

## 9. Optimizer transient budget binding

Each production optimizer step consumes the parent physical bounds:

```text
optimizerSegmentTransientPeakBytes
optimizerSerializationTransientPeakBytes
```

Serialization must be nonzero and no greater than the total segment/transient bound. PrivateUsage observations are performed around the optimizer step and at the existing live ownership points:

```text
optimizer_transient_triple_batch_inputs
optimizer_transient_candidate_outputs
optimizer_transient_serialization
```

The transient bound is not blindly summed with unrelated phase peaks.

## 10. PCIe host staging

When RAM Adam M/V PCIe overlap is admitted, configured host staging remains:

```text
3 slots * 6 vectors * 16 MiB = 301,989,888 bytes
```

The configured bound must exactly match the parent inventory evidence. Configured bound and current committed PrivateUsage remain separate concepts.

## 11. Windows physical cap

R1 installs a Windows Job Object before native GPU bootstrap and large training allocations.

```text
JOB_OBJECT_LIMIT_PROCESS_MEMORY
ProcessMemoryLimit = 38,654,705,664
```

Physical setup uses:

```text
CreateJobObjectW
SetInformationJobObject
AssignProcessToJobObject
```

Thus the authority is dual-layered:

```text
semantic guard = HostProcessRamBudget pre/post PrivateUsage checks
physical guard = Windows Job Object exact process-memory limit
```

Job creation, configuration or assignment failure is fail-closed. There is no ledger-only production fallback. Non-Windows execution cannot claim this Windows RAM36 physical authority.

## 12. Release CF1 requirement

RAM36 production admission requires:

```text
cf1.buildProfile = release
runtimeBinarySha256 = cf1.authoritativeBinarySha256
```

The parent inventory must also prove `cf1BuildProfile=release` and `cf1ReleaseBinaryExactMatch=true`.

Debug receipts and Debug memory observations are not production RAM36 authority. CF1 receipts do not synthesize or rewrite checkpoint state.

## 13. Explicit CLI admission

RAM36 requires:

```text
--admit-ram-budget-exact-inventory
--admit-ram36-process-budget-authority
--ram36-parent-inventory-receipt <passed Release inventory receipt>
```

The explicit parent receipt path prevents hardcoding or silently reconstructing previous physical evidence.

## 14. Initialization order

Canonical order:

```text
CLI/config validation
-> CF1 Release receipt validation
-> current Release executable exact SHA validation
-> parent RAM inventory path validation
-> Windows 36 GiB Job Object installation
-> process-cap-enforced marker
-> native WGPU bootstrap
-> HostProcessRamBudget construction
-> dataset admission/build/post-check
-> Adam M/V admission/hydration/post-check
-> eight optimizer-step transient preflights and observations
-> final writeback
-> RAM exact inventory receipt
-> RAM36 receipt and event ledger
```

The hard cap is never installed only after Adam hydration.

## 15. Receipts

Existing exact inventory receipt is preserved:

```text
basetrain_ram_exact_inventory_receipt.json
```

When RAM36 is active it records `processCapEnforced=true` without changing the old schema into a different authority.

New outputs:

```text
basetrain_ram36_process_budget_receipt.json
basetrain_ram36_process_budget_events.json
```

The RAM36 receipt records hard limit, parent receipt digest and evidence bounds, CF1 compile/runtime executable identities, process observation support, process-cap enforcement, baseline and peak Private/WorkingSet values, minimum remaining bytes, reservations, owner counts, violation counts and terminal admission state.

Physical PASS requires:

```text
hardLimitBytes = 38,654,705,664
processObservationSupported = true
processCapEnforced = true
cf1BuildProfile = release
cf1ReleaseBinaryExactMatch = true
unclassifiedOwnerCount = 0
nonExactOwnerCount = 0
reservationLeakCount = 0
privateLimitViolationCount = 0
observedPrivatePeakBytes <= 38,654,705,664
```

PASS tokens:

```text
PASS_ASH_BASETRAIN_RAM_RESIDENT_ADAM_MV_36GIB_PROCESS_BUDGET_AUTHORITY_R1_STATIC
PASS_ASH_BASETRAIN_RAM36_PROCESS_BUDGET_ADMISSION_R1
PASS_ASH_BASETRAIN_RAM36_RELEASE_PHYSICAL_EXECUTION_R1
```

Representative hard failures:

```text
FAIL_ASH_BASETRAIN_RAM36_PREALLOCATION_BUDGET_REJECTED
FAIL_ASH_BASETRAIN_RAM36_PRIVATE_USAGE_OVER_LIMIT
FAIL_ASH_BASETRAIN_RAM36_UNCLASSIFIED_OWNER
FAIL_ASH_BASETRAIN_RAM36_NON_EXACT_OWNER
FAIL_ASH_BASETRAIN_RAM36_RELEASE_CF1_REQUIRED
FAIL_ASH_BASETRAIN_RAM36_RELEASE_BINARY_MISMATCH
BASETRAIN_RAM36_PROCESS_CAP_CREATE_JOB_FAILED
BASETRAIN_RAM36_PROCESS_CAP_INSTALL_FAILED
BASETRAIN_RAM36_PROCESS_CAP_ASSIGN_FAILED
BASETRAIN_RAM36_WINDOWS_PROCESS_CAP_REQUIRED
```

No retry loop, silent batch shrink, precision downgrade or paging-based success follows a hard failure.

## 16. Static and compile-chain authority

New validator:

```text
tools/validate_ram36_process_budget_authority_r1_static.py
```

It is appended to the existing CF1 validator chain. Existing R6, R6A, R6A-R1, R6A-R2, R6A-R2-R1, R6A-R2-R2, CF1, R14, N8, storage-root, Adam-resident, Resume-Cut, PCIe overlap, TensorCube/Muon, QK RMSNorm, RAM inventory and CF1 Release validators remain required.

## 17. Non-goals

R1 does not introduce:

```text
Adam compression
Adam quantization
F32-to-F16/BF16 optimizer state conversion
mmap Adam state
allocator replacement
parallel hydration redesign
dataset byte-window streaming
batch geometry change
gradient accumulation change
scheduler change
loss change
gradient math change
optimizer math change
checkpoint migration
checkpoint rewrite
silent chunk reduction
user hard-limit inflation
```

## 18. Production execution authority

Production RAM36 execution is not `cargo run`.

Canonical sequence:

```text
CF1 compile chain with -BuildProfile Release
-> cargo build --release inside CF1
-> CF1 receipt seals target/release/base_train.exe SHA256
-> verify sealed SHA == current Release executable SHA
-> launch that exact target/release/base_train.exe directly
```

A later `cargo run` rebuild must not shadow the executable sealed by CF1.

## 19. Final SSOT

```text
HOST RAM AUTHORITY = ONE PROCESS / ONE BUDGET
HARD LIMIT = 38,654,705,664 BYTES EXACT
PROCESS MEMORY AUTHORITY = PRIVATE USAGE
WORKING SET = TELEMETRY ONLY
MANAGED PAYLOAD = OWNER LEDGER, NOT PROCESS MEMORY AUTHORITY
PRE-ALLOCATION = PRIVATE + RESERVED + REQUEST <= LIMIT
POST-ALLOCATION = PRIVATE <= LIMIT
PHYSICAL GUARD = WINDOWS JOB_OBJECT_LIMIT_PROCESS_MEMORY
UNKNOWN OWNER = FAIL CLOSED
NON-EXACT OWNER = FAIL CLOSED
RELEASE CF1 EXACT BINARY = REQUIRED
DEBUG EVIDENCE = NOT PRODUCTION AUTHORITY
NO PHASE-PEAK BLIND SUM
NO SILENT OVERCOMMIT
NO SILENT SHRINK
NO PAGING-AS-SUCCESS
NO ADAM COMPRESSION
NO ADAM QUANTIZATION
NO TRAINING MATH CHANGE
NO OPTIMIZER MATH CHANGE
NO BATCH GEOMETRY CHANGE
NO DATASET STREAMING REWRITE
NO CHECKPOINT REWRITE
```

> 36 GiB is not an Adam limit or a dataset limit. It is the single process-wide host-memory ceiling. Every managed host allocation must enter under that ceiling with an owner identity and exact byte authority, while Windows enforces the same ceiling physically.