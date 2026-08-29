# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-GPU-RESIDENT-EXPERT-BUCKET-VIEW-AND-HETEROGENEOUS-DISPATCH-R8A

## Zero-Payload-Repack Descriptor Indirection / Stable E0-E1-E2 Buckets / Multi-Pipeline Wave Dispatch / Exact Coverage / R8 Heterogeneous Materialization Closure

### 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-GPU-RESIDENT-EXPERT-BUCKET-VIEW-AND-HETEROGENEOUS-DISPATCH-R8A`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-DETERMINISTIC-PRECISION-EXPERT-ROUTER-AND-PATH-INTEGRAL-POLICY-COMPILER-R8`

Runtime gates:

- `ASH_UNIFIED_ATLAS_MCU_GPU_RESIDENT_EXPERT_BUCKET_R8A=1`
- `ASH_UNIFIED_ATLAS_MCU_GPU_RESIDENT_EXPERT_BUCKET_R8A_MODE=SHADOW_BUCKET_VIEW|ACTIVE_HETEROGENEOUS_DISPATCH`
- `ASH_UNIFIED_ATLAS_MCU_GPU_RESIDENT_EXPERT_BUCKET_R8A_QUALIFICATION_RECEIPT=<path>` for Active

### 1. Purpose

R8 can already produce an immutable per-job expert assignment, but the R8 parent intentionally refuses physically heterogeneous `{E0,E1,E2}` execution because the current resident Local Muon Wave owns one compact source/momentum payload. Naively splitting that payload on the host would regress the source-packing and host-scratch retirement contracts.

R8A materializes the R8 assignment without copying TensorCube numerical payload. It creates one bounded stable partition of `u32` execution-descriptor indices and lets the qualified E0/E1/E2 pipelines dereference the original descriptor array and original resident buffers.

### 2. Core invariant

`Expert Bucket = View of canonical jobs`.

`Expert Bucket != Copy of canonical payload`.

Production R8A requires:

- `source_payload_repack_bytes=0`
- `momentum_payload_repack_bytes=0`
- `candidate_payload_repack_bytes=0`
- `additional_bucket_payload_d2h_bytes=0`

### 3. Parent authority chain

- R6 owns canonical job identity, descriptor ranges, Atlas binding, independent-write proof.
- R7 owns E0/E1/E2 numerical contracts and qualification.
- R8 owns deterministic expert assignment.
- R8A owns physical descriptor-index grouping and indexed multi-pipeline dispatch.
- Wave remains readback, receipt, and commit membership authority.

R8A does not create a second job identity or router.

### 4. Parent admission

R8A may be enabled only when R8 is enabled. Active R8A additionally requires:

- R8 `ACTIVE_DETERMINISTIC_ROUTER`;
- valid R8 policy qualification;
- valid R8A qualification receipt matching the current R8 policy digest;
- current R7 expert manifest matching the receipt;
- every nonempty low-precision bucket ProductionQualified in R7.

Required errors include:

- `E_MCU_R8A_R8_PARENT_REQUIRED`
- `E_MCU_R8A_R8_ACTIVE_PARENT_REQUIRED`
- `E_MCU_R8A_PRODUCTION_QUALIFICATION_REQUIRED`
- `E_MCU_R8A_QUALIFICATION_POLICY_DIGEST_MISMATCH`
- `E_MCU_R8A_QUALIFICATION_EXPERT_MANIFEST_MISMATCH`

### 5. R8 failure preservation

R8 keeps `E_MCU_R8_HETEROGENEOUS_EXECUTION_NOT_MATERIALIZED` as its standalone behavior.

Only a ProductionQualified R8A child may call the R8 child routing API that permits a heterogeneous manifest to proceed to materialization.

No R8A means no bypass.

### 6. Active scope

R8A preserves R6's `WITHIN_WAVE` production scope. It does not enable multi-Wave or cross-parameter execution.

### 7. Structural bounds

Existing authority:

- F32 16x16 source tile = 1,024 bytes;
- Atlas page = 16 MiB;
- maximum complete jobs per Wave/page = 16,384.

R8A index width is exactly `u32` = 4 bytes.

Maximum packed index payload:

`16,384 * 4 = 65,536 bytes`.

This 64 KiB control view is not TensorCube payload materialization.

### 8. Bucket ABI

ABI:

`ASH.MCU.GPU-RESIDENT-EXPERT-BUCKET-VIEW.R8A.V1`

`McuGpuResidentExpertBucketViewR8A` binds:

- R6 queue generation/epoch;
- R6 descriptor manifest digest;
- R7 expert manifest digest;
- R8 policy digest;
- R8 assignment manifest digest;
- R8A view generation;
- E0/E1/E2 spans;
- packed descriptor indices;
- exact view digest.

### 9. Stable partition

Input ordering is canonical R6 descriptor ordering.

Output bucket order is fixed:

`E0 -> E1 -> E2`.

Within each expert bucket, descriptor indices remain in canonical job ordinal order.

Hash-map iteration order, thread completion order, or GPU execution order may not influence bucket layout.

### 10. Materialization algorithm

R8A uses bounded deterministic partitioning. A simple two/three-pass O(N) implementation is valid:

1. count assignments;
2. derive exact E0/E1/E2 bases;
3. scan canonical assignments and append only each descriptor index to its fixed expert span.

No per-expert TensorCube payload vectors are built.

### 11. Exact coverage

Every admitted descriptor must appear exactly once in the packed index view.

Required failures:

- `E_MCU_R8A_BUCKET_DUPLICATE_JOB`
- `E_MCU_R8A_BUCKET_MISSING_JOB`
- `E_MCU_R8A_DESCRIPTOR_INDEX_OUT_OF_RANGE`
- `E_MCU_R8A_BUCKET_EXPERT_MISMATCH`
- `E_MCU_R8A_UNQUALIFIED_EXPERT_BUCKET`

Passing coverage requires expected jobs = bucketed jobs and every divergence counter = 0.

### 12. R6 descriptor adoption

In Active R8A, R8 expert IDs are written into the existing R6 descriptor array job-by-job before the R8A view is sealed. R6 recomputes the descriptor manifest digest.

The R6 canonical job identity, source offsets, gradient ranges, candidate ranges, status ranges, Wave membership, and Atlas binding do not change.

Heterogeneous R6 seal summary uses no fabricated single expert authority. The child R8A execution path reads descriptors through a child-safe R6 descriptor conversion API.

### 13. Shadow isolation

`SHADOW_BUCKET_VIEW` computes the stable bucket view and coverage digest but does not mutate R6 descriptor expert IDs and does not execute indexed child pipelines.

Canonical execution remains the parent path.

### 14. Active execution plan

`ACTIVE_HETEROGENEOUS_DISPATCH` converts the sealed view to one compact backend execution plan:

- one packed `Vec<u32>` control index list;
- E0/E1/E2 counts;
- bucket view digest.

No source, momentum, candidate, or update values are copied into that plan.

### 15. GPU control buffers

The backend uploads:

1. one packed read-only descriptor-index buffer;
2. one fixed 32-byte E0/E1/E2 bucket directory.

Both are control data.

The numerical payload remains in the same buffers already owned by the Local Muon resident Wave.

### 16. Indexed shader ABI

R8A adds indexed child variants of the exact R7-qualified arithmetic shaders:

- E0: R5 F32 SoftMatrix + deterministic norm, indexed descriptor view;
- E1: R7 mixed F16/F32, indexed descriptor view;
- E2: R7 F16 SoftMatrix, indexed descriptor view.

New bindings:

- binding 9: packed descriptor indices;
- binding 10: fixed expert bucket directory.

Each shader hard-binds its expert identity and retrieves:

`bucket-local workgroup -> packed descriptor index -> canonical execution descriptor -> original resident payload/output ranges`.

### 17. No numerical rewrite

R8A indexed shader variants may change only descriptor lookup. The arithmetic body remains inherited from the exact R7 expert.

R8A itself has:

- `precision_contract_changed=false` relative to each selected R7 expert;
- `numerical_behavior_changed=false` relative to each selected R7 expert.

### 18. One descriptor array SSOT

R8A does not copy full GPU descriptor structs once per expert. One canonical execution descriptor array remains authoritative. Buckets store only indices into that array.

### 19. Canonical output ABI

All R7 experts already write canonical F32:

- candidate weight;
- candidate momentum;
- orthogonal update;
- common status ABI.

R8A expert pipelines write directly to the descriptor-defined canonical offsets. No expert-specific candidate buffer and no output merge kernel is introduced.

### 20. Mutable-range independence

R6's exact disjoint mutable-range proof remains authoritative. R8A only changes physical dispatch grouping, therefore expert buckets may share backing buffers only through already-proven disjoint ranges.

### 21. Dispatch topology

For one active Wave, R8A uses one command encoder and one shared indexed bind group. It emits exactly one direct dispatch for each nonempty expert bucket, in canonical order E0, E1, E2.

With the initial expert set:

`expert_dispatch_count = nonempty_expert_bucket_count`, therefore 1..3 dispatches per Wave.

Empty buckets emit no dummy dispatch.

### 22. Current single-physical-batch requirement

The R8A indexed path currently requires the full active Wave to fit the existing Local Muon physical batch capacity. This is consistent with the present 16 MiB Wave bound on the target substrate and preserves one packed descriptor array / one index view / one submit.

If device limits force the Wave into more than one Local Muon physical batch, R8A fails with:

`E_MCU_R8A_ONE_WAVE_BATCH_CAPACITY_REQUIRED`.

R8A does not silently create per-batch expert payload repacks.

### 23. Queue submission and waits

The current indexed Wave path records all nonempty expert dispatches into the same command encoder and submits once for that physical Wave batch.

R8A does not add per-expert waits or per-expert readbacks.

Existing Wave exact-wait authority remains, so:

`per_wave_exact_wait_retired=false`.

### 24. No payload repack

Forbidden production patterns include:

- `e0_source_wave_slab`, `e1_source_wave_slab`, `e2_source_wave_slab`;
- expert-specific momentum slabs;
- gathering selected TensorCube values into expert-specific GPU payload buffers;
- separate expert candidate output buffers followed by merge.

### 25. Control upload telemetry

R8A reports:

- bucket index H2D bytes;
- expert dispatch count;
- queue submit count;
- source/momentum/candidate repack bytes;
- additional bucket D2H bytes.

The repack/D2H fields must be zero for production PASS.

### 26. Qualification parity target

R8A is not compared universally against E0 bits.

Correct parity is:

`R8A indexed job under expert Ex == direct qualified R7 job under the same expert Ex`.

E1/E2 are allowed to differ from E0 according to their existing R7 numerical contracts.

### 27. First divergence witness

Physical qualification failure must identify:

- queue generation/epoch;
- view generation;
- selected expert;
- bucket-local index;
- execution descriptor index;
- canonical job/TensorCube ordinal;
- output class and logical element;
- direct-reference bits;
- indexed-execution bits;
- R6/R8/R8A digests.

A generic heterogeneous parity error is insufficient.

### 28. No routing rewrite

R8A may not reassign a job because an expert bucket is small or inconvenient.

A single-job E2 bucket is still E2. Small-bucket coalescing into E0 is a routing-policy mutation and is forbidden.

### 29. No automatic fallback

R8A does not implement `E2 -> E1 -> E0` retry. A failed selected expert remains a visible failed attempt.

`automatic_precision_escalation_enabled=false`.

Retry/attempt identity belongs to R9.

### 30. No work stealing / indirect requirement

R8A v1 uses sealed direct bucket dispatches. It does not introduce persistent worker kernels, atomic job claiming, work stealing, or require indirect dispatch.

### 31. Lifetime authority

Host/GPU index-buffer capacity may be reusable, but logical bucket membership is `WaveExecutionTransient`.

No detailed bucket history accumulates as StepTransient state.

Required:

- parameter lifetime closure preserved;
- step compact-state closure preserved;
- R3 compressed instrumentation preserved.

### 32. ActiveAsync remains off

The current one-view backing is safe because Wave lifetimes are not overlapped. R8A does not enable ActiveAsync.

A future async revision must introduce exact view-buffer lease/ring semantics before overlapping Wave generations.

### 33. Parent authority preservation

R8A preserves:

- R4 SoftMatrix ABI/mapping;
- R5 deterministic F32 norm;
- R6 queue identity/ranges/Atlas geometry;
- R7 expert arithmetic/qualification;
- R8 routing policy/assignment;
- 16 MiB / 3-slot Atlas geometry;
- RAM36 authority;
- Physical N2 immutability;
- current readback/commit authority.

The historical 1,044,033,536-byte allocation owner remains unclaimed.

### 34. Atlas lease limitation

R8A does not invent the AW01 exact slot lease generation still unavailable in the current Muon route.

`atlas_slot_lease_generation_available=false` remains honest.

### 35. Static validation

R8A static validation proves at least:

- R8A module/export and env gates;
- 16,384 Wave job bound;
- u32 index width and 65,536-byte maximum index payload;
- stable E0/E1/E2 partition;
- exact coverage/duplicate/out-of-range gates;
- R6 per-job expert adoption child API;
- R8 child delegation while standalone R8 fail remains present;
- binding 9 descriptor-index view and binding 10 bucket directory in all indexed shaders;
- E0/E1/E2 indexed pipeline materialization;
- one canonical descriptor array;
- no source/momentum/candidate expert payload repack;
- no automatic escalation/work stealing/ActiveAsync;
- parent validators remain passing.

### 36. Source/unit tests

Required source tests cover:

- 64 KiB maximum index payload;
- stable bucket base ordering;
- deterministic view digest;
- exact-once membership;
- duplicate/missing/out-of-range rejection;
- unqualified expert rejection;
- stale queue/assignment rejection;
- empty bucket skip;
- single-job bucket preservation;
- canonical job identity preservation.

### 37. Physical qualification fixtures

At minimum:

- E0/E1 alternating assignment;
- E1/E2 alternating if E2 qualified;
- E0/E1/E2 round-robin if all qualified;
- 16,383 safe jobs + one aggressive job;
- empty middle expert bucket;
- full-tile low precision plus E0 tail tile;
- direct-vs-indexed parity per expert;
- exact index upload/coverage witness;
- zero payload-repack witness.

### 38. Qualification receipt

`McuGpuResidentExpertBucketQualificationReceiptR8A` binds:

- patch/bucket ABI;
- R7 expert manifest digest;
- R8 policy digest;
- qualified and physically executed expert masks;
- nonzero fixture and heterogeneous fixture counts;
- indexed parity divergence count = 0;
- coverage divergence counts = 0;
- source/momentum/candidate repack bytes = 0;
- additional bucket D2H bytes = 0;
- maximum control-index upload;
- maximum nonempty bucket count >= 2;
- `heterogeneous_active_execution_materialized=true`;
- exact receipt digest and PASS verdict.

### 39. Production PASS semantics

R8A production PASS requires actual physical execution of at least one Wave with at least two nonempty expert buckets.

A Shadow view or homogeneous-only physical run is not sufficient.

If only E0/E1 are R7-qualified, a physically closed two-expert heterogeneous fixture is sufficient for R8A base PASS. R8A must not claim E2 physical closure when E2 was not executed.

### 40. Runtime witnesses

Required aggregate view witness:

`[ASH-UNIFIED-ATLAS-MCU-GPU-RESIDENT-EXPERT-BUCKET-VIEW-R8A]`

Required physical dispatch witness:

`[ASH-UNIFIED-ATLAS-MCU-HETEROGENEOUS-EXPERT-DISPATCH-R8A]`

Required final receipt:

`[ASH-BASETRAIN-UNIFIED-ATLAS-MCU-GPU-RESIDENT-EXPERT-BUCKET-VIEW-AND-HETEROGENEOUS-DISPATCH-R8A]`.

### 41. Final receipt minimum fields

- patch/bucket ABI;
- mode;
- maximum jobs per Wave = 16,384;
- index width = 4;
- maximum index payload = 65,536;
- total materialized Waves;
- assignment-heterogeneous Waves;
- physically heterogeneous Waves;
- E0/E1/E2 job totals;
- maximum nonempty bucket count;
- exact coverage divergence counts = 0;
- indexed execution divergence count = 0;
- payload repack bytes = 0;
- additional bucket D2H = 0;
- control index H2D bytes;
- expert dispatch count;
- queue submit count;
- automatic escalation/work stealing/ActiveAsync = false;
- heterogeneous Active materialized according to physical qualification;
- canonical job/output identity preserved.

### 42. PASS token

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_GPU_RESIDENT_EXPERT_BUCKET_VIEW_AND_HETEROGENEOUS_DISPATCH_R8A`

Only ProductionQualified Active R8A with observed physical heterogeneous execution may emit it.

### 43. Explicit non-goals

R8A does not:

- change the R8 router;
- create/modify experts;
- repack numerical payload by expert;
- create expert-specific candidate buffers;
- reroute small buckets;
- retry failed low-precision jobs;
- perform work stealing;
- require indirect dispatch;
- enable ActiveAsync;
- expand R6 beyond one Wave;
- retire Wave readback/waits;
- promote commit authority;
- change Atlas geometry, RAM36, or Physical N2.

### 44. Handoff to R9

After R8A, a failed low-precision job can be represented by its existing R6 descriptor index without moving source/momentum payload.

Recommended next revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-GPU-PRECISION-ESCALATION-AND-SAFE-EXPERT-REQUEUE-R9`

R9 should introduce execution-attempt identity and bounded `E2 -> E1 -> E0` retry views using the same R8A index substrate.

### 45. Authority declaration

Before R8A, R8 can say exactly which expert every job should use but a mixed assignment cannot be executed without violating the resident Wave payload architecture.

After R8A, the canonical R6 descriptor array and the canonical resident source/momentum buffers remain in place. R8A uploads only a bounded stable list of descriptor indices and a fixed expert directory. Each qualified expert pipeline dereferences the jobs assigned by R8 and writes directly to the original canonical output ranges. No expert-specific payload copy, candidate merge, routing rewrite, or retry is introduced.

### 46. Center sentence

**R8A does not repack the jobs. It leaves every TensorCube payload exactly where R6 already put it and uploads only a small index card telling each R7 expert which canonical descriptors belong to it. R8's routing decision is preserved byte-for-byte as policy authority, while heterogeneous E0/E1/E2 execution finally becomes a real GPU path rather than a shadow manifest.**
