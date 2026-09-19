# TENSORCUBE-CONSUME-R2

## GPU Parallel Consume Plane

```text
+ R1 RELATION EXECUTION AUTHORITY
+ TENSORCUBE TABLE-PARALLEL CONSUME
+ PACKED CANDIDATE -> DEVICE PARAMETER ASSEMBLY
+ BOUNDED MULTI-RANGE GPU D2D SUBMISSION
+ NONBLOCKING CONSUME COMPLETION
+ B06 SUCCESSOR CLAIM AFTER PHYSICAL CONSUME COMPLETION
+ NO PER-TILE HOST ROW CONSUME IN ACTIVEVERIFIED
+ NO FULL CANDIDATE D2H
+ NO CPU CANONICAL PROJECTION REBUILD
+ R3H / CF11 / RAM36 / R8A / BPDK / PACKED-MV PRESERVATION
```

## 0. Parent

Direct parent:

```text
TENSORCUBE-CONSUME-R1
ASH_PASS3_TENSORCUBE_CONSUME_R1_RELATION_AUTHORITY_CODE_ONLY.zip
SHA-256 9649b6147ef89e0156532a0fed6ef786ea8b7862d5cd91abe9713090202b7986
```

R2 class:

```text
GPU DEVICE-TO-DEVICE CONSUME EXECUTION
R1 RELATION PHYSICAL PROJECTION
DEVICE SUCCESSOR ASSEMBLY
B06 SUCCESSOR ORDERING CLOSURE
```

## 1. Physical motivation

The preceding physical campaign already reached:

```text
source-last-use-close                PASS
source-host-retired                  PASS
CF11 promotion materialize           PASS
source-retirement-closure            PASS
successor-materialized               PASS
full_candidate_heap_allocation_count 0
successor d2h_bytes                   0
full_temporary_copy_count             0
```

and then failed at:

```text
FAIL_B06_CANDIDATE_NOT_COMPLETE:muon-device-successor-missing
```

R2 does not weaken that B06 gate.

## 2. R1 remains relation SSOT

R2 does not create an independent TensorCube geometry authority.

R1 now exposes an exact per-R6-epoch projection:

```text
TensorCubeConsumeEpochProjectionR1
```

created by:

```text
TensorCubeConsumeRelationBuilderR1::admit_r6_epoch_with_projection(...)
```

The existing `admit_r6_epoch(...)` API remains as a compatibility wrapper.

Each epoch projection binds:

```text
parameter_index
queue_generation_id
queue_epoch_id
R6 descriptor digest
parameter authority digest
projection digest
R1 relation rows
R1 canonical weight row spans
```

The full R1 builder still seals the complete parameter relation and exact gap/overlap proof.

## 3. R2 physical plan

New module:

```text
crates/base_train/src/tensorcube_consume_plane_r2.rs
```

New authority:

```text
TensorCubeConsumeEpochPlanR2
TensorCubeConsumePhysicalRangeR2
TensorCubeConsumeExecutionReceiptR2
TensorCubeConsumePlaneModeR2
```

`TensorCubeConsumeEpochPlanR2::from_r1_projection(...)` consumes the R1 epoch projection plus the exact R6 descriptor snapshot.

It does not look up parameter names or rebuild parameter geometry.

## 4. Physical destination distinction

R1 canonical weight row spans remain the logical model projection proof.

The current ActiveVerified device segmented successor, however, is TensorCube-padded parameter storage used by the next device generation.

R2 therefore adds a physical assembly projection:

```text
parameter_element_start
    = canonical_job_ordinal * R6_TILE_ELEMENTS
```

while retaining R1 canonical weight row spans as exact logical lineage.

This does not replace or weaken the R1 canonical projection.

## 5. Source table

Each R2 physical range binds:

```text
source_weight_element_start
source_momentum_element_start
source_update_element_start
parameter_element_start
element_count
canonical_job_ordinal
```

W/M source starts come from the R1 relation.

Update source start comes from the same R6 descriptor whose digest is already bound into the R1 projection.

No host tensor values are reconstructed.

## 6. Exact range validation

Every physical range requires checked bounds for:

```text
candidate weight source
candidate momentum source
orthogonal update source
parameter assembly destination
```

No empty range is admitted.

R2 coalesces only ranges that are simultaneously contiguous in:

```text
canonical TensorCube ordinal
candidate W source
candidate M source
candidate update source
parameter assembly destination
```

No semantic reorder is allowed.

## 7. GPU execution implementation

This bake deliberately does **not** add a new WGSL scatter kernel.

The current physical source and destination ranges are contiguous D2D spans after R1/R6 projection, so R2 uses WGPU `copy_buffer_to_buffer` operations encoded from the admitted table into one command encoder per ready wave.

For every admitted range the encoder performs:

```text
candidate W      -> assembly W
candidate M      -> assembly M
orthogonal update -> assembly update
```

This is a GPU copy-engine consume plane.

It avoids adding arithmetic or a second numerical kernel to a bit-exact projection operation.

A future revision may introduce a WGSL scatter kernel only if canonical strided scatter or measured copy-engine limitations require it.

## 8. No per-tile host consume in ActiveVerified

In R2 ActiveVerified the path does not use:

```text
write_successor_muon_tile_f32(...)
HiMuonMomentumRuntimeR8::commit_candidate_range_r8(...)
```

for the active-async device successor.

The legacy fragment-copy path remains available only for R2 `Off` mode.

## 9. Runtime modes

Environment:

```text
ASH_TENSORCUBE_CONSUME_R2_MODE
```

Modes:

```text
OFF
OBSERVE_ONLY
ACTIVE_VERIFIED
```

### OFF

Parent assembly path remains authoritative.

### OBSERVE_ONLY

The enum is reserved, but a physically separate shadow assembly target is not materialized in this bake.

Selecting ObserveOnly fails closed with:

```text
E_TENSORCUBE_CONSUME_R2_OBSERVE_ONLY_SHADOW_TARGET_NOT_MATERIALIZED
```

No silent fallback occurs.

### ACTIVE_VERIFIED

R1 epoch projection is converted to the R2 physical range table and executed by GPU D2D submission.

## 10. Existing parameter assembly reused

R2 reuses:

```text
MuonDeviceParameterAssemblyR2
```

as the destination owner.

No second full parameter W/M/update surface is created.

The existing assembly coverage ledger remains authoritative:

```text
reserved_ranges
completed_ranges
active_fragment_writers
coverage_complete()
```

## 11. New backend table ABI

New backend types:

```text
MuonDeviceTensorCubeConsumeRangeR2
PendingTensorCubeConsumeTableR2
```

New methods:

```text
MuonDeviceParameterAssemblyR2::submit_tensorcube_consume_table_r2(...)
MuonDeviceParameterAssemblyR2::try_collect_tensorcube_consume_table_r2(...)
```

The submit path encodes all admitted table ranges into one command encoder and submits with exact source/target leases.

## 12. Submission lease authority

The consume submission registers source read leases for:

```text
tensorcube.consume.r2.source.weight
tensorcube.consume.r2.source.momentum
tensorcube.consume.r2.source.update
```

and destination write leases for:

```text
tensorcube.consume.r2.target.weight
tensorcube.consume.r2.target.momentum
tensorcube.consume.r2.target.update
```

Candidate source arenas remain live until consume submission completion.

## 13. No per-wave blocking wait

R2 table submission does not call `wait_for_submission_exact`.

Collection uses:

```text
poll_nonblocking_and_refresh(...)
submission_completed_nonblocking(...)
```

The caller may continue submitting other ready waves within the existing bounded pending-wave scheduler.

## 14. B06 ordering closure

Parent ActiveVerified previously claimed/staged the B06 successor ticket before the assembly copy.

R2 ActiveVerified changes the ordering to:

```text
physical Muon candidate ready
    -> submit R2 table consume
    -> nonblocking physical completion observed
    -> claim LocalMuonDeviceSuccessorTicketR1
    -> reclaim consumed source arenas
    -> stage real B06 successor ticket
```

Therefore B06 staging occurs only after the required R2 D2D consume has physically completed.

## 15. B06 gate preservation

Unchanged backend gates remain:

```text
FAIL_B06_CANDIDATE_NOT_COMPLETE:muon-device-successor-missing
FAIL_B06_CANDIDATE_NOT_COMPLETE:muon-successor-submission-drift
```

R2 does not modify `hybrid_optimizer_device_commit.rs`.

The B06 ticket retains the source compute submission epochs required by the existing equality contract.

R2 consume submission epochs are tracked separately by the R2 receipt rather than falsifying the source compute lineage.

## 16. Explicit consume consumer token

`McuWaveConsumerKindR1` gains:

```text
TensorCubeConsumePlaneR2
```

Active R2 waves register this consumer token in addition to existing:

```text
CanonicalCandidate
R6CompletionEvidence
B05DeviceCandidate
B06DeviceSuccessor
BpDkDevicePostUpdateEvidence
MuonSegmentedSuccessorApplication
```

All semantic consumers must close before atlas lease retirement.

## 17. R2 execution receipt

New compact receipt:

```text
[ASH-TENSORCUBE-CONSUME-R2][gpu-plane]
```

It binds:

```text
mode
parameter_index
R1 relation digest
source wave count
relation row count
physical range count
logical weight span count
W/M/update consumed element counts
consume submission ordinals
bulk_d2h_bytes
CPU tile write count
CPU momentum tile commit count
B06 successor ticket count
B06 successor sealed
gap count
overlap count
receipt digest
admitted
```

Active receipt requires:

```text
bulk_d2h_bytes = 0
cpu_weight_tile_write_count = 0
cpu_momentum_tile_commit_count = 0
b06_successor_tickets == source_wave_count
gap_count = 0
overlap_count = 0
```

## 18. BP-DK preservation

The existing device BP-DK post-update path remains unchanged after parameter successor assembly:

```text
bpdk_runtime.submit_parameter(...)
collect_parameter_after_exact_wait_r1a(...)
```

R2 does not yet close BP-DK checkpoint snapshot parameter-by-parameter readback.

That remains a separate bottleneck/revision.

## 19. Segmented successor preservation

After R2 coverage completes:

```text
assembly.finalize()
    -> LocalMuonDeviceSegmentedHandoffR1
    -> publish_local_muon_segmented_handoff_r1(...)
```

remains unchanged.

## 20. Memory preservation

R2 adds no full host candidate W/M/update vectors.

No additional full parameter assembly is created.

The parent R3H/CF11 laws remain external promotion requirements:

```text
old source retired before successor full reservation
full_candidate_heap_allocation_count = 0
full_temporary_copy_count = 0
successor bulk D2H = 0
```

## 21. Changed files

```text
MOD crates/base_train/src/lib.rs
ADD crates/base_train/src/tensorcube_consume_plane_r2.rs
MOD crates/base_train/src/tensorcube_consume_relation_r1.rs
MOD crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
MOD crates/base_train/src/unified_atlas_mcu_submission_epoch_dependency_active_async_r1.rs
MOD crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
MOD crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon_active_device_pending_r1.rs
ADD tools/validate_ash_tensorcube_consume_r2_gpu_parallel_plane_static.py
```

Delta:

```text
MOD 6
ADD 2
DEL 0
```

## 22. Source SHA-256

```text
7560a7c05187bcf080cc636c23090f1fdfcbdcc297ece02282e8da9299df2b85  crates/base_train/src/lib.rs
1cd8b8346ad89fbf5b8047459e2caeb0e8734a4bc2f327e12fdadde1c85ca8d1  crates/base_train/src/tensorcube_consume_relation_r1.rs
f2bfa751645cabb521769b3a0ba7c82909b04936aff6bbced6deb92d370f48b9  crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
dd3e29dd9b2a3bfec9c4a4b966db4e3dcb745ef32142dd586839670134fbc1b1  crates/base_train/src/unified_atlas_mcu_submission_epoch_dependency_active_async_r1.rs
408fd21f604e56dff38a8feb847c7b8d50ea2752d845cb518cc9e00fd7abde10  crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
30e178cc4ca971920921ebe60d541896af53ddc94dc281471893ea59b3d3ad1b  crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon_active_device_pending_r1.rs
d331e8f9611bb24d1880a3e98c4e2c1cf6496052f6d52095a3d1a0221828d930  crates/base_train/src/tensorcube_consume_plane_r2.rs
e60681910f2dbb975998e1a59e4800cd992f796fcf76bf7e13604a88d2ce032c  tools/validate_ash_tensorcube_consume_r2_gpu_parallel_plane_static.py
```

## 23. Static qualification

```text
PASS_TENSORCUBE_CONSUME_R2_GPU_PARALLEL_PLANE_STATIC checks=61
PASS_TENSORCUBE_CONSUME_R1_RELATION_AUTHORITY_STATIC checks=56
PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_GLOBAL_TENSORCUBE_JOB_QUEUE_AND_INDEPENDENT_WORK_ADMISSION_R6_STATIC
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_CF1_RAM36_CURRENT_SOURCE_PROMOTION_STATIC checks=32
PASS_EVE_MCU_R3H_CF11_R1_BOUNDED_COW_WORKSPACE_STATIC checks=22
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_BPDK_GENERATION_BINDING_STATIC checks=27
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_R8A_PREDURABILITY_SEAL_STATIC checks=30
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_MUON_PACKED_ADDRESS_STATIC checks=26
PASS_EVE_MCU_R3H_CF11_R1_CF1_PACKED_MV_DIGEST_STATIC checks=27
PYTHON_VALIDATOR_COMPILE_PASS
```

Rust toolchain is not present in the bake environment.

No Rust COMPILE, TEST, RUNTIME, PHYSICAL or PERFORMANCE PASS is claimed.

## 24. Artifacts

Overlay:

```text
ASH_TENSORCUBE_CONSUME_R2_GPU_PARALLEL_CONSUME_PLANE_OVERLAY_CODE_ONLY.zip
SHA-256 06cc3440326d76a70eade2fac5761787f20d51f049789f8b212117cd1b6d2763
FILES 8
CRC PASS
```

Full:

```text
ASH_PASS3_TENSORCUBE_CONSUME_R2_GPU_PARALLEL_CONSUME_PLANE_CODE_ONLY.zip
SHA-256 a2812495deb125a764ee7d112e1d69ad8d32a965b45b30ae82f2999cf43723cd
FILES 8444
CRC PASS
```

Both exclude:

```text
specs/
artifacts/
manifests/
Markdown
__pycache__
*.pyc
```

## 25. Compile acceptance

Required user-side:

```text
burn_webgpu_backend --lib --release
base_train --lib --release
base_train --bin base_train --release
```

Then run tests prefixed:

```text
tensorcube_consume_r2_
```

R2 source currently includes structural unit fixtures for:

```text
R1 projection -> R2 range-table construction
exact contiguous range coalescing
B06 wave/ticket coverage rejection
```

## 26. Physical acceptance

Run with:

```text
ASH_TENSORCUBE_CONSUME_R2_MODE=ACTIVE_VERIFIED
```

Expected per-parameter compact receipt:

```text
[ASH-TENSORCUBE-CONSUME-R2][gpu-plane]
mode=ActiveVerified
bulk_d2h_bytes=0
cpu_weight_tile_writes=0
cpu_momentum_tile_commits=0
b06_successor_tickets=<wave_count>
b06_successor_sealed=true
gaps=0
overlaps=0
admitted=true
```

Required absence:

```text
FAIL_B06_CANDIDATE_NOT_COMPLETE:muon-device-successor-missing
E_TENSORCUBE_CONSUME_R2_* coverage/range/ordering failures
```

The next first failure, if any, must be reported without weakening B06/R3C1 gates.

## 27. Performance boundary

This source bake changes execution topology but does not claim a speedup.

Measure before promotion:

```text
GPU compute utilization
GPU copy-engine utilization
host wait time
consume submission count
compute/consume overlap
parameter wall time
full step wall time
```

A copy-engine table path is not automatically faster than the parent contiguous fragment copy; performance must be measured physically.

## 28. Completion law

R2 closes only when:

1. R1 remains the sole relation/geometry SSOT.
2. Every active wave has an exact R1 epoch projection.
3. R2 physical ranges are derived from that projection plus the same R6 descriptor lineage.
4. W/M/update source bounds and assembly destination bounds are exact.
5. Ready ranges are submitted as a bounded GPU D2D table without per-range host wait.
6. Candidate source arenas remain live through consume completion.
7. B06 ticket claim occurs after physical consume completion.
8. Real B06 tickets are staged for every active wave.
9. The existing B06 missing-successor and submission-lineage gates remain intact.
10. Active R2 reports zero full candidate D2H and zero CPU tile successor writes.
11. Parameter assembly coverage is exact before segmented handoff.
12. BP-DK update evidence and segmented successor publication remain intact.
13. R3H/CF11/RAM36/R8A/packed-MV/BP-DK parent closures remain intact.
14. The previous `muon-device-successor-missing` blocker disappears because the physical successor path completed, not because the gate was removed.

## 29. Final law

> R1 defines the TensorCube consume relation. R2 executes a physical device-to-device projection derived from that exact relation and the same R6 descriptor lineage.

> R2 does not re-run Muon mathematics and does not add numerical transformation; it only moves already-computed candidate W/M/update into the existing parameter-level device successor authority.

> ActiveVerified consumption is nonblocking with respect to host exact waits, and B06 successor evidence is claimed only after the consume submission is physically complete.

> The first R2 implementation intentionally uses a batched WGPU copy-engine plane rather than a new scatter WGSL because the admitted physical ranges are contiguous and bit-exact. A shader is deferred until measurement or canonical strided execution requires one.

> ObserveOnly is not silently emulated. Until an independent shadow destination is materialized, ObserveOnly remains fail-closed.
