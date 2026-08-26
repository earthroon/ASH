# ASH-N8-VENDOR-PERF-ATTRIBUTION-08-BASE

## Physical N8 Attribution Baseline / Production Runtime Cost Decomposition / No-Optimization Measurement Authority

## 1. Patch identity

```text
ASH-N8-VENDOR-PERF-ATTRIBUTION-08-BASE

Physical N8 Eight-Step Baseline /
Production Path Only /

Forward·Backward·Optimizer Wall Attribution /
Local Muon Physical Attribution /
Fused HiMuon Physical Attribution /
AdamW Wall Attribution /

Queue Submit Attribution /
Exact Wait Attribution /
BindGroup Creation Attribution /

Vendor Alias Resolve·Lock·Clone Attribution /
Resolved Primitive Generic Downcast Attribution /
D2D Materialization Attribution /
Vendor Buffer Allocation Attribution /

Submission-Epoch-Compatible Measurement /
No New Blocking Wait /
No Scheduling Mutation /
No Optimizer Semantic Mutation /
No Synthetic Benchmark Substitution /

Baseline Truth Seal
```

Build revision:

```text
ash-n8-vendor-perf-attribution-08-base
```

Receipt schema:

```text
ash.n8.vendor_perf_attribution_08_base.v1
```

## 2. Purpose

08-BASE is a measurement authority, not an optimization patch.

It answers one question:

```text
Where does the canonical physical N8 eight-step production run spend time and runtime churn?
```

Every later revision 08A through 08G must compare against this baseline under the same production lineage.

A PASS means the attribution is trustworthy. It does not mean the current N8 implementation is fast.

## 3. Production route authority

Only the existing production N8 route is admissible.

```text
Canonical production entry
→ eight exact optimizer steps
→ existing forward
→ existing backward
→ existing hybrid optimizer routing
→ existing durability closure
```

Required:

```text
productionLoopOptimizerSteps = 8
```

No benchmark-only fast lane, fixture-only optimizer, alternate Muon route, or synthetic workload can substitute for the production route.

## 4. No-optimization invariant

08-BASE must not change:

```text
optimizer math
Muon / AdamW ownership
HiMuon planner authority
workgroup geometry
physical batch geometry
queue submission topology
exact-wait topology
bind-group reuse policy
D2D materialization policy
buffer allocation policy
fork/autotune policy
shader algorithm
```

Instrumentation is allowed. Scheduling mutation is not.

The baked source therefore records:

```text
physicalSemanticsUnchanged = true
instrumentationSchedulingChangeCount = 0
```

unless a later physical validation proves otherwise.

## 5. Existing SSOT reuse

08-BASE does not replace existing N8 wall-time or Muon execution receipts.

Authority order:

```text
existing N8 phase wall-time receipt
+
existing ProductionMuonExecutionCounters
+
existing vendor allocation/materialization hooks
+
08-BASE projection and deltas
```

The baseline layer is a projection over existing execution truth.

## 6. Step boundary

All attribution remains generation-bound and step-bound.

Each step records:

```text
stepIndex
sourceGeneration
targetGeneration
stepWallNs
forwardWallNs
backwardWallNs
optimizerWallNs
adamwWallNs
muonWallNs
```

The canonical run contains exactly eight step receipts.

## 7. Optimizer physical decomposition

The baseline distinguishes:

```text
Local Muon
Fused HiMuon
AdamW
optimizer control overhead
```

Local Muon and HiMuon are not inferred from policy artifacts.

HiMuon physical execution requires the existing planner-owned fused path and fused-pair executor counters.

## 8. Physical batch attribution

The baked runtime derives:

```text
physicalOptimizerBatchCount
localMuonPhysicalBatchCount
himuonPhysicalBatchCount
```

from existing production Muon counters.

The Local count is the total physical Muon batch count minus the fused physical batch count. Saturating arithmetic prevents a malformed counter relation from underflowing; physical validation must still reject an impossible topology upstream.

## 9. Exact wait attribution

The current Local Muon and Fused HiMuon executors physically perform an exact submission wait before compact status consumption.

08-BASE measures the wall interval around the existing wait call without removing, deferring, or adding a wait.

Recorded fields:

```text
exactWaitCount
localMuonExactWaitCount
himuonExactWaitCount

exactWaitWallNs
localMuonExactWaitWallNs
himuonExactWaitWallNs
```

This is the parent evidence for 08A.

## 10. Bind-group creation attribution

The existing per-physical-batch bind-group creation remains intact.

08-BASE measures the wall interval around `device.create_bind_group(...)` in the Local and Fused Muon executors.

Recorded fields:

```text
bindGroupCreateCount
localMuonBindGroupCreateCount
himuonBindGroupCreateCount

bindGroupCreateWallNs
localMuonBindGroupCreateWallNs
himuonBindGroupCreateWallNs
```

No bind-group cache is introduced by 08-BASE.

This is the parent evidence for 08C.

## 11. Queue and encoder topology

The existing Muon execution counters remain the queue topology authority.

Recorded fields include:

```text
queueSubmitCount
commandEncoderCount
physicalOptimizerBatchCount
```

Derived metric:

```text
submitsPerPhysicalOptimizerBatch
```

This is the parent evidence for 08B.

## 12. Compact status versus candidate payload

Compact status readback is measured separately from candidate payload D2H.

Recorded:

```text
compactStatusReadbackBytes
localMuonCompactStatusReadbackBytes
himuonCompactStatusReadbackBytes
candidatePayloadD2HBytes
```

For the admitted active-device-candidate production path:

```text
candidatePayloadD2HBytes = 0
```

is required for baseline validity.

## 13. Vendor alias registry attribution

The vendor storage alias registry receives low-overhead aggregate counters only.

Recorded:

```text
aliasResolveCount
aliasResolveWallNs
aliasLockAcquireCount
aliasLockWaitNs
aliasEntryCloneCount
aliasTombstoneFullScanCount
```

No per-resolve JSON, string trace file, or blocking telemetry export is added to the hot path.

The existing alias entry semantics are unchanged.

This is parent evidence for 08D.

## 14. Resolved primitive attribution

The existing `burn-fusion-local` resolved primitive registry already tracks full-key and alias hits/misses.

08-BASE additionally counts generic `Arc<dyn Any>` downcast attempts and failures.

```text
resolvedPrimitiveLookupCount
genericAnyDowncastCount
genericAnyDowncastFailureCount
```

No typed fast registry is introduced here.

## 15. D2D materialization attribution

The existing vendor buffer inventory hook remains the materialization authority.

08-BASE projects:

```text
d2dMaterializationCount
d2dMaterializationBytes
```

No materialization is elided by this revision.

This is parent evidence for 08E.

## 16. Vendor allocation attribution

The existing vendor buffer allocation hook remains authoritative.

08-BASE projects:

```text
vendorBufferCreateCount
vendorBufferCreateBytes
vendorBufferDestroyCount
```

No slab allocator or reuse policy is added here.

This is parent evidence for 08F.

## 17. Counter reset scope

Only measurement counters are reset at the beginning of the exact N8 baseline window.

The following are never reset by 08-BASE:

```text
model state
optimizer state
Muon momentum
alias registry entries
resolved primitive entries
submission state
resident GPU state
```

The reset applies only to aggregate telemetry counters so the eight-step delta has a clean origin.

## 18. Baseline root identity

The baked implementation binds a compact root identity to the current production source state and scheduler authority using existing digests.

Current baked components include:

```text
source generation
source optimizer step
candidate parameter-set digest
candidate manifest digest
scheduler profile digest
optimizer learning-rate bits
```

The root is hashed before publication.

Future revisions may extend the root with exact binary/device digests without changing the runtime cost fields.

## 19. GPU timestamp authority

08-BASE does not fabricate GPU subphase time.

The current bake does not yet bind a non-stalling WGPU timestamp-query ring to the N8 production phase tree.

Therefore:

```text
gpuTimestampAvailable = false
gpuPhaseTimingStatus = UNBOUND_NONSTALLING_PHASE_TIMESTAMP_DOMAIN_08_BASE
```

and the receipt emits:

```text
HOLD_ASH_N8_VENDOR_PERF_08_BASE_NONSTALLING_GPU_TIMESTAMP_DOMAIN_NOT_BOUND
```

CPU wall time is never relabeled as GPU time.

This HOLD does not invalidate the CPU/runtime-topology baseline, but GPU-specific performance promotion must remain unavailable until a non-stalling timestamp authority is added.

## 20. Measurement overhead policy

Instrumentation must not add:

```text
new device.poll(Wait)
new queue completion wait
new map readback
new D2H payload
per-event JSON serialization
hot-path stdout logging
```

The alias registry uses aggregate atomics and `Instant` wall intervals only.

The Local/Fused Muon timing wraps already-existing operations.

## 21. Runtime delta model

Each optimizer step captures a snapshot immediately before and after the existing optimizer execution.

```text
before snapshot
→ unchanged optimizer execution
→ after snapshot
→ saturating counter delta
```

The delta contains only activity produced within that optimizer window.

Eight deltas are paired with the existing eight N8 phase receipts.

## 22. Derived metrics

The baseline computes:

```text
waitFractionOfOptimizer
submitsPerPhysicalOptimizerBatch
bindGroupsPerPhysicalOptimizerBatch
```

These are diagnostic projections, not replacement authorities for the raw counters.

## 23. 08A admission evidence

08A should be prioritized when:

```text
exactWaitCount > 0
and
exactWaitWallNs materially contributes to optimizerWallNs
```

Especially strong evidence:

```text
exactWaitCount ≈ physicalOptimizerBatchCount
```

## 24. 08B admission evidence

08B should be prioritized when:

```text
queueSubmitCount ≈ physicalOptimizerBatchCount
```

with a low batches-per-submit ratio.

## 25. 08C admission evidence

08C should be prioritized when per-batch bind-group creation remains dominant:

```text
bindGroupCreateCount ≈ physicalOptimizerBatchCount
```

and bind-group wall time is material.

## 26. 08D admission evidence

08D is justified by one or more of:

```text
aliasResolveWallNs materially high
aliasLockWaitNs > 0
aliasEntryCloneCount high
genericAnyDowncastCount high
```

## 27. 08E admission evidence

08E is a speed priority only when:

```text
d2dMaterializationCount > 0
or
d2dMaterializationBytes materially high
```

Observed zero keeps 08E structurally interesting but performance-low-priority.

## 28. 08F admission evidence

08F is justified when vendor buffer creation repeats materially across the N8 window.

```text
vendorBufferCreateCount
vendorBufferCreateBytes
```

must be interpreted separately from A02-owned resident allocations.

## 29. 08G boundary

08-BASE does not yet add fork snapshot/merge wall counters.

08G remains a later structural/performance revision and must only be prioritized if fork/autotune activity is physically present in the canonical N8 run.

## 30. Runtime artifacts

The code may emit at runtime:

```text
n8_vendor_perf_attribution_08_base_receipt.json
n8_vendor_perf_attribution_08_base_steps.jsonl
```

These are runtime products, not source-package inputs.

They are deliberately excluded from the delivered source ZIPs for this bake.

## 31. Baseline validity

Current baked validity gate:

```text
productionStepCount = 8
baselineRootIdentity present
candidatePayloadD2HBytes = 0
physicalSemanticsUnchanged = true
instrumentationSchedulingChangeCount = 0
```

GPU timestamp truth is a separate HOLD as defined above.

## 32. PASS meaning

```text
PASS_ASH_N8_VENDOR_PERF_ATTRIBUTION_08_BASE
```

means:

```text
The physical N8 CPU/runtime topology can be compared against later optimization revisions.
```

It does not mean:

```text
GPU timestamp authority complete
N8 performance promoted
08A/08B/08C automatically admitted
```

## 33. Baked source touch points

The 08-BASE bake touches the following runtime boundaries:

```text
base_train N8 scheduler
N8 vendor perf projection module
ProductionMuon execution counters
Local Muon physical executor
Fused HiMuon physical executor
burn-wgpu-local alias registry
burn-fusion-local resolved primitive registry
burn_webgpu_backend vendor telemetry re-export surface
```

No manifest source is required for this patch.

## 34. Final authority declaration

```text
08-BASE
= Measurement Authority

08A+
= Optimization Authority
```

Core invariant:

> 08-BASE does not make N8 faster. It makes every later claim about why N8 became faster attributable to a physical runtime change instead of a guess.
