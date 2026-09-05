# ASH-MCU-SOFT-TENSOR-MATRIX-R1

## VARIABLE-TENSOR RESIDENCY + HIMUON-STYLE SEGMENT / GENERATION / DIRTY + ATLAS WAVE PASS-THROUGH

### 0. Revision

```text
Patch ID: ASH-MCU-SOFT-TENSOR-MATRIX-R1
Class: PHYSICAL RESIDENCY AUTHORITY CUTOVER
Direct source parent: ASH_PASS3_EVE_MCU_CLOSE_PHYS_R1C_ATLAS_STREAMING_COMPILEFIX_CODE_ONLY.zip
Parent SHA-256: a9bf9c6664c51fa83934440414e9a9a3ee7fd5e8b892657765e9b41d1a821d27
Source release: STATIC SOURCE MATERIALIZATION / UNCOMPILED IN BAKE ENVIRONMENT
Physical qualification: HOLD
```

Reserved tokens:

```text
PASS_ASH_MCU_SOFT_TENSOR_MATRIX_R1_STATIC
PASS_ASH_MCU_SOFT_TENSOR_MATRIX_R1_NATIVE
PASS_ASH_MCU_SOFT_TENSOR_MATRIX_R1_WGPU
HOLD_ASH_MCU_SOFT_TENSOR_MATRIX_R1_PHYSICAL_PENDING
```

Static source materialization does not issue the native or WGPU tokens.

### 1. Goal

R7A actual-object cache authority is replaced in the active Soft Matrix route by a logical variable-tensor residency authority.

```text
actual-object cache authority
    -> Soft Tensor Matrix coordinate/generation authority
    -> Atlas metadata grouping
    -> wave-ordered pass-through
    -> existing typed WGPU owner
```

The matrix does not serialize Device, Queue, Pipeline, BindGroup, Buffer, producer, packer, or executor objects.

### 2. Authority split

```text
CPU canonical optimizer state
    existing RamResidentAdamMv / HiMuon momentum authority

Soft Tensor Matrix
    topology + segment + generation + dirty + residency relation

Typed runtime owner
    actual WGPU producer / packer / executor

Pass-through
    temporary execution authority by matrix identity + lane + generation
```

Soft Matrix does not become Adam or HiMuon mathematical authority and does not become R3C/R3C1 semantic commit authority.

### 3. Variable tensor ABI

Active/reseved tensor families:

```text
Weight
AdamM
AdamV
HiMuonMomentum
PackedGradient
FastMemoryReserved
```

Each logical cell binds an immutable segment topology to mutable state:

```text
immutable:
  family / parameter identity / segment geometry / shape / dtype

mutable:
  committed generation / candidate generation / dirty state / residency / phase
```

Adam M/V actual `AdamRangeR1` admissions are projected into `AdamM` and `AdamV` Soft Matrix cells while canonical bytes remain owned by the CPU RAM Adam body.

HiMuon segmented momentum remains owned by the existing R8/R8A authority. R1 adopts its segment/generation/dirty grammar but does not copy or replace momentum storage.

### 4. Matrix state machine

```text
Canonical
Materializing
Resident
CandidateDirty
CommitPrepared
Retiring
```

Generation mismatch is fail-closed. Stale pass-through does not silently rebuild a resource.

### 5. Execution lanes

Actual WGPU execution is represented by typed logical lanes:

```text
AdamW
HiMuonGradientPack
HiMuonBatch
```

A session stores the actual typed object in its existing field and stores only matrix/pass-through metadata as execution authority.

### 6. Atlas planning

Parallel work is limited to metadata:

```text
coordinate
family
generation
dirty/dependency metadata
execution intent
```

`McuSoftTensorAtlasPlannerR1` canonicalizes requests, groups them into bounded deterministic waves, builds wave metadata in parallel, sorts by wave/family/segment/generation, then returns ordered wave plans.

Actual WGPU objects are not captured by Atlas planner threads.

### 7. Sequential WGPU pass-through

Resource realization/execution admission is wave ordered:

```text
Wave N
  -> resolve matrix/pass-through metadata
  -> borrow existing typed WGPU owner
  -> execute
  -> end borrow
  -> Wave N+1
```

This does not remove GPU kernel/workgroup parallelism. Only resource-authority realization is sequentially ordered.

### 8. R7A actual-object cache cutover

The old global/static R7A cache no longer stores actual WGPU producers/packers/bundles.

Global state is reduced to metadata-only observation:

```text
McuKernelCacheKeyR7A -> lightweight observation count / telemetry
```

The following graph is retired from static ownership:

```text
OnceLock<Mutex<... Arc<WGPU object> ...>>
```

Compatibility `cached_*` functions remain callable for legacy paths but do not own actual WGPU objects globally. Soft Matrix production mode bypasses them for AdamW/HiMuon execution and uses the existing session typed fields.

### 9. Single authority law

New config:

```text
admit_mcu_soft_tensor_matrix_r1: bool = false
```

Soft Matrix requires the persistent MCU R7 parent.

The following combination is rejected:

```text
admit_mcu_soft_tensor_matrix_r1 = true
admit_mcu_device_kernel_cache_r7a = true
```

with:

```text
E_SOFT_MATRIX_DUAL_CACHE_AUTHORITY_FORBIDDEN
```

This prevents legacy actual-cache authority and Soft Matrix authority from both admitting execution.

### 10. Adam lane

AdamW resource acquisition in Soft Matrix mode:

```text
Adam kernel ABI key
  -> SoftTensorExecutionLaneR1::AdamW
  -> pass-through generation
  -> existing session-persistent McuAdamWExecutorR7 producer
```

Same-session reuse requires the same lane generation. The CPU RAM Adam M/V body remains canonical state.

### 11. HiMuon lanes

HiMuon batch and gradient-pack production routes no longer require the old cached constructors when Soft Matrix mode is active.

```text
HiMuonGradientPack lane -> existing session gradient_packer field
HiMuonBatch lane        -> existing session batch_executor field
```

HiMuon mathematics, R8/R8A momentum storage, R7A1 packed-gradient lease/reclaim semantics remain unchanged.

### 12. ABA / stale protection

Pass-through includes:

```text
matrix identity
execution lane
expected lane generation
wave ordinal
```

If the lane generation changes, an old pass-through is rejected with `E_SOFT_MATRIX_PASS_THROUGH_STALE`.

### 13. Dirty/generation semantics

The common ABI supports:

```text
Clean
Dirty { generation }

committed G
candidate G+1
external commit permit
committed G+1
```

R1 materializes this ABI and projects Adam M/V ranges. It does not move semantic commit authority into the matrix. HiMuon existing dirty-page implementation remains the actual momentum dirty-state authority.

### 14. Compile-surface law

No recursion-limit increase is permitted as a solution.

Global/static and Atlas-parallel surfaces may contain only lightweight metadata structures. They must not own/capture actual WGPU Device/Queue/Pipeline/BindGroup/producer graphs.

The intended fix for the observed `validation::NumericDimension: Sync` trait-solver overflow is ownership-graph reduction, not a larger recursion limit.

### 15. Failure semantics

Minimum fail-closed errors:

```text
E_SOFT_MATRIX_COORD_NOT_FOUND
E_SOFT_MATRIX_GENERATION_DRIFT
E_SOFT_MATRIX_TOPOLOGY_DRIFT
E_SOFT_MATRIX_PASS_THROUGH_STALE
E_SOFT_MATRIX_RESIDENCY_NOT_READY
E_SOFT_MATRIX_WAVE_CONFLICT
E_SOFT_MATRIX_WAVE_BUDGET_EXCEEDED
E_SOFT_MATRIX_DIRTY_GENERATION_DRIFT
E_SOFT_MATRIX_COMMIT_WITHOUT_PERMIT
E_SOFT_MATRIX_RUNTIME_OWNER_DRIFT
E_SOFT_MATRIX_DUAL_CACHE_AUTHORITY_FORBIDDEN
```

### 16. Non-claims

R1 does not claim:

```text
MIRASASH fast memory active
DeltaK write/retention policy active
HiMuon optimizer applied to Adam
WGPU object serialization
multi-device execution
runtime performance improvement
process-restart GPU residency
```

### 17. Physical qualification

Native/WGPU promotion requires at minimum:

```text
base_train lib compile PASS
burn_webgpu_backend lib compile PASS
base_train lib tests PASS
burn_webgpu_backend lib tests PASS
no NumericDimension: Sync recursion overflow
8-step production PASS
4+4 same-session PASS
2+2+4 checkpoint PASS
Adam hydration = 1
runtime reconstruction = 0
successor source reload = 0
matrix identity stable
pass-through generation exact
numerical parity PASS
```

Until actually executed, physical state remains HOLD.

### 18. Direct successor

After WGPU stabilization:

```text
ASH-MIRASASH-MEMORY-R1
FAST-MEMORY TENSOR
+ DELTA-RULE BASELINE
+ SOFT-TENSOR-MATRIX RESIDENCY ADOPTION
```

Then ΔK write/retention policy can be layered without creating a second tensor residency runtime.

## Appendix A. Actual source bake record

```text
Artifact:
ASH_PASS3_MCU_SOFT_TENSOR_MATRIX_R1_STATIC_SOURCE_BAKE_CODE_ONLY.zip

SHA-256:
7d8b551c04f4fa6922a2a082f533a4ca770a16174d83959b2f67907e98cbbd2c

Files: 8,413
Bytes: 21,466,411
CRC: PASS
Duplicate paths: 0
PowerShell files: 0
specs/artifacts/manifests/reports directories in code ZIP: 0
```

Delta from direct parent:

```text
ADD 3
MOD 10
DEL 0
```

Added:

```text
crates/base_train/src/mcu_soft_tensor_matrix_r1.rs
crates/base_train/src/mcu_soft_tensor_atlas_r1.rs
crates/base_train/src/mcu_soft_tensor_pass_through_r1.rs
```

Modified:

```text
crates/base_train/src/config.rs
crates/base_train/src/eve_mcu_close_physical_qualification_r1.rs
crates/base_train/src/lib.rs
crates/base_train/src/mcu_device_resource_runtime_r7a.rs
crates/base_train/src/mcu_session_runtime_r7.rs
crates/base_train/src/pipeline.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/burn_webgpu_backend/src/mcu_device_kernel_cache_r7a.rs
tools/validate_ash_mcu_device_lifetime_kernel_cache_bounded_buffer_arena_r7a_static.py
```

No new Python or PowerShell loader was added. One existing static validator was updated to inspect the new ownership boundary.

## Appendix B. Static validation actually executed

```text
Soft Matrix source contract: 26 / 26 PASS
R7A static: 83 / 83 PASS
R7 static: 55 / 55 PASS
R7B static: 83 / 83 PASS
R7A1 static: 82 / 82 PASS
Eve R3G static: 35 / 35 PASS
R3C1 static: 30 / 30 PASS
```

Bake environment does not expose Cargo/Rustc, so compile, borrow checking, link, WGPU execution, and performance are NOT RUN / 판단불가.

## Appendix C. Explicit implementation boundary

This bake materially changes ownership:

```text
legacy global actual-object cache
    -> metadata-only global observation

actual WGPU producer/packer/executor
    -> existing typed session owner

production authority in active R1 mode
    -> Soft Matrix identity + lane generation + pass-through
```

HiMuon segmented momentum storage is not moved. Adam M/V canonical bytes are not moved. The commonized layer is residency/generation/dirty/pass-through semantics.
