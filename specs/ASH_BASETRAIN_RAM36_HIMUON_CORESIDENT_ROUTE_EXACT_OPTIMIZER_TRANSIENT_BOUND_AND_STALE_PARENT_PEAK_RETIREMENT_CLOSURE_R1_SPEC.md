# ASH-BASETRAIN-RAM36-HIMUON-CORESIDENT-ROUTE-EXACT-OPTIMIZER-TRANSIENT-BOUND-AND-STALE-PARENT-PEAK-RETIREMENT-CLOSURE-R1

## 0. Revision Identity

```text
ASH-BASETRAIN-RAM36-HIMUON-CORESIDENT-
ROUTE-EXACT-OPTIMIZER-TRANSIENT-BOUND-
AND-STALE-PARENT-PEAK-RETIREMENT-CLOSURE-R1
```

Parent source authority:

```text
ASH_BASETRAIN_WEIGHT_SUCCESSOR_BIT_EXACT_JOURNAL_SHADOW_R1_
BASETRAIN_COMPILE_BOUNDARY_HOTFIX_R2
```

This revision closes the RAM36 admission-model drift exposed when the existing HiMuon / TensorCube local-Muon production callsite is enabled together with:

- RAM-resident Adam M/V
- transactional committed-A / candidate-B Adam state
- persistent resident weight pack
- immutable N2 RAM36 parent authority
- N8 production continuity

The revision does not increase the process RAM limit and does not introduce disk spill.

---

## 1. Physical Trigger

Observed N8 failure:

```text
Error: RamAdamTransactionalCandidateExecutionFailed

Caused by:
    FAIL_ASH_BASETRAIN_RAM36_PREALLOCATION_BUDGET_REJECTED
```

Observed parent RAM inventory evidence:

```text
AdamMResidentGiB              = 4.346
AdamVResidentGiB              = 4.346
OptimizerSegmentPeakGiB       = 0.141
OptimizerSerializationPeakGiB = 0.047
HydrationScratchPeakGiB       = 0.008
DatasetManagedPeakGiB         = 0.170
OldObservedPrivatePeakGiB     = 24.530
OldBaselinePrivateGiB         = 0.238
```

Observed TensorCube / Muon capability evidence:

```text
subgroup_feature_observed=true
backend_id=F32_WORKGROUP_LEGACY
```

These lines prove the capability/backend path was reached. They do not by themselves prove a completed HiMuon fused physical execution.

Physical HiMuon qualification therefore remains separate from this source/static closure.

---

## 2. Causal Boundary

The previous scheduler used the historical RAM exact-inventory parent values directly for every optimizer preflight:

```text
parent.optimizer_segment_transient_peak_bytes
parent.optimizer_serialization_transient_peak_bytes
```

Those values remain useful historical evidence but are not automatically the correct current admission authority after optimizer routing changes from all-AdamW behavior to a verified Muon/AdamW partition.

However, this revision does not assume that the stale parent transient is the sole cause of the RAM36 rejection.

The observed historical transient is only approximately:

```text
0.141 GiB + 0.047 GiB
```

Therefore R1 has two independent obligations:

1. replace stale historical transient admission with a current route-derived bound on the HiMuon path;
2. expose the exact owner that actually causes any remaining RAM36 rejection.

If a persistent owner remains unsatisfiable under 36 GiB, the run must still fail closed.

---

## 3. SSOT Ownership

### 3.1 Process RAM authority

The sole process RAM admission authority remains:

```text
HostProcessRamBudget
```

No second mutable budget SSOT is introduced.

### 3.2 Adam mutable state

The production RAM Adam mutable-state owner remains:

```text
RamResidentAdamMv
```

with:

```text
Committed A
Candidate B
```

Candidate B remains persistent RAM and is never reclassified as transient to bypass RAM36.

### 3.3 HiMuon momentum

HiMuon momentum remains:

```text
HostRamOwner::TensorCubeLocalMuonMomentum
```

It remains fully charged as persistent RAM.

### 3.4 Resident weights

Current and successor resident weight ownership remains:

```text
HostRamOwner::ResidentWeightPack
```

Successor physical allocation is not hidden or discounted.

### 3.5 Optimizer route

The verified production Muon registry remains the routing SSOT:

```text
FirstCandidateEligibilityRegistry
optimizer_routing_digest
FirstCandidateParameterRoute
ProductionMuonRuntime::route_span(...)
```

R1 creates no mutable routing registry.

---

## 4. Core Invariant

```text
Persistent physical RAM is counted exactly.

Current HiMuon/AdamW route geometry determines the optimizer transient bound.

Historical parent transient peaks remain evidence,
not current HiMuon admission authority.
```

Equivalently:

```text
persistent state            -> unchanged accounting
historical transient peak   -> retained provenance only on HiMuon path
current route exact bound   -> current HiMuon optimizer admission authority
```

---

## 5. 36 GiB Hard Limit

The hard limit remains exactly:

```rust
pub const RAM36_PROCESS_BUDGET_HARD_LIMIT_BYTES: u64 = 38_654_705_664;
```

which equals:

```text
36 * 1024 * 1024 * 1024
```

Forbidden repairs:

```text
36 -> 48 GiB
36 -> 52 GiB
environment hard-limit override
physical-RAM-dependent silent increase
hidden fallback increase
```

---

## 6. Exact Reject-Owner Attribution

`HostProcessRamBudget` now records an exact rejection snapshot for both:

```text
reserve(...)
preflight_bound(...)
```

New structure:

```text
Ram36ExactOwnerRejectionR1
```

Fields include:

```text
phase
phaseLabel
owner
action
requestedBytes
observedPrivateBytes
reservedNotYetMaterializedBytes
projectedBytes
hardLimitBytes
exactExcessBytes
actualPrivateOverLimit
projectionOnlyOverLimit
```

New log identity:

```text
[ASH-RAM36-HIMUON-CORESIDENT-OWNER-REJECTED-R1]
```

New exact-owner failure identity:

```text
FAIL_ASH_BASETRAIN_RAM36_HIMUON_CORESIDENT_OWNER_REJECTED
```

The legacy outer compatibility token is preserved:

```text
FAIL_ASH_BASETRAIN_RAM36_PREALLOCATION_BUDGET_REJECTED
```

so existing semantic/static authorities that require the old fail-stop identity are not silently invalidated.

Persistent-owner reservation rejection additionally exposes:

```text
FAIL_ASH_BASETRAIN_RAM36_HIMUON_CORESIDENT_PERSISTENT_FOOTPRINT_UNSATISFIABLE
```

for owners including:

```text
ResidentWeightPack
AdamMResident
AdamVResident
AdamMCandidateResident
AdamVCandidateResident
TensorCubeLocalMuonMomentum
```

---

## 7. Current Route Geometry Proof

The scheduler now derives HiMuon route geometry from the already-verified runtime registry.

New helper:

```text
ram36_himuon_route_geometry_r1(...)
```

For every parameter it enumerates the complete logical range using:

```text
ProductionMuonRuntime::route_span(parameter_index, logical_start)
```

Every returned span must satisfy:

```text
span > 0
logical_end <= route.element_count
```

For every parameter:

```text
sum(non-Muon spans) == route.adamw_element_count
```

Across the whole registry:

```text
sum(non-Muon spans) == registry.adamw_element_count
```

Failure to prove exact geometry is fail-closed:

```text
FAIL_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_EXACT_GEOMETRY_UNPROVEN
```

This prevents a whole-parameter AdamW fallback from being used as a hidden route approximation.

---

## 8. Mixed Muon / AdamW Parameters

A single canonical parameter may contain both:

```text
Muon-owned full 16x16 tile regions
AdamW-owned residual regions
```

The planner explicitly detects:

```text
route.muon_element_count > 0
&& route.adamw_element_count > 0
```

and records mixed parameter count plus maximum mixed AdamW contiguous span.

Muon-owned spans are not charged as host AdamW optimizer work.

HiMuon momentum itself remains a persistent RAM36 owner and is still charged separately.

---

## 9. Route-Exact Transient Bound

New module:

```text
crates/base_train/src/
ram36_himuon_coresident_route_exact_optimizer_transient_bound_r1.rs
```

New input:

```text
Ram36HiMuonRouteExactOptimizerTransientInputR1
```

New receipt:

```text
Ram36HiMuonRouteExactOptimizerTransientBoundReceiptR1
```

The bound uses the same current optimizer topology quantities already present in the scheduler:

```text
R6_STREAM_CHUNK_ELEMENTS
RAM_ADAM_MV_PCIE_TRANSFER_SLOT_COUNT
RamResidentSegmentWork
R6AdamwCandidateOutput
R6AdamwTripleBatchInput
```

It does not derive a full-model AdamW allocation.

### 9.1 Pure AdamW live topology

For the largest currently reachable AdamW span, bounded by one R6 stream chunk, the planner accounts for:

```text
RamResidentSegmentWork outer capacity
weight/m/v nested vectors
candidate output outer capacity
candidate weight/m/v nested vectors
optional triple-batch input outer capacity
serialization weight/m/v byte vectors
```

When PCIe overlap is disabled, batch slot cardinality is one.

When overlap is enabled, the configured transfer slot cardinality is used.

### 9.2 Muon-owned parameter host topology

The current Muon parameter path processes one R6 chunk at a time.

The host chunk can contain:

```text
source weight
source M
source V
candidate weight
```

and during residual AdamW output or serialization at most three additional same-chunk vectors coexist.

Therefore the current source topology is bounded by seven same-chunk vectors for this branch.

The final route-exact segment bound is the maximum of the pure-AdamW and mixed-Muon branch bounds.

---

## 10. Historical Parent Peak Retirement

On the HiMuon production path:

```text
parentPeakUsedForAdmission = false
staleParentPeakRetiredFromAdmission = true
```

The historical values are retained in the receipt as:

```text
parentSegmentTransientPeakBytes
parentSerializationTransientPeakBytes
```

but the actual RAM36 preflight uses:

```text
routeExactSegmentTransientBoundBytes
routeExactSerializationTransientBoundBytes
```

On the non-HiMuon path, behavior is intentionally unchanged:

```text
parent.optimizer_segment_transient_peak_bytes
parent.optimizer_serialization_transient_peak_bytes
```

remain the admission values.

---

## 11. Runtime Receipt

Per optimizer step, the HiMuon + RAM36 path writes:

```text
ram36_himuon_coresident_route_exact_optimizer_transient_bound_r1.json
```

Schema:

```text
ash.basetrain.ram36_himuon_coresident_route_exact_optimizer_transient_bound.v1
```

Core fields include:

```text
revision
sourceTrainingGeneration
targetTrainingGeneration
sourceOptimizerStep
targetOptimizerStep
optimizerRoutingDigest
candidateParameterSetDigest

totalParameterCount
muonParameterCount
explicitAdamwParameterCount
mixedParameterCount
muonElementCount
adamwElementCount

maximumAdamwContiguousSpanElements
maximumMixedAdamwContiguousSpanElements
maximumAdamwSegmentElements
maximumAdamwSegmentBytes
maximumMuonParameterChunkElements

workOuterBoundBytes
workNestedBoundBytes
tripleBatchInputOuterBoundBytes
candidateOutputOuterBoundBytes
candidateOutputNestedBoundBytes

serializationWeightBoundBytes
serializationMBoundBytes
serializationVBoundBytes
mixedParameterLiveBoundBytes

routeExactSegmentTransientBoundBytes
routeExactSerializationTransientBoundBytes

parentSegmentTransientPeakBytes
parentSerializationTransientPeakBytes
parentPeakUsedForAdmission
staleParentPeakRetiredFromAdmission

hardLimitBytes
observedPrivateBeforeOptimizerBytes
reservedBeforeOptimizerBytes

residentWeightBytes
committedAdamMBytes
committedAdamVBytes
candidateAdamMBytes
candidateAdamVBytes
himuonMomentumBytes

projectedBeforeOptimizerBytes
remainingHeadroomBytes

rejectedOwner
exactExcessBytes
actualPrivateOverLimit
projectionOnlyOverLimit

currentRouteExact
admitted
physicalMeasurementClaimed
physicalHoldToken
receiptDigest
```

The receipt is written before preflight and rewritten with exact rejection evidence if optimizer preflight or later candidate-time RAM reservation fails.

---

## 12. Persistent Footprint Boundary

R1 must not force a PASS if the real persistent footprint is too large.

If:

```text
observed private bytes
+ live admitted reservations
+ physically necessary requested persistent allocation
> 36 GiB
```

then the process remains fail-closed.

Expected next-child categories, if needed, include:

```text
route-sparse Adam candidate storage
resident-weight generation handoff reduction
persistent owner lifetime reduction
```

Those changes are explicitly outside R1.

---

## 13. HDD Spill Prohibition

R1 introduces no:

```text
Adam candidate HDD spill
HiMuon momentum eviction to disk
resident-weight optimizer-time HDD fallback
swapfile/pagefile repair path
```

The target topology remains:

```text
RAM-resident optimizer state
+ GPU HiMuon execution
+ bounded durable publication
```

---

## 14. Weight Journal Isolation

Weight Successor Journal Shadow remains independent.

The existing owner:

```text
WeightSuccessorJournalShadowScratch
```

is unchanged.

R1 does not bind journal shadow state into RAM36 route-exact authority and does not make journal success a canonical training requirement.

---

## 15. Physical Claim Boundary

Source construction sets:

```text
physicalMeasurementClaimed = false
```

and carries:

```text
HOLD_ASH_BASETRAIN_RAM36_HIMUON_CORESIDENT_ROUTE_EXACT_OPTIMIZER_TRANSIENT_BOUND_PHYSICAL_PENDING_R1
```

The existence of the physical PASS token in source does not constitute a physical PASS.

Physical PASS requires a real N8 run under the current release binary and exact authorities.

---

## 16. Physical Qualification Requirements

A future physical PASS requires at minimum:

```text
N8 optimizer steps = 8
HiMuon production callsite admitted
optimizer routing digest exact
RAM36 hard limit = 36 GiB
current route exact = true
stale parent peak used for admission = false
private usage over hard limit = 0
unclassified owner = 0
non-exact owner = 0
reservation leak = 0
runtime observed optimizer transient <= route-exact bound
all eight generation promotions complete
```

HiMuon physical execution itself additionally requires direct execution evidence such as:

```text
actual Muon device execution count > 0
```

or, for the stronger active-fusion qualification:

```text
fused dispatch count > 0
fused physical batch count > 0
```

Capability probe output alone is insufficient.

---

## 17. Tokens

Static PASS:

```text
PASS_ASH_BASETRAIN_RAM36_HIMUON_CORESIDENT_ROUTE_EXACT_OPTIMIZER_TRANSIENT_BOUND_AND_STALE_PARENT_PEAK_RETIREMENT_CLOSURE_R1_STATIC
```

Physical HOLD:

```text
HOLD_ASH_BASETRAIN_RAM36_HIMUON_CORESIDENT_ROUTE_EXACT_OPTIMIZER_TRANSIENT_BOUND_PHYSICAL_PENDING_R1
```

Physical PASS identity reserved for a future real campaign:

```text
PASS_ASH_BASETRAIN_RAM36_HIMUON_CORESIDENT_ROUTE_EXACT_OPTIMIZER_TRANSIENT_BOUND_PHYSICAL_R1
```

Exact owner rejection:

```text
FAIL_ASH_BASETRAIN_RAM36_HIMUON_CORESIDENT_OWNER_REJECTED
```

Persistent footprint unsatisfiable:

```text
FAIL_ASH_BASETRAIN_RAM36_HIMUON_CORESIDENT_PERSISTENT_FOOTPRINT_UNSATISFIABLE
```

Route proof failure:

```text
FAIL_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_EXACT_GEOMETRY_UNPROVEN
```

Legacy compatibility failure retained:

```text
FAIL_ASH_BASETRAIN_RAM36_PREALLOCATION_BUDGET_REJECTED
```

---

## 18. Baked Source Truth

Actual implementation diff against the exact parent consists of five files.

New:

```text
crates/base_train/src/
ram36_himuon_coresident_route_exact_optimizer_transient_bound_r1.rs

tools/
validate_ash_basetrain_ram36_himuon_coresident_route_exact_optimizer_transient_bound_and_stale_parent_peak_retirement_closure_r1_static.py
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/ram36_process_budget.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Not modified:

```text
ram_budget_exact_inventory.rs
tensorcube_local_muon_production_callsite_adoption.rs
```

The existing exact-inventory receipt remains historical evidence.
The existing Muon registry/runtime remains the route SSOT and is read only by the new planner.

---

## 19. Static Validation

The new validator contains 18 explicit structural gates covering:

```text
36 GiB limit preservation
module wiring
HiMuon historical-parent retirement
non-HiMuon compatibility
optimizer routing digest binding
route_span exact enumeration
mixed Muon/AdamW handling
current topology accounting
persistent owner preservation
exact owner rejection attribution
legacy failure compatibility
failure receipt rewrite
no HDD spill
journal isolation
parent inventory evidence preservation
physical claim withholding
explicit failure identities
no whole-parameter AdamW fallback
```

The final regression chain at bake time is:

```text
STATIC_CHAIN_PASS = 16
STATIC_CHAIN_FAIL = 0
```

The 16 validators include this R1 plus the existing Weight Journal, RAM Adam A/B, durability descriptor, Eve R1/R2, MCU pending/B06/full-model/bounded-projection, SubmissionEpoch, P3, MCU control-plane, RAM36 underflow, successor-weight ownership, and immutable N2 RAM36 authorities.

No Rust compile or physical execution claim is made by the bake environment because the bake environment does not contain Cargo/Rustc.

---

## 20. Packaging

Full-source and overlay bakes exclude:

```text
Markdown specifications
generated runtime receipts
generated manifests/evidence
workspace
target*
.git
__pycache__
training-state outputs
```

They retain:

```text
Rust source
static validators
Cargo source/configuration already present in the parent
```

GitHub receives the specification only.
Implementation source is not committed to GitHub by this specification publication step.

---

## 21. Final Invariant

```text
No RAM36 cap inflation.
No HDD spill repair.
No fake persistent-to-transient reclassification.
No stale historical peak as current HiMuon route authority.
No Muon-only range charged as AdamW host work.
No silent whole-parameter fallback.
No generic RAM rejection without exact owner evidence.
No physical PASS without physical execution.

Exact current route.
Exact current owner.
Exact current process projection.
Exact failure identity.
```
