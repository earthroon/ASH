# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-GLOBAL-TENSORCUBE-JOB-QUEUE-AND-INDEPENDENT-WORK-ADMISSION-R6

## Global Job Identity / Bounded Resident Queue / Exact Independent-Work Admission / Wave Execution-Ownership Separation / R5 F32 Preservation

### 0. Revision identity

Revision: `ASH-BASETRAIN-UNIFIED-ATLAS-MCU-GLOBAL-TENSORCUBE-JOB-QUEUE-AND-INDEPENDENT-WORK-ADMISSION-R6`

Parent: `ASH-BASETRAIN-TENSORCUBE-MUON-DETERMINISTIC-SUBGROUP-NORM-REDUCTION-AND-SERIALLANE0-PRODUCTION-RETIREMENT-R5`

Runtime gates:

- `ASH_UNIFIED_ATLAS_MCU_GLOBAL_TENSORCUBE_JOB_QUEUE_R6=1`
- `ASH_UNIFIED_ATLAS_MCU_GLOBAL_TENSORCUBE_JOB_QUEUE_R6_MODE=SHADOW_QUEUE|QUEUE_WITHIN_WAVE`
- `ASH_UNIFIED_ATLAS_MCU_GLOBAL_TENSORCUBE_JOB_QUEUE_R6_QUALIFICATION_RECEIPT=<path>` for active production admission

### 1. Purpose

R6 moves Local Muon execution identity below Wave without retiring Wave. Every qualified 16x16 Local Muon TensorCube receives one immutable fixed-size job descriptor. One bounded MCU queue becomes the admission authority for those descriptors. Wave remains residency, readback, receipt, and canonical commit identity.

R6 changes scheduling representation only. It preserves R4 SoftMatrix16 F32 matrix semantics and the qualified R5 deterministic subgroup norm contract.

### 2. Parent admission

`QUEUE_WITHIN_WAVE` requires:

- qualified R4 `F32_SUBGROUP_SOFTMATRIX16`;
- qualified R5 `DETERMINISTIC_SUBGROUP32_R5`;
- observed subgroup size 32;
- F32 working dtype;
- valid R6 queue qualification receipt.

If R5 is not production-qualified, active R6 fails with `E_UNIFIED_ATLAS_MCU_R6_R5_PARENT_NOT_PRODUCTION_QUALIFIED`.

If R6 active qualification is absent, fail with `E_UNIFIED_ATLAS_MCU_R6_PRODUCTION_QUALIFICATION_REQUIRED`.

### 3. Shadow-first promotion

When R6 is enabled without explicit active mode, the default is `SHADOW_QUEUE`.

Shadow mode:

- derives the exact R6 descriptor epoch;
- validates job membership/ranges against the legacy Local Muon descriptors;
- does not use the R6 descriptors as execution input.

Active mode:

- seals the R6 epoch;
- regenerates the Local Muon execution descriptors from the sealed R6 descriptors;
- invokes the existing R5-qualified Local Muon executor with those regenerated descriptors.

This prevents a fake queue implementation that is never on the execution-input path.

### 4. Core separation

Before R6, Wave is both residency/receipt identity and the practical scheduling boundary.

After R6:

- Wave owns residency, readback, receipt, and commit membership;
- `McuTensorCubeJobDescriptorR6` owns one 16x16 execution identity;
- `McuGlobalTensorCubeJobQueueR6` owns bounded execution admission;
- GPU workgroup executes one qualified job.

### 5. Job granularity

One R6 job equals one logical 16x16 TensorCube Local Muon tile.

Current parent execution relation:

`1 job = 1 R4/R5 32-thread workgroup = 1 exact subgroup32 = 1 SoftMatrix16 Local Muon tile`.

R6 does not create full-matrix Muon.

### 6. Descriptor ABI

ABI: `ASH.UNIFIED.ATLAS.MCU.TENSORCUBE.JOB.DESCRIPTOR.F32.R5.R6`

The descriptor is `#[repr(C)]`, fixed-size, numeric/POD-like state with no `String`, `Vec`, or map/tree ownership.

It binds at least:

- queue generation and epoch;
- step and parameter generation IDs;
- source/candidate generation;
- canonical TensorCube ordinal and row/column;
- Wave ordinal;
- Atlas slot index;
- Atlas partition digest bytes;
- gradient source range;
- packed source/output offsets;
- status offset;
- valid tail rows/columns;
- qualified execution backend ID.

Queue position is not canonical job identity.

### 7. Canonical identity

Current Local Muon canonical job ordinal is the existing canonical TensorCube ordinal. Physical queue index, dispatch chunk, and GPU completion timing do not redefine it.

### 8. Current Atlas residency binding

The current Muon production callsite receives:

- exact Atlas page bytes;
- exact Atlas ring slot count;
- Wave ordinal;
- Atlas partition key digest;
- source generation;
- candidate generation.

It does **not** currently receive AW01's exact `lease_generation`.

R6 therefore must not fabricate a slot lease generation by substituting candidate generation or another unrelated counter.

Current exact R6 residency binding is:

- `atlas_slot_index = wave_ordinal % atlas_slot_count`;
- exact `atlas_partition_key_digest`;
- source generation;
- candidate generation.

The descriptor reserves `atlas_slot_lease_generation`, but current runtime writes zero and final receipts state `atlas_slot_lease_generation_available=false`.

A later revision may promote exact AW01 lease-generation binding after that authority is threaded to the Muon MCU.

### 9. Atlas geometry

R6 preserves:

- physical page = 16,777,216 bytes;
- slot count = 3;
- 16x16 F32 source tile = 1,024 bytes.

Thus:

- structural maximum complete jobs/page = 16,384;
- absolute three-slot descriptor capacity = 49,152.

These are structural bounds, not claims that all descriptors are simultaneously resident/executable.

### 10. Bounded queue

The global queue preallocates one descriptor vector to the structural maximum and reuses that backing across epochs.

No per-step unbounded descriptor accumulation and no hot-path `shrink_to_fit` are admitted.

### 11. Queue generation and epoch

Every sealed Wave epoch receives a monotonically increasing queue generation and epoch ID. Reusing descriptor backing under a later generation must not permit a stale seal to access the new descriptors.

Stale queue execution fails with `E_UNIFIED_ATLAS_MCU_STALE_TENSORCUBE_JOB_QUEUE_GENERATION_R6`.

### 12. Immutable epoch

After an epoch is sealed, its semantic descriptor state is immutable until completion/abort. Source/output offsets, backend identity, parameter identity, and Atlas binding may not be rewritten mid-execution.

### 13. Job independence

R6 active admission is permitted only for Local Muon jobs whose mutable output ranges are disjoint.

The current Local Muon parent already requires:

- `full_matrix_muon=false`;
- `cross_cube_orthogonalization=false`;
- `global_orthogonality_claim=false`.

The R6 descriptor assigns disjoint packed output bases to candidate weight, candidate momentum, orthogonal update, and status ownership.

Duplicate TensorCube identity fails with `E_UNIFIED_ATLAS_MCU_DUPLICATE_TENSORCUBE_JOB_R6`.

Mutable range alias fails with `E_UNIFIED_ATLAS_MCU_TENSORCUBE_JOB_MUTABLE_RANGE_ALIAS_R6`.

### 14. O(N) structural proof

R6 does not retain O(N^2) pairwise independence evidence. Canonical tile uniqueness plus injective fixed-size output-offset mapping provides the normal O(N) admission proof.

### 15. Wave bound

A Local Muon Wave may not exceed 16,384 F32 16x16 source tiles under the current 16 MiB page authority.

Violation fails with `E_UNIFIED_ATLAS_MCU_WAVE_TENSORCUBE_JOB_BOUND_VIOLATION_R6`.

The absolute reusable queue capacity remains 49,152.

### 16. Active admission scope

Initial active scope is exactly `WITHIN_WAVE`.

R6 does not promote `MULTI_WAVE_SAME_PARAMETER` or `CROSS_PARAMETER` scheduling merely because the descriptor ABI contains parameter/Wave identity.

This deliberately keeps existing per-Wave wait/readback semantics unchanged.

### 17. Fused-pair exclusion

R5 did not qualify the fused-pair Muon backend under the deterministic R5 norm contract. Therefore R6 does not admit fused-pair jobs.

If fused-pair execution is reached while R6 is enabled, fail with `E_UNIFIED_ATLAS_MCU_R6_FUSED_PAIR_JOB_UNQUALIFIED`.

### 18. Execution backend

R6 has exactly one active execution backend:

`R5_F32_SOFTMATRIX16_SUBGROUP32`.

The descriptor carries an execution backend ID for future ABI compatibility, but R6 does not make expert-routing decisions.

### 19. No numerical change

Relative to qualified R5:

- `precision_contract_changed=false`;
- `reduction_order_changed=false`;
- `numerical_behavior_changed=false`.

R6 does not alter matrix arithmetic or norm arithmetic.

### 20. Active output parity requirement

Promotion from shadow to active requires a qualification receipt proving R6 queued execution is bit-identical to R5 parent execution for candidate weight, candidate momentum, orthogonal update, and status on a bounded deterministic fixture/sample plan.

The active production path will not open without this receipt.

### 21. Qualification receipt

The R6 qualification receipt binds:

- R6 patch and descriptor ABI;
- shadow membership parity PASS;
- active output bit parity PASS;
- stale-generation fixture PASS;
- mutable-alias fixture PASS;
- nonzero fixture count;
- zero divergence count;
- canonical receipt digest.

### 22. No work stealing

R6 does not introduce persistent kernels, atomic job heads, dynamic job stealing, or nondeterministic descriptor claim order.

Those are separate scheduling revisions.

### 23. No indirect dispatch requirement

R6 does not require GPU indirect dispatch. The current Local Muon executor retains its qualified direct-dispatch behavior after R6 descriptor-to-execution translation.

`indirect_dispatch_enabled=false`.

### 24. No mixed precision / router

Required:

- `mixed_precision_enabled=false`;
- `path_integral_router_enabled=false`;
- one execution backend only.

R7+ may add expert ABIs to the reserved backend field.

### 25. Wave completion

An R6 Wave epoch completes only when executor output reports exactly the admitted logical tile count and zero omission, duplicate execution, or writable-alias telemetry.

Required witness:

`[ASH-UNIFIED-ATLAS-MCU-WAVE-JOB-COMPLETION-R6]`.

### 26. Admission witness

Required aggregate witness:

`[ASH-UNIFIED-ATLAS-MCU-TENSORCUBE-JOB-ADMISSION-R6]`.

It includes queue generation/epoch, parameter generation, Wave ordinal, job count, Atlas slot, lease-generation availability, duplicate/alias/shadow mismatch counts, manifest digest, mode, and verdict.

No one-line-per-job production logging is introduced.

### 27. Queue manifest digest

The manifest digest is over explicit descriptor semantic fields in canonical descriptor order. It excludes timestamps, queue memory address, host scheduling, and GPU completion timing.

### 28. Descriptor retirement

After successful epoch completion, logical descriptor length resets and the preallocated backing remains reusable. Completed descriptors are not appended to StepTransient historical evidence.

### 29. Parent lifetime preservation

Required:

- R2-B parameter lifetime closure preserved;
- R2-C step compact-state closure preserved;
- R3 compressed instrumentation preserved;
- R4 SoftMatrix ABI preserved;
- R5 deterministic norm preserved.

The R6 queue is bounded execution-transient state, not a new unbounded StepTransient evidence ledger.

### 30. Readback/wait preservation

R6 keeps the current Wave-level candidate/momentum/update/status readback and exact waits.

Required: `per_wave_exact_wait_retired=false`.

R6 does not claim B05/B06 active authority or D2H retirement.

### 31. Static validation

Static validation must prove:

- fixed descriptor ABI exists;
- descriptor contains no dynamic collections/Strings;
- structural 16,384/49,152 bounds exist;
- queue backing is bounded/reused;
- queue generation exists;
- canonical job identity is independent of queue index;
- duplicate and mutable-alias failures exist;
- Atlas lease generation is explicitly unavailable rather than fabricated;
- R5 parent and R6 qualification gates exist;
- actual active execution descriptors are derived from the sealed R6 descriptor set;
- fused pairs fail closed;
- work stealing, indirect dispatch, mixed precision, Path-Integral routing, D2H/wait retirement remain off;
- R4/R5 numerical contracts remain unchanged.

### 32. Unit tests

At minimum:

- queue capacity equals 49,152;
- jobs/page equals 16,384;
- stale queue generation rejected;
- duplicate TensorCube rejected;
- mutable output alias rejected;
- descriptor remains fixed-size numeric state;
- epoch reuse does not preserve old logical membership.

### 33. Physical qualification sequence

`R6 static -> R5/R4/R3/R2 parent regressions -> cargo check -> focused Rust tests -> queue shadow parity -> stale/alias fixtures -> active R6-vs-R5 bit parity -> qualification receipt -> release build -> fresh Native CF1 -> fresh cross-release authority -> immutable Physical N2 -> Exact N8`.

Unobserved stages must not be reported as PASS.

### 34. Final runtime receipt

Required runtime receipt:

`[ASH-BASETRAIN-UNIFIED-ATLAS-MCU-GLOBAL-TENSORCUBE-JOB-QUEUE-AND-INDEPENDENT-WORK-ADMISSION-R6]`

Minimum state includes:

- descriptor ABI;
- mode;
- qualification state;
- queue capacity = 49,152;
- page bytes = 16 MiB;
- slots = 3;
- jobs/page = 16,384;
- generation/epoch counts;
- queue high water;
- admitted/completed counts;
- duplicate/alias/stale/shadow/output divergence counts;
- `atlas_slot_lease_generation_available=false` for the current source route;
- selected backend = R5 F32 SoftMatrix16 subgroup32;
- active scope = WITHIN_WAVE;
- work stealing / indirect dispatch / mixed precision / Path-Integral routing = false;
- fused-pair execution claim = false;
- per-Wave exact wait retired = false;
- no numerical-contract change.

### 35. PASS semantics

R6 may emit `PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_GLOBAL_TENSORCUBE_JOB_QUEUE_AND_INDEPENDENT_WORK_ADMISSION_R6` only when:

- mode is `QUEUE_WITHIN_WAVE`;
- R5 is production-qualified;
- R6 qualification receipt is valid;
- at least one job executed;
- admitted count equals completed count;
- duplicate/alias/shadow/output divergence counts are zero.

Shadow-only runs are not production PASS.

### 36. Explicit non-goals

R6 does not:

- remove Wave identity;
- enable multi-Wave or cross-parameter active scheduling;
- introduce dynamic work stealing;
- use indirect dispatch as an authority;
- add F16/BF16/mixed precision;
- connect Path-Integral Synapse routing;
- execute fused-pair jobs;
- promote B05/B06 active authority;
- retire bulk D2H or per-Wave waits;
- activate ActiveAsync;
- change 16 MiB/3-slot Atlas geometry;
- mutate Physical N2 or RAM36 authority.

### 37. Handoff

After qualified R6, the stable job descriptor may support multiple execution backends without changing job identity.

Recommended next revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-MIXED-PRECISION-EXECUTION-EXPERT-ABI-R7`

R7 should define and qualify expert numerical contracts only. Deterministic routing and Path-Integral policy compilation remain a later revision.

### 38. Center sentence

**R6 does not destroy Wave. It gives every 16x16 Local Muon operation a fixed execution identity and makes one bounded MCU queue the admission authority. The first active scope stays inside one Wave, so queue adoption can be proven without quietly changing readback, wait, commit, precision, or numerical semantics. Where the current source does not expose AW01 slot lease generation, R6 says that it is unavailable instead of inventing one.**
