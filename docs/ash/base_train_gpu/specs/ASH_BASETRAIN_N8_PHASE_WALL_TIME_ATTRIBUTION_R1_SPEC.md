# ASH-BASETRAIN-N8-PHASE-WALL-TIME-ATTRIBUTION-R1

## 1. Patch identity

```text
ASH-BASETRAIN-N8-PHASE-WALL-TIME-ATTRIBUTION-R1

Monotonic Wall Clock Authority /
Eight-Step Phase Ledger /
Forward·Backward·Optimizer Separation /
AdamW·Muon·HiMuon Execution Identity /
Resident Atlas Projection·Readahead Attribution /
Final Triple-Pack Write·Sync Timing /
Cross-Volume Publication·Digest Timing /
Explicit Unattributed Time /
No Fabricated GPU Timing /
Low-Overhead Judgment Deferral Seal
```

Build revision:

```text
n8-phase-wall-time-attribution-r1
```

Receipt schema:

```text
ash.basetrain.n8_phase_wall_time_attribution.v1
```

## 2. Purpose

N8 end-to-end wall time alone cannot distinguish training-compute regression from
resident/Atlas movement, optimizer routing, final packed durability, cross-volume
publication, or digest verification. This patch attributes the canonical eight-step N8
run into independently inspectable wall-time domains without changing training or
persistence semantics.

The immediate question is whether an observed multi-minute regression belongs to
forward/backward compute, AdamW/Muon/HiMuon execution, Atlas traffic, final triple-pack
materialization, or `D:` to `E:\ASH` durable publication and verification.

R1 is an observation patch. It does not add a new training admission and does not alter
route selection. The receipt is produced for the canonical admitted N8 long-horizon
8-step execution.

## 3. Clock authority

CPU/orchestration timing uses monotonic `std::time::Instant`.

Forbidden wall-time authorities:

```text
SystemTime
filesystem modification time
console/log timestamps
calendar time
```

Durations are serialized as unsigned nanoseconds.

GPU execution timing is a separate clock domain. R1 does not fabricate GPU nanoseconds
from CPU wall time and does not add blocking timestamp readback. Until a non-stalling
phase timestamp domain is physically bound, the receipt records:

```text
gpuTimestampSupported = null
gpuPhaseTimingStatus = UNBOUND_NONSTALLING_PHASE_TIMESTAMP_DOMAIN_R1
himuonGpuNs = null
optimizerSubphaseGpuSeparationSupported = false
```

No `map_async`/forced `device.poll(...Wait)` profiling barrier is introduced by the R1
attribution module.

## 4. Top-level attribution domains

Canonical hierarchy:

```text
N8_TOTAL
|
+-- STARTUP
|
+-- TRAINING_LOOP
|   +-- STEP_1
|   +-- STEP_2
|   +-- ...
|   +-- STEP_8
|
+-- FINAL_DURABILITY
|   +-- weights.r6pack write + sync
|   +-- adam_m.r6pack write + sync
|   +-- adam_v.r6pack write + sync
|
+-- STORAGE_PUBLICATION
|   +-- copy/source-stream work
|   +-- destination digest verification
|
+-- FINALIZATION
```

Parent durations and nested detail are not blindly summed. The final receipt maintains
an explicit known-exclusive ledger and an `unattributedWallNs` remainder.

## 5. Per-step ledger

Each of the eight optimizer steps records:

```text
stepIndex
sourceGeneration
targetGeneration
stepWallNs

atlasPlanWallNs
waveWallNs
forwardWallNs
backwardWallNs

atlasProjectionCount
atlasProjectionBytes
atlasProjectionWallNs

atlasReadaheadProjectionCount
atlasReadaheadProjectionBytes
atlasReadaheadWallNs

optimizerWallNs
adamwWallNs
muonWallNs

finalWeightPackWriteWallNs
finalWeightPackSyncWallNs
finalAdamMPackWriteWallNs
finalAdamMPackSyncWallNs
finalAdamVPackWriteWallNs
finalAdamVPackSyncWallNs

finalMaterialization
```

Forward wall is measured around the existing forward/loss-tape preparation execution.
Backward wall is measured around the existing backward/gradient-accumulator execution.
They are host-observed wall domains and are not mislabeled as GPU timestamp durations.

## 6. AdamW, Muon, and HiMuon identity

Optimizer timing distinguishes execution identity from timing availability.

The receipt exposes:

```text
adamwExecuted
adamwWallNs
muonExecuted
muonWallNs
himuonExecuted
himuonFusionExecutionCount
himuonGpuNs
```

`adamwWallNs` and `muonWallNs` are host-observed execution-call wall time.

`himuonExecuted` is not inferred from a nonzero generic optimizer duration. It is bound
to the existing `bp_dk_himuon_fusion_execution_count` authority. Therefore a run can
truthfully report local Muon execution while HiMuon fusion remains unexecuted.

If HiMuon GPU subphase timing cannot be separated without adding a synchronization
barrier, R1 records it as unavailable rather than estimating it.

## 7. Burn/runtime scaffold retirement evidence

The phase receipt preserves the already-retired runtime-arena authority as explicit zero
fields:

```text
runtimeArenaCreateCount = 0
runtimeArenaRewriteCount = 0
runtimeArenaWallNs = 0
```

This prevents a slower end-to-end run from being incorrectly interpreted as proof that
the retired Burn/runtime-arena path returned.

## 8. Resident Atlas attribution

The checkpoint resident range reader accumulates monotonic wall time for actual resident
range projection and its read-ahead projection work.

Per-step attribution is coupled to the existing resident reader receipt:

```text
residentProjectionCount
residentProjectionBytes
residentProjectionWallNs
residentReadaheadProjectionCount
residentReadaheadProjectionBytes
residentReadaheadWallNs
```

No per-projection console logging is allowed on the hot path.

The existing micro-atlas vocabulary page counts/bytes remain available from the R6A-R2
receipts. R1 does not claim an isolated per-page GPU duration because that clock domain
is not yet safely separated; such time remains contained in the measured forward or
backward wall domain rather than being silently invented.

## 9. Packed writer attribution

`SequentialPackWriter` records two separate wall domains:

```text
writeWallNs
syncWallNs
```

Write timing covers the actual payload write call. Sync timing covers the existing
flush/durability sync boundary. R1 does not change writer cardinality or sync semantics.

For N8 Deferred Durable Writeback, intermediate steps continue to materialize zero
packed payload bytes, while step 8 retains final-only weight/Adam M/Adam V
materialization and the already-promoted packed-sync cardinality of three.

## 10. Storage publication attribution

`BaseTrainStoragePublicationReceipt` is extended with:

```text
publicationWallNs
copyWallNs
digestVerifyWallNs
digestVerifiedBytes
```

`copyWallNs` is the host wall domain for the existing source stream, destination write,
source hash, flush, and destination sync performed by `copy_verify`.

`digestVerifyWallNs` is the separate destination reread/hash verification pass.

The storage receipt continues to provide:

```text
runtimeVolume
storageVolume
crossVolumePublication
copiedPayloadCount
copiedPayloadBytes
digestVerifiedPayloadCount
```

This allows cross-volume HDD publication cost to be distinguished from training compute.

## 11. Receipt and diagnostics

Runtime receipt:

```text
n8_phase_wall_time_attribution_receipt.json
```

Primary diagnostics:

```text
[ASH-N8-PHASE-WALL-TIME-R1]
[ASH-N8-OPTIMIZER-TIME-R1]
[ASH-N8-ATLAS-TIME-R1]
[ASH-N8-STORAGE-TIME-R1]
```

The receipt contains total, startup, training-loop, derived training-compute, final
packed durability, storage publication/copy/digest, finalization, optimizer, Atlas, and
unattributed wall domains plus the eight step records.

## 12. No-double-count and unattributed authority

`knownExclusiveWallNs` must never exceed `totalWallNs`.

Hard failure:

```text
N8PhaseDoubleCountDetected
```

Unresolved time is not assigned to a convenient phase. It remains:

```text
unattributedWallNs
unattributedRatio
```

Completeness target:

```text
unattributedRatio <= 0.05
```

If the target is not met, the receipt emits a HOLD rather than fabricating attribution.

## 13. Instrumentation overhead authority

R1 deliberately does not claim the <=1% instrumentation-overhead target from a single
instrumented run. A true overhead verdict requires an equivalent baseline/candidate
comparison.

Therefore R1 records:

```text
instrumentationOverheadNs = null
instrumentationOverheadJudgment = JUDGMENT_DEFERRED_BASELINE_REQUIRED
HOLD_ASH_BASETRAIN_N8_PHASE_WALL_TIME_ATTRIBUTION_LOW_OVERHEAD_REQUIRES_BASELINE_COMPARISON_R1
```

This HOLD is intentional and is not a training failure.

## 14. Semantic no-change boundary

R1 does not change:

- forward/backward equations,
- loss or gradient values,
- AdamW, Muon, or HiMuon equations,
- optimizer routing,
- scheduler or learning-rate policy,
- dataset/token ordering,
- generation progression,
- TensorCube topology,
- subgroup32 execution,
- Atlas geometry,
- resident weight ownership,
- packed checkpoint serialization,
- Deferred Durable Writeback semantics,
- packed sync cardinality,
- storage publication semantics,
- archive format.

## 15. Implementation surface

Baked R1 overlay:

```text
crates/base_train/src/n8_phase_wall_time_attribution.rs
crates/base_train/src/lib.rs
crates/base_train/src/base_train_atlas_wave_01_checkpoint_reader.rs
crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
crates/base_train/src/storage_root_authority.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
tools/validate_ash_basetrain_n8_phase_wall_time_attribution_r1_static.py
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

The overlay excludes generated artifacts, manifests, `.sha256` sidecars, and Python
cache output.

## 16. Structural evidence

Observed in the reconstructed cumulative source tree:

```text
N8 phase wall-time attribution R1:                           73/73 PASS
N8 Deferred Durable Writeback + resident + sync closures:   118/118 PASS
RAM-resident Adam M/V final writeback:                       73/73 PASS
N8 source-weight generation SSOT:                            PASS
N8 long-horizon continuity:                                  70/70 PASS
RAM weight persistent residency / Atlas readahead:           67/67 PASS
VRAM hot-weight residency:                                   70/70 PASS
GPU successor continuity:                                    52/52 PASS
Storage-root authority:                                      39/39 PASS
RAM36 process-budget authority:                              63/63 PASS
Resume-cut exact determinism static:                         118/118 PASS
RAM Adam M/V PCIe overlap static:                             76/76 PASS
Persistent TensorCube resource slab/reuse:                    68/68 PASS
```

The bake environment does not provide the Rust toolchain. Release CF1 in the
authoritative local checkout is therefore the compilation/type/borrow authority.

## 17. Promotion tokens

Structural:

```text
PASS_ASH_BASETRAIN_N8_PHASE_WALL_TIME_ATTRIBUTION_STRUCTURAL_R1
```

Physical attribution:

```text
PASS_ASH_BASETRAIN_N8_PHASE_WALL_TIME_ATTRIBUTION_PHYSICAL_R1
```

Completeness when <=5% unattributed:

```text
PASS_ASH_BASETRAIN_N8_PHASE_WALL_TIME_ATTRIBUTION_COMPLETENESS_R1
```

Low-overhead promotion is deliberately not emitted by a single R1 run. It remains HOLD
until an equivalent uninstrumented/instrumented comparison establishes the overhead
budget.

Final promotion may only be declared after physical attribution, acceptable completeness,
and independent overhead evidence are all present.

## 18. Physical acceptance questions

The first physical run must provide enough evidence to answer separately:

```text
How long did the eight-step training loop take?
How much of it was forward/backward/optimizer host wall?
Did AdamW execute?
Did local Muon execute?
Did HiMuon fusion execute?
How much resident Atlas projection/readahead wall was observed?
How long did final packed writes and syncs take?
How long did durable storage copy/source-stream work take?
How long did destination digest verification take?
How much time remains unattributed?
```

A performance regression must not be assigned to HiMuon, Burn-scaffold changes, Atlas,
or HDD publication until the corresponding observed phase supports that judgment.

## 19. Final SSOT

```text
N8 performance is judged by attributed phase time, not end-to-end wall time alone.

CPU/orchestration phase authority uses monotonic Instant durations.
GPU subphase durations are reported only when a non-stalling timestamp domain is
physically available; unavailable GPU time is never synthesized from CPU wall time.

AdamW, local Muon, and HiMuon execution identities are explicit and separate.
Resident Atlas projection/readahead, final packed writer write/sync, cross-volume storage
publication, and destination digest verification are independently observable domains.

Nested timing is not double-counted in the exclusive total. Unknown time remains
explicitly unattributed.

Instrumentation overhead is judgment-deferred until an equivalent baseline comparison
exists.

Only these observed boundaries may be used to attribute an N8 slowdown.
```
